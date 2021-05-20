import streamlit as st
import Utils
import Simulator.World
from UI.UI import UI_Base

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

    def run(self, state):
        self.show_configuration(state)

        st_list = Utils.get_progress_UI_list()
        button = st.button("Click to Run!")
        if(Utils.files_checker(config_obj)):
            if(button):

                # User Model and Policy
                model = Utils.get_model('')
                policy_list, event_restriction_fn=Utils.get_policy('')

                # Simulation Run
                world_obj=Simulator.World.World(config_obj,model,policy_list,event_restriction_fn,config_obj.agents_filename,\
                config_obj.list_interactions_files,config_obj.locations_filename,config_obj.list_events_files,st_list)
                plt = world_obj.simulate_worlds()
                st.pyplot(plt)

        st.write("Sum of number of agents and worlds : ")
        st.write("{0}".format(state.params['Agents']['no_agents']+state.params['General Configuration']['worlds']))
