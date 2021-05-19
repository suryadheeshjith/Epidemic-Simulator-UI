import streamlit as st
import UI
import Simulator.World
import os.path as osp
import importlib.util


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_model(example_path):
    UserModel = module_from_file("Generate_model", osp.join(example_path,'UserModel.py'))
    model = UserModel.UserModel()
    return model

def get_policy(example_path):
    Generate_policy = module_from_file("Generate_policy", osp.join(example_path,'Generate_policy.py'))
    policy_list, event_restriction_fn=Generate_policy.generate_policy()
    return policy_list, event_restriction_fn


if __name__ == "__main__":

    # Session state
    session = UI.get_session_state(run_id=0)

    st.write("""
    # Welcome to our Epidemic Simulator!
    """)
    st.write("------------------------------------------------------------------------------------")

    st.write("This implementation of the simulator is based on the [Episimmer](https://github.com/healthbadge/episimmer) simulator.")
    st.write("""
    To get started, choose your mode of inputting your data. Do note that by choosing to upload your files directly, you harness the highest possible capability
    the simulator has to offer. Inputting data through the website will only have limited capability.
    """)

    input_options = ['Upload files', 'Input data on the Website']
    option = st.selectbox('Input Mode : ', input_options)
    st.write("------------------------------------------------------------------------------------")
    if(option=='Upload files'):

        clear_button = st.button("Click here to clear all files")
        if(clear_button):
            UI.clear_files()
            session.run_id += 1

        config_obj = UI.get_uploaders(key=session.run_id)

        button = st.button("Click here to Run!")

        st_list = UI.get_progress_UI_list()

        if(button):
            if(not config_obj):
                st.write("config.txt file has not been uploaded correctly!")
                
            elif(UI.files_checker(config_obj)):

                example_path = ''

                # User Model and Policy
                model = get_model(example_path)
                policy_list, event_restriction_fn=get_policy(example_path)

                # Creation of World object
                world_obj=Simulator.World.World(config_obj,model,policy_list,event_restriction_fn,config_obj.agents_filename,\
                config_obj.list_interactions_files,config_obj.locations_filename,config_obj.list_events_files,st_list)
                plt = world_obj.simulate_worlds()
                st.pyplot(plt)


    elif(option == 'Input data on the Website'):
        UI.clear_files()
        app = UI.MultiPage()
        app.navbar_name = "Navigation"
        app.next_page_button = "Next Page"
        app.previous_page_button = "Previous Page"
        app.add_app("Simulation Configuration", UI.UI_Simulation_Config)
        app.add_app("Agents", UI.UI_Agents)
        app.add_app("Model", UI.UI_Model)
        app.add_app("Events", UI.UI_Events)
        app.add_app("Results", UI.UI_Results)
        app.run()
