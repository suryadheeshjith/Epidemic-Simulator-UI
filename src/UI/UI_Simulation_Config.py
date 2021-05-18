import streamlit as st
import Simulator.ReadFile

def UI_Simulation_Config():

    days=st.slider("Select number of days", min_value=1 , max_value=200 , value=100 , step=1 , format=None , key=None )
    worlds=st.slider("Select number of worlds", min_value=1 , max_value=30 , value=5 , step=1 , format=None , key=None )

    config_obj = Simulator.ReadFile.ReadConfiguration()
    config_obj.worlds=worlds
    config_obj.time_steps=days
    save(var_list=[config_obj], name="Simulation Configuration", page_names=["Agents"])
