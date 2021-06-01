from Utils.streamlit_utils import get_progress_UI_list
from Utils.file_utils import files_checker, get_model_from_file, get_policy_from_file, get_file_names_list, get_config_path, get_file_paths
import Simulator.World
import Simulator.vulnerability_detection.Algorithm as Algorithm
import Simulator.ReadFile as ReadFile
import streamlit as st
import pandas as pd
import copy
import os.path as osp

##########################################################################################
# Common utils for all modes
def plot_disease_graph(world_obj):
    plt = world_obj.simulate_worlds()
    st.pyplot(plt)

def run_vulnerable_agents(world_obj, no_iterations):
    mc_obj=Algorithm.Vulnerable_Agent_MC1(world_obj)
    mc_obj.do_MC(no_iterations)
    st.markdown("Top 10 vulnerable agents : ")
    dict = mc_obj.get_maximum_vulnerable_agents(10)
    for key in dict.keys():
        dict[key] = [dict[key]]
    df1 = pd.DataFrame.from_dict(dict)
    st.dataframe(df1)
    st.markdown("Bottom 10 vulnerable agents : ")
    dict = mc_obj.get_minimum_vulnerable_agents(10)
    for key in dict.keys():
        dict[key] = [dict[key]]
    df2 = pd.DataFrame.from_dict(dict)
    st.dataframe(df2)

def run_agent_vulnerabilities(config_obj,no_iterations):
    config_obj.config_obj = config_obj
    mc_obj = Algorithm.Agent_Vulnerabilities_MC3(config_obj,[50,50])
    mc_obj.do_MC(no_iterations,1)

    st.markdown("Top 10 agent vulnerabilities : ")
    dict = mc_obj.get_maximum_agent_vulnerability(10)
    for key in dict.keys():
        dict[key] = [dict[key]]
    df1 = pd.DataFrame.from_dict(dict)
    st.dataframe(df1)
    st.markdown("Bottom 10 agent vulnerabilities : ")
    dict = mc_obj.get_minimum_agent_vulnerability(10)
    for key in dict.keys():
        dict[key] = [dict[key]]
    df2 = pd.DataFrame.from_dict(dict)
    st.dataframe(df2)

def get_no_iterations(option):
    if option == "High":
        st.info("Running for 10000 iterations....")
        return 10000

    elif option == "Medium":
        st.info("Running for 1000 iterations....")
        return 1000

    elif option == "Low":
        st.info("Running for 100 iterations....")
        return 100

def get_options_to_run(fn, *args):
    compute_options = ["High", "Medium", "Low"]
    button0 = st.button("Run simulation")
    col0, col1 = st.beta_columns(2)
    button1 = col0.button("Vulnerable agents")
    choice = col1.selectbox("Choose computation level for vulnerability detection", compute_options, 1,key="Vul_agents")
    button2 = col0.button("Agent vulnerabilities")
    if(button0):
        world_obj=fn(*args)
        plot_disease_graph(world_obj)

    elif(button1):
        world_obj=fn(*args)
        no_iterations = get_no_iterations(choice)
        run_vulnerable_agents(world_obj, no_iterations)

    elif(button2):
        world_obj=fn(*args)
        config_obj = world_obj.config_obj
        no_iterations = get_no_iterations(choice)
        run_agent_vulnerabilities(config_obj, no_iterations)


##########################################################################################
# Run simulation from upload
def get_world_object_upload(config_obj, st_list):
    model = get_model_from_file('')
    policy_list, event_restriction_fn=get_policy_from_file('')
    config_obj.model = model
    config_obj.policy_list = policy_list
    config_obj.event_restriction_fn = event_restriction_fn

    world_obj=Simulator.World.World(config_obj,config_obj.model,config_obj.policy_list,config_obj.event_restriction_fn,config_obj.agents_filename,\
                                    config_obj.list_interactions_files,config_obj.locations_filename,config_obj.list_events_files,st_list)

    config_obj.world_obj = world_obj
    return world_obj

def run_simulation_from_upload(config_obj):
    st_list = get_progress_UI_list()
    if(files_checker(config_obj)):
        get_options_to_run(get_world_object_upload,config_obj, st_list)

##########################################################################################
# Run simulation from web
def get_world_object_web(config_obj, state, st_list):
    config_obj.model = state.params['Model']['model']
    config_obj.policy_list = copy.deepcopy(state.params['Policy']['Policy list']) ### Very important to deep copy because streamlit refreshes if any of its variables change.
    config_obj.event_restriction_fn = state.params['Policy']['Event Restriction Function']
    config_obj.list_interactions_files = get_file_names_list(config_obj.interactions_files_list)
    config_obj.list_events_files = get_file_names_list(config_obj.events_files_list)
    world_obj=Simulator.World.World(config_obj,config_obj.model,config_obj.policy_list,config_obj.event_restriction_fn,config_obj.agents_filename,\
                                    config_obj.list_interactions_files,config_obj.locations_filename,config_obj.list_events_files,st_list)
    config_obj.world_obj = world_obj
    return world_obj


def run_simulation_from_web(config_obj,state):
    st_list = get_progress_UI_list()
    if(config_obj):
        get_options_to_run(get_world_object_web, config_obj, state, st_list)

##########################################################################################
# Run simulation from template

def get_world_object_template(example_path, config_obj, st_list):

    model = get_model_from_file(example_path)
    policy_list, event_restriction_fn=get_policy_from_file(example_path)
    config_obj.model = model
    config_obj.policy_list = policy_list
    config_obj.event_restriction_fn = event_restriction_fn
    config_obj.list_interactions_files = None
    config_obj.list_events_files = None
    try:
        ls = get_file_names_list(config_obj.interactions_files_list)
        config_obj.list_interactions_files = [osp.join(example_path,f) for f in ls]
    except:
        pass
    try:
        ls = get_file_names_list(config_obj.events_files_list)
        config_obj.list_events_files = [osp.join(example_path,f) for f in ls]
    except:
        pass

    world_obj=Simulator.World.World(config_obj,config_obj.model,config_obj.policy_list,config_obj.event_restriction_fn,config_obj.agents_filename,\
                                    config_obj.list_interactions_files,config_obj.locations_filename,config_obj.list_events_files,st_list)

    config_obj.world_obj = world_obj
    return world_obj

def run_simulation_from_template(choice):
    example_path = osp.join('examples',choice)
    st_list = get_progress_UI_list()

    config_filename = get_config_path(example_path)
    config_obj=ReadFile.ReadConfiguration(config_filename)
    agents_filename, interactions_FilesList_filename,\
    events_FilesList_filename, locations_filename = get_file_paths(example_path,config_obj)
    config_obj.agents_filename = agents_filename
    config_obj.interactions_files_list = interactions_FilesList_filename
    config_obj.events_files_list = events_FilesList_filename
    config_obj.locations_filename = locations_filename

    get_options_to_run(get_world_object_template, example_path, config_obj, st_list)
