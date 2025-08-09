# lib/utils.py
import pandas as pd
import numpy as np
from typing import Optional, Union, List
import logging

logger = logging.getLogger(__name__)

class DataCleaner:
    """Utilities for data cleaning and validation."""
    
    @staticmethod
    def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Strip whitespace from column names."""
        df.columns = df.columns.str.strip()
        return df
    
    @staticmethod
    def coerce_numeric(
        df: pd.DataFrame, 
        columns: List[str],
        fill_value: Optional[float] = None
    ) -> pd.DataFrame:
        """Convert columns to numeric, optionally filling NaN values."""
        for col in columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if fill_value is not None:
                    df[col] = df[col].fillna(fill_value)
        return df
    
    @staticmethod
    def impute_zero_prices(
        df: pd.DataFrame,
        price_col: str = 'total_net_price',
        method: str = 'median_by_sector'
    ) -> pd.DataFrame:
        """Impute zero or missing net prices."""
        if price_col not in df.columns:
            return df
        
        mask = (df[price_col] == 0) | df[price_col].isna()
        
        if not mask.any():
            return df
        
        logger.info(f"Imputing {mask.sum()} zero/missing prices using {method}")
        
        if method == 'median_by_sector':
            # Impute by sector median
            for sector in df['Sector'].unique():
                sector_mask = (df['Sector'] == sector) & mask
                if sector_mask.any():
                    sector_median = df[
                        (df['Sector'] == sector) & ~mask
                    ][price_col].median()
                    
                    if pd.notna(sector_median):
                        df.loc[sector_mask, price_col] = sector_median
        
        elif method == 'overall_median':
            # Simple overall median
            median_price = df[~mask][price_col].median()
            df.loc[mask, price_col] = median_price
        
        return df

class Formatters:
    """Formatting utilities for display."""
    
    @staticmethod
    def format_currency(value: Union[int, float]) -> str:
        """Format as currency."""
        if pd.isna(value):
            return "—"
        return f"${value:,.0f}"
    
    @staticmethod
    def format_rank_change(value: Union[int, float]) -> str:
        """Format rank change with arrows."""
        if pd.isna(value):
            return "—"
        
        value = int(value)
        if value > 0:
            return f"↑ +{value}"
        elif value < 0:
            return f"↓ {value}"
        else:
            return "—"
    
    @staticmethod
    def format_roi_years(value: Union[int, float]) -> str:
        """Format ROI in years."""
        if pd.isna(value):
            return "—"
        
        if value < 0:
            return "Immediate"
        elif value > 100:
            return "> 100 years"
        else:
            return f"{value:.1f} years"

class Validators:
    """Data validation utilities."""
    
    @staticmethod
    def check_required_columns(
        df: pd.DataFrame,
        required: List[str]
    ) -> List[str]:
        """Check for missing required columns."""
        return [col for col in required if col not in df.columns]
    
    @staticmethod
    def validate_roi_data(df: pd.DataFrame) -> Dict[str, Any]:
        """Validate ROI data quality."""
        issues = {}
        
        # Check for negative earnings
        if 'median_earnings_10yr' in df.columns:
            neg_earnings = (df['median_earnings_10yr'] < 0).sum()
            if neg_earnings > 0:
                issues['negative_earnings'] = neg_earnings
        
        # Check for extreme ROI values
        roi_cols = ['roi_statewide_years', 'roi_regional_years']
        for col in roi_cols:
            if col in df.columns:
                extreme = ((df[col] < -10) | (df[col] > 100)).sum()
                if extreme > 0:
                    issues[f'extreme_{col}'] = extreme
        
        # Check data completeness
        completeness = {}
        for col in df.columns:
            missing_pct = df[col].isna().mean()
            if missing_pct > 0.1:  # More than 10% missing
                completeness[col] = f"{missing_pct:.1%}"
        
        if completeness:
            issues['high_missing_data'] = completeness
        
        return issues