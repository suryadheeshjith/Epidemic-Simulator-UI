import streamlit as st
import Utils
from UI.UI import UI_Base
import os.path as osp
from Utils.file_utils import get_info_keys

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

    def save_general_config(self,dict,config_obj):
        config_obj.worlds = dict['Worlds']
        config_obj.time_steps = dict['Days']


    def save_data_files(self, dict, config_obj):
        # Agents
        agents_dict = dict['Agents']
        if(agents_dict['Input Mode']['index']==0):
            Utils.save_agents_file(agents_dict, config_obj)

        elif(agents_dict['Input Mode']['index']==1):
            path = agents_dict['Input Mode']['filename']
            if(path):
                config_obj.agent_info_keys = get_info_keys(path)
                config_obj.agents_filename = path
            else:
                st.markdown("No Agent file has been uploaded! Please check your environment again!")
                return False

        # Locations
        loc_dict = dict['Locations']
        if(loc_dict['Input Mode']['index']==0):
            Utils.save_locations_file(loc_dict, config_obj)

        elif(loc_dict['Input Mode']['index']==1):
            path = loc_dict['Input Mode']['filename']
            if(path):
                config_obj.location_info_keys = get_info_keys(path)
                config_obj.locations_filename = path
            else:
                st.markdown("No Location file has been uploaded! Please check your environment again!")
                return False

        # Interactions
        int_dict = dict['Interactions']
        if(int_dict['Input Mode']['index']==0):
            Utils.save_interactions_file(int_dict, config_obj, agents_dict['Number of Agents'])

        elif(int_dict['Input Mode']['index']==1):
            path = int_dict['Input Mode']['list_filename']
            if(path):
                config_obj.interaction_info_keys = get_info_keys(path)
                config_obj.interactions_files_list = list_path
            else:
                st.markdown("No Interaction files have been uploaded! Please check your environment again!")
                return False

        # Events
        events_dict = dict['Events']
        if(events_dict['Input Mode']['index']==0):
            Utils.save_events_file(events_dict, config_obj, agents_dict['Number of Agents'])

        elif(events_dict['Input Mode']['index']==1):
            path = events_dict['Input Mode']['list_filename']
            if(path):
                config_obj.event_info_keys = get_info_keys(path)
                config_obj.events_files_list = list_path
            else:
                st.markdown("No Event files have been uploaded! Please check your environment again!")
                return False

        return True



    def run(self, state):
        self.show_configuration(state)
        config_obj = Utils.get_start_config(osp.join("Data","start_config.pkl"))
        self.save_general_config(state.params['General Configuration'],config_obj)
        flag = self.save_data_files(state.params['Environment'],config_obj)

        if(flag):
            try:
                Utils.run_simulation_from_web(config_obj,state)
            except Exception as e:
                st.error(e)
