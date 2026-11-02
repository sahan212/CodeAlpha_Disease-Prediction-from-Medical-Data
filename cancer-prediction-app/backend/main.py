import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

try:
    from .schemas import TumorFeatures, DiagnosisResponse
    from .model import get_or_train_cancer_model, predict_tumor_case
except ImportError:
    from schemas import TumorFeatures, DiagnosisResponse
    from model import get_or_train_cancer_model, predict_tumor_case

app = FastAPI(
    title="OncoPredict AI - Breast Cancer Diagnostic API",
    description="Cellular Biomarker Malignancy Diagnostic Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None

@app.on_event("startup")
def startup_event():
    global model
    model = get_or_train_cancer_model()

@app.post("/api/diagnose", response_model=DiagnosisResponse)
def diagnose_biopsy(tumor: TumorFeatures):
    result = predict_tumor_case(tumor.dict(), model)
    return result

@app.get("/api/health")
def health():
    return {"status": "online", "model_loaded": model is not None}

frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))
