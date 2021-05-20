import streamlit as st
from UI.UI import UI_Base

class UI_Agents(UI_Base):
    def __init__(self):
        self.name = 'UI_Agents'

    # def write_agents(self, filename,n):
    #     header='Agent Index'
    #
    #     f=open(filename,'w')
    #     f.write(str(n)+'\n')
    #     f.write(header+'\n')
    #
    #     for i in range(n):
    #         f.write(str(i)+'\n')

    def get_defaults_dict(self):
        dict = {}
        dict['no_agents'] = 300
        return dict

    def run(self, state):
        # file_name = 'agents.txt'
        # config_obj.agents_filename = file_name
        state.params[self.name]['no_agents']=st.slider("Select number of agents",0,1000,state.params[self.name]['no_agents'],10)
        # write_agents(config_obj.agents_filename,no_agents)
