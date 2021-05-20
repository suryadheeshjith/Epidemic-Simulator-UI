import streamlit as st
from UI.UI import UI_Base

class UI_Simulation_Config(UI_Base):
    def __init__(self):
        super().__init__()
        self.name = 'UI_Simulation_Config'

    def get_defaults_dict(self):
        dict = {}
        dict['days'] = 30
        dict['worlds'] = 1
        return dict

    def run(self, state):
        state.params[self.name]['days']=st.slider("Select number of days",1,200,state.params[self.name]['days'],1)
        state.params[self.name]['worlds']=st.slider("Select number of worlds",1,30,state.params[self.name]['worlds'],1)
