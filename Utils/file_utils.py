import os.path as osp
import os
from os import listdir
from os.path import isfile, join
import logging
import Simulator.ReadFile
import importlib.util
import streamlit as st
import pickle
import random
from csv import DictReader

file_list = ['requirements.txt','README.md','.gitignore','app.py','create_config_pickle.py']

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


def get_start_config(filename):
    with open(filename, 'rb') as input:
        config_obj = pickle.load(input)
    return config_obj

def get_value(line):
    if line.endswith('\n'):
        line=line[:-1]
    return line

def get_info_keys(filename):
    fp=open(filename,'r')
    file_type = filename[-3:]
    info_keys = None
    if(file_type=='txt'):
        fp.readline()
        info_keys=get_value(fp.readline())

    elif(file_type=='csv'):
        csv_dict_reader=DictReader(fp)
        info_keys = ':'.join(csv_dict_reader.fieldnames)

    fp.close()
    return info_keys

def save_agents_file(dict, config_obj):
    path = "web_agents.txt"
    header = "Agent Index"

    string = str(dict['Number of Agents'])+'\n'
    string += header+'\n'

    for i in range(dict['Number of Agents']):
        string +=str(i)+'\n'

    write_to_file(string,path)
    config_obj.agent_info_keys = header
    config_obj.agents_filename = path

def save_locations_file(dict, config_obj):

    if(dict['Number of Locations']<=0):
        return

    path = "web_locations.txt"
    header = "Location Index"

    string = str(dict['Number of Locations'])+'\n'
    string += header+'\n'
    for i in range(dict['Number of Locations']):
        string += dict[i]['Name']+'\n'

    write_to_file(string,path)
    config_obj.location_info_keys = header
    config_obj.locations_filename = path

def get_random_graph_lines(n,p):
    lines=[]
    for i in range(n-1):
        for j in range(i+1,n):
            if random.random()<p:
                lines.append(str(i)+':'+str(j)+'\n')
                lines.append(str(j)+':'+str(i)+'\n')
    return lines

def get_star_graph_lines(n):
    lines=[]
    for i in range(1,n):
        lines.append(str(i)+':'+str(0)+'\n')
        lines.append(str(0)+':'+str(i)+'\n')
    return lines

def save_interactions_file(dict, config_obj, n):

    if(n==0 or dict['Interaction Graph']['name']=='No Interactions'):
        return

    list_path = "web_list_interactions.txt"
    single_path = "web_single_interaction.txt"
    string = "<"+single_path+">"
    write_to_file(string, list_path)

    header = "Agent Index:Interacting Agent Index"
    p=0.0
    lines = []
    if(dict['Interaction Graph']['name']=='Random Graph'):
        p = dict['Interaction Graph']['params']['prob']
        lines = get_random_graph_lines(n,p)

    elif(dict['Interaction Graph']['name']=='Fully Connected Graph'):
        lines = get_random_graph_lines(n,1.0)

    elif(dict['Interaction Graph']['name']=='Star Graph'):
        lines = get_star_graph_lines(n)

    string = str(len(lines))+'\n'
    string += header+'\n'
    for line in lines:
        string += line

    write_to_file(string,single_path)
    config_obj.interaction_info_keys = header
    config_obj.interactions_files_list = list_path


def save_events_file(dict, config_obj, n):

    if(config_obj.locations_filename is None or n==0 or dict['Number of Events']<=0):
        return

    list_path = "web_list_events.txt"
    single_path = "web_single_event.txt"
    string = "<"+single_path+">"

    header = "Location Index:Agents"


    total_agents = list(range(n))

    num_events =0
    string2 =""
    for i in range(dict['Number of Events']):
        num = dict[i]['Number of Agents']
        name = dict[i]['Name']
        if(num>0):
            num_events+=1
        elif(num==0):
            continue

        agents_list = random.sample(total_agents, min(num,n))
        agents_list_str = [str(num) for num in agents_list]
        string2 +=name+':'+','.join(agents_list_str)+'\n'

    string1 = str(dict['Number of Events'])+'\n'
    string1 += header+'\n'
    if(num_events>0):
        string1 = str(num_events)+'\n'
        string1 += header+'\n'
        string1 += string2
        write_to_file(string,list_path)
        write_to_file(string1,single_path)
        config_obj.event_info_keys = header
        config_obj.events_files_list = list_path

####################################################################
# Retrieve list from file with list of filenames

def get_file_names_list(fileslist_filename, example_path):

    files_list = []
    if fileslist_filename=='':
        print('No files uploaded!')
    else:
        Files_obj = [Simulator.ReadFile.ReadFilesList(osp.join(example_path, file)) for file in fileslist_filename]
        files_list = [list(map(lambda x: osp.join(example_path, x), obj.file_list)) for obj in Files_obj]
        if files_list==[]:
            print('Nothing in files')

    return files_list

####################################################################
# File checking

def check_single_file(filename):
    if(not osp.isfile(filename)):
        st.info("Please upload {0}!".format(filename))
        return False
    return True

def check_files_list_list(files_list_list):
    for file in files_list_list:
        if(not check_single_file(file)):
            return False
    return True

def files_checker(config_obj):

    if(not config_obj):
        st.info("Begin by uploading the config.txt file")
        return False

    if(not osp.isfile('config.txt')):
        st.info("config.txt file has not been uploaded correctly!")
        return False

    if(not check_single_file(config_obj.agents_filename)):
        return False

    if(not check_single_file('UserModel.py')):
        return False

    if(not check_single_file('Generate_policy.py')):
        return False

    if(config_obj.interactions_files_list_list != ['']):

        if(not check_files_list_list(config_obj.interactions_files_list_list)):
            return False
        for ls in config_obj.list_interactions_files:
            for file in ls:
                if(not check_single_file(file)):
                    return False

    if(config_obj.locations_filename):
        if(not check_single_file(config_obj.locations_filename)):
            return False

    if(config_obj.events_files_list_list != ['']):
        if(not check_files_list_list(config_obj.events_files_list_list)):
            return False

        for ls in config_obj.list_events_files:
            for file in ls:
                if(not check_single_file(file)):
                    return False

    return True

####################################################################
# Examples reading and template helpers
def get_example_names_list(dir_path):
    ls = [f.path.split("/")[-1] for f in os.scandir(dir_path) if f.is_dir()]
    ls.sort()
    return ls

def get_config_path(path):
    config_filepath=osp.join(path,'config.txt')
    return config_filepath


def get_file_paths(example_path,config_obj):

    # File Names
    locations_filename = None
    events_FilesList_filename = interactions_FilesList_filename = []
    agents_filename=osp.join(example_path, config_obj.agents_filename)
    if config_obj.interactions_files_list_list != ['']:
        interactions_FilesList_filename = [osp.join(example_path, interactions_files_list) for interactions_files_list in config_obj.interactions_files_list_list]
    if config_obj.events_files_list_list != ['']:
        events_FilesList_filename = [osp.join(example_path, events_files_list) for events_files_list in config_obj.events_files_list_list]
    if config_obj.locations_filename != "":
    	locations_filename=osp.join(example_path,config_obj.locations_filename)
    return agents_filename, interactions_FilesList_filename, events_FilesList_filename, locations_filename


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
