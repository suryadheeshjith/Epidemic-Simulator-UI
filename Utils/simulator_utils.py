from Utils.streamlit_utils import get_progress_UI_list
from Utils.file_utils import files_checker, get_model, get_policy
import Simulator.World
import streamlit as st

def run_simulation(config_obj):

    st_list = get_progress_UI_list()
    if(files_checker(config_obj)):
        button = st.button("Click here to Run!")
        if(button):
            # User Model and Policy
            model = get_model('')
            policy_list, event_restriction_fn=get_policy('')

            # Simulation Run
            world_obj=Simulator.World.World(config_obj,model,policy_list,event_restriction_fn,config_obj.agents_filename,\
            config_obj.list_interactions_files,config_obj.locations_filename,config_obj.list_events_files,st_list)
            plt = world_obj.simulate_worlds()
            st.pyplot(plt)
