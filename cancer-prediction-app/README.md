# OncoPredict AI - Breast Cancer Diagnostic Full-Stack App

An intelligent cellular biopsy diagnostic platform powered by **FastAPI**, **scikit-learn**, and a modern **Oncology Dashboard**.

---

## Folder Structure

```
cancer-prediction-app/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI REST API & Static UI Server
│   ├── model.py         # Model Training, Caching & Inference
│   └── schemas.py       # Pydantic 30-Biomarker Schema & Defaults
├── frontend/
│   ├── index.html       # Oncology Pathology Dashboard (Tailwind CSS)
│   └── app.js           # Client Logic, Presets & Dynamic Gauges
├── requirements.txt     # Python Dependencies
├── run.sh               # 1-Click Startup Script
└── README.md            # Documentation
```

---

## Quick Start (Run in 2 Steps)

### Step 1: Open Terminal
```bash
cd /Users/pranithreddy/Desktop/cancer-prediction-app
```

### Step 2: Launch App
```bash
chmod +x run.sh
./run.sh
```

*(Or manually: `pip install -r requirements.txt && python3 -m uvicorn backend.main:app --reload --port 8000`)*

---

## Using the Dashboard
1. Open your browser and go to:
   ```
   http://127.0.0.1:8000
   ```
2. **Instant Testing**: Click **Malignant Case** or **Benign Case** to populate the 30 cell measurements in one click.
3. Click **Run Diagnostic Evaluation** to see:
   - Automated Pathology Verdict (`MALIGNANT` vs `BENIGN`)
   - Malignancy Risk Gauge (%)
   - Diagnostic Confidence Tier
   - Key Morphological Features (`Worst Radius`, `Worst Area`, `Worst Concave Points`)

---

## Interactive API Documentation
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc UI: `http://127.0.0.1:8000/redoc`
