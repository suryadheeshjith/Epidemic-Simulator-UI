import streamlit as st
import UI
import Simulator.ReadFile
import Simulator.World
import os
import os.path as osp
import importlib.util

import sys
sys.path.append("Simulator")

def write_to_file(string, filepath):
    fp = open(filepath,"w")
    fp.writelines(string)
    fp.close()


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_file_names_list(fileslist_filename, mode):
    # Reading through a file (for interactions/events) that contain file names which contain interactions and event details for a time step

    files_list = None

    if fileslist_filename=='':
        if(mode=="Interactions"):
            print('No Interaction files uploaded!')
        else:
            print('No Event files uploaded!')
    else:
        obj=Simulator.ReadFile.ReadFilesList(fileslist_filename)
        files_list=obj.file_list
        if files_list==[]:
            if(mode=="Interactions"):
                print('No Interactions inputted')
            else:
                print('No Events inputted')

    return files_list

def get_model(example_path):
    UserModel = module_from_file("Generate_model", osp.join(example_path,'UserModel.py'))
    model = UserModel.UserModel()
    return model

def get_policy(example_path):
    Generate_policy = module_from_file("Generate_policy", osp.join(example_path,'Generate_policy.py'))
    policy_list, event_restriction_fn=Generate_policy.generate_policy()
    return policy_list, event_restriction_fn

def files_checker():
    if(os.path.isfile('config.txt') and os.path.isfile('agents.txt') and os.path.isfile('UserModel.py') and os.path.isfile('Generate_Policy.py')):
        return True

    return False

def upload_run():
    config_obj = None
    interactions_files_list = None
    events_files_list = None

    file = st.file_uploader("Upload config file")
    if(file is not None):
        string = file.getvalue().decode("utf-8")
        write_to_file(string, "config.txt")
        config_obj=Simulator.ReadFile.ReadConfiguration("config.txt")

    if(config_obj is not None):
        file = st.file_uploader("Upload agents file")
        if(file is not None):
            string = file.getvalue().decode("utf-8")
            write_to_file(string, config_obj.agents_filename)

        file = st.file_uploader("Upload Model file")
        if(file is not None):
            string = file.getvalue().decode("utf-8")
            write_to_file(string, "UserModel.py")

        file = st.file_uploader("Upload Policy file")
        if(file is not None):
            string = file.getvalue().decode("utf-8")
            write_to_file(string, "Generate_Policy.py")

        interactions = st.checkbox("Add Interactions")
        if(interactions):
            file = st.file_uploader("Upload Interactions list file")
            if(file is not None):
                string = file.getvalue().decode("utf-8")
                write_to_file(string, config_obj.interactions_files_list)
                interactions_files_list = get_file_names_list(config_obj.interactions_files_list, "Interactions")
                for file_name in interactions_files_list:
                    f = st.file_uploader("Upload File name : {0}".format(file_name))
                    if(f is not None):
                        string = f.getvalue().decode("utf-8")
                        write_to_file(string, file_name)


        loc = st.checkbox("Add Locations")
        if(loc):
            file = st.file_uploader("Upload Locations")
            if(file is not None):
                string = file.getvalue().decode("utf-8")
                write_to_file(string, config_obj.locations_filename)

        eve = st.checkbox("Add Events")
        if(eve):
            file = st.file_uploader("Upload Events list file")
            if(file is not None):
                string = file.getvalue().decode("utf-8")
                write_to_file(string, config_obj.events_files_list)
                events_files_list = get_file_names_list(config_obj.interactions_files_list, "Events")
                for file_name in events_files_list:
                    f = st.file_uploader("Upload File name : {0}".format(file_name))
                    if(f is not None):
                        string = f.getvalue().decode("utf-8")
                        write_to_file(string, file_name)

    text = st.empty()
    button = st.button("Click here to Run!")
    running_world = st.empty()
    progress_bar_world = st.empty()
    running_time_step = st.empty()
    progress_bar_time_step = st.empty()
    st_list = [running_world, progress_bar_world, running_time_step, progress_bar_time_step]

    if(button):
        if(files_checker()):

            example_path = ''
            config_filename = 'config.txt'

            # User Model and Policy
            model = get_model(example_path)
            policy_list, event_restriction_fn=get_policy(example_path)

            # Creation of World object
            world_obj=Simulator.World.World(config_obj,model,policy_list,event_restriction_fn,config_obj.agents_filename,\
            interactions_files_list,config_obj.locations_filename,events_files_list,st_list)
            plt = world_obj.simulate_worlds()
            st.pyplot(plt)

        else:
            text.write("""
                Need more files! Files that are mandatory are :\n
                1. config.txt
                2. agents.txt
                3. UserModel.py
                4. Generate_Policy.py
                """)


if __name__ == "__main__":

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

    app = UI.MultiPage()
    app.navbar_name = "Navigation"
    app.next_page_button = "Next Page"
    app.previous_page_button = "Previous Page"

    if(option=='Upload files'):
        upload_run()

    elif(option == 'Input data on the Website'):
        # app.add_app("Welcome", UI.UI_Welcome)
        app.add_app("Simulation Configuration", UI.UI_Simulation_Config)
        app.add_app("Agents", UI.UI_Agents)
        app.add_app("Model", UI.UI_Model)
        app.add_app("Events", UI.UI_Events)
        app.run()


    # def app1():
    #     clear_cache()
    #     st.button("Do nothing...")
    #     var1 = 10
    #     var2 = 5
    #     if st.button("Click here to save the variables..."):
    #         st.write("First number: " + str(var1))
    #         st.write('Second number: ' + str(var2))
    #         save(var_list=[var1, var2], name="App1", page_names=["App2", "App3"])
    #         ######
    #
    # def app2(prev_vars):
    #     if prev_vars == None:
    #         st.write("Ooops... You forgot to save the variables...")
    #
    #     else:
    #         var1, var2 = prev_vars
    #         if st.button("Click here to sum the variables"):
    #             sum_var = var1+var2
    #             st.write(sum_var)
    #
    #         if st.button("Click here to save a new variable"):
    #             var3 = 27
    #             st.write(var3)
    #             save(var_list=[var3], name="App2", page_names=["App3"])
    #
    #
    #
    #         #####
    #
    # def app3(prev_vars):
    #     if prev_vars == None:
    #         st.write("Ooops... You forgot to save the variables...")
    #     else:
    #         try:
    #             var1, var2, var3 = prev_vars
    #             if st.button("Click here to multiply the variables"):
    #                 st.write(var1*var2*var3)
    #         except:
    #             ("Ooops... You forgot to save the last variable...")
