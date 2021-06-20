import streamlit as st
from UI.UI import UI_Base

class UI_Simulation_Config(UI_Base):
    def __init__(self):
        super().__init__()
        self.name = 'General Configuration'

    def get_defaults_dict(self, state):
        dict = {}
        dict['Random Seed'] = 42
        dict['Days'] = 30
        dict['Worlds'] = 1
        return dict

    def run(self, state):
        state.params[self.name]['Random Seed']=st.slider("Select random seed",1,100,state.params[self.name]['Random Seed'],1)
        state.params[self.name]['Days']=st.slider("Select number of days",1,200,state.params[self.name]['Days'],1)
        state.params[self.name]['Worlds']=st.slider("Select number of worlds",1,30,state.params[self.name]['Worlds'],1)
