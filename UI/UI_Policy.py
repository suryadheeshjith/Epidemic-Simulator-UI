import streamlit as st
from UI.UI import UI_Base

def generate_policy():
    policy_list=[]

    def event_restriction_fn(agent,event_info,current_time_step):
        return False

    return policy_list,event_restriction_fn

class UI_Policy(UI_Base):
    def __init__(self):
        super().__init__()
        self.name = 'Policy'

    def get_defaults_dict(self, state):
        dict = {}
        policy_list, event_restriction_fn=generate_policy()
        dict['Policy list'] = policy_list
        dict['Event Restriction Function'] = event_restriction_fn
        return dict

    def run(self, state):
        policy_list, event_restriction_fn=generate_policy()
        state.params['Policy']['Policy list'] = policy_list
        state.params['Policy']['Event Restriction Function'] = event_restriction_fn
