import streamlit as st
from UI.UI import UI_Base

class UI_Environment(UI_Base):
    def __init__(self):
        super().__init__()
        self.name = 'Environment'

    def get_defaults_dict(self, state):
        dict = {}
        dict['Agents'] = {'Number of Agents':300}
        dict['Interactions'] = {'Interaction Graph':{'index':1, 'name': 'Random Graph','params':{'prob':0.01}}}
        dict['Locations'] = {}
        dict['Locations']['Number of Locations'] = 2
        dict['Locations'][0] = {'Name':'0'}
        dict['Locations'][1] = {'Name':'1'}
        dict['Events'] = {}
        dict['Events']['Number of Events'] = 1
        dict['Events'][0] = {'Number of Agents':10, 'Location Index':0, 'Name':'0'}
        return dict

    def get_list_of_locations(self, dict):
        ls = []
        for i in range(dict['Number of Locations']):
            if(dict[i]['Name'] and dict[i]['Name'] not in ls):
                ls.append(dict[i]['Name'])
        return ls

    def run(self, state):
        dict = state.params[self.name]
        st.markdown("#### Agents")
        dict['Agents']['Number of Agents']=st.slider("Select number of agents",0,1000,dict['Agents']['Number of Agents'],10)

        st.markdown("#### Interaction Graph")
        if(dict['Agents']['Number of Agents']==0):
            st.markdown("There are no agents!")
        else:
            list_of_graphs = ['No Interactions', 'Random Graph', 'Fully Connected Graph']
            name_of_graph=st.selectbox("Select interaction graph",list_of_graphs,dict['Interactions']['Interaction Graph']['index'])

            if(name_of_graph == 'No Interactions'):
                dict['Interactions']['Interaction Graph']['index'] = 0
                dict['Interactions']['Interaction Graph']['name'] = 'No Interactions'
                dict['Interactions']['Interaction Graph']['params']['prob']=0.0

            elif(name_of_graph == 'Random Graph'):
                dict['Interactions']['Interaction Graph']['index'] = 1
                dict['Interactions']['Interaction Graph']['name'] = 'Random Graph'
                dict['Interactions']['Interaction Graph']['params']['prob'] = st.slider("Select probability of interaction",0.0,1.0,dict['Interactions']['Interaction Graph']['params']['prob'],0.01)

            elif(name_of_graph == 'Fully Connected Graph'):
                dict['Interactions']['Interaction Graph']['index'] = 2
                dict['Interactions']['Interaction Graph']['name'] = 'Fully Connected Graph'
                dict['Interactions']['Interaction Graph']['params']['prob'] = 0.0

        st.markdown("#### Locations")
        dict['Locations']['Number of Locations'] = st.slider("Select number of locations",0,10,dict['Locations']['Number of Locations'],1)
        for i in range(dict['Locations']['Number of Locations']):
            try:
                cur_dict = dict['Locations'][i]
            except:
                dict['Locations'][i] = {'Name':str(i)}
                cur_dict = dict['Locations'][i]

            cur_dict['Name'] = st.text_input("Name of Location "+str(i+1), cur_dict['Name'])

        st.markdown("#### Events")
        if(dict['Agents']['Number of Agents']==0):
            st.markdown("There are no agents!")
        elif(dict['Locations']['Number of Locations']==0):
            st.markdown("Add Locations to add Events!")
        else:
            dict['Events']['Number of Events'] = st.slider("Select number of events",0,10,dict['Events']['Number of Events'],1)
            for i in range(dict['Events']['Number of Events']):
                try:
                    cur_dict = dict['Events'][i]
                except:
                    dict['Events'][i] = {'Number of Agents':0, 'Location Index':0, 'Name':None}
                    cur_dict = dict['Events'][i]
                cur_dict['Number of Agents'] = st.slider("Select number of agents for Event"+str(i+1),0,dict['Agents']['Number of Agents'],min(cur_dict['Number of Agents'],dict['Agents']['Number of Agents']),1,key=i)
                list_locations = self.get_list_of_locations(dict['Locations'])
                try:
                    name_of_location=st.selectbox("Select location for Event"+str(i+1),list_locations,cur_dict['Location Index'])
                except:
                    name_of_location=st.selectbox("Select location for Event"+str(i+1),list_locations,0)

                for j in range(dict['Locations']['Number of Locations']):
                    if(dict['Locations'][j]['Name']==name_of_location):
                        cur_dict['Location Index'] = j
                        cur_dict['Name'] = name_of_location
