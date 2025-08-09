# lib/models.py
from typing import Optional, List
from dataclasses import dataclass
import pandas as pd

@dataclass
class DataConfig:
    """Configuration for data paths and column mappings."""
    combined_path: str = "data/roi_with_county_baseline_combined_clean.csv"
    public_path: str = "data/public.csv"
    private_path: str = "data/private.csv"
    county_earnings_path: str = "data/hs_median_county_25_34.csv"
    
    # Expected columns with their types
    numeric_columns: List[str] = None
    required_columns: List[str] = None
    
    def __post_init__(self):
        if self.numeric_columns is None:
            self.numeric_columns = [
                "total_net_price", "median_earnings_10yr", 
                "premium_statewide", "premium_regional",
                "roi_statewide_years", "roi_regional_years", 
                "rank_statewide", "rank_regional",
                "rank_change", "hs_median_income"
            ]
        if self.required_columns is None:
            self.required_columns = [
                "UNITID", "Institution", "Region", "County", "Sector"
            ]

@dataclass 
class Institution:
    """Represents a single institution with its metrics."""
    unitid: Optional[str]
    name: str
    region: str
    county: str
    sector: str
    net_price: Optional[float]
    earnings_10yr: Optional[float]
    roi_statewide: Optional[float]
    roi_regional: Optional[float]
    rank_statewide: Optional[int]
    rank_regional: Optional[int]
    
    @property
    def rank_change(self) -> Optional[int]:
        """Calculate rank improvement (positive = better under regional)."""
        if self.rank_statewide and self.rank_regional:
            return self.rank_statewide - self.rank_regional
        return None
    
    @classmethod
    def from_row(cls, row: pd.Series) -> 'Institution':
        """Create Institution from a DataFrame row."""
        return cls(
            unitid=row.get('UNITID'),
            name=row.get('Institution', 'Unknown'),
            region=row.get('Region', 'Unknown'),
            county=row.get('County', 'Unknown'),
            sector=row.get('Sector', 'Unknown'),
            net_price=pd.to_numeric(row.get('total_net_price'), errors='coerce'),
            earnings_10yr=pd.to_numeric(row.get('median_earnings_10yr'), errors='coerce'),
            roi_statewide=pd.to_numeric(row.get('roi_statewide_years'), errors='coerce'),
            roi_regional=pd.to_numeric(row.get('roi_regional_years'), errors='coerce'),
            rank_statewide=pd.to_numeric(row.get('rank_statewide'), errors='coerce'),
            rank_regional=pd.to_numeric(row.get('rank_regional'), errors='coerce')
        )