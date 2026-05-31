# server.py
# Flask REST API — exposes the LSTM model to the browser frontend.
# Run:  python server.py
# Then open index.html — it will POST to http://localhost:5000/predict

from flask import Flask, request, jsonify
from flask_cors import CORS
from lstm_loader import LSTMSpectreDetector
import numpy as np

app = Flask(__name__)
CORS(app)   # allow browser requests from file:// or any origin

# ── Load model ONCE at startup ─────────────────────────────────────────────
detector = LSTMSpectreDetector(
    model_path="lstm_spectre_model.keras",
    scaler_path="lstm_scaler.pkl",
)
print("[Server] LSTM ready. Listening on http://localhost:5000")


# ══════════════════════════════════════════════════════════════════════════════
# POST /predict
# Body: { "sequence": [[f0,f1,f2,f3], ...] }   — 10 rows × 4 features
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/predict", methods=["POST"])
def predict():
    body = request.get_json()
    if not body or "sequence" not in body:
        return jsonify({"error": "Missing 'sequence' key"}), 400
    try:
        result = detector.predict(body["sequence"])
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ══════════════════════════════════════════════════════════════════════════════
# POST /simulate
# Generates a synthetic HPC stream (normal → attack), runs it through LSTM,
# returns tick-by-tick scores the browser can animate.
# Body: { "mode": "attack" | "normal" }
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/simulate", methods=["POST"])
def simulate():
    body = request.get_json(silent=True) or {}
    mode = body.get("mode", "attack")

    ticks = []
    if mode == "attack":
        # Phase 1: normal (ticks 0-1)
        for _ in range(2):
            ticks.append([np.random.uniform(0.02, 0.07),   # cache_miss
                          np.random.uniform(0.01, 0.04),   # branch_mis
                          np.random.uniform(0.00, 0.03),   # stride
                          np.random.uniform(0.00, 0.02)])  # probe
        # Phase 2: predictor training spike (ticks 2-4)
        for _ in range(3):
            ticks.append([np.random.uniform(0.03, 0.08),
                          np.random.uniform(0.15, 0.28),   # branch SPIKE
                          np.random.uniform(0.02, 0.08),
                          np.random.uniform(0.01, 0.05)])
        # Phase 3: flush + speculative access (ticks 5-6)
        for _ in range(2):
            ticks.append([np.random.uniform(0.55, 0.80),   # cache EXPLODES
                          np.random.uniform(0.20, 0.35),
                          np.random.uniform(0.15, 0.35),
                          np.random.uniform(0.08, 0.20)])
        # Phase 4: probe array scan (ticks 7-9)
        for _ in range(3):
            ticks.append([np.random.uniform(0.40, 0.72),
                          np.random.uniform(0.18, 0.30),
                          np.random.uniform(0.70, 0.95),   # stride PEAK
                          np.random.uniform(0.68, 0.94)])  # probe PEAK
    else:
        # All normal
        for _ in range(10):
            ticks.append([np.random.uniform(0.02, 0.08),
                          np.random.uniform(0.01, 0.05),
                          np.random.uniform(0.00, 0.04),
                          np.random.uniform(0.00, 0.03)])

    result = detector.predict(ticks)
    result["ticks"] = [[round(v, 4) for v in row] for row in ticks]
    result["feature_names"] = LSTMSpectreDetector.FEATURE_NAMES
    return jsonify(result)


# ══════════════════════════════════════════════════════════════════════════════
# GET /health
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model": "LSTM Spectre Detector",
        "threshold": detector._threshold,
        "seq_len": detector._seq_len,
        "features": LSTMSpectreDetector.FEATURE_NAMES,
    })


if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0")
