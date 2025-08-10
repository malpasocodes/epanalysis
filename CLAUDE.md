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

### Data Flow (Updated v0.4)
1. **Data Loading**: `lib/data.py` handles optimized CSV loading and merging:
   - **Primary dataset**: `data/roi-metrics.csv` (327 institutions with calculated ROI metrics)
   - **Institution data**: `data/dataprep/gr-institutions.csv` (consolidated institutional characteristics)
   - **County baselines**: `data/hs_median_county_25_34.csv` (county-specific HS earnings)
   - **Statewide baseline**: $24,939.44 (weighted average calculated in `lib/hs_baseline.py`)
   - **Legacy datasets** (archived): `data/archive/public.csv`, `data/archive/private.csv`

2. **UI Structure**: Hierarchical sidebar navigation with expandable sections:
   - **Home**: Project overview and baseline impact analysis
   - **Metrics Comparison**: 
     - **Earnings Premium**: C-Metric vs H-Metric analysis with Delta tables
     - **ROI**: Years to recoup costs analysis (coming soon)
   - **Data Analysis**: Interactive quadrant charts and sector analysis
   - **ROI Rankings**: Side-by-side rankings showing baseline methodology impacts
   - **Methodology & Data**: Data sources, calculations, and assumptions
   - **Advanced Analysis**: Institution profiles and statistical tests (coming soon)
   - **Tools & Export**: Data export and report generation (coming soon)
   - **About & Help**: Project background and user guidance (coming soon)

3. **Key Data Columns** (roi-metrics.csv):
   - `roi_statewide_years` / `roi_regional_years`: Years to recoup educational costs
   - `rank_statewide` / `rank_regional`: ROI rankings (1=best)
   - `premium_statewide` / `premium_regional`: Earnings above high school baseline
   - `total_net_price`: Annual net price after financial aid
   - `median_earnings_10yr`: Graduate earnings 10 years after enrollment
   - `hs_median_income`: County-specific high school baseline earnings
   - `Sector`: Institution type (Public, Private for-profit, Private non-profit)

### Module Organization
- `app.py`: Main entry point with hierarchical sidebar navigation and page routing
- `lib/data.py`: Optimized data loading with `load_roi_metrics_dataset()` as primary loader
- `lib/ui.py`: Page rendering functions for Home, Explore, Rankings, Methodology
- `lib/charts.py`: Altair chart generation (quadrant chart)
- `lib/hs_baseline.py`: Statewide high school baseline calculation ($24,939.44)

### Data Architecture (v0.4)
- **Two-dataset approach**: `roi-metrics.csv` (calculations) + `gr-institutions.csv` (characteristics)
- **327 total institutions**: 206 private + 121 public California higher education institutions
- **Complete ROI coverage**: All institutions have calculated statewide/regional ROI metrics
- **Optimized performance**: Direct loading of pre-calculated metrics eliminates runtime calculations

### Key Features (v0.4)
- **Earnings Premium Analysis**: Interactive C-Metric vs H-Metric comparison
- **Delta Analysis**: Customizable top N institution tables (10-50, default 15)
- **Currency Sorting**: Proper numeric sorting with `st.column_config.NumberColumn`
- **Comprehensive Coverage**: Public and private institutions integrated
- **User Controls**: Single "Number of institutions to display" selectbox

### Data Handling Notes
- **Primary loader**: `load_roi_metrics_dataset()` merges roi-metrics.csv with gr-institutions.csv
- **Column normalization**: Automatic whitespace stripping and type coercion
- **Missing data handling**: County baselines fallback to statewide ($24,939.44)
- **Invalid ROI handling**: Negative premiums marked as 999 years (excluded from rankings)
- **Merge strategy**: Left join on Institution name preserves all 327 institutions

### Caching Strategy
- All data loading functions use `@st.cache_data` decorator
- Cache invalidated when CSV files change
- Primary dataset cached once per session for optimal performance
- Clear cache during development: `st.cache_data.clear()`

### Version History
- **v0.1**: Initial refactoring with hierarchical navigation
- **v0.2**: Fixed currency column sorting issues
- **v0.3**: Integrated private institutions (327 total)
- **v0.4**: Simplified user controls, improved navigation labels

### Current Limitations
- Some advanced analysis sections marked "Coming Soon"
- ROI Analysis page placeholder (methodology complete)
- Export and reporting features not yet implemented
- Institution profile pages in development