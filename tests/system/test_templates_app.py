import sys
sys.path.insert(1, '../../')
sys.path.insert(1, '../../Simulator')

import streamlit as st
import ReadFile
from Utils.simulator_utils import get_world_object_template, plot_disease_graph, run_vulnerable_agents, run_agent_vulnerabilities
from Utils.streamlit_utils import get_progress_UI_list
from Utils.file_utils import get_config_path, get_file_paths
import Utils
import os.path as osp
import os

def get_options_to_run(fn, *args):
    world_obj=fn(*args)
    plot_disease_graph(world_obj)
    world_obj=fn(*args)
    run_vulnerable_agents(world_obj,2)
    world_obj=fn(*args)
    config_obj = world_obj.config_obj
    run_agent_vulnerabilities(config_obj,2)

def run_simulation_from_template(p, choice):

    example_path = osp.join(p,choice)
    # print(example_path)
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

def test_templates():
    dir_path = osp.join(osp.dirname(osp.dirname(os.getcwd())),"examples")
    ls = [f.path.split("/")[-1] for f in os.scandir(dir_path) if f.is_dir()]
    ls.sort()
    for i,l in enumerate(ls):
        run_simulation_from_template(dir_path, l)
        st.sidebar.write("{0}/{1} complete".format(i+1,len(ls)))

test_templates()
st.sidebar.write("Completed!")
