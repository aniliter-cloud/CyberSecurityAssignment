# lstm_loader.py
# Loads the trained LSTM model and exposes a clean predict() interface.

import joblib
import numpy as np
from pathlib import Path
import tensorflow as tf

class LSTMSpectreDetector:
    """
    Loads the trained LSTM and classifies HPC sequences as Normal or Attack.

    Usage:
        detector = LSTMSpectreDetector()
        result = detector.predict(sequence)   # sequence: list of 10 ticks × 4 features
    """

    FEATURE_NAMES = ["cache_miss_rate", "branch_mispredict_rate",
                     "stride_pattern_score", "probe_array_scan"]

    def __init__(self, model_path="lstm_spectre_model.keras",
                       scaler_path="lstm_scaler.pkl"):
        artifacts       = joblib.load(scaler_path)
        self._scaler    = artifacts["scaler"]
        self._seq_len   = artifacts["seq_len"]
        self._n_feat    = artifacts["n_features"]
        self._threshold = artifacts.get("threshold", 0.5)
        #self._model     = tf.keras.models.load_model(model_path)
        self._model = tf.keras.models.load_model(model_path, compile=False)
        self._model.compile(
        optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=["accuracy"],
)
        print(f"[LSTM] Loaded model. Threshold={self._threshold:.4f}")

    def predict(self, sequence: list) -> dict:
        """
        Args:
            sequence: list of dicts or list of lists, shape (10, 4)
                      Each row: [cache_miss, branch_mispredict, stride, probe_scan]
                      All values normalised 0.0–1.0 (fraction, not percentage)
        Returns:
            {label, confidence, anomaly_score, tick_scores, is_attack}
        """
        # Accept list-of-dicts or list-of-lists
        if isinstance(sequence[0], dict):
            arr = np.array([[t[k] for k in self.FEATURE_NAMES] for t in sequence])
        else:
            arr = np.array(sequence, dtype=float)

        if arr.shape != (self._seq_len, self._n_feat):
            raise ValueError(f"Expected shape ({self._seq_len}, {self._n_feat}), got {arr.shape}")

        # Scale
        arr_scaled = self._scaler.transform(arr).reshape(1, self._seq_len, self._n_feat)

        # Full sequence score
        score = float(self._model.predict(arr_scaled, verbose=0)[0][0])
        is_attack = score >= self._threshold

        # Per-tick scores — pass rolling windows of length 1 through the model
        # (simplified: use a 1-tick model approximation via the full model on sub-sequences)
        tick_scores = []
        for i in range(self._seq_len):
            # Build a padded sub-sequence ending at tick i
            sub = arr_scaled[0, max(0, i-self._seq_len+1):i+1]
            pad = np.zeros((self._seq_len - len(sub), self._n_feat))
            padded = np.vstack([pad, sub]).reshape(1, self._seq_len, self._n_feat)
            s = float(self._model.predict(padded, verbose=0)[0][0])
            tick_scores.append(round(s, 4))

        return {
            "label":        "ATTACK" if is_attack else "NORMAL",
            "is_attack":    bool(is_attack),
            "anomaly_score": round(score, 4),
            "confidence":    round(score if is_attack else 1 - score, 4),
            "threshold":     round(self._threshold, 4),
            "tick_scores":   tick_scores,
        }
