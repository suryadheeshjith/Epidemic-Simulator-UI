import streamlit as st
import Simulator.ReadFile
from Utils.file_utils import write_to_file, get_file_names_list
from pyvis.network import Network

def get_progress_UI_list():

    running_world = st.empty()
    progress_bar_world = st.empty()
    running_time_step = st.empty()
    progress_bar_time_step = st.empty()
    st_list = [running_world, progress_bar_world, running_time_step, progress_bar_time_step]
    return st_list

####################################################################
# File Uploader Functions

def get_config_file_uploader(key):

    config_obj = None
    file = st.file_uploader("Upload config file",key=key)
    if(file is not None):
        if(file.name == "config.txt"):
            string = file.getvalue().decode("utf-8")
            write_to_file(string, "config.txt")
            config_obj=Simulator.ReadFile.ReadConfiguration("config.txt")
            config_obj.list_interactions_files = None #### Editing simulator
            config_obj.list_events_files = None #### Editing simulator
        else:
            st.error("""
                    Given File : {0}  Required File : config.txt
                    """.format(file.name))

    return config_obj

def get_agents_file_uploader(config_obj):
    file = st.file_uploader("Upload agents file")
    if(file is not None):
        if(file.name == config_obj.agents_filename):
            string = file.getvalue().decode("utf-8")
            write_to_file(string, config_obj.agents_filename)
        else:
            st.error("""
                    Given File : {0}  Required File : {1}
                    """.format(file.name,config_obj.agents_filename))

def get_model_file_uploader():
    file = st.file_uploader("Upload Model file")
    if(file is not None):
        if(file.name == "UserModel.py"):
            string = file.getvalue().decode("utf-8")
            write_to_file(string, "UserModel.py")
        else:
            st.error("""
                    Given File : {0}  Required File : {1}
                    """.format(file.name,"UserModel.py"))

def get_policy_file_uploader():
    file = st.file_uploader("Upload Policy file")
    if(file is not None):
        if(file.name == "Generate_policy.py"):
            string = file.getvalue().decode("utf-8")
            write_to_file(string, "Generate_policy.py")
        else:
            st.error("""
                    Given File : {0}  Required File : {1}
                    """.format(file.name,"Generate_policy.py"))

def get_location_file_uploader(config_obj):
    file = st.file_uploader("Upload Locations")
    if(file is not None):
        if(file.name == config_obj.locations_filename):
            string = file.getvalue().decode("utf-8")
            write_to_file(string, config_obj.locations_filename)
        else:
            st.error("""
                    Given File : {0}  Required File : {1}
                    """.format(file.name,config_obj.locations_filename))

def get_interaction_files_uploaders(config_obj):
    file = st.file_uploader("Upload Interactions list file")
    if(file is not None):
        if(file.name == config_obj.interactions_files_list):
            string = file.getvalue().decode("utf-8")
            write_to_file(string, config_obj.interactions_files_list)
            config_obj.list_interactions_files = get_file_names_list(config_obj.interactions_files_list)
            for file_name in config_obj.list_interactions_files:
                f = st.file_uploader("Upload File name : {0}".format(file_name))
                if(f is not None):
                    if(f.name == file_name):
                        string = f.getvalue().decode("utf-8")
                        write_to_file(string, file_name)
                    else:
                        st.error("""
                                Given File : {0}  Required File : {1}
                                """.format(f.name,file_name))
        else:
            st.error("""
                    Given File : {0}  Required File : {1}
                    """.format(file.name,config_obj.interactions_files_list))


def get_event_files_uploaders(config_obj):
    file = st.file_uploader("Upload Events list file")
    if(file is not None):
        if(file.name == config_obj.events_files_list):
            string = file.getvalue().decode("utf-8")
            write_to_file(string, config_obj.events_files_list)
            config_obj.list_events_files = get_file_names_list(config_obj.events_files_list)
            for file_name in config_obj.list_events_files:
                f = st.file_uploader("Upload File name : {0}".format(file_name))
                if(f is not None):
                    if(f.name == file_name):
                        string = f.getvalue().decode("utf-8")
                        write_to_file(string, file_name)
                    else:
                        st.error("""
                                Given File : {0}  Required File : {1}
                                """.format(f.name,file_name))
        else:
            st.error("""
                    Given File : {0}  Required File : {1}
                    """.format(file.name,config_obj.events_files_list))


def get_uploaders(key):

    config_obj = get_config_file_uploader(key)

    if(config_obj):
        get_agents_file_uploader(config_obj)
        get_model_file_uploader()
        get_policy_file_uploader()

        if(config_obj.interactions_files_list):
            get_interaction_files_uploaders(config_obj)

        if(config_obj.locations_filename):
            get_location_file_uploader(config_obj)

        if(config_obj.events_files_list):
            get_event_files_uploaders(config_obj)

    return config_obj


####################################################################
# Graph display
def get_num_agents(agents_file):
    fp = open(agents_file,'r')
    num = int(fp.readline())
    return num

def get_graph(agents_file, interaction_file_path):

    number_of_agents = get_num_agents(agents_file)
    fp = open(interaction_file_path,'r')

    outpath = interaction_file_path[:-3]+'html'

    num = int(fp.readline())
    fp.readline()

    ls = list(range(number_of_agents))
    net = Network()

    net.add_nodes(ls)

    for i in range(num):
        line = fp.readline()
        line = line[:-1]
        a,b = line.split(':')
        net.add_edge(int(a),int(b))

    fp.close()
    net.show(outpath)
    return outpath
