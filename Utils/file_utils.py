import os.path as osp
import os
from os import listdir
from os.path import isfile, join
import logging
import Simulator.ReadFile
import importlib.util
import streamlit as st

file_list = ['requirements.txt','README.md','.gitignore','app.py']

####################################################################
# Reading and Writing files
def clear_files():
    onlyfiles = [f for f in listdir('.') if isfile(join('', f))]

    for file in onlyfiles:
        if file not in file_list:
            os.remove(file)
            logging.warning("Removed File {0}".format(file))

def write_to_file(string, filepath):
    fp = open(filepath,"w")
    fp.writelines(string)
    fp.close()

####################################################################
# Generating strings for web run

def write_agents(self, filename,n):
    header='Agent Index'

    f=open(filename,'w')
    f.write(str(n)+'\n')
    f.write(header+'\n')

    for i in range(n):
        f.write(str(i)+'\n')

####################################################################
# Retrieve list from file with list of filenames

def get_file_names_list(fileslist_filename):

    files_list = []
    if fileslist_filename=='':
        print('No files uploaded!')
    else:
        obj=Simulator.ReadFile.ReadFilesList(fileslist_filename)
        files_list=obj.file_list
        if files_list==[]:
            print('Nothing in files')

    return files_list

####################################################################
# File checking

def files_checker(config_obj):

    if(not config_obj):
        st.write("Begin by uploading the config.txt file")
        return False

    if(not osp.isfile('config.txt')):
        st.write("config.txt file has not been uploaded correctly!")
        return False

    if(not osp.isfile(config_obj.agents_filename)):
        st.write("Please upload the agents file specified in config.txt!")
        return False

    if(not osp.isfile('UserModel.py')):
        st.write("Please upload UserModel.py!")
        return False

    if(not osp.isfile('Generate_policy.py')):
        st.write("Please upload Generate_policy.py!")
        return False

    if(config_obj.locations_filename):
        if(not osp.isfile(config_obj.locations_filename)):
            st.write("Please upload the locations file specified in config.txt!")
            return False

    if(config_obj.interactions_files_list):
        if(not osp.isfile(config_obj.interactions_files_list)):
            st.write("Please upload the interactions list file specified in config.txt!")
            return False
        else:
            for file in config_obj.list_interactions_files:
                if(not osp.isfile(file)):
                    st.write("Please upload the individual interactions file specified in your interactions files list!")
                    return False

    if(config_obj.events_files_list):
        if(not osp.isfile(config_obj.events_files_list)):
            st.write("Please upload the events list file specified in config.txt!")
            return False
        else:
            for file in config_obj.list_events_files:
                if(not osp.isfile(file)):
                    st.write("Please upload the individual events file specified in your events files list!")
                    return False

    return True

####################################################################
# Model and Policy file reading

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_model_from_file(example_path):
    UserModel = module_from_file("Generate_model", osp.join(example_path,'UserModel.py'))
    model = UserModel.UserModel()
    return model

def get_policy_from_file(example_path):
    Generate_policy = module_from_file("Generate_policy", osp.join(example_path,'Generate_policy.py'))
    policy_list, event_restriction_fn=Generate_policy.generate_policy()
    return policy_list, event_restriction_fn
