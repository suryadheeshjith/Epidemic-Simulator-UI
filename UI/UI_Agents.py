import streamlit as st
from UI.UI import UI_Base

class UI_Agents(UI_Base):
    def __init__(self):
        super().__init__()
        self.name = 'Agents'

    def get_defaults_dict(self):
        dict = {}
        dict['Number of Agents'] = 300
        return dict

    def run(self, state):
        state.params[self.name]['Number of Agents']=st.slider("Select number of agents",0,1000,state.params[self.name]['Number of Agents'],10)
