# lib/ui.py
import streamlit as st
import pandas as pd
from .charts import quadrant_chart

def render_home():
    st.title("Earnings Premium & ROI — Why the Baseline Matters")
    st.write(
        "This project examines how the **Earnings Premium** regulation assesses college value, "
        "and shows how switching from a single **statewide** high-school earnings baseline to a "
        "**local (county)** baseline can radically change ROI and rankings."
    )
    st.subheader("What you’ll find here")
    st.markdown(
        "- **Explore Data**: Interactive quadrant chart (Price vs 10-year Earnings) with region/sector filters.\n"
        "- **Rankings**: Before/after ROI ranks (Statewide vs Local baseline).\n"
        "- **Methodology**: Definitions, data sources, assumptions, and limitations.\n"
        "- **About**: Project background and credits."
    )
    st.info("Use the left sidebar to navigate.")

def render_explore(df: pd.DataFrame):
    import altair as alt  # lazy import to avoid blank app if Altair missing
    st.title("Explore: Price vs. 10-Year Earnings")
    st.caption("Each point is an institution. Quadrants split by medians of the filtered set.")

    # Filters (Region & Sector)
    st.sidebar.header("Filters")
    regions = sorted([r for r in df["Region"].dropna().unique()])
    sectors = sorted([s for s in df["Sector"].dropna().unique()])
    sel_regions = st.sidebar.multiselect("Region", options=regions, default=regions)
    sel_sectors = st.sidebar.multiselect("Sector", options=sectors, default=sectors)

    f = df[(df["Region"].isin(sel_regions)) & (df["Sector"].isin(sel_sectors))].copy()
    if f.empty:
        st.warning("No data after filters. Adjust selections.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Institutions", f"{len(f):,}")
    c2.metric("Median Total Net Price", f"${f['total_net_price'].median():,.0f}")
    c3.metric("Median 10-Year Earnings", f"${f['median_earnings_10yr'].median():,.0f}")

    st.altair_chart(quadrant_chart(f), use_container_width=True)

    st.subheader("Filtered institutions")
    show_cols = [
        "Institution", "Region", "County", "Sector",
        "total_net_price", "median_earnings_10yr",
        "premium_statewide", "premium_regional",
        "roi_statewide_years", "roi_regional_years",
    ]
    existing = [c for c in show_cols if c in f.columns]
    st.dataframe(
        f[existing].rename(columns={
            "total_net_price": "Total Net Price",
            "median_earnings_10yr": "Median Earnings (10y)",
            "premium_statewide": "Premium (Statewide)",
            "premium_regional": "Premium (Local)",
            "roi_statewide_years": "ROI (Statewide, yrs)",
            "roi_regional_years": "ROI (Local, yrs)",
        }),
        use_container_width=True, hide_index=True,
    )

def render_rankings(df):
    import pandas as pd
    import streamlit as st

    st.title("Rankings")
    st.caption("Institution • Region • ROI Rank (Statewide) • ROI Rank (Local) • Δ (SW→Local)")

    # 🔧 Normalize again just in case (cheap and safe)
    df = df.copy()
    df.columns = df.columns.str.strip()

    required = ["Institution", "Region", "rank_statewide", "rank_regional"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing expected columns: {missing}")
        st.caption("Here are the columns I do see (check for stray spaces or different names):")
        st.code(list(df.columns))
        return

    # Ensure numeric ranks
    for c in ["rank_statewide", "rank_regional"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Δ = statewide − local (positive = improved under local baseline)
    delta = (pd.to_numeric(df.get("rank_change"), errors="coerce")
             if "rank_change" in df.columns else df["rank_statewide"] - df["rank_regional"])

    base = (
        df.assign(**{"Δ (SW→Local)": delta})
          .dropna(subset=["rank_statewide", "rank_regional"])
          .loc[:, ["Institution", "Region", "rank_statewide", "rank_regional", "Δ (SW→Local)"]]
          .rename(columns={
              "rank_statewide": "ROI Rank (Statewide)",
              "rank_regional":  "ROI Rank (Local)",
          })
    )

    # Simple arrow for Δ
    def delta_arrow(x):
        if pd.isna(x): return ""
        try:
            xi = int(x)
        except Exception:
            return ""
        if xi > 0:  return f"↑ +{xi}"
        if xi < 0:  return f"↓ {xi}"
        return "—"
    base["Δ"] = base["Δ (SW→Local)"].apply(delta_arrow)

    # Controls
    c1, c2, c3 = st.columns([2, 1.2, 1])
    with c1:
        q = st.text_input("Search (Institution or Region)", value="", placeholder="Type to filter…").strip().lower()
    with c2:
        sort_by = st.selectbox("Sort by", ["ROI Rank (Local)", "ROI Rank (Statewide)", "Δ (SW→Local)"], index=0)
    with c3:
        asc = st.toggle("Ascending", value=True)

    if q:
        mask = (
            base["Institution"].astype(str).str.lower().str.contains(q)
            | base["Region"].astype(str).str.lower().str.contains(q)
        )
        base = base[mask]

    # Sort
    if sort_by == "Δ (SW→Local)" and not asc:
        base = base.assign(_abs=base["Δ (SW→Local)"].abs()).sort_values("_abs", ascending=False).drop(columns="_abs")
    else:
        base = base.sort_values(sort_by, ascending=asc, na_position="last")

    # Show
    st.dataframe(
        base[["Institution", "Region", "ROI Rank (Statewide)", "ROI Rank (Local)", "Δ", "Δ (SW→Local)"]],
        use_container_width=True, hide_index=True,
    )

def render_methodology():
    st.title("Methodology")
    st.markdown(
        "- **Earnings (10y):** Median earnings ~10 years after enrollment (College Scorecard).\n"
        "- **HS baselines:** Statewide and county medians for HS grads (ages 25–34; ACS/IPUMS).\n"
        "- **Premiums:** Graduate earnings − HS baseline.\n"
        "- **ROI (years):** Total net price ÷ annual earnings premium (simple payback).\n"
        "- **Assumptions & Limitations:** Completion time, imputation rules, missing-data handling; not causal."
    )

