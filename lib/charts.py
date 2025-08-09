# lib/charts.py
import pandas as pd
import altair as alt

def quadrant_chart(df: pd.DataFrame) -> alt.Chart:
    price_median = df["total_net_price"].median()
    earn_median = df["median_earnings_10yr"].median()

    base = alt.Chart(df).encode(
        x=alt.X("total_net_price:Q", title="Total Net Price (USD)", scale=alt.Scale(zero=False)),
        y=alt.Y("median_earnings_10yr:Q", title="Median Earnings After 10 Years (USD)", scale=alt.Scale(zero=False)),
        tooltip=[
            "Institution:N", "Region:N", "County:N", "Sector:N",
            alt.Tooltip("total_net_price:Q", title="Total Net Price", format=","),
            alt.Tooltip("median_earnings_10yr:Q", title="Median Earnings", format=","),
            alt.Tooltip("roi_statewide_years:Q", title="ROI (Statewide, yrs)", format=".2f"),
            alt.Tooltip("roi_regional_years:Q", title="ROI (Local, yrs)", format=".2f"),
        ],
    )
    points = base.mark_circle(size=70).encode(color=alt.Color("Sector:N", legend=alt.Legend(title="Sector")))
    vline = alt.Chart(pd.DataFrame({"x": [price_median]})).mark_rule(color="gray", strokeDash=[4,4]).encode(x="x:Q")
    hline = alt.Chart(pd.DataFrame({"y": [earn_median]})).mark_rule(color="gray", strokeDash=[4,4]).encode(y="y:Q")
    return (points + vline + hline).properties(height=520)