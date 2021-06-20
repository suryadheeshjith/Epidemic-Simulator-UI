import streamlit as st
import Simulator.ReadFile
import Simulator.Model as Model
from Utils.file_utils import write_to_file, get_file_names_list, get_random_graph_lines, get_star_graph_lines, check_files_list_list
from csv import DictReader
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
            config_obj.list_interactions_files = [] #### Editing simulator
            config_obj.list_events_files = [] #### Editing simulator
        else:
            st.error("""
                    Given File : {0}  Required File : config.txt
                    """.format(file.name))

    return config_obj

def get_single_file_uploader(mode, file_name):
    file = st.file_uploader("Upload {0} file".format(mode))
    if(file is not None):
        if(file.name == file_name):
            string = file.getvalue().decode("utf-8")
            write_to_file(string, file_name)
        else:
            st.error("""
                    Given File : {0}  Required File : {1}
                    """.format(file.name,file_name))


def get_multiple_file_uploaders(mode, files_list_list):
    listOflist_files = []
    st.markdown("Upload {0} Files ".format(mode))
    for files_list in files_list_list:
        f1 = st.file_uploader("Upload File name : {0}".format(files_list))
        if(f1 is not None):
            if(f1.name == files_list):
                string = f1.getvalue().decode("utf-8")
                write_to_file(string, files_list)
            else:
                st.error("""
                        Given File : {0}  Required File : {1}
                        """.format(f1.name,files_list))

    if(check_files_list_list(files_list_list)):
        listOflist_files = get_file_names_list(files_list_list, "")
        for ls in listOflist_files:
            for file_name in ls:
                f2 = st.file_uploader("Upload File name : {0}".format(file_name))
                if(f2 is not None):
                    if(f2.name == file_name):
                        string = f2.getvalue().decode("utf-8")
                        write_to_file(string, file_name)
                    else:
                        st.error("""
                                Given File : {0}  Required File : {1}
                                """.format(f2.name,file_name))
    return listOflist_files

def get_uploaders(key):

    config_obj = get_config_file_uploader(key)

    if(config_obj):
        get_single_file_uploader("Agents", config_obj.agents_filename)
        get_single_file_uploader("Model", "UserModel.py")
        get_single_file_uploader("Policy", "Generate_policy.py")

        if(config_obj.interactions_files_list_list != ['']):
            config_obj.list_interactions_files = get_multiple_file_uploaders("Interactions",config_obj.interactions_files_list_list)

        if(config_obj.locations_filename):
            get_single_file_uploader("Locations",config_obj.locations_filename)

        if(config_obj.events_files_list_list != ['']):
            config_obj.list_events_files = get_multiple_file_uploaders("Events",config_obj.events_files_list_list)

    return config_obj


####################################################################
# Graph display
def get_num_agents(agents_file):
    fp = open(agents_file,'r')
    num = int(fp.readline())
    return num

def get_interaction_graph_from_file(number_of_agents, interaction_file_path):

    fp = open(interaction_file_path,'r')
    file_type = interaction_file_path[-3:]

    outpath = interaction_file_path[:-3]+'html'
    net = Network()
    if(file_type=='txt'):
        num = int(fp.readline())
        fp.readline()

        ls = list(range(number_of_agents))

        net.add_nodes(ls)

        for i in range(num):
            line = fp.readline()
            line = line[:-1]
            a,b = line.split(':')
            net.add_edge(int(a),int(b))

    elif(file_type=='csv'):
        csv_dict_reader=DictReader(fp)
        csv_list=list(csv_dict_reader)
        n=len(csv_list)
        ls = list(range(n))
        net.add_nodes(ls)

        for i in range(n):
            info_dict=csv_list[i]
            net.add_edge(int(info_dict['Agent Index']),int(info_dict['Interacting Agent Index']))

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
