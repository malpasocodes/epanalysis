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

def render_earnings_premium_rankings(df):
    """Render side-by-side Earnings Premium rankings for C-Metric and H-Metric."""
    st.title("Earnings Premium Rankings")
    st.markdown("Side-by-side comparison of rankings based on C-Metric (Statewide) and H-Metric (Regional) earnings premiums")
    
    # Check if data is available
    if df.empty:
        st.error("No data available. Please check the dataset files.")
        return
    
    # Sort data for rankings
    df_cmetric = df.copy().sort_values('premium_statewide', ascending=False)
    df_hmetric = df.copy().sort_values('premium_regional', ascending=False)
    
    # Add rank columns
    df_cmetric['Rank'] = range(1, len(df_cmetric) + 1)
    df_hmetric['Rank'] = range(1, len(df_hmetric) + 1)
    
    # Create two columns for side-by-side display
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 C-Metric Rankings")
        st.markdown("*Based on Statewide Baseline ($24,939)*")
        
        # Prepare display dataframe
        display_cmetric = df_cmetric[['Rank', 'Institution', 'Sector', 'premium_statewide']].copy()
        display_cmetric.columns = ['Rank', 'Institution', 'Sector', 'Earnings Premium']
        # Round earnings premium to whole numbers (keep as float to handle NaN)
        display_cmetric['Earnings Premium'] = display_cmetric['Earnings Premium'].round(0)
        
        # Display table with formatting
        st.dataframe(
            display_cmetric,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.NumberColumn(
                    "Rank",
                    format="%d"
                ),
                "Earnings Premium": st.column_config.NumberColumn(
                    "Earnings Premium",
                    format="$%,.0f"
                )
            },
            height=600
        )
    
    with col2:
        st.subheader("📊 H-Metric Rankings")
        st.markdown("*Based on Regional (County) Baselines*")
        
        # Prepare display dataframe
        display_hmetric = df_hmetric[['Rank', 'Institution', 'Sector', 'premium_regional']].copy()
        display_hmetric.columns = ['Rank', 'Institution', 'Sector', 'Earnings Premium']
        # Round earnings premium to whole numbers (keep as float to handle NaN)
        display_hmetric['Earnings Premium'] = display_hmetric['Earnings Premium'].round(0)
        
        # Display table with formatting
        st.dataframe(
            display_hmetric,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.NumberColumn(
                    "Rank",
                    format="%d"
                ),
                "Earnings Premium": st.column_config.NumberColumn(
                    "Earnings Premium",
                    format="$%,.0f"
                )
            },
            height=600
        )
    
    # Scatterplot section
    st.markdown("---")
    st.subheader("📈 Earnings Premium vs. Cost Analysis")
    
    # Create scatterplot using Altair
    import altair as alt
    
    # Prepare data for both C-Metric and H-Metric
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**C-Metric (Statewide) Scatterplot**")
        
        # Create chart for C-Metric
        chart_c = alt.Chart(df).mark_circle(size=60, opacity=0.7).encode(
            x=alt.X('total_net_price:Q', 
                   title='Total Net Price (2 years)', 
                   scale=alt.Scale(zero=False)),
            y=alt.Y('premium_statewide:Q', 
                   title='Earnings Premium (C-Metric)', 
                   scale=alt.Scale(zero=False)),
            color=alt.Color('Sector:N', 
                          scale=alt.Scale(domain=['Public', 'Private for-profit', 'Private non-profit'], 
                                        range=['#1f77b4', '#ff7f0e', '#2ca02c']),
                          title='Sector'),
            tooltip=['Institution:N', 'Sector:N', 'total_net_price:Q', 'premium_statewide:Q']
        ).properties(
            width=350,
            height=400,
            title="Cost vs Statewide Earnings Premium"
        )
        
        st.altair_chart(chart_c, use_container_width=True)
    
    with col2:
        st.markdown("**H-Metric (Regional) Scatterplot**")
        
        # Create chart for H-Metric
        chart_h = alt.Chart(df).mark_circle(size=60, opacity=0.7).encode(
            x=alt.X('total_net_price:Q', 
                   title='Total Net Price (2 years)', 
                   scale=alt.Scale(zero=False)),
            y=alt.Y('premium_regional:Q', 
                   title='Earnings Premium (H-Metric)', 
                   scale=alt.Scale(zero=False)),
            color=alt.Color('Sector:N', 
                          scale=alt.Scale(domain=['Public', 'Private for-profit', 'Private non-profit'], 
                                        range=['#1f77b4', '#ff7f0e', '#2ca02c']),
                          title='Sector'),
            tooltip=['Institution:N', 'Sector:N', 'total_net_price:Q', 'premium_regional:Q']
        ).properties(
            width=350,
            height=400,
            title="Cost vs Regional Earnings Premium"
        )
        
        st.altair_chart(chart_h, use_container_width=True)
    
    # Key Insights section (moved below scatterplots)
    st.markdown("---")
    st.subheader("📈 Key Insights")
    
    # Find institutions with biggest rank changes
    rank_comparison = pd.merge(
        df_cmetric[['Institution', 'Rank']].rename(columns={'Rank': 'C_Rank'}),
        df_hmetric[['Institution', 'Rank']].rename(columns={'Rank': 'H_Rank'}),
        on='Institution'
    )
    rank_comparison['Rank_Change'] = rank_comparison['C_Rank'] - rank_comparison['H_Rank']
    
    # Biggest gainers and losers
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔺 Biggest Gainers (H-Metric favors)**")
        gainers = rank_comparison.nlargest(5, 'Rank_Change')[['Institution', 'C_Rank', 'H_Rank', 'Rank_Change']]
        gainers['Change'] = gainers['Rank_Change'].apply(lambda x: f"+{x}" if x > 0 else str(x))
        st.dataframe(gainers[['Institution', 'C_Rank', 'H_Rank', 'Change']], hide_index=True)
    
    with col2:
        st.markdown("**🔻 Biggest Losers (C-Metric favors)**")
        losers = rank_comparison.nsmallest(5, 'Rank_Change')[['Institution', 'C_Rank', 'H_Rank', 'Rank_Change']]
        losers['Change'] = losers['Rank_Change'].apply(lambda x: f"+{x}" if x > 0 else str(x))
        st.dataframe(losers[['Institution', 'C_Rank', 'H_Rank', 'Change']], hide_index=True)

def render_roi_rankings(df):
    """Render side-by-side ROI rankings for Statewide and Regional baselines."""
    st.title("ROI Rankings")
    st.markdown("Side-by-side comparison of Return on Investment rankings (years to recoup educational costs)")
    
    # Check if data is available
    if df.empty:
        st.error("No data available. Please check the dataset files.")
        return
    
    # Filter out institutions with invalid ROI (999 values)
    df_valid = df[(df['roi_statewide_years'] < 999) & (df['roi_regional_years'] < 999)].copy()
    
    if df_valid.empty:
        st.error("No institutions with valid ROI data.")
        return
    
    # Sort data for rankings (lower ROI is better)
    df_statewide = df_valid.copy().sort_values('roi_statewide_years', ascending=True)
    df_regional = df_valid.copy().sort_values('roi_regional_years', ascending=True)
    
    # Add rank columns
    df_statewide['Rank'] = range(1, len(df_statewide) + 1)
    df_regional['Rank'] = range(1, len(df_regional) + 1)
    
    # Create two columns for side-by-side display
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Statewide ROI Rankings")
        st.markdown("*Based on Statewide Baseline ($24,939)*")
        
        # Prepare display dataframe
        display_statewide = df_statewide[['Rank', 'Institution', 'Sector', 'roi_statewide_years', 'total_net_price']].copy()
        display_statewide.columns = ['Rank', 'Institution', 'Sector', 'ROI (Years)', 'Total Cost (2yr)']
        
        # Format ROI years with month approximation
        display_statewide['ROI (Years)'] = display_statewide['ROI (Years)'].apply(
            lambda x: f"{x:.2f} years (≈ {x*12:.1f} months)" if x < 1 else f"{x:.2f} years"
        )
        
        # Display table with formatting
        st.dataframe(
            display_statewide,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.NumberColumn(
                    "Rank",
                    format="%d"
                ),
                "Total Cost (2yr)": st.column_config.NumberColumn(
                    "Total Cost (2yr)",
                    format="$%,.0f"
                )
            },
            height=600
        )
    
    with col2:
        st.subheader("💰 Regional ROI Rankings")
        st.markdown("*Based on Regional (County) Baselines*")
        
        # Prepare display dataframe
        display_regional = df_regional[['Rank', 'Institution', 'Sector', 'roi_regional_years', 'total_net_price']].copy()
        display_regional.columns = ['Rank', 'Institution', 'Sector', 'ROI (Years)', 'Total Cost (2yr)']
        
        # Format ROI years with month approximation
        display_regional['ROI (Years)'] = display_regional['ROI (Years)'].apply(
            lambda x: f"{x:.2f} years (≈ {x*12:.1f} months)" if x < 1 else f"{x:.2f} years"
        )
        
        # Display table with formatting
        st.dataframe(
            display_regional,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.NumberColumn(
                    "Rank",
                    format="%d"
                ),
                "Total Cost (2yr)": st.column_config.NumberColumn(
                    "Total Cost (2yr)",
                    format="$%,.0f"
                )
            },
            height=600
        )
    
    # Scatterplot section
    st.markdown("---")
    st.subheader("📈 ROI vs. Cost Analysis")
    
    # Create scatterplot using Altair
    import altair as alt
    
    # Prepare data for both Statewide and Regional ROI
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Statewide ROI Scatterplot**")
        
        # Create chart for Statewide ROI
        chart_sw = alt.Chart(df_valid).mark_circle(size=60, opacity=0.7).encode(
            x=alt.X('total_net_price:Q', 
                   title='Total Net Price (2 years)', 
                   scale=alt.Scale(zero=False)),
            y=alt.Y('roi_statewide_years:Q', 
                   title='ROI (Years) - Statewide', 
                   scale=alt.Scale(zero=False)),
            color=alt.Color('Sector:N', 
                          scale=alt.Scale(domain=['Public', 'Private for-profit', 'Private non-profit'], 
                                        range=['#1f77b4', '#ff7f0e', '#2ca02c']),
                          title='Sector'),
            tooltip=['Institution:N', 'Sector:N', 'total_net_price:Q', 'roi_statewide_years:Q']
        ).properties(
            width=350,
            height=400,
            title="Cost vs Statewide ROI (Years)"
        )
        
        st.altair_chart(chart_sw, use_container_width=True)
    
    with col2:
        st.markdown("**Regional ROI Scatterplot**")
        
        # Create chart for Regional ROI
        chart_reg = alt.Chart(df_valid).mark_circle(size=60, opacity=0.7).encode(
            x=alt.X('total_net_price:Q', 
                   title='Total Net Price (2 years)', 
                   scale=alt.Scale(zero=False)),
            y=alt.Y('roi_regional_years:Q', 
                   title='ROI (Years) - Regional', 
                   scale=alt.Scale(zero=False)),
            color=alt.Color('Sector:N', 
                          scale=alt.Scale(domain=['Public', 'Private for-profit', 'Private non-profit'], 
                                        range=['#1f77b4', '#ff7f0e', '#2ca02c']),
                          title='Sector'),
            tooltip=['Institution:N', 'Sector:N', 'total_net_price:Q', 'roi_regional_years:Q']
        ).properties(
            width=350,
            height=400,
            title="Cost vs Regional ROI (Years)"
        )
        
        st.altair_chart(chart_reg, use_container_width=True)
    
    # ROI Analysis section (moved below scatterplots)
    st.markdown("---")
    st.subheader("📈 ROI Analysis")
    
    # Compare rankings
    rank_comparison = pd.merge(
        df_statewide[['Institution', 'Rank', 'roi_statewide_years']].rename(columns={'Rank': 'SW_Rank'}),
        df_regional[['Institution', 'Rank', 'roi_regional_years']].rename(columns={'Rank': 'Reg_Rank'}),
        on='Institution'
    )
    rank_comparison['Rank_Change'] = rank_comparison['SW_Rank'] - rank_comparison['Reg_Rank']
    
    # Top performers and biggest changes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏆 Top 5 Overall ROI**")
        top_roi = df_valid.nsmallest(5, 'roi_statewide_years')[['Institution', 'roi_statewide_years', 'roi_regional_years']]
        top_roi.columns = ['Institution', 'Statewide', 'Regional']
        for col in ['Statewide', 'Regional']:
            top_roi[col] = top_roi[col].apply(lambda x: f"{x:.2f} yrs")
        st.dataframe(top_roi, hide_index=True)
    
    with col2:
        st.markdown("**🔺 Regional Baseline Helps**")
        helps = rank_comparison.nlargest(5, 'Rank_Change')[['Institution', 'SW_Rank', 'Reg_Rank']]
        helps.columns = ['Institution', 'SW', 'Reg']
        st.dataframe(helps, hide_index=True)
    
    with col3:
        st.markdown("**🔻 Statewide Baseline Helps**")
        hurts = rank_comparison.nsmallest(5, 'Rank_Change')[['Institution', 'SW_Rank', 'Reg_Rank']]
        hurts.columns = ['Institution', 'SW', 'Reg']
        st.dataframe(hurts, hide_index=True)

