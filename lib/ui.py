# lib/ui.py
import streamlit as st
import pandas as pd
from pathlib import Path
from .charts import quadrant_chart

def load_markdown_content(filename: str) -> str:
    """Load markdown content from the content directory."""
    content_dir = Path(__file__).parent.parent / "content"
    file_path = content_dir / filename
    
    if file_path.exists():
        return file_path.read_text()
    else:
        return f"Content file not found: {filename}"

def render_markdown_page(filename: str):
    """Render a markdown file as a Streamlit page."""
    content = load_markdown_content(filename)
    st.markdown(content)

def render_home():
    st.title("Higher Ed ROI Research Lab")
    st.markdown("*Data-driven insights on college earnings premiums and ROI outcomes*")
    
    st.markdown("---")
    
    # Mission
    st.subheader("Mission")
    st.markdown(
        "The **Higher Ed ROI Research Lab** provides independent, data-driven analysis of higher education "
        "return on investment (ROI) and earnings premium outcomes. Our primary audience is researchers, "
        "policymakers, and education analysts. We take no advocacy position on individual institutions, "
        "programs, metrics or policies. Instead, our goal is to provide clear, well-documented methods that "
        "help inform policy discussions, institutional accountability, and public understanding of "
        "postsecondary education value."
    )
    
    # Current Focus
    st.subheader("Current Focus")
    st.markdown(
        "Our current work examines the policy implications of new federal accountability rules, "
        "particularly the **Earnings Premium Regulation** introduced under Title VIII, Subtitle E "
        "of the Higher Education Act amendments (effective July 1, 2026) "
        "This rule may make certain programs ineligible for federal funding if graduates' median "
        "earnings fall below the median for comparable high school graduates in their state or nationwide.\n\n"
        "We are using **California's two-year and certificate-granting colleges** as a pilot dataset to explore "
        "how these rules may operate and how alternative metrics may "
        "yield different policy outcomes."
    )
    
    
    # Disclaimer
    st.subheader("Disclaimer")
    st.markdown(
        "The data and analyses on this site are intended **solely for research and policy analysis purposes**. "
        "They should **not** be used to make enrollment decisions about individual colleges or programs. "
        "Metrics are based on public datasets (IPEDS, U.S. Census, Golden Returns) and may not capture all factors "
        "affecting individual educational or economic outcomes."
    )
    
    st.info("Use the sidebar navigation to explore our research tools and datasets.")

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

def render_college_view(df):
    """Render the College View page for searching and viewing individual institution details."""
    st.title("College View")
    st.markdown("Search for a college to view detailed metrics and analysis")
    
    # Check if data is available
    if df.empty:
        st.error("No data available. Please check the dataset files.")
        return
    
    # Create search box
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Get list of institutions for selectbox
        institutions = sorted(df['Institution'].unique())
        
        # Search selectbox with placeholder
        selected_institution = st.selectbox(
            "Search for a college:",
            options=[""] + institutions,
            format_func=lambda x: "Type to search..." if x == "" else x,
            help="Start typing to search for a college"
        )
    
    # Display institution details if one is selected
    if selected_institution and selected_institution != "":
        # Get data for selected institution
        inst_data = df[df['Institution'] == selected_institution].iloc[0]
        
        st.markdown("---")
        
        # Institution header
        st.header(f"📍 {selected_institution}")
        
        # Basic information in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("County", inst_data.get('County', 'N/A'))
            if 'Region' in inst_data:
                st.metric("Region", inst_data.get('Region', 'N/A'))
        
        with col2:
            st.metric("Sector", inst_data.get('Sector', 'N/A'))
            if 'Predominant Award' in inst_data:
                st.metric("Award Type", inst_data.get('Predominant Award', 'N/A'))
        
        with col3:
            st.metric("10-Year Median Earnings", f"${inst_data['median_earnings_10yr']:,.0f}")
            st.metric("Total Net Price (2 years)", f"${inst_data['total_net_price']:,.0f}")
        
        # Earnings Premium Section
        st.markdown("---")
        st.subheader("📊 Earnings Premium")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Statewide Premium",
                f"${inst_data['premium_statewide']:,.0f}",
                help="Earnings above statewide HS baseline ($24,939)"
            )
        
        with col2:
            st.metric(
                "Regional Premium", 
                f"${inst_data['premium_regional']:,.0f}",
                help=f"Earnings above county HS baseline (${inst_data['hs_median_income']:,.0f})"
            )
        
        with col3:
            delta = inst_data['premium_statewide'] - inst_data['premium_regional']
            st.metric(
                "Premium Delta",
                f"${abs(delta):,.0f}",
                delta=f"{'Higher' if delta > 0 else 'Lower'} statewide",
                delta_color="normal" if delta > 0 else "inverse"
            )
        
        # ROI Section
        st.markdown("---")
        st.subheader("💰 Return on Investment (ROI)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            roi_sw = inst_data['roi_statewide_years']
            if roi_sw < 999:
                st.metric(
                    "Statewide ROI",
                    f"{roi_sw:.1f} years",
                    help="Years to recoup costs using statewide baseline"
                )
            else:
                st.metric(
                    "Statewide ROI",
                    "N/A",
                    help="Negative earnings premium"
                )
        
        with col2:
            roi_reg = inst_data['roi_regional_years']
            if roi_reg < 999:
                st.metric(
                    "Regional ROI",
                    f"{roi_reg:.1f} years",
                    help="Years to recoup costs using regional baseline"
                )
            else:
                st.metric(
                    "Regional ROI",
                    "N/A",
                    help="Negative earnings premium"
                )
        
        with col3:
            if roi_sw < 999 and roi_reg < 999:
                roi_delta = roi_sw - roi_reg
                st.metric(
                    "ROI Difference",
                    f"{abs(roi_delta):.1f} years",
                    delta=f"{'Longer' if roi_delta > 0 else 'Shorter'} statewide",
                    delta_color="inverse" if roi_delta > 0 else "normal"
                )
            else:
                st.metric("ROI Difference", "N/A")
        
        # Rankings Section
        st.markdown("---")
        st.subheader("🏆 Rankings")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rank_sw = int(inst_data['rank_statewide'])
            total_institutions = len(df)
            st.metric(
                "Statewide Rank",
                f"#{rank_sw} of {total_institutions}",
                help="Ranking based on statewide ROI (lower is better)"
            )
        
        with col2:
            rank_reg = int(inst_data['rank_regional'])
            st.metric(
                "Regional Rank",
                f"#{rank_reg} of {total_institutions}",
                help="Ranking based on regional ROI (lower is better)"
            )
        
        with col3:
            rank_change = int(inst_data['rank_change'])
            if rank_change != 0:
                st.metric(
                    "Rank Change",
                    f"{abs(rank_change)} positions",
                    delta=f"{'Better' if rank_change > 0 else 'Worse'} regionally",
                    delta_color="normal" if rank_change > 0 else "inverse"
                )
            else:
                st.metric("Rank Change", "Same rank")
        
        # Detailed Metrics Table
        st.markdown("---")
        st.subheader("📋 Detailed Metrics")
        
        # Create a detailed metrics dataframe
        metrics_data = {
            "Metric": [
                "Graduate Median Earnings (10yr)",
                "Annual Net Price",
                "Total Net Price (2 years)",
                "County HS Baseline",
                "Statewide HS Baseline",
                "Statewide Earnings Premium",
                "Regional Earnings Premium",
                "Statewide ROI (years)",
                "Regional ROI (years)",
                "Statewide Rank",
                "Regional Rank",
                "Rank Change"
            ],
            "Value": [
                f"${inst_data['median_earnings_10yr']:,.0f}",
                f"${inst_data['total_net_price']/2:,.0f}",
                f"${inst_data['total_net_price']:,.0f}",
                f"${inst_data['hs_median_income']:,.0f}",
                "$24,939",
                f"${inst_data['premium_statewide']:,.0f}",
                f"${inst_data['premium_regional']:,.0f}",
                f"{inst_data['roi_statewide_years']:.2f}" if inst_data['roi_statewide_years'] < 999 else "N/A",
                f"{inst_data['roi_regional_years']:.2f}" if inst_data['roi_regional_years'] < 999 else "N/A",
                f"#{int(inst_data['rank_statewide'])}",
                f"#{int(inst_data['rank_regional'])}",
                f"{int(inst_data['rank_change']):+d}"
            ]
        }
        
        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)

