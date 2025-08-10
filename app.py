# app.py
import streamlit as st
import pandas as pd
from lib.data import load_roi_metrics_dataset
from lib.ui import render_home, render_explore, render_rankings, render_methodology

st.set_page_config(page_title="Earnings Premium & ROI Explorer", layout="wide")

# Load new primary dataset with all institutions (public + private)
df = load_roi_metrics_dataset("data/roi-metrics.csv")

# Sidebar with expandable sections for navigation
st.sidebar.title("Navigation")

# Initialize session state for page tracking
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'current_subpage' not in st.session_state:
    st.session_state.current_subpage = None

# Home Section
with st.sidebar.expander("🏠 Home", expanded=True):
    if st.button("Project Overview", use_container_width=True):
        st.session_state.current_page = 'home'
        st.session_state.current_subpage = None

# Metrics Comparison Section
with st.sidebar.expander("📊 Metrics Comparison", expanded=False):
    if st.button("Earnings Premium", use_container_width=True):
        st.session_state.current_page = 'earnings'
        st.session_state.current_subpage = 'comparison'
    if st.button("ROI", use_container_width=True):
        st.session_state.current_page = 'earnings'
        st.session_state.current_subpage = 'analysis'

# Data Analysis Section
with st.sidebar.expander("📊 Data Analysis", expanded=False):
    if st.button("Quadrant Chart", use_container_width=True):
        st.session_state.current_page = 'explore'
        st.session_state.current_subpage = 'quadrant'
    if st.button("Regional Comparison", use_container_width=True):
        st.session_state.current_page = 'explore'
        st.session_state.current_subpage = 'regional'
    if st.button("Sector Analysis", use_container_width=True):
        st.session_state.current_page = 'explore'
        st.session_state.current_subpage = 'sector'
    if st.button("Data Filters", use_container_width=True):
        st.session_state.current_page = 'explore'
        st.session_state.current_subpage = 'filters'

# ROI Rankings Section
with st.sidebar.expander("📈 ROI Rankings", expanded=False):
    if st.button("Side-by-Side Rankings", use_container_width=True):
        st.session_state.current_page = 'rankings'
        st.session_state.current_subpage = 'sidebyside'
    if st.button("Rank Changes", use_container_width=True):
        st.session_state.current_page = 'rankings'
        st.session_state.current_subpage = 'changes'
    if st.button("Top Performers", use_container_width=True):
        st.session_state.current_page = 'rankings'
        st.session_state.current_subpage = 'top'

# Methodology & Data Section
with st.sidebar.expander("📋 Methodology & Data", expanded=False):
    if st.button("Data Sources", use_container_width=True):
        st.session_state.current_page = 'methodology'
        st.session_state.current_subpage = 'sources'
    if st.button("Calculations", use_container_width=True):
        st.session_state.current_page = 'methodology'
        st.session_state.current_subpage = 'calculations'
    if st.button("Assumptions", use_container_width=True):
        st.session_state.current_page = 'methodology'
        st.session_state.current_subpage = 'assumptions'

# Additional Analysis Section
with st.sidebar.expander("📊 Advanced Analysis", expanded=False):
    if st.button("Institution Profiles", use_container_width=True):
        st.session_state.current_page = 'advanced'
        st.session_state.current_subpage = 'profiles'
    if st.button("Trend Analysis", use_container_width=True):
        st.session_state.current_page = 'advanced'
        st.session_state.current_subpage = 'trends'
    if st.button("Statistical Tests", use_container_width=True):
        st.session_state.current_page = 'advanced'
        st.session_state.current_subpage = 'stats'

# Export & Tools Section
with st.sidebar.expander("🔧 Tools & Export", expanded=False):
    if st.button("Data Export", use_container_width=True):
        st.session_state.current_page = 'tools'
        st.session_state.current_subpage = 'export'
    if st.button("Report Generator", use_container_width=True):
        st.session_state.current_page = 'tools'
        st.session_state.current_subpage = 'report'
    if st.button("API Access", use_container_width=True):
        st.session_state.current_page = 'tools'
        st.session_state.current_subpage = 'api'

# About & Help Section
with st.sidebar.expander("ℹ️ About & Help", expanded=False):
    if st.button("Project Background", use_container_width=True):
        st.session_state.current_page = 'about'
        st.session_state.current_subpage = 'background'
    if st.button("User Guide", use_container_width=True):
        st.session_state.current_page = 'about'
        st.session_state.current_subpage = 'guide'
    if st.button("Contact & Feedback", use_container_width=True):
        st.session_state.current_page = 'about'
        st.session_state.current_subpage = 'contact'

# Main content area - render based on current page/subpage
current_page = st.session_state.current_page
current_subpage = st.session_state.current_subpage

if current_page == 'home':
    render_home()
elif current_page == 'earnings':
    if current_subpage == 'comparison':
        # Earnings Premium Page
        st.header("Earnings Premium Analysis")
        st.markdown("**Comparison of County-level vs Statewide earnings premiums for California institutions**")
        
        # Check if we have data
        if df.empty:
            st.error("No data available. Please check the dataset files.")
            st.stop()
            
        # Prepare data for display
        display_df = df.copy()
        
        # Determine institution type (Public/Private) from Sector
        display_df['Type'] = display_df['Sector'].apply(
            lambda x: 'Private' if 'Private' in str(x) else 'Public'
        )
        
        # Calculate Delta (difference between C-Metric and H-Metric)
        # Since C-Metric = statewide and H-Metric = county: Delta = C-Metric - H-Metric
        display_df['Delta'] = display_df['premium_statewide'] - display_df['premium_regional']
        
        # Add statewide HS baseline constant
        STATEWIDE_HS_BASELINE = 24939.44
        
        # Select and rename columns for display (including debugging columns)
        metrics_df = display_df[[
            'Institution', 'Region', 'Type', 'median_earnings_10yr', 'total_net_price', 'hs_median_income', 
            'premium_statewide', 'premium_regional', 'Delta'
        ]].copy()
        
        # Add statewide HS baseline column
        metrics_df['HS_Statewide'] = STATEWIDE_HS_BASELINE
        
        # Rename columns for clarity (CORRECTED: C-Metric = statewide, H-Metric = county)
        metrics_df.columns = ['Institution', 'Region', 'Type', 'Median Earnings (Grad)', 
                             'Net Tuition', 'HS Earnings County', 'C-Metric', 'H-Metric', 'Delta', 'HS Earnings Statewide']
        
        # Reorder columns for better readability
        metrics_df = metrics_df[['Institution', 'Region', 'Type', 'Median Earnings (Grad)', 'Net Tuition',
                                'HS Earnings Statewide', 'HS Earnings County', 'C-Metric', 'H-Metric', 'Delta']]
        
        # DON'T format currency columns as strings - keep numeric for proper sorting
        # Use column_config in st.dataframe instead
        
        # Use all data without filters
        filtered_df = metrics_df.copy()
        
        # Add explanation of what metrics comparison means
        st.markdown("""
        This comparison shows how earnings premium calculations change when using different high school baseline earnings. 
        
        **C-Metric** uses a single statewide baseline ($24,939) for all institutions, while **H-Metric** uses each institution's local county baseline. 
        The **Delta** column shows which approach gives graduates a higher earnings advantage - positive values favor the statewide method, 
        negative values favor the county method.
        
        This matters because it affects how institutions are evaluated and ranked for return on investment.
        """)
        
        # Add side-by-side Delta analysis tables
        st.subheader("Delta Analysis: Top Institutions")
        
        # Add control for number of institutions to display
        col1, col2 = st.columns([1, 3])
        with col1:
            num_institutions = st.selectbox(
                "Number of institutions to display", 
                [10, 15, 20, 25, 30, 50],
                index=1,  # Default to 15
                help="Select how many institutions to show in each table"
            )
        
        # Create separate dataframes for Delta analysis (using original numeric values)
        delta_df = display_df[['Institution', 'Region', 'Type', 'Delta']].copy()
        
        # Sort for top positive and negative deltas (limited to selected number)
        top_positive = delta_df.nlargest(num_institutions, 'Delta')
        top_negative = delta_df.nsmallest(num_institutions, 'Delta')
        
        # DON'T format Delta column as string - keep numeric for proper sorting
        
        # Display side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Top {num_institutions} Positive Delta**")
            st.markdown("*Institutions with highest advantage from statewide baseline*")
            st.dataframe(
                top_positive,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Delta": st.column_config.NumberColumn(
                        "Delta",
                        format="$%d",
                    )
                }
            )
        
        with col2:
            st.markdown(f"**Top {num_institutions} Negative Delta**")
            st.markdown("*Institutions with highest advantage from county baseline*")
            st.dataframe(
                top_negative,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Delta": st.column_config.NumberColumn(
                        "Delta",
                        format="$%d",
                    )
                }
            )
        
        # Display the full table with proper currency formatting and numeric sorting
        st.subheader("Metrics Comparison (All Institutions)")
        st.dataframe(
            filtered_df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Median Earnings (Grad)": st.column_config.NumberColumn(
                    "Median Earnings (Grad)",
                    format="$%d",
                ),
                "Net Tuition": st.column_config.NumberColumn(
                    "Net Tuition",
                    format="$%d",
                ),
                "HS Earnings Statewide": st.column_config.NumberColumn(
                    "HS Earnings Statewide",
                    format="$%d",
                ),
                "HS Earnings County": st.column_config.NumberColumn(
                    "HS Earnings County",
                    format="$%d",
                ),
                "C-Metric": st.column_config.NumberColumn(
                    "C-Metric",
                    format="$%d",
                ),
                "H-Metric": st.column_config.NumberColumn(
                    "H-Metric",
                    format="$%d",
                ),
                "Delta": st.column_config.NumberColumn(
                    "Delta",
                    format="$%d",
                ),
            }
        )
        
        # Add explanation
        with st.expander("ℹ️ Column Definitions"):
            st.markdown("""
            - **Institution**: Name of the educational institution
            - **Region**: Geographic region in California
            - **Type**: Public or Private institution
            - **Median Earnings (Grad)**: Graduate earnings 10 years after enrollment
            - **Net Tuition**: Annual net price after financial aid
            - **HS Earnings Statewide**: Statewide high school baseline ($24,939)
            - **HS Earnings County**: County-specific high school baseline
            - **C-Metric**: Statewide earnings premium (Median Earnings - HS Earnings Statewide)
            - **H-Metric**: County earnings premium (Median Earnings - HS Earnings County)
            - **Delta**: Difference between C-Metric and H-Metric (positive means statewide baseline yields higher premium)
            """)
            st.markdown("**Expected calculation verification:**")
            st.markdown("- C-Metric should equal: Median Earnings (Grad) - HS Earnings Statewide")
            st.markdown("- H-Metric should equal: Median Earnings (Grad) - HS Earnings County")
    
    elif current_subpage == 'analysis':
        # ROI Analysis Page
        st.header("ROI Analysis")
        st.markdown("**Comparison of County-level vs Statewide ROI calculations for California institutions**")
        
        # Check if we have data
        if df.empty:
            st.error("No data available. Please check the dataset files.")
            st.stop()
            
        # Prepare data for display
        display_df = df.copy()
        
        # Determine institution type (Public/Private) from Sector
        display_df['Type'] = display_df['Sector'].apply(
            lambda x: 'Private' if 'Private' in str(x) else 'Public'
        )
        
        # Calculate Delta (difference between C-Metric ROI and H-Metric ROI)
        # Since C-Metric = statewide and H-Metric = regional: Delta = C-Metric - H-Metric
        display_df['ROI_Delta'] = display_df['roi_statewide_years'] - display_df['roi_regional_years']
        
        # Select and rename columns for display
        roi_df = display_df[[
            'Institution', 'Region', 'Type', 'total_net_price',
            'roi_statewide_years', 'roi_regional_years', 'ROI_Delta'
        ]].copy()
        
        # Rename columns for clarity (C-Metric = statewide, H-Metric = regional)
        roi_df.columns = ['Institution', 'Region', 'Type', 'Net Tuition', 'C-Metric ROI', 'H-Metric ROI', 'Delta']
        
        # Create formatted ROI columns with years and months
        roi_df['C-Metric ROI Display'] = roi_df['C-Metric ROI'].apply(
            lambda x: f"{x:.2f} years (≈ {x*12:.1f} months)" if pd.notna(x) and x < 999 else str(x)
        )
        roi_df['H-Metric ROI Display'] = roi_df['H-Metric ROI'].apply(
            lambda x: f"{x:.2f} years (≈ {x*12:.1f} months)" if pd.notna(x) and x < 999 else str(x)
        )
        roi_df['Delta Display'] = roi_df['Delta'].apply(
            lambda x: f"{x:.2f} years (≈ {x*12:.1f} months)" if pd.notna(x) and abs(x) < 999 else str(x)
        )
        
        # Filter out institutions with invalid ROI (999 years indicates negative premium)
        roi_df = roi_df[(roi_df['C-Metric ROI'] < 999) & (roi_df['H-Metric ROI'] < 999)]
        
        # Add explanation of what ROI comparison means
        st.markdown("""
        This comparison shows how Return on Investment (ROI) calculations change when using different high school baseline earnings. 
        
        **C-Metric ROI** uses a single statewide baseline ($24,939) for all institutions, while **H-Metric ROI** uses each institution's local county baseline. 
        The **Delta** column shows the difference in years to recoup costs - negative values mean the statewide method shows faster payback.
        
        Lower ROI years = better investment (faster to recoup educational costs).
        """)
        
        # Add side-by-side Delta analysis tables
        st.subheader("Delta Analysis: Top Institutions")
        
        # Add control for number of institutions to display
        col1, col2 = st.columns([1, 3])
        with col1:
            num_institutions = st.selectbox(
                "Number of institutions to display", 
                [10, 15, 20, 25, 30, 50],
                index=1,  # Default to 15
                help="Select how many institutions to show in each table",
                key="roi_num_institutions"
            )
        
        # Create separate dataframes for best ROI analysis
        c_metric_df = roi_df[['Institution', 'Region', 'Type', 'Net Tuition', 'C-Metric ROI', 'C-Metric ROI Display']].copy()
        h_metric_df = roi_df[['Institution', 'Region', 'Type', 'Net Tuition', 'H-Metric ROI', 'H-Metric ROI Display']].copy()
        
        # Sort for best ROI (smallest years = better payback)
        best_c_metric = c_metric_df.nsmallest(num_institutions, 'C-Metric ROI')
        best_h_metric = h_metric_df.nsmallest(num_institutions, 'H-Metric ROI')
        
        # Display side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Top {num_institutions} C-Metric ROI**")
            st.markdown("*Best payback using statewide baseline*")
            # Drop the numeric column and rename display column
            display_c = best_c_metric.drop(columns=['C-Metric ROI']).rename(columns={'C-Metric ROI Display': 'C-Metric ROI'})
            st.dataframe(
                display_c,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Net Tuition": st.column_config.NumberColumn(
                        "Net Tuition",
                        format="$%d",
                    )
                }
            )
        
        with col2:
            st.markdown(f"**Top {num_institutions} H-Metric ROI**")
            st.markdown("*Best payback using county baseline*")
            # Drop the numeric column and rename display column
            display_h = best_h_metric.drop(columns=['H-Metric ROI']).rename(columns={'H-Metric ROI Display': 'H-Metric ROI'})
            st.dataframe(
                display_h,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Net Tuition": st.column_config.NumberColumn(
                        "Net Tuition",
                        format="$%d",
                    )
                }
            )
        
        # Display the full table with proper formatting
        st.subheader("ROI Comparison (All Institutions)")
        # Prepare display dataframe with formatted columns
        display_full = roi_df[['Institution', 'Region', 'Type', 'Net Tuition', 
                               'C-Metric ROI Display', 'H-Metric ROI Display', 'Delta Display']].copy()
        display_full.columns = ['Institution', 'Region', 'Type', 'Net Tuition', 
                                'C-Metric ROI', 'H-Metric ROI', 'Delta']
        st.dataframe(
            display_full, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Net Tuition": st.column_config.NumberColumn(
                    "Net Tuition",
                    format="$%d",
                )
            }
        )
        
        # Add explanation
        with st.expander("ℹ️ Column Definitions"):
            st.markdown("""
            - **Institution**: Name of the educational institution
            - **Region**: Geographic region in California
            - **Type**: Public or Private institution
            - **Net Tuition**: Annual net price after financial aid
            - **C-Metric ROI**: Years to recoup costs using statewide baseline ($24,939)
            - **H-Metric ROI**: Years to recoup costs using county-specific baseline
            - **Delta**: Difference between C-Metric and H-Metric ROI (negative means statewide baseline shows faster payback)
            """)
            st.markdown("**Note:** Institutions with negative earnings premiums (indicating costs exceed benefits) are excluded from this analysis.")
    else:
        st.header("Metrics Comparison")
        st.info("🚧 **Coming Soon**: Comprehensive metrics comparison tools")
elif current_page == 'explore':
    if current_subpage == 'quadrant':
        render_explore(df)  # Current quadrant chart implementation
    elif current_subpage == 'regional':
        st.header("Regional Comparison")
        st.info("🚧 **Coming Soon**: Regional analysis comparing counties and regions")
    elif current_subpage == 'sector':
        st.header("Sector Analysis") 
        st.info("🚧 **Coming Soon**: Analysis by institution sector (Public 2-year, Public 4-year, Private)")
    elif current_subpage == 'filters':
        st.header("Advanced Data Filters")
        st.info("🚧 **Coming Soon**: Advanced filtering and data export capabilities")
    else:
        render_explore(df)  # Default to quadrant chart
elif current_page == 'rankings':
    if current_subpage == 'sidebyside':
        render_rankings(df)  # Current side-by-side implementation
    elif current_subpage == 'changes':
        st.header("Rank Changes Analysis")
        st.info("🚧 **Coming Soon**: Detailed analysis of ranking changes between baselines")
    elif current_subpage == 'top':
        st.header("Top Performing Institutions")
        st.info("🚧 **Coming Soon**: Spotlight on highest ROI institutions")
    else:
        render_rankings(df)  # Default to side-by-side
elif current_page == 'methodology':
    if current_subpage == 'sources':
        st.header("Data Sources")
        st.info("🚧 **Coming Soon**: Detailed information about data sources and provenance")
    elif current_subpage == 'calculations':
        render_methodology()  # Current methodology implementation
    elif current_subpage == 'assumptions':
        st.header("Assumptions and Limitations")
        st.info("🚧 **Coming Soon**: Discussion of methodological assumptions and data limitations")
    else:
        render_methodology()  # Default to calculations
elif current_page == 'advanced':
    if current_subpage == 'profiles':
        st.header("Institution Profiles")
        st.info("🚧 **Coming Soon**: Detailed profiles for individual institutions")
    elif current_subpage == 'trends':
        st.header("Trend Analysis")
        st.info("🚧 **Coming Soon**: Historical trends and projections")
    elif current_subpage == 'stats':
        st.header("Statistical Tests")
        st.info("🚧 **Coming Soon**: Statistical significance testing and correlation analysis")
    else:
        st.header("Advanced Analysis")
        st.info("🚧 **Coming Soon**: Advanced analytical tools and visualizations")
elif current_page == 'tools':
    if current_subpage == 'export':
        st.header("Data Export")
        st.info("🚧 **Coming Soon**: Export filtered data in various formats (CSV, Excel, JSON)")
    elif current_subpage == 'report':
        st.header("Report Generator")
        st.info("🚧 **Coming Soon**: Generate custom reports and summaries")
    elif current_subpage == 'api':
        st.header("API Access")
        st.info("🚧 **Coming Soon**: Programmatic access to data and analysis functions")
    else:
        st.header("Tools & Export")
        st.info("🚧 **Coming Soon**: Data export and automation tools")
elif current_page == 'about':
    if current_subpage == 'background':
        st.header("Project Background")
        st.info("🚧 **Coming Soon**: Project context, goals, and impact of EP regulation")
    elif current_subpage == 'guide':
        st.header("User Guide")
        st.info("🚧 **Coming Soon**: How to use this application and interpret results")
    elif current_subpage == 'contact':
        st.header("Contact & Feedback")
        st.info("🚧 **Coming Soon**: Contact information and feedback form")
    else:
        st.header("About This Project")
        st.info("🚧 **Coming Soon**: Project information and documentation")
