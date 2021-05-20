import sys
import pickle
import importlib.util
import os.path as osp
import streamlit as st
import Simulator.ReadFile
import Simulator.World
from UI.UI import UI_Base

def event_contribute_fn(agent,event_info,location,current_time_step):
        if agent.state in infected_states:
            return infectious_dict[agent.state]
        return 0

def event_recieve_fn(agent,ambient_infection,event_info,location,current_time_step):
    #Example 1
    beta=0.1
    return ambient_infection*beta

class UI_Model(UI_Base):
    def __init__(self):
        super().__init__()
        self.name = 'Model'

    def get_defaults_dict(self):
        dict = {}
        dict['model'] = None
        dict['Number of compartments']
        return dict

    def run(self, state):
        no_states=st.sidebar.slider("Select number of compartments",1,10,=3,1)
        no_transitions=st.sidebar.slider("Select number of transitions",0,3,=2,1)

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
