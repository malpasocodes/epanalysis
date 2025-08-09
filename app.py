# app.py
import streamlit as st
from lib.data import load_dataset
from lib.ui import render_home, render_explore, render_rankings, render_methodology

st.set_page_config(page_title="Earnings Premium & ROI Explorer", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Explore Data", "Rankings", "Methodology"], index=0)

# Load once; includes Golden Returns ROI merge
df = load_dataset(
    combined_path="data/roi_with_county_baseline_combined_clean.csv",
    public_path="data/public.csv",
)

if page == "Home":
    render_home()
elif page == "Explore Data":
    render_explore(df)
elif page == "Rankings":
    render_rankings(df)
elif page == "Methodology":
    render_methodology()
