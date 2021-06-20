import streamlit as st
from UI.UI import UI_Base
from Utils.file_utils import write_to_file, get_file_names_list
from Utils.streamlit_utils import display_interaction_graph

class UI_Environment(UI_Base):
    def __init__(self):
        super().__init__()
        self.name = 'Environment'

    def get_defaults_dict(self, state):
        dict = {}
        dict['Agents'] = {}
        dict['Agents']['Number of Agents'] = 100
        dict['Agents']['Input Mode'] = {'index':0, 'name':'Website', 'filename':None}
        dict['Interactions'] = {}
        dict['Interactions']['Interaction Graph'] = {'index':1, 'name': 'Random Graph','params':{'prob':0.01}}
        dict['Interactions']['Input Mode'] = {'index':0, 'name':'Website', 'list_filename':None, 'single_filenames':[]}
        dict['Locations'] = {}
        dict['Locations']['Number of Locations'] = 2
        dict['Locations'][0] = {'Name':'0'}
        dict['Locations'][1] = {'Name':'1'}
        dict['Locations']['Input Mode'] = {'index':0, 'name':'Website', 'filename':None}
        dict['Events'] = {}
        dict['Events']['Number of Events'] = 1
        dict['Events'][0] = {'Number of Agents':10, 'Location Index':0, 'Name':'0'}
        dict['Events']['Input Mode'] = {'index':0, 'name':'Website', 'list_filename':None, 'single_filenames':[]}
        return dict

    def get_list_of_locations(self, dict):
        ls = []
        for i in range(dict['Number of Locations']):
            if(dict[i]['Name'] and dict[i]['Name'] not in ls):
                ls.append(dict[i]['Name'])
        return ls

    def run(self, state):
        input_options = ['Website', 'Upload File']
        dict = state.params[self.name]
        self.run_agents(dict,input_options)
        self.run_interactions(dict,input_options)
        display_interaction_graph(dict['Agents']['Number of Agents'],state.params['Environment'])
        self.run_locations(dict,input_options)
        self.run_events(dict,input_options)

    def run_agents(self, dict, input_options):
        st.markdown("#### Agents")
        cur_dict = dict['Agents']
        option = st.radio("Choose input mode", input_options, cur_dict['Input Mode']['index'], key = "Agents")
        if(option == input_options[0]):
            cur_dict['Input Mode']['index'] = 0
            cur_dict['Input Mode']['name'] = option
            cur_dict['Number of Agents']=st.slider("Select number of agents",0,1000,cur_dict['Number of Agents'],10)

        elif(option == input_options[1]):
            cur_dict['Input Mode']['index'] = 1
            cur_dict['Input Mode']['name'] = option
            file = st.file_uploader("Upload agents file")
            if(file is not None):
                string = file.getvalue().decode("utf-8")
                write_to_file(string, file.name)
                cur_dict['Input Mode']['filename'] = file.name
            if(cur_dict['Input Mode']['filename']):
                st.info("Saved {0}!".format(cur_dict['Input Mode']['filename']))

    def run_interactions(self, dict, input_options):
        st.markdown("#### Interactions")
        if(dict['Agents']['Number of Agents']==0):
            st.info("There are no agents!")
        else:
            cur_dict = dict['Interactions']
            option = st.radio("Choose input mode", input_options, cur_dict['Input Mode']['index'], key = "Interactions")
            if(option == input_options[0]):
                cur_dict['Input Mode']['index'] = 0
                cur_dict['Input Mode']['name'] = option

                list_of_graphs = ['No Interactions', 'Random Graph', 'Fully Connected Graph', 'Star Graph']
                name_of_graph=st.selectbox("Select interaction graph",list_of_graphs,cur_dict['Interaction Graph']['index'])

                if(name_of_graph == 'No Interactions'):
                    cur_dict['Interaction Graph']['index'] = 0
                    cur_dict['Interaction Graph']['name'] = 'No Interactions'
                    cur_dict['Interaction Graph']['params']['prob']=0.0

                elif(name_of_graph == 'Random Graph'):
                    cur_dict['Interaction Graph']['index'] = 1
                    cur_dict['Interaction Graph']['name'] = 'Random Graph'
                    cur_dict['Interaction Graph']['params']['prob'] = st.slider("Select probability of interaction",0.0,1.0,\
                                                                        cur_dict['Interaction Graph']['params']['prob'],0.01)

                elif(name_of_graph == 'Fully Connected Graph'):
                    cur_dict['Interaction Graph']['index'] = 2
                    cur_dict['Interaction Graph']['name'] = 'Fully Connected Graph'
                    cur_dict['Interaction Graph']['params']['prob'] = 0.0

                elif(name_of_graph == 'Star Graph'):
                    cur_dict['Interaction Graph']['index'] = 3
                    cur_dict['Interaction Graph']['name'] = 'Star Graph'
                    cur_dict['Interaction Graph']['params']['prob'] = None

            elif(option == input_options[1]):
                cur_dict['Input Mode']['index'] = 1
                cur_dict['Input Mode']['name'] = option

                file = st.file_uploader("Upload Interactions list file")
                if(file is not None):
                    string = file.getvalue().decode("utf-8")
                    write_to_file(string, file.name)
                    cur_dict['Input Mode']['list_filename'] = file.name
                    list_interactions_files = get_file_names_list([file.name], '')[0]

                    if(not list_interactions_files):
                        st.error("Could not read any interaction files!")
                        cur_dict['Input Mode']['list_filename'] = None
                        cur_dict['Input Mode']['single_filenames'] = []
                    else:
                        cur_dict['Input Mode']['list_filename'] = file.name

                    for file_name in list_interactions_files:
                        f = st.file_uploader("Upload File name : {0}".format(file_name))
                        if(f is not None):
                            if(f.name == file_name):
                                string = f.getvalue().decode("utf-8")
                                write_to_file(string, file_name)
                                cur_dict['Input Mode']['single_filenames'].append(f.name)
                            else:
                                st.error("""
                                        Given File : {0}  Required File : {1}
                                        """.format(f.name,file_name))

                if(cur_dict['Input Mode']['list_filename']):
                    st.info("Saved {0}!".format(cur_dict['Input Mode']['list_filename']))

                if(cur_dict['Input Mode']['single_filenames']):
                    st.info("Saved {0}!".format(set(cur_dict['Input Mode']['single_filenames'])))

    def run_locations(self,dict,input_options):
        st.markdown("#### Locations")
        cur_dict = dict['Locations']
        option = st.radio("Choose input mode", input_options, cur_dict['Input Mode']['index'], key = "Locations")


        if(option == input_options[0]):
            cur_dict['Input Mode']['index'] = 0
            cur_dict['Input Mode']['name'] = option

            cur_dict['Number of Locations'] = st.slider("Select number of locations",0,10,cur_dict['Number of Locations'],1)
            for i in range(cur_dict['Number of Locations']):
                try:
                    cur_dict_i = cur_dict[i]
                except:
                    cur_dict[i] = {'Name':str(i)}
                    cur_dict_i = cur_dict[i]

                cur_dict_i['Name'] = st.text_input("Name of Location "+str(i+1), cur_dict_i['Name'])

        elif(option == input_options[1]):
            cur_dict['Input Mode']['index'] = 1
            cur_dict['Input Mode']['name'] = option

            file = st.file_uploader("Upload locations file")
            if(file is not None):
                string = file.getvalue().decode("utf-8")
                write_to_file(string, file.name)
                cur_dict['Input Mode']['filename'] = file.name
            if(cur_dict['Input Mode']['filename']):
                st.info("Saved {0}!".format(cur_dict['Input Mode']['filename']))

    def run_events(self,dict,input_options):
        st.markdown("#### Events")
        if(dict['Agents']['Number of Agents']==0):
            st.info("There are no agents!")
        elif(dict['Locations']['Number of Locations']==0):
            st.info("Add Locations to add Events!")
        else:
            cur_dict = dict['Events']
            option = st.radio("Choose input mode", input_options, cur_dict['Input Mode']['index'], key = "Events")
            if(option == input_options[0]):
                cur_dict['Input Mode']['index'] = 0
                cur_dict['Input Mode']['name'] = option

                cur_dict['Number of Events'] = st.slider("Select number of events",0,10,cur_dict['Number of Events'],1)
                for i in range(cur_dict['Number of Events']):
                    try:
                        cur_dict_i = cur_dict[i]
                    except:
                        cur_dict[i] = {'Number of Agents':0, 'Location Index':0, 'Name':None}
                        cur_dict_i = cur_dict[i]

                    cur_dict_i['Number of Agents'] = st.slider("Select number of agents for Event"+str(i+1),0,dict['Agents']['Number of Agents'],min(cur_dict_i['Number of Agents'],dict['Agents']['Number of Agents']),1,key=i)
                    list_locations = self.get_list_of_locations(dict['Locations'])
                    try:
                        name_of_location=st.selectbox("Select location for Event"+str(i+1),list_locations,cur_dict_i['Location Index'])
                    except:
                        name_of_location=st.selectbox("Select location for Event"+str(i+1),list_locations,0)

                    for j in range(dict['Locations']['Number of Locations']):
                        if(dict['Locations'][j]['Name']==name_of_location):
                            cur_dict_i['Location Index'] = j
                            cur_dict_i['Name'] = name_of_location

            elif(option == input_options[1]):
                cur_dict['Input Mode']['index'] = 1
                cur_dict['Input Mode']['name'] = option

                file = st.file_uploader("Upload Events list file")
                if(file is not None):
                    string = file.getvalue().decode("utf-8")
                    write_to_file(string, file.name)
                    list_events_files = get_file_names_list([file.name], '')[0]

                    if(not list_events_files):
                        st.error("Could not read any event files!")
                        cur_dict['Input Mode']['list_filename'] = None
                        cur_dict['Input Mode']['single_filenames'] = []
                    else:
                        cur_dict['Input Mode']['list_filename'] = file.name

                    for file_name in list_events_files:
                        f = st.file_uploader("Upload File name : {0}".format(file_name))
                        if(f is not None):
                            if(f.name == file_name):
                                string = f.getvalue().decode("utf-8")
                                write_to_file(string, file_name)
                                cur_dict['Input Mode']['single_filenames'].append(f.name)
                            else:
                                st.error("""
                                        Given File : {0}  Required File : {1}
                                        """.format(f.name,file_name))

                if(cur_dict['Input Mode']['list_filename']):
                    st.info("Saved {0}!".format(cur_dict['Input Mode']['list_filename']))

                if(cur_dict['Input Mode']['single_filenames']):
                    st.info("Saved {0}!".format(set(cur_dict['Input Mode']['single_filenames'])))
