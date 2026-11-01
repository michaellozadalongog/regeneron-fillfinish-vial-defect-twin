# Fill/Finish Vial Defect Twin — fill weight + visual inspection Monte Carlo (student project)
Independent student project by Michael Lozada-Longog (HPU BME), inspired by sterile fill/finish manufacturing (e.g., biologics manufacturers like Regeneron). Not affiliated with Regeneron; all parameters are assumptions.

Simulates 200,000 vials per setting across line speed (150–400 vials/min) × lighting (1000–3000 lux) × vision reject threshold (0.35–0.55). Outputs yield, false-reject rate, defect escape ppm, fill-weight Cpk, Pareto, and X̄ control limits.

## Run
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/twin.py   # -> figs/*.png, figs/results.json
```
## Results (seed 11; assumed spec 2.20–2.35 mL, target 2.28)
- Baseline 200 vpm / 2000 lux / thr 0.45: yield 99.18%, false reject 0.64%, escapes 20 ppm, Cpk 1.95.
- Cpk falls with speed: 2.43 (150) → 1.94 (200) → 1.39 (300) → 1.08 (400 vpm, fails 1.33).
- Recommended (max throughput with Cpk ≥1.33 and escapes <50 ppm): **300 vpm, 2000 lux, thr 0.55** → yield 99.78%, Cpk 1.39, escapes 45 ppm.
- Pareto (baseline): cosmetic scratch 263 > stopper misplacement 62 > particulate 40 > glass crack 15.
- X̄ chart (n=5) limits at baseline: 2.264–2.296 mL.

Figures: `figs/defect_pareto.png`, `figs/escape_vs_speed.png`, `figs/threshold_tradeoff.png`, `figs/fill_weight.png`.

## Skills → fill/finish & manufacturing intern work
SPC/Cpk, control limits, AQL/inspection tradeoffs (false reject vs escape), line-speed/process capability, Pareto-driven improvement, Python data analysis. Context: USP <790>/<1790> visible-particulate inspection.

## Limitations
Defect rates and vision-score model are invented; escape ppm is based on few events (~0–13 per cell) and is noisy; no real images or machine vision model; speed→variability relationship assumed linear.
