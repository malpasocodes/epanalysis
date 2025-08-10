#!/usr/bin/env python3
"""
Update ROI calculations with methodologically consistent statewide HS baseline.

This script:
1. Recalculates premium_statewide using the weighted average from county data ($24,939.44)
2. Recalculates roi_statewide_years based on the new premiums
3. Recalculates rank_statewide based on the new ROI values
4. Updates the cleaned dataset file
"""

import pandas as pd
from lib.hs_baseline import STATEWIDE_HS_BASELINE

def update_statewide_calculations(input_file: str, output_file: str = None):
    """Update the dataset with corrected statewide baseline calculations."""
    
    if output_file is None:
        output_file = input_file
    
    print(f"Loading data from: {input_file}")
    df = pd.read_csv(input_file)
    
    print(f"Original statewide baseline (implied): ${df.iloc[0]['median_earnings_10yr'] - df.iloc[0]['premium_statewide']:,.2f}")
    print(f"New statewide baseline (weighted): ${STATEWIDE_HS_BASELINE:,.2f}")
    
    # Recalculate premium_statewide
    df['premium_statewide'] = df['median_earnings_10yr'] - STATEWIDE_HS_BASELINE
    
    # Recalculate roi_statewide_years (handle division by zero)
    df['roi_statewide_years'] = df['total_net_price'] / df['premium_statewide']
    df.loc[df['premium_statewide'] <= 0, 'roi_statewide_years'] = float('inf')
    
    # Recalculate rank_statewide (lower ROI years = better rank)
    # Handle infinite values by ranking them last
    finite_roi = df['roi_statewide_years'].replace([float('inf'), -float('inf')], float('nan'))
    df['rank_statewide'] = finite_roi.rank(method='min', ascending=True)
    
    # Fill NaN ranks (from infinite ROI) with worst possible rank
    max_finite_rank = df['rank_statewide'].max()
    df['rank_statewide'] = df['rank_statewide'].fillna(max_finite_rank + 1)
    df['rank_statewide'] = df['rank_statewide'].astype(int)
    
    # Recalculate rank_change
    df['rank_change'] = df['rank_regional'] - df['rank_statewide']
    
    # Summary statistics
    print(f"\nSummary of changes:")
    print(f"Premium statewide - Mean: ${df['premium_statewide'].mean():,.2f}, Median: ${df['premium_statewide'].median():,.2f}")
    print(f"ROI statewide years - Mean: {df['roi_statewide_years'].replace([float('inf')], float('nan')).mean():.2f}")
    print(f"Institutions with negative premium: {(df['premium_statewide'] <= 0).sum()}")
    
    # Save updated data
    print(f"\nSaving updated data to: {output_file}")
    df.to_csv(output_file, index=False)
    
    return df

if __name__ == "__main__":
    # Update the main dataset
    updated_df = update_statewide_calculations(
        "data/roi_with_county_baseline_combined_clean.csv"
    )
    
    print("\nFirst 3 rows after update:")
    cols = ['Institution', 'median_earnings_10yr', 'premium_statewide', 'roi_statewide_years', 'rank_statewide']
    print(updated_df[cols].head(3))