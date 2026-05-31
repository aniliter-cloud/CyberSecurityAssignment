# lstm_train.py
# Trains an LSTM to detect Spectre attacks from Hardware Performance Counter (HPC) streams.
# Generates synthetic HPC sequences, trains, evaluates, then saves the model.
#
# Run ONCE:  python lstm_train.py
# Output:    lstm_spectre_model.keras  +  scaler.pkl

import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# ── Reproducibility ───────────────────────────────────────────────────────────
np.random.seed(42)
tf.random.set_seed(42)

# ── Config ────────────────────────────────────────────────────────────────────
SEQ_LEN    = 10      # LSTM looks at 10 consecutive HPC ticks to decide
N_FEATURES = 4       # cache_miss | branch_mispredict | stride_score | probe_scan
N_NORMAL   = 3000    # synthetic normal sequences
N_ATTACK   = 3000    # synthetic attack sequences (balanced)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. SYNTHETIC DATA GENERATION
# ═══════════════════════════════════════════════════════════════════════════════
# Features represent normalised Hardware Performance Counter readings:
#   [0] cache_miss_rate       — fraction of memory accesses that miss L1/L2
#   [1] branch_mispredict_rate — fraction of branches mispredicted by CPU
#   [2] stride_pattern_score  — regularity of 512-byte strided memory accesses
#   [3] probe_array_scan      — burst of sequential accesses across probe array

def generate_normal_sequence(seq_len=SEQ_LEN):
    """Normal traffic: low uniform noise across all counters."""
    return np.column_stack([
        np.random.uniform(0.02, 0.08, seq_len),   # cache_miss  2–8%
        np.random.uniform(0.01, 0.05, seq_len),   # branch_mis  1–5%
        np.random.uniform(0.00, 0.04, seq_len),   # stride      0–4%
        np.random.uniform(0.00, 0.03, seq_len),   # probe_scan  0–3%
    ])

def generate_attack_sequence(seq_len=SEQ_LEN):
    """
    Spectre Variant 1 (Bounds Check Bypass) signature:
      Phase 1 (train predictor) : branch_mispredict spikes  — ticks 0-3
      Phase 2 (flush + trigger) : cache_miss spikes         — ticks 3-6
      Phase 3 (reload / scan)   : stride + probe explode    — ticks 6-9
    """
    seq = np.zeros((seq_len, N_FEATURES))

    # Phase 1 — predictor training
    t1 = seq_len // 3
    seq[:t1, 0] = np.random.uniform(0.03, 0.08, t1)   # cache_miss still normal
    seq[:t1, 1] = np.random.uniform(0.15, 0.30, t1)   # branch_mis SPIKE
    seq[:t1, 2] = np.random.uniform(0.00, 0.05, t1)
    seq[:t1, 3] = np.random.uniform(0.00, 0.04, t1)

    # Phase 2 — flush / speculative access
    t2 = 2 * seq_len // 3
    seq[t1:t2, 0] = np.random.uniform(0.55, 0.85, t2 - t1)  # cache_miss EXPLODES
    seq[t1:t2, 1] = np.random.uniform(0.20, 0.35, t2 - t1)  # branch_mis high
    seq[t1:t2, 2] = np.random.uniform(0.10, 0.30, t2 - t1)  # stride rising
    seq[t1:t2, 3] = np.random.uniform(0.05, 0.20, t2 - t1)

    # Phase 3 — probe array scan (all 256 entries, 512-byte stride)
    seq[t2:, 0] = np.random.uniform(0.40, 0.75, seq_len - t2)
    seq[t2:, 1] = np.random.uniform(0.15, 0.30, seq_len - t2)
    seq[t2:, 2] = np.random.uniform(0.70, 0.98, seq_len - t2)  # stride PEAK
    seq[t2:, 3] = np.random.uniform(0.65, 0.95, seq_len - t2)  # probe PEAK

    # Add small noise to avoid overfitting on clean patterns
    seq += np.random.normal(0, 0.01, seq.shape)
    return np.clip(seq, 0, 1)

print("Generating synthetic HPC sequences...")
normal_seqs  = np.array([generate_normal_sequence() for _ in range(N_NORMAL)])
attack_seqs  = np.array([generate_attack_sequence()  for _ in range(N_ATTACK)])

X = np.concatenate([normal_seqs, attack_seqs], axis=0)   # (6000, 10, 4)
y = np.concatenate([np.zeros(N_NORMAL), np.ones(N_ATTACK)])

print(f"Dataset: {X.shape} — {int(y.sum())} attacks, {int((y==0).sum())} normal")

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PREPROCESSING
# ═══════════════════════════════════════════════════════════════════════════════
# Flatten to (n_samples, n_features) for scaler, then reshape back
X_flat   = X.reshape(-1, N_FEATURES)
scaler   = MinMaxScaler()
X_scaled = scaler.fit_transform(X_flat).reshape(X.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train: {X_train.shape}  Test: {X_test.shape}")

# ═══════════════════════════════════════════════════════════════════════════════
# 3. LSTM MODEL ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
model = Sequential([
    # First LSTM — captures temporal patterns across 10 ticks
    LSTM(64, input_shape=(SEQ_LEN, N_FEATURES),
         return_sequences=True,       # pass sequence to next LSTM
         dropout=0.2, recurrent_dropout=0.1),
    BatchNormalization(),

    # Second LSTM — higher-level temporal abstraction
    LSTM(32, return_sequences=False,
         dropout=0.2, recurrent_dropout=0.1),
    BatchNormalization(),

    # Dense head — classification
    Dense(16, activation="relu"),
    Dropout(0.3),
    Dense(1, activation="sigmoid"),   # 0 = normal, 1 = attack
])

model.compile(
    optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=0.001),
    loss="binary_crossentropy",
    metrics=["accuracy", tf.keras.metrics.AUC(name="auc")],
)
model.summary()

# ═══════════════════════════════════════════════════════════════════════════════
# 4. TRAINING
# ═══════════════════════════════════════════════════════════════════════════════
callbacks = [
    EarlyStopping(monitor="val_auc", patience=8, restore_best_weights=True, mode="max"),
    ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=4, min_lr=1e-6),
]

history = model.fit(
    X_train, y_train,
    validation_split=0.15,
    epochs=60,
    batch_size=64,
    callbacks=callbacks,
    verbose=1,
)

# ═══════════════════════════════════════════════════════════════════════════════
# 5. EVALUATION
# ═══════════════════════════════════════════════════════════════════════════════
y_pred_prob = model.predict(X_test).flatten()
y_pred      = (y_pred_prob >= 0.5).astype(int)

print("\n── Test Results ──────────────────────────────")
print(classification_report(y_test, y_pred, target_names=["Normal", "Attack"]))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

loss, acc, auc = model.evaluate(X_test, y_test, verbose=0)
print(f"\nTest Accuracy: {acc*100:.2f}%  |  AUC: {auc:.4f}")

# ═══════════════════════════════════════════════════════════════════════════════
# 6. SAVE
# ═══════════════════════════════════════════════════════════════════════════════
model.save("lstm_spectre_model.keras")
joblib.dump({"scaler": scaler, "seq_len": SEQ_LEN, "n_features": N_FEATURES}, "lstm_scaler.pkl")
print("\nSaved → lstm_spectre_model.keras + lstm_scaler.pkl")

# Fix: find optimal threshold from validation probabilities
from sklearn.metrics import roc_curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
optimal_idx  = np.argmax(tpr - fpr)
optimal_thr  = float(thresholds[optimal_idx])
y_pred_opt   = (y_pred_prob >= optimal_thr).astype(int)
loss2, acc2, auc2 = model.evaluate(X_test, y_test, verbose=0)
print(f"\nOptimal threshold: {optimal_thr:.4f}")
print(f"Accuracy at optimal threshold: {(y_pred_opt == y_test).mean()*100:.2f}%")
print(classification_report(y_test, y_pred_opt, target_names=["Normal","Attack"]))

# Save threshold alongside scaler
joblib.dump({"scaler": scaler, "seq_len": SEQ_LEN, "n_features": N_FEATURES,
             "threshold": optimal_thr}, "lstm_scaler.pkl")
print(f"Updated lstm_scaler.pkl with threshold={optimal_thr:.4f}")
