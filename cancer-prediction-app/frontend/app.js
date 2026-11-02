// Actual representative cases from the dataset
const presets = {
  malignant: {
    mean_radius: 17.99, mean_texture: 10.38, mean_perimeter: 122.8, mean_area: 1001.0, mean_smoothness: 0.1184,
    mean_compactness: 0.2776, mean_concavity: 0.3001, mean_concave_points: 0.1471, mean_symmetry: 0.2419, mean_fractal_dimension: 0.0787,
    radius_error: 1.095, texture_error: 0.905, perimeter_error: 8.589, area_error: 153.4, smoothness_error: 0.0064,
    compactness_error: 0.049, concavity_error: 0.0537, concave_points_error: 0.0159, symmetry_error: 0.030, fractal_dimension_error: 0.0062,
    worst_radius: 25.38, worst_texture: 17.33, worst_perimeter: 184.6, worst_area: 2019.0, worst_smoothness: 0.1622,
    worst_compactness: 0.6656, worst_concavity: 0.7119, worst_concave_points: 0.2654, worst_symmetry: 0.4601, worst_fractal_dimension: 0.1189
  },
  benign: {
    mean_radius: 13.54, mean_texture: 14.36, mean_perimeter: 87.46, mean_area: 566.3, mean_smoothness: 0.0978,
    mean_compactness: 0.0813, mean_concavity: 0.0666, mean_concave_points: 0.0478, mean_symmetry: 0.1885, mean_fractal_dimension: 0.0577,
    radius_error: 0.2699, texture_error: 0.7886, perimeter_error: 2.058, area_error: 23.56, smoothness_error: 0.0085,
    compactness_error: 0.0146, concavity_error: 0.0239, concave_points_error: 0.0132, symmetry_error: 0.0198, fractal_dimension_error: 0.0023,
    worst_radius: 15.11, worst_texture: 19.26, worst_perimeter: 99.70, worst_area: 711.2, worst_smoothness: 0.1440,
    worst_compactness: 0.1773, worst_concavity: 0.2390, worst_concave_points: 0.1288, worst_symmetry: 0.2977, worst_fractal_dimension: 0.0726
  }
};

function switchTab(tabName) {
  ['mean', 'worst', 'error'].forEach(t => {
    document.getElementById(`tab-${t}`).classList.add('hidden');
    document.getElementById(`tabBtn-${t}`).className = "pb-2 border-b-2 border-transparent text-slate-400 hover:text-slate-200";
  });
  document.getElementById(`tab-${tabName}`).classList.remove('hidden');
  document.getElementById(`tabBtn-${tabName}`).className = "pb-2 border-b-2 border-rose-500 text-rose-400 font-bold";
}

function loadPreset(type) {
  const p = presets[type];
  if (!p) return;
  for (const [key, val] of Object.entries(p)) {
    const el = document.getElementById(key);
    if (el) el.value = val;
  }
}

// Initial populate with Benign
window.onload = () => loadPreset('benign');

document.getElementById('cancerForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const payload = {};
  const inputs = document.querySelectorAll('#cancerForm input');
  inputs.forEach(i => {
    payload[i.id] = parseFloat(i.value) || 0.0;
  });

  const btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-2"></i> Analyzing Biopsy...`;

  try {
    const res = await fetch('/api/diagnose', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error("Diagnostic request failed.");
    const data = await res.json();
    renderDiagnosis(data);
  } catch (err) {
    alert("Error: " + err.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<i class="fa-solid fa-stethoscope mr-2"></i> Run Diagnostic Evaluation`;
  }
});

function renderDiagnosis(data) {
  const verdictBadge = document.getElementById('verdictBadge');
  const confidenceText = document.getElementById('confidenceText');
  const riskBar = document.getElementById('riskBar');
  const riskLabel = document.getElementById('riskLabel');

  if (data.is_malignant) {
    verdictBadge.innerHTML = `<span class="text-rose-500"><i class="fa-solid fa-triangle-exclamation mr-2"></i>MALIGNANT (Cancerous)</span>`;
    confidenceText.innerHTML = `Diagnostic Confidence: <strong class="text-rose-400">${data.confidence_tier}</strong>`;
    riskBar.className = "h-3.5 rounded-full bg-rose-500 transition-all duration-700";
  } else {
    verdictBadge.innerHTML = `<span class="text-emerald-400"><i class="fa-solid fa-shield-check mr-2"></i>BENIGN (Safe)</span>`;
    confidenceText.innerHTML = `Diagnostic Confidence: <strong class="text-emerald-400">${data.confidence_tier}</strong>`;
    riskBar.className = "h-3.5 rounded-full bg-emerald-500 transition-all duration-700";
  }

  riskBar.style.width = `${Math.min(data.malignancy_risk_pct, 100)}%`;
  riskLabel.innerText = `${data.malignancy_risk_pct}%`;

  // Update Morphological Indicators
  document.getElementById('bioWorstRadius').innerText = data.key_biomarkers["Worst Radius"];
  document.getElementById('bioWorstArea').innerText = data.key_biomarkers["Worst Area"];
  document.getElementById('bioMeanRadius').innerText = data.key_biomarkers["Mean Radius"];
  document.getElementById('bioWorstConcave').innerText = data.key_biomarkers["Worst Concave Points"];
}
