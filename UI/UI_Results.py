import streamlit as st
import Utils
from UI.UI import UI_Base
import os.path as osp
from Utils.file_utils import get_info_keys
from Utils.streamlit_utils import get_interaction_graph
import streamlit.components.v1 as components

class UI_Results(UI_Base):
    def __init__(self):
        super().__init__()
        self.name = 'Results'
        self.requires_reset = False

    def show_configuration(self, state):
        # for i, key in enumerate(state.params.keys()):
        #     if(i!=len(state.params)-1):
        #         st.markdown("#### {0}".format(key))
        #         for inner_key in state.params[key]:
        #             st.markdown("{0} : {1}".format(inner_key,state.params[key][inner_key]))

        for key in state.params.keys():

            if(key=="General Configuration"):
                st.markdown("#### {0}".format(key))
                st.markdown("Days : {0}".format(state.params[key]['Days']))
                st.markdown("Worlds : {0}".format(state.params[key]['Worlds']))

            if(key=="Environment"):
                st.markdown("#### {0}".format(key))
                st.markdown("<ins>Agents</ins>", unsafe_allow_html=True)
                if(state.params[key]['Agents']['Input Mode']['index']==0):
                    st.markdown("Number of Agents : {0}".format(state.params[key]['Agents']['Number of Agents']))
                st.markdown("Type of Input for Agents : {0}".format(state.params[key]['Agents']['Input Mode']['name']))

                st.markdown("<ins>Interactions</ins>", unsafe_allow_html=True)
                if(state.params[key]['Interactions']['Input Mode']['index']==0):
                    st.markdown("Interaction Type : {0}".format(state.params[key]['Interactions']['Interaction Graph']['name']))
                st.markdown("Type of Input for Interactions : {0}".format(state.params[key]['Interactions']['Input Mode']['name']))

                st.markdown("<ins>Locations</ins>", unsafe_allow_html=True)
                if(state.params[key]['Locations']['Input Mode']['index']==0):
                    st.markdown("Number of Locations : {0}".format(state.params[key]['Locations']['Number of Locations']))
                st.markdown("Type of Input for Locations : {0}".format(state.params[key]['Locations']['Input Mode']['name']))

                st.markdown("<ins>Events</ins>", unsafe_allow_html=True)
                if(state.params[key]['Events']['Input Mode']['index']==0):
                    st.markdown("Number of Events : {0}".format(state.params[key]['Events']['Number of Events']))
                st.markdown("Type of Input for Events : {0}".format(state.params[key]['Events']['Input Mode']['name']))

            if(key=="Model"):
                st.markdown("#### {0}".format(key))
                if(state.params[key]['Input Mode']['index']==0):
                    st.markdown("Number of Compartments : {0}".format(state.params[key]['Number of compartments']))
                    st.markdown("Number of Transitions : {0}".format(state.params[key]['Number of transitions']))

                    for i in range(state.params[key]['Number of compartments']):
                        name = state.params[key]['compartments'][i]['name']
                        st.markdown("Compartment {0} : {1}".format(i+1,name))
                st.markdown("Type of Input for the Model : {0}".format(state.params[key]['Input Mode']['name']))

            # if(key=="Policy"):
            #     st.markdown("#### {0}".format(key))
                # st.markdown("Type of Input for the Policy : {0}".format(state.params[key]['Input Mode']['name']))


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
                st.error("No Agent file has been uploaded! Please check your environment again!")
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
                st.error("No Location file has been uploaded! Please check your environment again!")
                return False

        # Interactions
        int_dict = dict['Interactions']
        if(int_dict['Input Mode']['index']==0):
            Utils.save_interactions_file(int_dict, config_obj, agents_dict['Number of Agents'])

        elif(int_dict['Input Mode']['index']==1):
            path = int_dict['Input Mode']['list_filename']
            if(path):
                config_obj.interaction_info_keys = get_info_keys(int_dict['Input Mode']['single_filenames'][0])
                config_obj.interactions_files_list = path
            else:
                st.error("No Interaction files have been uploaded! Please check your environment again!")
                return False

        # Events
        events_dict = dict['Events']
        if(events_dict['Input Mode']['index']==0):
            Utils.save_events_file(events_dict, config_obj, agents_dict['Number of Agents'])

        elif(events_dict['Input Mode']['index']==1):
            path = events_dict['Input Mode']['list_filename']
            if(path):
                config_obj.event_info_keys = get_info_keys(events_dict['Input Mode']['single_filenames'][0])
                config_obj.events_files_list = path
            else:
                st.error("No Event files have been uploaded! Please check your environment again!")
                return False

        return True

    def display_graph(self, config_obj, dict):
        int_dict = dict['Interactions']
        int_dict['Input Mode']['single_filenames'] = list(set(int_dict['Input Mode']['single_filenames']))

        if(int_dict['Input Mode']['index']==0):
            outpath = get_interaction_graph(config_obj.agents_filename, "web_single_interaction.txt")
            HtmlFile = open(outpath, 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.html(source_code, height = 600,width=600)

        elif(not int_dict['Input Mode']['single_filenames']):
            st.info("No interaction networks!")
        else:
            x=0
            for file in int_dict['Input Mode']['single_filenames']:
                if(x==3):
                    break
                outpath = get_interaction_graph(config_obj.agents_filename, file)
                HtmlFile = open(outpath, 'r', encoding='utf-8')
                source_code = HtmlFile.read()
                components.html(source_code, height = 900,width=900)
                x+=1


    def run(self, state):

        no_iterations = st.sidebar.slider("Number of Monte Carlo iterations",1,1000,100)
        self.show_configuration(state)
        config_obj = Utils.get_start_config(osp.join("Data","start_config.pkl"))
        self.save_general_config(state.params['General Configuration'],config_obj)
        flag = self.save_data_files(state.params['Environment'],config_obj)
        self.display_graph(config_obj,state.params['Environment'])

        if(flag):
            Utils.run_simulation_from_web(config_obj,state,no_iterations)
