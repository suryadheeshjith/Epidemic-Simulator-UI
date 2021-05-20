from Utils.streamlit_utils import get_progress_UI_list
from Utils.file_utils import files_checker, get_model_from_file, get_policy_from_file
import Simulator.World
import streamlit as st

def run_simulation_from_upload(config_obj):
    st_list = get_progress_UI_list()
    if(files_checker(config_obj)):
        button = st.button("Click here to Run!")
        if(button):
            # User Model and Policy
            model = get_model_from_file('')
            policy_list, event_restriction_fn=get_policy_from_file('')

            # Simulation Run
            world_obj=Simulator.World.World(config_obj,model,policy_list,event_restriction_fn,config_obj.agents_filename,\
            config_obj.list_interactions_files,config_obj.locations_filename,config_obj.list_events_files,st_list)
            plt = world_obj.simulate_worlds()
            st.pyplot(plt) 

def run_simulation_from_web(config_obj,state):
    st_list = get_progress_UI_list()
    if(config_obj):
        button = st.button("Click here to Run!")
        if(button):
            # User Model and Policy
            model = state.params['Model']['model']
            policy_list = state.params['Policy']['policy_list']
            event_restriction_fn=state.params['Policy']['Event Restriction Function']

            # Simulation Run
            world_obj=Simulator.World.World(config_obj,model,policy_list,event_restriction_fn,config_obj.agents_filename,\
            config_obj.list_interactions_files,config_obj.locations_filename,config_obj.list_events_files,st_list)
            plt = world_obj.simulate_worlds()
            st.pyplot(plt)
