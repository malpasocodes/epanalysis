# lib/data_improved.py
import pandas as pd
import streamlit as st
from typing import Optional, Dict, Any, List
from pathlib import Path
import logging
from .models import DataConfig

logger = logging.getLogger(__name__)

class DataLoader:
    """Handles all data loading operations with validation and error handling."""
    
    def __init__(self, config: Optional[DataConfig] = None):
        self.config = config or DataConfig()
        self._validate_paths()
    
    def _validate_paths(self) -> None:
        """Validate that all required data files exist."""
        required_files = [
            self.config.combined_path,
            self.config.public_path
        ]
        missing = [f for f in required_files if not Path(f).exists()]
        if missing:
            logger.warning(f"Missing data files: {missing}")
    
    @st.cache_data
    def load_golden_roi(_self, path: str) -> pd.DataFrame:
        """Load Golden Ventures ROI data with robust parsing."""
        try:
            df = pd.read_csv(path)
            
            # Parse ROI column with multiple formats
            roi_col = "ROI: Years to Recoup Net Costs"
            if roi_col not in df.columns:
                logger.error(f"Expected column '{roi_col}' not found in {path}")
                return pd.DataFrame()
            
            # Clean and parse ROI values
            df['golden_roi_years'] = _self._parse_roi_values(df[roi_col])
            
            # Ensure required columns
            if 'UNITID' not in df.columns:
                df['UNITID'] = pd.NA
                
            return df[['UNITID', 'Institution', 'golden_roi_years']]
            
        except Exception as e:
            logger.error(f"Error loading {path}: {e}")
            st.error(f"Failed to load Golden Ventures data: {e}")
            return pd.DataFrame()
    
    def _parse_roi_values(self, series: pd.Series) -> pd.Series:
        """Parse ROI values handling parentheses for negative values."""
        cleaned = (series.astype(str)
                  .str.strip()
                  .str.replace(r'^\((.*)\)$', r'-\1', regex=True)  # (1.2) -> -1.2
                  .str.replace(r'[^0-9.\-]', '', regex=True))       # Remove non-numeric
        return pd.to_numeric(cleaned, errors='coerce')
    
    @st.cache_data
    def load_combined(_self, path: str) -> pd.DataFrame:
        """Load and validate combined dataset."""
        try:
            df = pd.read_csv(path)
            df.columns = df.columns.str.strip()  # Normalize column names
            
            # Add missing columns with defaults
            for col in _self.config.required_columns:
                if col not in df.columns:
                    logger.warning(f"Adding missing column: {col}")
                    df[col] = pd.NA
            
            # Convert numeric columns
            for col in _self.config.numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Validate data quality
            _self._validate_data_quality(df)
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading {path}: {e}")
            st.error(f"Failed to load combined dataset: {e}")
            return pd.DataFrame()
    
    def _validate_data_quality(self, df: pd.DataFrame) -> None:
        """Check data quality and log warnings."""
        # Check for institutions with zero net price
        zero_price = df[df['total_net_price'] == 0]
        if not zero_price.empty:
            logger.warning(f"{len(zero_price)} institutions have $0 net price")
        
        # Check for missing earnings data
        missing_earnings = df['median_earnings_10yr'].isna().sum()
        if missing_earnings > 0:
            logger.warning(f"{missing_earnings} institutions missing earnings data")
    
    @st.cache_data
    def merge_datasets(_self, combined_df: pd.DataFrame, golden_df: pd.DataFrame) -> pd.DataFrame:
        """Merge datasets with fallback strategies."""
        if combined_df.empty or golden_df.empty:
            return combined_df
        
        # Try merge by UNITID first
        if 'UNITID' in combined_df.columns and combined_df['UNITID'].notna().any():
            merged = combined_df.merge(golden_df, on='UNITID', how='left', suffixes=('', '_golden'))
        else:
            # Fallback to name matching
            merged = _self._merge_by_name(combined_df, golden_df)
        
        # Clean up duplicate columns
        merged = _self._resolve_duplicate_columns(merged)
        
        return merged
    
    def _merge_by_name(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        """Merge by normalized institution names."""
        df1['name_key'] = df1['Institution'].str.lower().str.strip()
        df2['name_key'] = df2['Institution'].str.lower().str.strip()
        
        merged = df1.merge(
            df2.drop(columns=['Institution'], errors='ignore'),
            on='name_key',
            how='left',
            suffixes=('', '_golden')
        )
        return merged.drop(columns=['name_key'])
    
    def _resolve_duplicate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Resolve columns with _x/_y suffixes from merges."""
        # Find columns with suffixes
        base_cols = set()
        for col in df.columns:
            if col.endswith('_x') or col.endswith('_y'):
                base_cols.add(col[:-2])
        
        # Coalesce duplicate columns
        for base in base_cols:
            x_col = f"{base}_x"
            y_col = f"{base}_y"
            
            if x_col in df.columns and y_col in df.columns:
                df[base] = df[x_col].fillna(df[y_col])
                df = df.drop(columns=[x_col, y_col])
        
        return df
    
    def load_all(self) -> pd.DataFrame:
        """Main entry point to load all data."""
        combined = self.load_combined(self.config.combined_path)
        golden = self.load_golden_roi(self.config.public_path)
        return self.merge_datasets(combined, golden)