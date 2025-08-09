# lib/data_schema.py
from enum import Enum
from typing import Optional, List
from dataclasses import dataclass

class Sector(Enum):
    """Institution sector types."""
    PUBLIC = "Public"
    PRIVATE_FOR_PROFIT = "Private for-profit"
    PRIVATE_NON_PROFIT = "Private non-profit"

class AwardType(Enum):
    """Predominant credential types."""
    CERTIFICATE = "Certificate"
    ASSOCIATES = "Associate's"
    BACHELORS = "Bachelor's"
    MASTERS = "Master's"
    DOCTORAL = "Doctoral"

@dataclass
class InstitutionBase:
    """Common fields across all institutions."""
    unitid: str
    opeid6: str
    institution: str
    city: str
    county: str
    region: str
    regional_rank: Optional[int]
    roi_years: Optional[float]
    predominant_award: AwardType
    sector: Sector
    undergrad_students: Optional[int]
    median_earnings_10yr: Optional[float]
    earnings_above_hs: Optional[float]
    annual_net_price: Optional[float]
    zip_code: str
    latitude: float
    longitude: float

@dataclass
class PublicInstitution(InstitutionBase):
    """Public institution with additional statistical fields."""
    total_net_price_2yr: Optional[float]
    value: Optional[float]  # Statistical value for EP calculation
    denom: Optional[float]  # Denominator for EP calculation

@dataclass
class PrivateInstitution(InstitutionBase):
    """Private institution with credential-based pricing."""
    total_net_price_credential: Optional[float]
    is_for_profit: bool

class InstitutionLoader:
    """Unified loader that maintains separate handling for each type."""
    
    def __init__(self, public_path: str, private_path: str):
        self.public_path = public_path
        self.private_path = private_path
    
    def load_all(self) -> dict:
        """Load both institution types, maintaining their distinctions."""
        return {
            'public': self._load_public(),
            'private': self._load_private(),
            'combined': self._create_combined_view()
        }
    
    def _load_public(self) -> pd.DataFrame:
        """Load public institutions with their specific schema."""
        df = pd.read_csv(self.public_path)
        # Preserve VALUE and DENOM columns
        return df
    
    def _load_private(self) -> pd.DataFrame:
        """Load private institutions with their specific schema."""
        df = pd.read_csv(self.private_path)
        # Add is_for_profit flag
        df['is_for_profit'] = df['Sector'] == 'Private for-profit'
        return df
    
    def _create_combined_view(self) -> pd.DataFrame:
        """Create a unified view when needed, preserving sector differences."""
        public = self._load_public()
        private = self._load_private()
        
        # Mark source for tracking
        public['source'] = 'public'
        private['source'] = 'private'
        
        # Align common columns only
        common_cols = list(set(public.columns) & set(private.columns))
        
        combined = pd.concat([
            public[common_cols + ['source']],
            private[common_cols + ['source']]
        ], ignore_index=True)
        
        return combined