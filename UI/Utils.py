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
            write_to_file(string, "Generate_policy.py")

        interactions = st.checkbox("Add Interactions")
        if(interactions):
            file = st.file_uploader("Upload Interactions list file")
            if(file is not None):
                string = file.getvalue().decode("utf-8")
                write_to_file(string, config_obj.interactions_files_list)
                interactions_files_list = get_file_names_list(config_obj.interactions_files_list)
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
                events_files_list = get_file_names_list(config_obj.events_files_list)
                for file_name in events_files_list:
                    f = st.file_uploader("Upload File name : {0}".format(file_name))
                    if(f is not None):
                        string = f.getvalue().decode("utf-8")
                        write_to_file(string, file_name)

    return config_obj, interactions_files_list, events_files_list

def config_checker(config_obj):
    if(config_obj.interactions_files_list or config_obj.locations_filename or config_obj.events_files_list):
        return True

    config_obj.interactions_files_list = None
    config_obj.locations_filename = None
    config_obj.events_files_list = None

    return False

def files_checker(config_obj):
    if(osp.isfile('config.txt') and osp.isfile(config_obj.agents_filename) and osp.isfile('UserModel.py') and osp.isfile('Generate_policy.py')):
        if(config_checker(config_obj)):
            st.write("Looks like you have some files you haven't uploaded yet (Based on the config.txt file given). We've still run the simulation though!")

        return True

    return False
