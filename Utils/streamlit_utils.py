import streamlit as st
import Simulator.ReadFile
from Utils.file_utils import write_to_file, get_file_names_list

def get_progress_UI_list():

    running_world = st.empty()
    progress_bar_world = st.empty()
    running_time_step = st.empty()
    progress_bar_time_step = st.empty()
    st_list = [running_world, progress_bar_world, running_time_step, progress_bar_time_step]
    return st_list

# This function is a mess.... Requires refactoring
def get_uploaders(key):

    config_obj = None
    interactions_files_list = None
    events_files_list = None

    file = st.file_uploader("Upload config file",key=key)
    if(file is not None):
        if(file.name == "config.txt"):
            string = file.getvalue().decode("utf-8")
            write_to_file(string, "config.txt")
            config_obj=Simulator.ReadFile.ReadConfiguration("config.txt")
            config_obj.list_interactions_files = None #### Editing simulator
            config_obj.list_events_files = None #### Editing simulator
        else:
            st.write("""
                    Given File : {0} ; Required File : config.txt
                    """.format(file.name))

    if(config_obj is not None):
        file = st.file_uploader("Upload agents file")
        if(file is not None):
            if(file.name == config_obj.agents_filename):
                string = file.getvalue().decode("utf-8")
                write_to_file(string, config_obj.agents_filename)
            else:
                st.write("""
                        Given File : {0} ; Required File : {1}
                        """.format(file.name,config_obj.agents_filename))

        file = st.file_uploader("Upload Model file")
        if(file is not None):
            if(file.name == "UserModel.py"):
                string = file.getvalue().decode("utf-8")
                write_to_file(string, "UserModel.py")
            # else:
            #     st.write("Please add the file UserModel.py (Check cases too)")

        file = st.file_uploader("Upload Policy file")
        if(file is not None):
            if(file.name == "Generate_policy.py"):
                string = file.getvalue().decode("utf-8")
                write_to_file(string, "Generate_policy.py")
            # else:
            #     st.write("Please add the file Generate_policy.py (Check cases too)")

        if(config_obj.interactions_files_list):
            file = st.file_uploader("Upload Interactions list file")
            if(file is not None):
                if(file.name == config_obj.agents_filename):
                    string = file.getvalue().decode("utf-8")
                    write_to_file(string, config_obj.interactions_files_list)
                    interactions_files_list = get_file_names_list(config_obj.interactions_files_list)
                    config_obj.list_interactions_files = interactions_files_list
                    for file_name in interactions_files_list:
                        f = st.file_uploader("Upload File name : {0}".format(file_name))
                        if(f is not None):
                            if(f.name == file_name):
                                string = f.getvalue().decode("utf-8")
                                write_to_file(string, file_name)
                            else:
                                st.write("""
                                        Given File : {0} ; Required File : {1}
                                        """.format(f.name,file_name))
                else:
                    st.write("""
                            Given File : {0} ; Required File : {1}
                            """.format(file.name,config_obj.interactions_files_list))


        if(config_obj.locations_filename):
            file = st.file_uploader("Upload Locations")
            if(file is not None):
                if(file.name == config_obj.locations_filename):
                    string = file.getvalue().decode("utf-8")
                    write_to_file(string, config_obj.locations_filename)
                else:
                    st.write("""
                            Given File : {0} ; Required File : {1}
                            """.format(file.name,config_obj.locations_filename))

        if(config_obj.events_files_list):
            file = st.file_uploader("Upload Events list file")
            if(file is not None):
                if(file.name == config_obj.events_files_list):
                    string = file.getvalue().decode("utf-8")
                    write_to_file(string, config_obj.events_files_list)
                    events_files_list = get_file_names_list(config_obj.events_files_list)
                    config_obj.list_events_files = events_files_list
                    for file_name in events_files_list:
                        f = st.file_uploader("Upload File name : {0}".format(file_name))
                        if(f is not None):
                            if(f.name == file_name):
                                string = f.getvalue().decode("utf-8")
                                write_to_file(string, file_name)
                            else:
                                st.write("""
                                        Given File : {0} ; Required File : {1}
                                        """.format(f.name,file_name))
                else:
                    st.write("""
                            Given File : {0} ; Required File : {1}
                            """.format(file.name,config_obj.events_files_list))

    return config_obj
