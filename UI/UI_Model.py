import sys
import pickle
import importlib.util
import os.path as osp
import streamlit as st
import Simulator.ReadFile
import Simulator.World
import Simulator.Model as Model
from UI.UI import UI_Base

class UI_Model(UI_Base):
    def __init__(self):
        super().__init__()
        self.name = 'Model'

    def get_defaults_dict(self, state):
        dict = {}
        dict['Number of compartments'] = 3
        dict['Number of transitions'] = 2
        dict['compartments'] = {}
        dict['compartments'][0] = {'name':'Susceptible','infectious':False,'initial_prop':0.99}
        dict['compartments'][1] = {'name':'Infected','infectious':True,'initial_prop':0.01}
        dict['compartments'][2] = {'name':'Recovered','infectious':False,'initial_prop':0.0}
        dict['transitions'] = {}
        dict['transitions'][0] = {'depends_infectious':True, 'initial_index':0, 'final_index':1, 'normal_rate':0.03, 'infectious_rate':{'Infected':0.01}}
        dict['transitions'][1] = {'depends_infectious':False, 'initial_index':1, 'final_index':2, 'normal_rate':0.03, 'infectious_rate':{'Infected':0.01}}
        dict['model'] = self.get_model(dict)
        return dict


    def run(self, state):
        state.params[self.name]['Number of compartments']=st.slider("Select number of compartments",1,10,\
                                                                state.params[self.name]['Number of compartments'],1)
        state.params[self.name]['Number of transitions']=st.slider("Select number of transitions",0,30,\
                                                                state.params[self.name]['Number of transitions'],1)

        for i in range(state.params[self.name]['Number of compartments']):
            st.header("Compartment "+str(i+1))
            col1, col2 = st.beta_columns(2)
            name = None

            try:
                cur_dict = state.params[self.name]['compartments'][i]
            except:
                state.params[self.name]['compartments'][i] = {'name':None,'infectious':False,'initial_prop':0.0}
                cur_dict = state.params[self.name]['compartments'][i]

            cur_dict['name'] = col1.text_input("Name of compartment "+str(i+1), cur_dict['name'])

            if cur_dict['name'] !='None':
                cur_dict['infectious'] = st.checkbox("Is compartment \'"+cur_dict['name']+"\' infectious?",cur_dict['infectious'])

            if cur_dict['name']!='None':
                cur_dict['initial_prop'] = col2.slider("Intial proportion of \'"+cur_dict['name']+"\'",0.0,1.0,cur_dict['initial_prop'],0.01)


        st.write("------------------------------------------------------------------------------------")
        individual_types, infected_states, state_proportion = self.get_model_parameters(state.params[self.name])
        for i in range(state.params[self.name]['Number of transitions']):
            st.header("Transition "+str(i+1))
            try:
                cur_dict = state.params[self.name]['transitions'][i]
            except:
                state.params[self.name]['transitions'][i] = {'depends_infectious':False,'initial_index':0,'final_index':0,'normal_rate':0.03,'infectious_rate':{}}
                cur_dict = state.params[self.name]['transitions'][i]

            cur_dict['depends_infectious'] = st.checkbox("Does transition "+str(i+1)+" depend on infectious states?",cur_dict['depends_infectious'])

            col1, col2, col3 = st.beta_columns(3)

            name1 = col1.selectbox("Initial compartment for transition "+str(i+1),individual_types,index=cur_dict['initial_index'])
            name2 = col2.selectbox("Final compartment for transition "+str(i+1),individual_types,index=cur_dict['final_index'])

            for j in range(state.params[self.name]['Number of compartments']):
                if(name1==state.params[self.name]['compartments'][j]['name']):
                    cur_dict['initial_index'] = j
                elif(name2==state.params[self.name]['compartments'][j]['name']):
                    cur_dict['final_index'] = j

            if cur_dict['depends_infectious']:
                for istate in infected_states:
                    try:
                        cur_dict['infectious_rate'][istate] = float(col3.text_input("Rate of infection from compartment "+istate+ " for transition "+str(i+1),cur_dict['infectious_rate'][istate]))
                    except:
                        cur_dict['infectious_rate'][istate] = 0.01
                        cur_dict['infectious_rate'][istate] = float(col3.text_input("Rate of infection from compartment "+istate+ " for transition "+str(i+1),cur_dict['infectious_rate'][istate]))
            else:
                cur_dict['normal_rate']=float(col3.text_input("Rate constant for transition "+str(i+1),cur_dict['normal_rate']))

        state.params[self.name]['model'] = self.get_model(state.params[self.name])

    def get_model_parameters(self,dict):

        individual_types=[]
        infected_states=[]
        state_proportion={}
        for i in range(dict['Number of compartments']):
            cur_dict = dict['compartments'][i]
            if cur_dict['name']!='None':
                individual_types.append(cur_dict['name'])
                if cur_dict['infectious']:
                    infected_states.append(cur_dict['name'])
                state_proportion[cur_dict['name']]=cur_dict['initial_prop']

        return individual_types, infected_states, state_proportion

    def set_transitions(self, model, dict, infected_states):
        self.infectious_dict={}
        for i in range(dict['Number of transitions']):
            cur_dict = dict['transitions'][i]

            initial_state = dict['compartments'][cur_dict['initial_index']]['name']
            final_state = dict['compartments'][cur_dict['final_index']]['name']

            if cur_dict['depends_infectious']:
                l=[]
                for istate in infected_states:
                    l.append(None)
                    self.infectious_dict[istate] = cur_dict['infectious_rate'][istate]
                model.set_transition(initial_state, final_state, model.p_infection(l,None))

            else:
                model.set_transition(initial_state, final_state, model.p_standard(cur_dict['normal_rate']))


    def get_model(self,dict):

        individual_types, infected_states, state_proportion = self.get_model_parameters(dict)
        model = Model.StochasticModel(individual_types,infected_states,state_proportion)
        self.set_transitions(model,dict,infected_states)
        model.set_event_contribution_fn(self.event_contribute_fn)
        model.set_event_recieve_fn(self.event_recieve_fn)

        return model

    def event_contribute_fn(agent,event_info,location,current_time_step):
            if agent.state in infected_states:
                return self.infectious_dict[agent.state]
            return 0

    def event_recieve_fn(agent,ambient_infection,event_info,location,current_time_step):
        beta=0.1
        return ambient_infection*beta
