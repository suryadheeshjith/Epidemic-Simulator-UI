import streamlit as st
from UI.UI import UI_Base

class UI_Events(UI_Base):
    def __init__(self):
        pass

    def run(self,state):
        events_fileslist_filename = "all_events.txt"
        events_list = []
        write_events('one_event.txt',1,no_agents)

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
