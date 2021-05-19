import streamlit as st
from UI.MultiPage import save

def generate_policy():
	policy_list=[]

	def event_restriction_fn(agent,event_info,current_time_step):
		return False

	return policy_list,event_restriction_fn


policy_list, event_restriction_fn=generate_policy()
