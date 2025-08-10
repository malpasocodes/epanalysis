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

### Run with different ports (if default 8501 is in use)
```bash
uv run streamlit run app.py --server.port 8502
```

## Architecture

This is a Streamlit application for analyzing California college ROI data comparing statewide vs regional (county-based) baselines, demonstrating the impact of the Earnings Premium (EP) regulation.

### Data Flow
1. **Data Loading**: `lib/data.py` handles all CSV loading and merging:
   - Main dataset: `roi_with_county_baseline_combined_clean.csv` 
   - Golden Ventures ROI: `public.csv` (merged by UNITID or Institution name)
   - County earnings: `hs_median_county_25_34.csv`
   - Private institutions: `private.csv`
   - Automatic column normalization and type coercion for numeric fields

2. **UI Structure**: Single-page app with sidebar navigation (not using Streamlit pages):
   - **Home**: Project overview and impact of baseline changes
   - **Explore Data**: Interactive quadrant chart (Price vs Earnings) with filters
   - **Rankings**: Side-by-side ROI rankings showing rank changes between baselines
   - **Methodology**: Data definitions, assumptions, and EP regulation details
   - **About**: Project background and context

3. **Key Data Columns**:
   - `roi_statewide_years` / `roi_regional_years`: Years to recoup costs
   - `rank_statewide` / `rank_regional`: ROI rankings
   - `premium_statewide` / `premium_regional`: Earnings above HS baseline  
   - `total_net_price`: Annual attendance cost
   - `median_earnings_10yr`: Graduate earnings after 10 years
   - `county`: Institution's county location
   - `sector`: Institution type (Public 2-year, Public 4-year, Private)

### Module Organization
- `app.py`: Main entry point, navigation routing, uses @st.cache_data
- `lib/data.py`: Data loading, merging, and cleaning logic
- `lib/ui.py`: All page rendering functions  
- `lib/charts.py`: Altair chart generation (quadrant chart)

### Enhanced Modules (Available for migration)
- `lib/data_improved.py`: DataLoader class with better error handling
- `lib/components.py`: Reusable UI components (FilterSidebar, MetricsRow, RankingsTable)
- `lib/models.py`: Data models with type hints
- `lib/utils.py`: Utilities for data cleaning and formatting
- `config.py`: Centralized configuration

### Data Handling Notes
- Column names are automatically stripped of whitespace to prevent merge issues
- Merge suffix columns (_x, _y) are coalesced and dropped
- Missing expected columns get defensive defaults
- Numeric columns are coerced with `pd.to_numeric(errors="coerce")`
- Some institutions have $0 net price requiring special handling

### Caching Strategy
- All data loading functions use `@st.cache_data` decorator
- Cache is invalidated when underlying CSV files change
- Consider clearing cache during development: `st.cache_data.clear()`

### Known Issues & Considerations
- Golden Ventures ROI data integration needs decision on display strategy
- Zero net price institutions may need imputation or special handling
- Rankings can have ties requiring stable sort algorithms
- County baseline data may be missing for some institutions