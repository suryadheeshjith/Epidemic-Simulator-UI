import streamlit as st
import Simulator.ReadFile
import os.path as osp
import os

files_added = []

def clear_files():
    for file in files_added:
        if osp.isfile(file):
            os.remove(file)
            print("Removed",file)

def write_to_file(string, filepath):
    fp = open(filepath,"w")
    files_added.append(filepath)
    fp.writelines(string)
    fp.close()


def get_file_names_list(fileslist_filename):
    # Reading through a file (for interactions/events) that contain file names which contain interactions and event details for a time step

    files_list = []
    if fileslist_filename=='':
        print('No files uploaded!')
    else:
        obj=Simulator.ReadFile.ReadFilesList(fileslist_filename)
        files_list=obj.file_list
        if files_list==[]:
            print('Nothing in files')

    return files_list


def get_progress_UI_list():

    running_world = st.empty()
    progress_bar_world = st.empty()
    running_time_step = st.empty()
    progress_bar_time_step = st.empty()
    st_list = [running_world, progress_bar_world, running_time_step, progress_bar_time_step]
    return st_list

def get_uploaders(key):

    config_obj = None
    interactions_files_list = None
    events_files_list = None

    file = st.file_uploader("Upload config file",key=key)
    if(file is not None):
        string = file.getvalue().decode("utf-8")
        write_to_file(string, "config.txt")
        config_obj=Simulator.ReadFile.ReadConfiguration("config.txt")
        config_obj.list_interactions_files = None #### Editing simulator
        config_obj.list_events_files = None #### Editing simulator

    if(config_obj is not None):
        file = st.file_uploader("Upload agents file")
        if(file is not None):
            if(file.name == config_obj.agents_filename):
                string = file.getvalue().decode("utf-8")
                write_to_file(string, config_obj.agents_filename)
            else:
                st.write("""
                        Add the correct agent file corresponding to agent file given in config.txt.\n
                        Given File : {0} ; Required File : {1}
                        """.format(file.name,config_obj.agents_filename))

        file = st.file_uploader("Upload Model file")
        if(file is not None):
            if(file.name == "UserModel.py"):
                string = file.getvalue().decode("utf-8")
                write_to_file(string, "UserModel.py")
            else:
                st.write("Please add the file UserModel.py (Check cases too)")

        file = st.file_uploader("Upload Policy file")
        if(file is not None):
            if(file.name == "Generate_policy.py"):
                string = file.getvalue().decode("utf-8")
                write_to_file(string, "Generate_policy.py")
            else:
                st.write("Please add the file Generate_policy.py (Check cases too)")

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
                                        Add the correct Interactions file corresponding to files given in {0}.\n
                                        Given File : {1} ; Required File : {2}
                                        """.format(config_obj.interactions_files_list,f.name,file_name))
                else:
                    st.write("""
                            Add the correct Interactions list file corresponding to Interactions list file given in config.txt.\n
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
                            Add the correct locations file corresponding to locations file given in config.txt.\n
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
                                        Add the correct event file corresponding to files given in {0}.\n
                                        Given File : {1} ; Required File : {2}
                                        """.format(config_obj.events_files_list,f.name,file_name))
                else:
                    st.write("""
                            Add the correct Events list file corresponding to Events list file given in config.txt.\n
                            Given File : {0} ; Required File : {1}
                            """.format(file.name,config_obj.events_files_list))

    return config_obj

def files_checker(config_obj):

    if(not osp.isfile('config.txt')):
        st.write("config.txt file has not been uploaded correctly!")
        return False

    if(not osp.isfile(config_obj.agents_filename)):
        st.write("Agents file has not been uploaded correctly!")
        return False

    if(not osp.isfile('UserModel.py')):
        st.write("UserModel.py has not been uploaded correctly!")
        return False

    if(not osp.isfile('Generate_policy.py')):
        st.write("Generate_policy.py has not been uploaded correctly!")
        return False

    if(config_obj.locations_filename):
        if(not osp.isfile(config_obj.locations_filename)):
            st.write("Location file present in config.txt has not been uploaded correctly!")
            return False

    if(config_obj.interactions_files_list):
        if(not osp.isfile(config_obj.interactions_files_list)):
            st.write("Interaction file present in config.txt has not been uploaded correctly!")
            return False
        else:
            for file in config_obj.list_interactions_files:
                if(not osp.isfile(file)):
                    st.write("All individual time step interaction files have not been uploaded correctly!")
                    return False

    if(config_obj.events_files_list):
        if(not osp.isfile(config_obj.events_files_list)):
            st.write("Events file present in config.txt has not been uploaded correctly!")
            return False
        else:
            for file in config_obj.list_events_files:
                if(not osp.isfile(file)):
                    st.write("All individual time step event files have not been uploaded correctly!")
                    return False

    return True
