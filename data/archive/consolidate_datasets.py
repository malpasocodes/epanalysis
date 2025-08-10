#!/usr/bin/env python3
"""
Dataset Consolidation Script
Consolidates gr-private.csv and gr-public.csv into a single gr-institutions.csv file
with 13 standardized fields including Annual Net Price.
"""

import pandas as pd
import os
from pathlib import Path

def clean_bom(text):
    """Remove BOM (Byte Order Mark) characters from text"""
    if isinstance(text, str):
        return text.replace('\ufeff', '').strip()
    return text

def clean_monetary_field(series):
    """Clean monetary fields by removing formatting and converting to numeric"""
    if series.dtype == 'object':
        # Remove currency symbols, commas, and parentheses
        cleaned = series.astype(str).str.replace(r'[\$,()]', '', regex=True)
        # Handle negative values in parentheses format
        cleaned = cleaned.str.replace(r'^\((.*)\)$', r'-\1', regex=True)
        # Convert to numeric, coercing errors to NaN
        return pd.to_numeric(cleaned, errors='coerce')
    return series

def load_and_clean_dataset(filepath):
    """Load CSV file and perform initial cleaning"""
    print(f"Loading: {filepath}")
    
    # Read CSV with proper encoding handling
    df = pd.read_csv(filepath, encoding='utf-8-sig')
    
    # Clean column names (remove BOM and whitespace)
    df.columns = [clean_bom(col) for col in df.columns]
    
    # Clean string columns of BOM characters
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(clean_bom)
    
    print(f"Loaded {len(df)} rows with columns: {list(df.columns)}")
    return df

def consolidate_datasets():
    """Main consolidation function"""
    script_dir = Path(__file__).parent
    
    # Define required fields for consolidation (13 fields total)
    required_fields = [
        'OPEID6',
        'Institution', 
        'City',
        'County',
        'Region',
        'Predominant Award',
        'Sector',
        'Undergraduate Degree-seeking students',
        'ZIP',
        'Latitude',
        'Longitude',
        'Median Earnings 10 Years After Enrollment',
        'Annual Net Price'  # NEW FIELD ADDED
    ]
    
    print("=== Dataset Consolidation Process ===")
    print(f"Target fields ({len(required_fields)}): {required_fields}")
    print()
    
    # Load both datasets
    private_df = load_and_clean_dataset(script_dir / 'gr-private.csv')
    public_df = load_and_clean_dataset(script_dir / 'gr-public.csv')
    
    print("\n=== Field Availability Check ===")
    
    # Check field availability in both datasets
    private_fields = set(private_df.columns)
    public_fields = set(public_df.columns)
    
    missing_private = [field for field in required_fields if field not in private_fields]
    missing_public = [field for field in required_fields if field not in public_fields]
    
    if missing_private:
        print(f"Missing from gr-private.csv: {missing_private}")
    if missing_public:
        print(f"Missing from gr-public.csv: {missing_public}")
    
    if not missing_private and not missing_public:
        print("✓ All required fields found in both datasets")
    
    print(f"\nPrivate dataset available fields: {sorted(private_fields)}")
    print(f"Public dataset available fields: {sorted(public_fields)}")
    
    # Extract required fields from each dataset
    print("\n=== Data Extraction and Cleaning ===")
    
    private_subset = private_df[required_fields].copy()
    public_subset = public_df[required_fields].copy()
    
    print(f"Private subset: {len(private_subset)} rows")
    print(f"Public subset: {len(public_subset)} rows")
    
    # Clean monetary and numeric fields
    monetary_fields = ['Annual Net Price', 'Median Earnings 10 Years After Enrollment']
    numeric_fields = ['OPEID6', 'Undergraduate Degree-seeking students', 'Latitude', 'Longitude']
    
    for field in monetary_fields:
        if field in private_subset.columns:
            private_subset[field] = clean_monetary_field(private_subset[field])
            public_subset[field] = clean_monetary_field(public_subset[field])
            print(f"Cleaned monetary field: {field}")
    
    for field in numeric_fields:
        if field in private_subset.columns:
            # Remove commas from numeric fields that might be formatted
            if private_subset[field].dtype == 'object':
                private_subset[field] = private_subset[field].astype(str).str.replace(',', '')
                public_subset[field] = public_subset[field].astype(str).str.replace(',', '')
            
            private_subset[field] = pd.to_numeric(private_subset[field], errors='coerce')
            public_subset[field] = pd.to_numeric(public_subset[field], errors='coerce')
            print(f"Cleaned numeric field: {field}")
    
    # Concatenate datasets
    print("\n=== Dataset Concatenation ===")
    consolidated_df = pd.concat([private_subset, public_subset], ignore_index=True)
    print(f"Consolidated dataset: {len(consolidated_df)} rows")
    
    # Sort by OPEID6
    consolidated_df = consolidated_df.sort_values('OPEID6').reset_index(drop=True)
    print("Sorted by OPEID6")
    
    # Data quality checks
    print("\n=== Data Quality Summary ===")
    print(f"Total institutions: {len(consolidated_df)}")
    print(f"Unique OPEID6s: {consolidated_df['OPEID6'].nunique()}")
    print(f"Private institutions: {len(private_subset)}")
    print(f"Public institutions: {len(public_subset)}")
    
    # Check for missing values in key fields
    for field in required_fields:
        missing_count = consolidated_df[field].isnull().sum()
        if missing_count > 0:
            print(f"Missing values in {field}: {missing_count}")
    
    # Check Annual Net Price statistics
    net_price_stats = consolidated_df['Annual Net Price'].describe()
    print(f"\nAnnual Net Price Statistics:")
    print(net_price_stats)
    
    # Save consolidated dataset
    output_path = script_dir / 'gr-institutions.csv'
    consolidated_df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\n✓ Consolidated dataset saved to: {output_path}")
    
    # Display sample of final dataset
    print("\n=== Sample of Consolidated Dataset ===")
    print(consolidated_df.head(3).to_string())
    
    return consolidated_df, {
        'total_rows': len(consolidated_df),
        'private_rows': len(private_subset),
        'public_rows': len(public_subset),
        'unique_opeid6': consolidated_df['OPEID6'].nunique(),
        'fields': required_fields,
        'output_path': str(output_path)
    }

if __name__ == "__main__":
    consolidated_df, summary = consolidate_datasets()
    print("\n=== Consolidation Complete ===")
    print(f"Final dataset contains {summary['total_rows']} institutions")
    print(f"Saved to: {summary['output_path']}")