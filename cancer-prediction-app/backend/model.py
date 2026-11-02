import os
import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

MODEL_FILE = os.path.join(os.path.dirname(__file__), 'cancer_model.joblib')
PRIMARY_DATASET = '/Users/pranithreddy/Downloads/disease_prediction_breast_cancer.csv'

# Column name mapping between CSV and standard snake_case
FEATURE_MAP = {
    'mean radius': 'mean_radius', 'mean texture': 'mean_texture', 'mean perimeter': 'mean_perimeter',
    'mean area': 'mean_area', 'mean smoothness': 'mean_smoothness', 'mean compactness': 'mean_compactness',
    'mean concavity': 'mean_concavity', 'mean concave points': 'mean_concave_points', 'mean symmetry': 'mean_symmetry',
    'mean fractal dimension': 'mean_fractal_dimension', 'radius error': 'radius_error', 'texture error': 'texture_error',
    'perimeter error': 'perimeter_error', 'area error': 'area_error', 'smoothness error': 'smoothness_error',
    'compactness error': 'compactness_error', 'concavity error': 'concavity_error', 'concave points error': 'concave_points_error',
    'symmetry error': 'symmetry_error', 'fractal dimension error': 'fractal_dimension_error', 'worst radius': 'worst_radius',
    'worst texture': 'worst_texture', 'worst perimeter': 'worst_perimeter', 'worst area': 'worst_area',
    'worst smoothness': 'worst_smoothness', 'worst compactness': 'worst_compactness', 'worst concavity': 'worst_concavity',
    'worst concave points': 'worst_concave_points', 'worst symmetry': 'worst_symmetry', 'worst fractal dimension': 'worst_fractal_dimension'
}

def get_or_train_cancer_model():
    if os.path.exists(MODEL_FILE):
        print(f"[+] Loading cached model from {MODEL_FILE}")
        return joblib.load(MODEL_FILE)

    if os.path.exists(PRIMARY_DATASET):
        try:
            print(f"[+] Training model from external CSV: {PRIMARY_DATASET}")
            df = pd.read_csv(PRIMARY_DATASET)
            X = df.drop(columns=['diagnosis'])
            y = df['diagnosis']
        except Exception:
            data = load_breast_cancer(as_frame=True)
            X = data.data
            y = data.target
    else:
        print("[!] Loading standard Wisconsin Breast Cancer dataset...")
        data = load_breast_cancer(as_frame=True)
        X = data.data
        y = data.target

    # Normalize feature column names to snake_case
    X = X.rename(columns=FEATURE_MAP)

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
    ])

    pipeline.fit(X, y)
    joblib.dump(pipeline, MODEL_FILE)
    print(f"[✓] Model trained and cached to {MODEL_FILE}")
    return pipeline

def predict_tumor_case(sample_dict: dict, model, risk_threshold: float = 0.50) -> dict:
    df_sample = pd.DataFrame([sample_dict])

    # Probability of Class 0 (Malignant) vs Class 1 (Benign)
    probs = model.predict_proba(df_sample)[0]
    prob_malignant = float(probs[0])
    prob_benign = float(probs[1])

    is_malignant = prob_malignant >= risk_threshold
    verdict = "MALIGNANT (High Risk / Cancerous)" if is_malignant else "BENIGN (Non-Cancerous / Safe)"

    confidence = "High Confidence" if max(prob_malignant, prob_benign) > 0.85 else "Borderline (Recommend Re-test)"

    return {
        "verdict": verdict,
        "diagnosis_code": 0 if is_malignant else 1,
        "is_malignant": is_malignant,
        "malignancy_risk_pct": round(prob_malignant * 100, 2),
        "benign_pct": round(prob_benign * 100, 2),
        "confidence_tier": confidence,
        "key_biomarkers": {
            "Mean Radius": f"{sample_dict.get('mean_radius', 0):.2f} mm",
            "Worst Radius": f"{sample_dict.get('worst_radius', 0):.2f} mm",
            "Worst Area": f"{sample_dict.get('worst_area', 0):.1f} mm²",
            "Worst Concave Points": f"{sample_dict.get('worst_concave_points', 0):.4f}"
        }
    }
