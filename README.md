#  Biyepaticom — Supply Chain Management Project

> **Biyepati.com** is a Dhaka-based online wedding vendor marketplace (biyepati.com).  
> This repository contains a full Supply Chain Management (SCM) analysis built for the platform, covering demand forecasting, vendor evaluation, risk assessment, cost-to-serve analysis, and order fulfillment optimization.

---

##  About Biyepati

Biyepati is a WordPress-based wedding vendor platform connecting couples in Dhaka with verified vendors — venues, decorators, photographers, and caterers. This SCM project was built to model and optimize the platform's supply chain operations.

---

##  Project Structure

```
biye-scm/
│
├── 01_risk_assessment.py          # Module 4  — Supply Chain Risk Assessment
├── 02_demand_forecasting.py       # Module 6  — Demand Forecasting Dashboard
├── 03_vendor_cost_fulfillment.py  # Modules 2, 5, 1 — Vendor Ranking + Cost-to-Serve + Fulfillment
│
├── risk_heatmap.png               # Probability-Impact Heat Map
├── risk_distribution.png          # Risk Score Distribution Charts
├── risk_register_table.png        # Risk Register Summary Table
├── demand_forecast_dashboard.png  # 2024–2026 Demand Forecast Dashboard
├── demand_vs_capacity.png         # Demand vs Vendor Capacity Planning
├── vendor_ranking.png             # Vendor Evaluation Radar + Weighted Scores
├── cost_to_serve.png              # Cost Breakdown + Margin + Profit Waterfall
├── fulfillment_cycle_time.png     # Order Fulfillment Cycle Time Analysis
│
└── tableau_data/
    ├── demand_forecast.csv
    ├── vendor_scores.csv
    ├── cost_to_serve.csv
    ├── fulfillment_cycle.csv
    ├── risk_data.csv
    └── kpi_dashboard.csv
```

---

##  Modules Overview

### Module 6 — Demand Forecasting
- Seasonal demand analysis for Dhaka wedding market (2024–2026)
- 12-month forecast with ±15% confidence bands
- Seasonal index by month
- Demand vs vendor capacity gap analysis

### Module 4 — Risk Assessment
- 12 supply chain risks identified and scored (Probability × Impact)
- Probability-Impact heat map
- Risk register with Critical / High / Medium / Low classification

### Module 2 — Vendor Evaluation
- Weighted scoring model across 6 criteria (Quality, Pricing, Reliability, Communication, Availability, Compliance)
- Radar chart comparison for top 4 vendors
- Ranked scoring for 8 vendors

### Module 5 — Cost-to-Serve Analysis
- Cost breakdown per service category (Venue, Vendor/Decor, Photography, Catering)
- Gross margin analysis
- Full package profit waterfall (250,000 BDT event)

### Module 1 — Order Fulfillment Optimization
- 7-stage fulfillment cycle mapped (Discovery → Post-Event Close)
- Current vs optimized cycle time comparison
- Bottleneck identification

---

##  Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Data processing & visualization |
| Pandas | Data structuring |
| Matplotlib | Chart generation |
| NumPy | Numerical calculations |
| Tableau (CSV ready) | Dashboard visualization |

---

##  How to Run

**1. Install dependencies:**
```bash
pip install matplotlib numpy pandas
```

**2. Run each module:**
```bash
python 01_risk_assessment.py
python 02_demand_forecasting.py
python 03_vendor_cost_fulfillment.py
```

**3. Output:**  
PNG charts are saved in the same folder. CSV files for Tableau are saved in the `tableau_data/` folder.

---

##  Data Note

All data in this project is **assumption-based**, modeled from Bangladesh wedding industry benchmarks (2025). Biyepati is currently pre-revenue and live at [biyepati.com](https://biyepati.com). Real operational data will replace assumptions as the platform scales.

---

##  Author

**Fahim**  
Founder & CEO, Biyepati  
Industrial & Production Engineering, IUT Bangladesh  
🌐 [biyepati.com](https://biyepati.com)

---

© 2026 Fahim. All rights reserved.
