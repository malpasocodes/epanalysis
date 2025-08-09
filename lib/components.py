# lib/components.py
import streamlit as st
import pandas as pd
from typing import List, Optional, Tuple, Dict, Any

class FilterSidebar:
    """Reusable sidebar filter component."""
    
    @staticmethod
    def render(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
        """Render region and sector filters, return selections."""
        st.sidebar.header("Filters")
        
        regions = sorted(df["Region"].dropna().unique().tolist())
        sectors = sorted(df["Sector"].dropna().unique().tolist())
        
        selected_regions = st.sidebar.multiselect(
            "Region", 
            options=regions, 
            default=regions,
            help="Filter institutions by region"
        )
        
        selected_sectors = st.sidebar.multiselect(
            "Sector",
            options=sectors,
            default=sectors,
            help="Filter by institution type (Public/Private)"
        )
        
        return selected_regions, selected_sectors

class MetricsRow:
    """Display a row of metric cards."""
    
    @staticmethod
    def render(metrics: Dict[str, Any], columns: Optional[int] = None):
        """
        Render metrics in columns.
        
        Args:
            metrics: Dictionary of {label: value} pairs
            columns: Number of columns (defaults to number of metrics)
        """
        columns = columns or len(metrics)
        cols = st.columns(columns)
        
        for i, (label, value) in enumerate(metrics.items()):
            with cols[i % columns]:
                if isinstance(value, (int, float)):
                    if label.lower().contains('price') or label.lower().contains('earning'):
                        st.metric(label, f"${value:,.0f}")
                    else:
                        st.metric(label, f"{value:,}")
                else:
                    st.metric(label, value)

class RankingsTable:
    """Enhanced rankings table with search and sorting."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare and validate ranking data."""
        self.df.columns = self.df.columns.str.strip()
        
        # Ensure numeric types
        for col in ['rank_statewide', 'rank_regional']:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Calculate rank change
        if 'rank_change' not in self.df.columns:
            self.df['rank_change'] = (
                self.df['rank_statewide'] - self.df['rank_regional']
            )
    
    def render(self):
        """Render the rankings table with controls."""
        # Search and sort controls
        col1, col2, col3 = st.columns([2, 1.2, 1])
        
        with col1:
            search_query = st.text_input(
                "Search (Institution or Region)",
                placeholder="Type to filter...",
                help="Search by institution name or region"
            )
        
        with col2:
            sort_options = [
                "ROI Rank (Local)",
                "ROI Rank (Statewide)", 
                "Rank Change"
            ]
            sort_by = st.selectbox("Sort by", sort_options, index=0)
        
        with col3:
            ascending = st.toggle("Ascending", value=True)
        
        # Apply filters and sorting
        filtered_df = self._apply_filters(search_query)
        sorted_df = self._apply_sorting(filtered_df, sort_by, ascending)
        
        # Format for display
        display_df = self._format_for_display(sorted_df)
        
        # Render table
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank Change": st.column_config.NumberColumn(
                    "Δ (SW→Local)",
                    help="Positive = improved under local baseline"
                ),
            }
        )
        
        # Summary stats
        if not filtered_df.empty:
            self._render_summary(filtered_df)
    
    def _apply_filters(self, query: str) -> pd.DataFrame:
        """Apply search filters to dataframe."""
        if not query:
            return self.df
        
        query = query.lower().strip()
        mask = (
            self.df['Institution'].str.lower().str.contains(query, na=False) |
            self.df['Region'].str.lower().str.contains(query, na=False)
        )
        return self.df[mask]
    
    def _apply_sorting(self, df: pd.DataFrame, sort_by: str, ascending: bool) -> pd.DataFrame:
        """Apply sorting to dataframe."""
        column_map = {
            "ROI Rank (Local)": "rank_regional",
            "ROI Rank (Statewide)": "rank_statewide",
            "Rank Change": "rank_change"
        }
        
        sort_col = column_map.get(sort_by, "rank_regional")
        
        # Special handling for rank change (sort by absolute value)
        if sort_col == "rank_change" and not ascending:
            return df.assign(
                _abs=df[sort_col].abs()
            ).sort_values('_abs', ascending=False).drop(columns='_abs')
        
        return df.sort_values(sort_col, ascending=ascending, na_position='last')
    
    def _format_for_display(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format dataframe for display."""
        # Create display columns
        display = pd.DataFrame({
            'Institution': df['Institution'],
            'Region': df['Region'],
            'ROI Rank (Statewide)': df['rank_statewide'].round().astype('Int64'),
            'ROI Rank (Local)': df['rank_regional'].round().astype('Int64'),
            'Rank Change': df['rank_change'].round().astype('Int64')
        })
        
        # Add visual indicators
        display['Change Indicator'] = display['Rank Change'].apply(self._format_change)
        
        return display
    
    def _format_change(self, value: float) -> str:
        """Format rank change with arrows."""
        if pd.isna(value):
            return ""
        
        value = int(value)
        if value > 0:
            return f"↑ +{value}"
        elif value < 0:
            return f"↓ {value}"
        else:
            return "—"
    
    def _render_summary(self, df: pd.DataFrame):
        """Render summary statistics."""
        with st.expander("Summary Statistics"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                improved = (df['rank_change'] > 0).sum()
                st.metric("Improved Rankings", improved)
            
            with col2:
                worsened = (df['rank_change'] < 0).sum()
                st.metric("Worsened Rankings", worsened)
            
            with col3:
                avg_change = df['rank_change'].mean()
                st.metric("Average Change", f"{avg_change:+.1f}")