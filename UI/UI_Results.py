import streamlit as st
import Utils
from UI.UI import UI_Base
import os.path as osp

class UI_Results(UI_Base):
    def __init__(self):
        super().__init__()
        self.name = 'Results'
        self.requires_reset = False

    def show_configuration(self, state):
        for i, key in enumerate(state.params.keys()):
            if(i!=len(state.params)-1):
                st.markdown("#### {0}".format(key))
                for inner_key in state.params[key]:
                    st.markdown("{0} : {1}".format(inner_key,state.params[key][inner_key]))

    def save_general_config(self,state,config_obj):
        config_obj.worlds = state.params['General Configuration']['Worlds']
        config_obj.time_steps = state.params['General Configuration']['Days']


    def save_data_files(self, state, config_obj):
        # Agents
        Utils.save_agents_file(state.params['Agents'], config_obj)

        # Locations
        # Utils

        # Interactions
        pass

        # Events
        pass


    def run(self, state):
        self.show_configuration(state)
        config_obj = Utils.get_start_config(osp.join("Data","start_config.pkl"))
        config_obj.list_interactions_files = None #### Editing simulator
        config_obj.list_events_files = None #### Editing simulator
        self.save_general_config(state,config_obj)
        self.save_data_files(state,config_obj)

        # config_obj = None # temp
        Utils.run_simulation_from_web(config_obj,state)

        st.write("Sum of number of agents and worlds : ")
        st.write("{0}".format(state.params['Agents']['Number of Agents']+state.params['General Configuration']['Worlds']))
