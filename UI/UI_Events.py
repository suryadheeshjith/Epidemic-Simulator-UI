import streamlit as st
#from UI.MultiPage import save

def UI_Events(prev_vars):
	def write_events(filename,no_locations,no_agents):
		info_dict={}
		#ID enumerates from 0 to n-1
		header='Location Index:Agents'

		f=open(filename,'w')
		f.write(str(1)+'\n')
		f.write(header+'\n')

		line=str(0)+':'
		for i in range(no_agents):
			line+=str(i)
			if i!=no_agents-1:
				line+=','

		f.write(line)

	no_agents = prev_vars[1]
	events_fileslist_filename = "all_events.txt"
	events_list = []
	write_events('one_event.txt',1,no_agents)
