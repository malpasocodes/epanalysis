import pandas as pd
from pathlib import Path

def calculate_statewide_hs_median(county_data_path: str = "data/hs_median_county_25_34.csv") -> float:
    """
    Calculate the statewide high school median income as a weighted average
    of county-level medians using ACS survey weights.
    
    Formula:
    Statewide = Σ(hs_median_income_i × weight_sum_i) / Σ(weight_sum_i)
    
    Returns:
        float: Weighted average high school median income for California
    """
    df = pd.read_csv(county_data_path)
    
    numerator = (df['hs_median_income'] * df['weight_sum']).sum()
    denominator = df['weight_sum'].sum()
    
    return numerator / denominator

# Calculate and store as a constant
STATEWIDE_HS_BASELINE = calculate_statewide_hs_median()

if __name__ == "__main__":
    print(f"California Statewide HS Median Income (weighted): ${STATEWIDE_HS_BASELINE:,.2f}")
    
    # Verify calculation
    df = pd.read_csv("data/hs_median_county_25_34.csv")
    print(f"Based on {len(df)} counties")
    print(f"Total weighted population: {df['weight_sum'].sum():,.0f}")