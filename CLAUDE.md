# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Run the application
```bash
uv run streamlit run app.py
```

### Install dependencies
```bash
uv sync
```

### Add new dependencies
```bash
uv add <package-name>
```

## Architecture

This is a Streamlit application for analyzing California college ROI data comparing statewide vs regional (county-based) baselines.

### Data Flow
1. **Data Loading**: `lib/data.py` handles all CSV loading and merging:
   - Main dataset: `roi_with_county_baseline_combined_clean.csv` 
   - Golden Ventures ROI: `public.csv` (merged by UNITID or Institution name)
   - Automatic column normalization and type coercion for numeric fields

2. **UI Structure**: Single-page app with sidebar navigation (not using Streamlit pages):
   - **Home**: Project overview
   - **Explore Data**: Interactive quadrant chart (Price vs Earnings) with filters
   - **Rankings**: Side-by-side ROI rankings showing rank changes between baselines
   - **Methodology**: Data definitions and assumptions
   - **About**: Project background

3. **Key Data Columns**:
   - `roi_statewide_years` / `roi_regional_years`: Years to recoup costs
   - `rank_statewide` / `rank_regional`: ROI rankings
   - `premium_statewide` / `premium_regional`: Earnings above HS baseline
   - `total_net_price`: Annual attendance cost
   - `median_earnings_10yr`: Graduate earnings after 10 years

### Module Organization
- `app.py`: Main entry point, navigation routing
- `lib/data.py`: Data loading, merging, and cleaning logic
- `lib/ui.py`: All page rendering functions
- `lib/charts.py`: Altair chart generation (quadrant chart)

### Data Handling Notes
- Column names are automatically stripped of whitespace to prevent merge issues
- Merge suffix columns (_x, _y) are coalesced and dropped
- Missing expected columns get defensive defaults
- Numeric columns are coerced with `pd.to_numeric(errors="coerce")`