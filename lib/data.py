# lib/data.py
import pandas as pd
import streamlit as st

NUMERIC_COLS = [
    "total_net_price","median_earnings_10yr","premium_statewide","premium_regional",
    "roi_statewide_years","roi_regional_years","rank_statewide","rank_regional",
    "rank_change","hs_median_income",
]
EXPECTED_COLS = {"UNITID": None,"Institution": None,"Region": None,"County": None,"Sector": None, **{c: None for c in NUMERIC_COLS}}

@st.cache_data
def load_public_roi(path: str) -> pd.DataFrame:
    """Return Golden Returns ROI as [UNITID, Institution, golden_roi_years] from data/public.csv."""
    try:
        pub = pd.read_csv(path)
    except FileNotFoundError:
        st.warning(f"Public ROI file not found: {path}")
        return pd.DataFrame(columns=["UNITID","Institution","golden_roi_years"])

    col = "ROI: Years to Recoup Net Costs"
    if col not in pub.columns:
        st.warning(f"'{col}' not found in {path}")
        return pd.DataFrame(columns=["UNITID","Institution","golden_roi_years"])

    s = pub[col].astype(str).str.strip()
    s = s.str.replace(r"^\((.*)\)$", r"-\1", regex=True)  # (1.2) -> -1.2
    s = s.str.replace(r"[^0-9.\-]", "", regex=True)      # strip $, commas, spaces
    pub["golden_roi_years"] = pd.to_numeric(s, errors="coerce")

    if "UNITID" not in pub.columns: pub["UNITID"] = pd.NA
    if "Institution" not in pub.columns: pub["Institution"] = pd.NA
    return pub[["UNITID","Institution","golden_roi_years"]]

@st.cache_data
def load_combined(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Combined dataset not found: {path}")
        return pd.DataFrame(columns=list(EXPECTED_COLS.keys()))

    # 🔧 Normalize column names to avoid trailing spaces / weird chars
    df.columns = df.columns.str.strip()

    for col, default in EXPECTED_COLS.items():
        if col not in df.columns:
            df[col] = default

    for c in NUMERIC_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

@st.cache_data
def load_roi_metrics_dataset(roi_metrics_path: str = "data/roi-metrics.csv", 
                             institutions_path: str = "data/gr-institutions.csv") -> pd.DataFrame:
    """New primary loader: roi-metrics dataset merged with institutions data."""
    try:
        # Load ROI metrics
        roi_df = pd.read_csv(roi_metrics_path)
        
        # Load institutions data for additional fields like Region
        inst_df = pd.read_csv(institutions_path)
        
        # Filter for Associate's institutions only
        inst_df = inst_df[inst_df['Predominant Award'] == "Associate's"]
        
        # Merge on Institution name (both datasets should have this)
        # Using inner join to only keep institutions that are Associate's
        df = roi_df.merge(
            inst_df[['Institution', 'Region', 'Predominant Award']], 
            on='Institution', 
            how='inner'
        )
        
        # Handle any missing regions
        if df['Region'].isna().any():
            missing_count = df['Region'].isna().sum()
            st.warning(f"Missing Region data for {missing_count} institutions")
        
        # Ensure numeric columns are properly typed
        numeric_cols = [
            'median_earnings_10yr', 'total_net_price', 'premium_statewide', 'premium_regional',
            'roi_statewide_years', 'roi_regional_years', 'rank_statewide', 'rank_regional', 
            'rank_change', 'hs_median_income'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Correct total_net_price: Associate's degrees are 2-year programs
        # So total cost should be 2x annual net price
        df['total_net_price'] = df['total_net_price'] * 2
        
        # Recalculate ROI metrics with corrected total_net_price
        # Statewide ROI
        statewide_baseline = 24939.44
        df['premium_statewide'] = df['median_earnings_10yr'] - statewide_baseline
        df['roi_statewide_years'] = df['total_net_price'] / df['premium_statewide']
        
        # Regional ROI
        df['premium_regional'] = df['median_earnings_10yr'] - df['hs_median_income']
        df['roi_regional_years'] = df['total_net_price'] / df['premium_regional']
        
        # Handle invalid ROI (negative premium or division by zero)
        df.loc[df['premium_statewide'] <= 0, 'roi_statewide_years'] = 999
        df.loc[df['premium_regional'] <= 0, 'roi_regional_years'] = 999
        
        # Recalculate rankings based on corrected ROI
        df['rank_statewide'] = df['roi_statewide_years'].rank(method='min')
        df['rank_regional'] = df['roi_regional_years'].rank(method='min')
        df['rank_change'] = df['rank_statewide'] - df['rank_regional']
        
        return df
        
    except FileNotFoundError as e:
        st.error(f"Dataset file not found: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading datasets: {e}")
        return pd.DataFrame()

@st.cache_data
def load_dataset(combined_path: str, public_path: str = None) -> pd.DataFrame:
    """Legacy loader: combined file (public.csv no longer used - archived)."""
    df = load_combined(combined_path)
    if df.empty:
        return df
    
    # Skip Golden Returns ROI merge - public.csv archived
    if public_path is None:
        return df
        
    # Legacy code for public.csv merge (kept for backward compatibility)
    pub = load_public_roi(public_path)
    if pub.empty:
        return df

    merged = df.copy()
    if "UNITID" in merged.columns and merged["UNITID"].notna().any():
        merged = merged.merge(pub, on="UNITID", how="left")
    else:
        merged["Institution_key"] = merged["Institution"].astype(str).strip().str.lower()
        pub["Institution_key"] = pub["Institution"].astype(str).strip().str.lower()
        merged = merged.merge(pub.drop(columns=["Institution"]), on="Institution_key", how="left")
        merged = merged.drop(columns=["Institution_key"])

    # --- Coalesce Institution column after merge ---
    if "Institution" not in merged.columns:
        inst_x = merged.get("Institution_x")
        inst_y = merged.get("Institution_y")
        if inst_x is not None or inst_y is not None:
            merged["Institution"] = (
                (inst_x if inst_x is not None else pd.Series([None] * len(merged)))
                .fillna(inst_y if inst_y is not None else pd.Series([None] * len(merged)))
            )
    # Drop merge suffix columns if present
    for col in ["Institution_x", "Institution_y"]:
        if col in merged.columns:
            merged.drop(columns=col, inplace=True)

    return merged