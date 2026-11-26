import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Student Commute Analysis", page_icon="🚌", layout="wide")
st.title("🚌 Student Commute Mode Analysis")
st.caption("BTech CSE (AI & ML) mini-project | Rishta Bharti | CGC University")
st.info("Demo dataset contains synthetic records, not an actual campus survey. Replace with consented survey data for real findings.")

DATA = Path(__file__).resolve().parent.parent / "data" / "cleaned_data.csv"
if not DATA.exists():
    DATA = Path(__file__).resolve().parent.parent / "data" / "survey_data.csv"
df = pd.read_csv(DATA)

st.sidebar.header("Filters")
year_filter = st.sidebar.multiselect("Year", sorted(df.Year.unique()), default=list(sorted(df.Year.unique())))
section_filter = st.sidebar.multiselect("Section", sorted(df.Section.unique()), default=list(sorted(df.Section.unique())))
mode_filter = st.sidebar.multiselect("Commute mode", sorted(df.Commute_Mode.unique()), default=list(sorted(df.Commute_Mode.unique())))
hostel_filter = st.sidebar.multiselect("Residence", sorted(df.Hostel_DayScholar.unique()), default=list(sorted(df.Hostel_DayScholar.unique())))
filtered = df[df.Year.isin(year_filter) & df.Section.isin(section_filter) & df.Commute_Mode.isin(mode_filter) & df.Hostel_DayScholar.isin(hostel_filter)]

factors = {"Bus":0.08,"Car":0.18,"Carpool":0.09,"Motorbike":0.10,"Bicycle":0.0,"Walking":0.0,"Auto-Rickshaw":0.11}
filtered["Emissions_kg_oneway"] = filtered.apply(lambda r: r.Distance_km*factors.get(r.Commute_Mode,0.12), axis=1)
filtered["Burden_Score"] = (filtered.Travel_Time_min/filtered.Travel_Time_min.max()*40 + filtered.Distance_km/filtered.Distance_km.max()*35 + filtered.Daily_Cost_INR/max(filtered.Daily_Cost_INR.max(),1)*25).round(1)

if filtered.empty:
    st.warning("No records match the current filters. Adjust the filters.")
    st.stop()

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Students surveyed",len(filtered))
c2.metric("Most popular mode",filtered.Commute_Mode.mode().iloc[0])
c3.metric("Avg. commute time",f"{filtered.Travel_Time_min.mean():.1f} min")
c4.metric("Avg. distance",f"{filtered.Distance_km.mean():.1f} km")
c5.metric("Estimated CO₂ / one-way",f"{filtered.Emissions_kg_oneway.mean():.2f} kg/student")

st.subheader("Transport patterns")
col1,col2 = st.columns(2)
with col1:
    fig=px.bar(filtered.Commute_Mode.value_counts().reset_index(), x="Commute_Mode", y="count", labels={"count":"Students","Commute_Mode":"Mode"}, title="Students per commute mode")
    st.plotly_chart(fig,use_container_width=True)
with col2:
    fig=px.pie(filtered, names="Commute_Mode", title="Mode share", hole=.45)
    st.plotly_chart(fig,use_container_width=True)

st.subheader("Distance, time and cost")
col1,col2 = st.columns(2)
with col1:
    fig=px.histogram(filtered, x="Distance_km", nbins=15, title="Commute distance distribution")
    st.plotly_chart(fig,use_container_width=True)
with col2:
    fig=px.box(filtered, x="Commute_Mode", y="Travel_Time_min", title="Travel time by mode")
    st.plotly_chart(fig,use_container_width=True)
col1,col2 = st.columns(2)
with col1:
    fig=px.scatter(filtered, x="Distance_km", y="Travel_Time_min", color="Commute_Mode", title="Distance vs travel time")
    st.plotly_chart(fig,use_container_width=True)
with col2:
    cost=filtered.groupby("Commute_Mode",as_index=False).Daily_Cost_INR.mean()
    fig=px.bar(cost, x="Commute_Mode", y="Daily_Cost_INR", title="Average daily commute cost (INR)")
    st.plotly_chart(fig,use_container_width)

st.subheader("Advanced features")
st.markdown("**Illustrative emission factors (kg CO₂ per passenger-km):** "+", ".join(f"{k}: {v}" for k,v in factors.items()))
mode_summary=filtered.groupby("Commute_Mode").agg(Students=("Student_ID","count"),Avg_Distance_km=("Distance_km","mean"),Avg_Time_min=("Travel_Time_min","mean"),Avg_Cost_INR=("Daily_Cost_INR","mean"),Avg_Emission_kg=("Emissions_kg_oneway","mean")).reset_index()
st.dataframe(mode_summary.round(2),use_container_width=True)

st.markdown("### What-if switch simulator")
switch_pct=st.slider("Share of motorized trips shifted to bus/carpool (illustrative)",0,100,20,5)
base_em=filtered.Emissions_kg_oneway.sum()
target_factor=0.085
estimated_savings=base_em*(switch_pct/100)*(1-target_factor/max(filtered.Emissions_kg_oneway.mean(),0.001))
st.metric("Scenario emissions savings (rough model)",f"{estimated_savings:.2f} kg CO₂")
st.caption("Scenario is a simplified illustration. It assumes the selected share of motorized travel is replaced by a lower-emission alternative; actual savings depend on distance, occupancy and vehicle factors.")

st.markdown("### Rule-based commute suggestions")
def suggest(row):
    if row.Distance_km <= 2:
        return "Consider walking (if safe and practical)"
    if row.Distance_km <= 5:
        return "Consider bicycle or shared ride"
    if row.Distance_km <= 15:
        return "Consider bus or carpool"
    return "Consider public transport or coordinated carpool"
st.dataframe(filtered[["Student_ID","Commute_Mode","Distance_km","Travel_Time_min","Daily_Cost_INR"]].assign(Suggestion=filtered.apply(suggest,axis=1)),use_container_width=True)
