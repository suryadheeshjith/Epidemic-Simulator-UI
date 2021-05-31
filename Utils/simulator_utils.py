from Utils.streamlit_utils import get_progress_UI_list
from Utils.file_utils import files_checker, get_model_from_file, get_policy_from_file, get_file_names_list
import Simulator.World
import Simulator.vulnerability_detection.Algorithm as Algorithm
import streamlit as st
import pandas as pd

##########################################################################################
# Common utils for both modes
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
    no_iterations = st.sidebar.slider("Number of Monte Carlo iterations",1,1000,100)
    if(files_checker(config_obj)):
        button0 = st.button("Run simulation")
        button1 = st.button("Vulnerable agents")
        button2 = st.button("Agent vulnerabilities")
        if(button0):
            world_obj=get_world_object_upload(config_obj, st_list)
            plot_disease_graph(world_obj)

        elif(button1):
            world_obj=get_world_object_upload(config_obj, st_list)
            run_vulnerable_agents(world_obj, no_iterations)

        elif(button2):
            world_obj=get_world_object_upload(config_obj, st_list)
            run_agent_vulnerabilities(config_obj,no_iterations)

##########################################################################################
# Run simulation from web
def get_world_object_web(config_obj, state, st_list):
    model = state.params['Model']['model']
    policy_list = []
    event_restriction_fn=state.params['Policy']['Event Restriction Function']

    config_obj.model = model
    config_obj.policy_list = policy_list
    config_obj.event_restriction_fn = event_restriction_fn
    config_obj.list_interactions_files = get_file_names_list(config_obj.interactions_files_list)
    config_obj.list_events_files = get_file_names_list(config_obj.events_files_list)
    world_obj=Simulator.World.World(config_obj,model,policy_list,event_restriction_fn,config_obj.agents_filename,\
    config_obj.list_interactions_files,config_obj.locations_filename,config_obj.list_events_files,st_list)
    config_obj.world_obj = world_obj
    return world_obj


def run_simulation_from_web(config_obj,state,no_iterations):
    st_list = get_progress_UI_list()
    if(config_obj):
        button0 = st.button("Run simulation")
        button1 = st.button("Vulnerable agents")
        button2 = st.button("Agent vulnerabilities")
        if(button0):
            world_obj = get_world_object_web(config_obj, state, st_list)
            plot_disease_graph(world_obj)

        elif(button1):
            world_obj=get_world_object_web(config_obj, state, st_list)
            run_vulnerable_agents(world_obj, no_iterations)

        elif(button2):
            world_obj=get_world_object_web(config_obj, state, st_list)
            run_agent_vulnerabilities(config_obj,no_iterations)
