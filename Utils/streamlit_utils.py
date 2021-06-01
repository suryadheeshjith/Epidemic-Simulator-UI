import streamlit as st
import Simulator.ReadFile
import Simulator.Model as Model
from Utils.file_utils import write_to_file, get_file_names_list, get_random_graph_lines, get_star_graph_lines
from pyvis.network import Network
import streamlit.components.v1 as components

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

def get_interaction_graph_from_file(number_of_agents, interaction_file_path):

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
    net.show_buttons(filter_=['physics'])
    net.show(outpath)
    return outpath


def get_interaction_graph_from_dict(number_of_agents, dict):

    outpath = "dummy_int_graph.html"
    ls = list(range(number_of_agents))
    net = Network()

    net.add_nodes(ls)
    p=0.0
    lines = []
    if(dict['Interaction Graph']['name']=='Random Graph'):
        p = dict['Interaction Graph']['params']['prob']
        lines = get_random_graph_lines(number_of_agents,p)

    elif(dict['Interaction Graph']['name']=='Fully Connected Graph'):
        lines = get_random_graph_lines(number_of_agents,1.0)

    elif(dict['Interaction Graph']['name']=='Star Graph'):
        lines = get_star_graph_lines(number_of_agents)

    for line in lines:
        line = line[:-1]
        a,b = line.split(':')
        net.add_edge(int(a),int(b))

    net.show_buttons(filter_=['physics'])
    net.show(outpath)
    return outpath

def display_interaction_graph(number_of_agents, dict):
    int_dict = dict['Interactions']
    int_dict['Input Mode']['single_filenames'] = list(set(int_dict['Input Mode']['single_filenames']))

    if(int_dict['Input Mode']['index']==0):
        outpath = get_interaction_graph_from_dict(number_of_agents, int_dict)
        HtmlFile = open(outpath, 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, height = 600,width=1200)

    elif(not int_dict['Input Mode']['single_filenames']):
        st.info("No interaction networks!")
    else:
        x=0
        for file in int_dict['Input Mode']['single_filenames']:
            if(x==3):
                break
            outpath = get_interaction_graph_from_file(number_of_agents, file)
            HtmlFile = open(outpath, 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.html(source_code, height = 600,width=1200)
            x+=1



def get_model_graph(model):
    outpath = "dummy_model.html"
    net = Network(directed=True)
    states = model.individual_state_types
    infected_states = model.infected_states
    for i,state in enumerate(states):
        if(state in infected_states):
            net.add_node(i, label=state, shape='box', color = '#fc9283', borderWidth=30, borderWidthSelected=30)
        else:
            net.add_node(i, label=state, shape='box', color = '#99bdf7', borderWidth=30, borderWidthSelected=30)

    transitions = model.transmission_prob
    for i,state_i in enumerate(states):
        for j,state_j in enumerate(states):
            if(transitions[state_i][state_j].args!=(0,)):
                str1 = '<function StochasticModel.'
                str2 = str(transitions[state_i][state_j].func.__func__)[len(str1):]
                func_name = str2.split(' ')[0]
                if(func_name=="full_p_infection"):
                    net.add_edge(i,j,color='#fc9283')
                else:
                    net.add_edge(i,j,color='#99bdf7')


    net.show(outpath)
    HtmlFile = open(outpath, 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height = 600,width=1200)
