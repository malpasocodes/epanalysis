# Earnings Premium Analysis — Project Status Summary

## 1. Project Overview

We’re building a Streamlit app to analyze and visualize the Earnings Premium (EP) Regulation data for California colleges.
	•	Core comparison: Statewide ROI metric vs. Regional (county-based) ROI metric.
	•	Goal: Show how the statewide baseline disadvantages colleges in lower-income regions and how rankings change when using a fairer local baseline.
	•	Data sources:
	•	roi_with_county_baseline_combined_clean.csv (combined dataset)
	•	public.csv (Golden Ventures ROI data)
	•	hs_median_count_25_34.csv (county-level high school earnings)

## 2. Streamlit App Structure
	•	Single-page app (app.py) with sidebar navigation (no Streamlit “pages” to avoid the wonky multi-page look).
	•	Navigation wireframe:
	•	Main — project description
	•	Rankings — side-by-side statewide vs. local ROI, showing Institution, Region, ROI Rank (Statewide), ROI Rank (Local), and Δ rank
	•	Visualizations — planned quadrant chart (Net Price vs Median Earnings), plus others later
	•	About — methodology, credits, data sources


## 3. Data Loading & Cleanup
	•	We now load and merge the combined ROI dataset with Golden Ventures ROI from public.csv.
	•	Fixed merge issues by coalescing Institution_x / Institution_y into a single Institution column and dropping the suffix columns after merge.
	•	Added numeric coercion for ROI-related fields to prevent type errors.
	•	Applied defensive defaults if expected columns are missing.


## 4. Current Functionality
	•	Rankings view: Single table showing:
	•	Institution
	•	Region
	•	ROI Rank (Statewide)
	•	ROI Rank (Local)
	•	Δ (rank change)
	•	Golden Ventures ROI column is loaded but not yet displayed.
	•	No filters yet; starting with clean, minimal output.

## 5. Known Issues / Next Steps
	•	Net Price = 0 for some colleges: need imputation strategy (we discussed approximating or imputing).
	•	Golden Ventures ROI integration: decide if it’s shown alongside current ROI metrics.
	•	Visualizations: implement quadrant chart (Price vs. Earnings) and possibly regional maps.
	•	Improve column naming consistency to avoid future merge conflicts.
	•	Optional: add automatic dropping of all _x / _y suffix columns except where needed.

## 6. Files & Directories

epanalysis/
│
├── app.py                  # Main Streamlit app
├── lib/
│   ├── data.py              # Data loading, merging, cleanup
│   ├── ui.py                # UI rendering functions
│   └── utils.py             # (future helper functions)
├── data/
│   ├── roi_with_county_baseline_combined_clean.csv
│   ├── public.csv
│   ├── private.csv
│   └── hs_median_count_25_34.csv
├── pyproject.toml           # uv / project dependencies
└── README.md                # (to be created)