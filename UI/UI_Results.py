import streamlit as st
import Utils
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

    def save_files(self, state):
        pass
    def run(self, state):
        self.show_configuration(state)
        self.save_files()
        config_obj = None # temp
        Utils.run_simulation_from_web(config_obj)

        st.write("Sum of number of agents and worlds : ")
        st.write("{0}".format(state.params['Agents']['Number of Agents']+state.params['General Configuration']['Worlds']))
