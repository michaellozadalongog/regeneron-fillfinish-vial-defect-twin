Every sterile vial line fights the same tradeoff: run faster and fill-weight variation creeps up; tighten the vision threshold and you throw away good product.

So I built a "Fill/Finish Vial Defect Twin" — a Monte Carlo of 200,000 vials per setting across line speed, inspection lighting, and vision reject threshold (36 settings).

What my sim showed:
• Fill-weight Cpk drops from 2.43 at 150 vials/min to 1.08 at 400 (below the 1.33 target)
• Best setting under Cpk ≥1.33 + <50 ppm escapes: 300 vpm, 2000 lux → 99.78% yield
• Pareto: cosmetic scratches dominate rejects, then stopper misplacement

📊 Fig 1: defect Pareto · Fig 2: escapes vs speed · Fig 3: threshold tradeoff · Fig 4: fill-weight capability

Honest limits: all defect rates are assumptions, escape ppm is noisy (few events), and there's no real machine-vision model or line data.

Inspired by biologics fill/finish challenges at companies like Regeneron — a student project, not company work.

I'm a 2nd-year BME student at HPU looking for Summer 2027 internships in manufacturing, fill/finish, or quality. Feedback from manufacturing engineers welcome!

Mahalo 🤙
#Manufacturing #FillFinish #Biologics #BiomedicalEngineering #SPC
