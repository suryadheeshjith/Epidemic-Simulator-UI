import sys
import pickle
import importlib.util
import os.path as osp
import streamlit as st
import Simulator.ReadFile
import Simulator.World
#from UI.MultiPage import save

def UI_Model(prev_vars):

    def module_from_file(module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def get_example_path():
        return sys.argv[1]


    def get_config_path(path):
        config_filepath=osp.join(path,'config.txt')
        return config_filepath


    def get_file_paths(example_path,config_obj):
        # File Names
        locations_filename=None
        agents_filename=osp.join(example_path,config_obj.agents_filename)
        interactions_FilesList_filename=osp.join(example_path,config_obj.interactions_files_list)
        events_FilesList_filename=osp.join(example_path,config_obj.events_files_list)
        if config_obj.locations_filename=="":
            locations_filename=None
        else:
            locations_filename=osp.join(example_path,config_obj.locations_filename)

        return agents_filename, interactions_FilesList_filename, events_FilesList_filename, locations_filename


    def get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,config_obj):
        # Reading through a file (for interactions/events) that contain file names which contain interactions and event details for a time step

        interactions_files_list=None
        events_files_list=None

        if config_obj.interactions_files_list=='':
            print('No Interaction files uploaded!')
        else:
            interactionFiles_obj=ReadFile.ReadFilesList(interactions_FilesList_filename)
            interactions_files_list=list(map(lambda x : osp.join(example_path,x) ,interactionFiles_obj.file_list))
            if interactions_files_list==[]:
                print('No Interactions inputted')


        if config_obj.events_files_list=='':
            print('No Event files uploaded!')
        else:
            eventFiles_obj=ReadFile.ReadFilesList(events_FilesList_filename)
            events_files_list=list(map(lambda x : osp.join(example_path,x) ,eventFiles_obj.file_list))
            if events_files_list==[]:
                print('No Events inputted')

        return interactions_files_list, events_files_list

    def get_model(example_path):
        UserModel = module_from_file("Generate_model", osp.join(example_path,'UserModel.py'))
        model = UserModel.UserModel()
        return model

    def get_policy(example_path):
        Generate_policy = module_from_file("Generate_policy", osp.join(example_path,'Generate_policy.py'))
        policy_list, event_restriction_fn=Generate_policy.generate_policy()
        return policy_list, event_restriction_fn



    def event_contribute_fn(agent,event_info,location,current_time_step):
            if agent.state in infected_states:
                return infectious_dict[agent.state]
            return 0

    def event_recieve_fn(agent,ambient_infection,event_info,location,current_time_step):
        #Example 1
        beta=0.1
        return ambient_infection*beta

    if __name__=="__main__":
        st.write("""
        # Agent based custom compartment model
        """)
        st.write("------------------------------------------------------------------------------------")


        no_states=st.sidebar.slider("Select number of compartments", min_value=1 , max_value=10 , value=3 , step=1 , format=None , key=None )
        no_transitions=st.sidebar.slider("Select number of transitions", min_value=0 , max_value=30 , value=2 , step=1 , format=None , key=None )

        individual_types=[]
        infected_states=[]
        state_proportion={}

        for i in range(no_states):
            st.header("Compartment "+str(i+1))
            col1, col2 = st.beta_columns(2)
            default='None'
            if i==0:
                default='Susceptible'
            if i==1:
                default='Infected'
            if i==2:
                default='Recovered'

            state = col1.text_input("Name of compartment "+str(i+1), default)
            infectious=False
            initial_prop=0
            inf_default=False
            if i==1:
                inf_default=True
            if state !='None':
                infectious = st.checkbox("Is compartment \'"+state+"\' infectious?",inf_default)
            if i==0 and no_states>1:
                val=0.99
            elif i==0 and no_states==1:
                val=1.0
            elif i==1:
                val=0.01
            else:
                val=0.0
            if state!='None':
                initial_prop = col2.slider("Intial proportion of \'"+state+"\'", min_value=0.0 , max_value=1.0 , value=val , step=0.01 , format=None , key=None )

            if state!='None':
                individual_types.append(state)
                if infectious:
                    infected_states.append(state)
                state_proportion[state]=initial_prop

        st.write("------------------------------------------------------------------------------------")


        infectious_dict={}
        model = Model.StochasticModel(individual_types,infected_states,state_proportion)
        for i in range(no_transitions):
            st.header("Transition "+str(i+1))
            def_bool=False
            if i==0 and infected_states!=[]:
                def_bool=True
            p_infection = st.checkbox("Does transition "+str(i+1)+" depend on infectious states?",def_bool)
            col1, col2, col3 = st.beta_columns(3)
            def_s1=def_s2=0
            if i==0 and no_states>1:
                def_s1=0
                def_s2=1
            if i==1 and no_states>2:
                def_s1=1
                def_s2=2
            state1 = col1.selectbox("Initial compartment for transition "+str(i+1),individual_types,index=def_s1)
            state2 = col2.selectbox("Final compartment for transition "+str(i+1),individual_types,index=def_s2)
            G.add_edge(state1, state2)
            if p_infection:
                l=[]
                for istate in infected_states:
                    l.append(None)
                    infectious_dict[istate]=float(col3.text_input("Rate of infection from compartment "+istate+ " for transition "+str(i+1), 0.01))
                model.set_transition(state1, state2, model.p_infection(l,None))
            else:
                rate=float(col3.text_input("Rate constant for transition "+str(i+1), 0.03))
                model.set_transition(state1, state2, model.p_standard(rate))

        model.set_event_contribution_fn(event_contribute_fn)
        model.set_event_recieve_fn(event_recieve_fn)






        example_path = get_example_path()
        config_filename = get_config_path(example_path)

        # Read Config file using ReadFile.ReadConfiguration
        config_obj=ReadFile.ReadConfiguration(config_filename)

        agents_filename, interactions_FilesList_filename,\
        events_FilesList_filename, locations_filename = get_file_paths(example_path,config_obj)
        interactions_files_list, events_files_list = get_file_names_list(example_path,interactions_FilesList_filename,events_FilesList_filename,config_obj)

        # User Model and Policy
        model = get_model(example_path)
        policy_list, event_restriction_fn=get_policy(example_path)

        # Creation of World object
        world_obj=World.World(config_obj,model,policy_list,event_restriction_fn,agents_filename,interactions_files_list,locations_filename,events_files_list)
        world_obj.simulate_worlds()
