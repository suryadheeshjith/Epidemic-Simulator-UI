import streamlit as st
#from UI.MultiPage import save

def UI_Agents(prev_vars):
	def write_agents(filename,n):
		header='Agent Index'

		f=open(filename,'w')
		f.write(str(n)+'\n')
		f.write(header+'\n')

		for i in range(n):
			f.write(str(i)+'\n')

	config_obj = prev_vars[0]
	file_name = 'agents.txt'
	config_obj.agents_filename = file_name
	no_agents=st.slider("Select number of agents", min_value=0 , max_value=1000 , value=300 , step=10 , format=None , key=None )
	write_agents(config_obj.agents_filename,no_agents)
	save(var_list=[config_obj,no_agents], name="Agents", page_names=["Events"])
