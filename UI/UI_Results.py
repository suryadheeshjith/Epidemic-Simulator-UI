import streamlit as st
from UI.UI import UI_Base

class UI_Results(UI_Base):
    def __init__(self):
        super().__init__()
        self.name = 'UI_Results'
        self.requires_reset = False


    def run(self, state):
        st.write("Sum of number of agents and worlds : ")
        st.write("{0}".format(state.params['UI_Agents']['no_agents']+state.params['UI_Simulation_Config']['worlds']))
