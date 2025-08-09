# config.py
from typing import Dict, Any
import os
from pathlib import Path

class Config:
    """Central configuration for the application."""
    
    # Application settings
    APP_TITLE = "Earnings Premium & ROI Explorer"
    PAGE_LAYOUT = "wide"
    
    # Data paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    
    DATA_FILES = {
        "combined": DATA_DIR / "roi_with_county_baseline_combined_clean.csv",
        "public": DATA_DIR / "public.csv",
        "private": DATA_DIR / "private.csv",
        "county_earnings": DATA_DIR / "hs_median_county_25_34.csv"
    }
    
    # Column definitions
    NUMERIC_COLUMNS = [
        "total_net_price",
        "median_earnings_10yr",
        "premium_statewide",
        "premium_regional",
        "roi_statewide_years",
        "roi_regional_years",
        "rank_statewide",
        "rank_regional",
        "rank_change",
        "hs_median_income",
        "golden_roi_years"
    ]
    
    REQUIRED_COLUMNS = [
        "UNITID",
        "Institution",
        "Region",
        "County",
        "Sector"
    ]
    
    # Display settings
    DISPLAY_COLUMNS = {
        "rankings": [
            "Institution",
            "Region",
            "rank_statewide",
            "rank_regional",
            "rank_change"
        ],
        "explore": [
            "Institution",
            "Region",
            "County",
            "Sector",
            "total_net_price",
            "median_earnings_10yr",
            "roi_statewide_years",
            "roi_regional_years"
        ]
    }
    
    # Chart settings
    CHART_HEIGHT = 520
    CHART_POINT_SIZE = 70
    
    # Formatting
    CURRENCY_FORMAT = "${:,.0f}"
    PERCENT_FORMAT = "{:.1%}"
    YEAR_FORMAT = "{:.1f} years"
    
    @classmethod
    def get_env(cls, key: str, default: Any = None) -> Any:
        """Get environment variable with fallback."""
        return os.environ.get(key, default)
    
    @classmethod
    def validate_paths(cls) -> Dict[str, bool]:
        """Check which data files exist."""
        return {
            name: path.exists() 
            for name, path in cls.DATA_FILES.items()
        }