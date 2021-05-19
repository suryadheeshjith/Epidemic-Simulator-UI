import streamlit as st
from UI.MultiPage import save

def UI_Simulation_Config():

    days=st.slider("Select number of days", min_value=1 , max_value=200 , value=100 , step=1 , format=None , key=None )
    worlds=st.slider("Select number of worlds", min_value=1 , max_value=30 , value=5 , step=1 , format=None , key=None )

    save(var_list=[days,worlds], name="Simulation Configuration", page_names=["Agents"])
