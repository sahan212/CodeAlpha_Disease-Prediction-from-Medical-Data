from typing import Dict
from pydantic import BaseModel, Field

class TumorFeatures(BaseModel):
    # Mean Dimensions
    mean_radius: float = Field(14.13, example=17.99)
    mean_texture: float = Field(19.29, example=10.38)
    mean_perimeter: float = Field(91.97, example=122.8)
    mean_area: float = Field(654.88, example=1001.0)
    mean_smoothness: float = Field(0.096, example=0.1184)
    mean_compactness: float = Field(0.104, example=0.2776)
    mean_concavity: float = Field(0.088, example=0.3001)
    mean_concave_points: float = Field(0.048, example=0.1471)
    mean_symmetry: float = Field(0.181, example=0.2419)
    mean_fractal_dimension: float = Field(0.062, example=0.0787)

    # Standard Errors
    radius_error: float = Field(0.405, example=1.095)
    texture_error: float = Field(1.216, example=0.905)
    perimeter_error: float = Field(2.866, example=8.589)
    area_error: float = Field(40.33, example=153.4)
    smoothness_error: float = Field(0.007, example=0.0064)
    compactness_error: float = Field(0.025, example=0.049)
    concavity_error: float = Field(0.031, example=0.0537)
    concave_points_error: float = Field(0.011, example=0.0158)
    symmetry_error: float = Field(0.020, example=0.030)
    fractal_dimension_error: float = Field(0.003, example=0.0061)

    # Worst / Largest Extremes
    worst_radius: float = Field(16.27, example=25.38)
    worst_texture: float = Field(25.67, example=17.33)
    worst_perimeter: float = Field(107.26, example=184.6)
    worst_area: float = Field(880.58, example=2019.0)
    worst_smoothness: float = Field(0.132, example=0.1622)
    worst_compactness: float = Field(0.254, example=0.6656)
    worst_concavity: float = Field(0.272, example=0.7119)
    worst_concave_points: float = Field(0.114, example=0.2654)
    worst_symmetry: float = Field(0.290, example=0.4601)
    worst_fractal_dimension: float = Field(0.083, example=0.1189)

class DiagnosisResponse(BaseModel):
    verdict: str
    diagnosis_code: int
    is_malignant: bool
    malignancy_risk_pct: float
    benign_pct: float
    confidence_tier: str
    key_biomarkers: Dict[str, str]
