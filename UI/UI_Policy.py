import streamlit as st
from UI.UI import UI_Base
from Utils.file_utils import get_policy_from_file, write_to_file
import Simulator.Testing_Policy as Testing_Policy
import Simulator.Lockdown_Policy as Lockdown_Policy
import Simulator.Vaccination_policy as Vaccination_policy

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
        dict['Input Mode'] = {'index':0, 'name':'Website', 'filename':None}
        dict['Number of Testing Policies'] = 0
        dict['Number of Vaccination Policies'] = 0
        dict['Testing'] = {}
        dict['Vaccination'] = {}

        policy_list, event_restriction_fn=generate_policy()
        dict['Policy list'] = policy_list
        dict['Event Restriction Function'] = event_restriction_fn
        return dict

    def run(self, state):
        dict = state.params[self.name]
        input_options = ['Website', 'Upload File']

        option = st.radio("Choose input mode", input_options, dict['Input Mode']['index'], key = "Policy")

        if(option == input_options[0]):
            dict['Input Mode']['index'] = 0
            dict['Input Mode']['name'] = option

            dict['Number of Testing Policies']=st.slider("Select number of testing policies",0,10,\
                                                                    dict['Number of Testing Policies'],1)
            dict['Number of Vaccination Policies']=st.slider("Select number of vaccination policies",0,10,\
                                                                    dict['Number of Vaccination Policies'],1)
            self.test_policy_ui(dict)
            st.write("---")
            self.vaccine_policy_ui(dict)
            dict['Policy list'], dict['Event Restriction Function'] = self.get_policy_items(dict)

        elif(option == input_options[1]):
            dict['Input Mode']['index'] = 1
            dict['Input Mode']['name'] = option

            file = st.file_uploader("Upload Policy file")
            if(file is not None):
                if(file.name == "Generate_policy.py"):
                    string = file.getvalue().decode("utf-8")
                    write_to_file(string, file.name)
                    dict['Input Mode']['filename'] = file.name
                else:
                    st.error("""
                            Given File : {0}  Required File : {1}
                            """.format(file.name,"Generate_policy.py"))
                    dict['Input Mode']['filename'] = None

            if(dict['Input Mode']['filename']):
                st.info("Saved {0}!".format(dict['Input Mode']['filename']))
            if(dict['Input Mode']['filename'] == "Generate_policy.py"):
                dict['Policy list'], dict['Event Restriction Function'] = get_policy_from_file('')

    def test_policy_ui(self, dict):
        if(dict['Number of Testing Policies']):
            st.markdown("<ins>Testing parameters</ins>", unsafe_allow_html=True)

        for j in range(dict['Number of Testing Policies']):
            st.write("Testing policy {0}".format(j+1))
            try:
                cur_dict = dict['Testing'][j]
            except:
                # dict['Testing'][j] = {'machines':{},'testing_methods_list':{"Normal Testing":{}, "Group Testing":{"napt":1,"ntpa":1}, "Friendship Testing":{'min_days':5}},\
                #                     'test_option':"Normal Testing", 'test_option_index':0, 'num_days_lockdown':5, 'num_agents_per_step':100, 'num_distinct_tests':1}
                dict['Testing'][j] = {'machines':{},'testing_methods_list':{"Normal Testing":{}, "Group Testing":{"napt":1,"ntpa":1}},\
                                    'test_option':"Normal Testing", 'test_option_index':0, 'num_days_lockdown':5, 'num_agents_per_step':100, 'num_distinct_tests':1}
                cur_dict = dict['Testing'][j]

            cur_dict['num_agents_per_step'] = st.slider("Number of Agents to test every day",0,1000,cur_dict['num_agents_per_step'],10,key=j)
            cur_dict['num_distinct_tests'] = st.slider("Number of distinct tests",0,10,cur_dict['num_distinct_tests'],1,key=j)

            for i in range(cur_dict['num_distinct_tests']):
                st.text("Test Type {0}".format(i+1))
                try:
                    cur_dict_i = cur_dict['machines']['Test'+str(i+1)]
                except:
                    cur_dict['machines']['Test'+str(i+1)] = {'cost':1, 'false_positive_rate':0.0, 'false_negative_rate':0.0,'turnaround_time':0,'capacity':20}
                    cur_dict_i = cur_dict['machines']['Test'+str(i+1)]

                cur_dict_i['cost'] = st.slider("Cost of test",1,1000,cur_dict_i['cost'],1,key=(j,i))
                cur_dict_i['false_positive_rate']=st.slider("False Positive Rate",0.0,1.0,cur_dict_i['false_positive_rate'],0.01,key=(j,i))
                cur_dict_i['false_negative_rate']=st.slider("False Negative Rate",0.0,1.0,cur_dict_i['false_negative_rate'],0.01,key=(j,i))
                cur_dict_i['turnaround_time']=st.slider("Turnaround time (Steps for the test to complete)",0,100,cur_dict_i['turnaround_time'],1,key=(j,i))
                cur_dict_i['capacity']=st.slider("Maximum tests done by Test {0} per day".format(i+1),1,1000,cur_dict_i['capacity'],1,key=(j,i))

            if(cur_dict['num_distinct_tests']):
                test_option = st.radio('Choose Testing Method',list(dict['Testing'][i]['testing_methods_list'].keys()),cur_dict['test_option_index'],key=j)

                if(test_option=="Normal Testing"):
                    cur_dict['test_option_index'] = 0
                    cur_dict['test_option'] = test_option
                    cur_dict['testing_methods_list'][test_option] = True

                elif(test_option=="Group Testing"):
                    cur_dict['test_option_index'] = 1
                    cur_dict['test_option'] = test_option
                    cur_dict['testing_methods_list'][test_option]["napt"] = st.slider("Number of agents per test",1,15,cur_dict['testing_methods_list'][test_option]["napt"],1,key=j)
                    cur_dict['testing_methods_list'][test_option]["ntpa"] = st.slider("Number of tests per agent",1,15,cur_dict['testing_methods_list'][test_option]["ntpa"],1,key=j)

                elif(test_option=="Friendship Testing"):
                    cur_dict['test_option_index'] = 2
                    cur_dict['test_option'] = test_option
                    cur_dict['testing_methods_list'][test_option]["min_days"] = st.slider("Minimum days for agent to test again",1,100,cur_dict['testing_methods_list'][test_option]["min_days"],1,key=j)

                st.write("Lockdown parameters")
                cur_dict['num_days_lockdown'] = st.slider("Number of days to lockdown agent when tested positive",0,100,cur_dict['num_days_lockdown'],1,key=j)
            else:
                no_tests_text = st.empty()
                no_tests_text.text("No testing done!")

    def update_test_policy(self, dict, policy_list):
        for j in range(dict['Number of Testing Policies']):
            cur_dict = dict['Testing'][j]
            if(cur_dict['machines']):
                testing_policy = Testing_Policy.Test_Policy(lambda x:cur_dict['num_agents_per_step'])
                for machine in cur_dict['machines'].keys():
                    testing_policy.add_machine(machine,cur_dict['machines'][machine]["cost"],cur_dict['machines'][machine]["false_positive_rate"],\
                                                    cur_dict['machines'][machine]["false_negative_rate"],cur_dict['machines'][machine]["turnaround_time"],cur_dict['machines'][machine]["capacity"])

                test_option = cur_dict['test_option']
                if(test_option=="Normal Testing"):
                    testing_policy.set_register_agent_testtube_func(testing_policy.random_agents(1,1))

                elif(test_option=="Group Testing"):
                    num_agents_per_test = cur_dict['testing_methods_list'][test_option]['napt']
                    num_tests_per_agent = cur_dict['testing_methods_list'][test_option]['ntpa']
                    testing_policy.set_register_agent_testtube_func(testing_policy.random_agents(num_agents_per_test,num_tests_per_agent))

                elif(test_option=="Friendship Testing"):
                    min_days = cur_dict['testing_methods_list'][test_option]['min_days']
                    testing_policy.set_register_agent_testtube_func(testing_policy.friendship_testing(min_days))


                lockdown_policy = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:True,cur_dict['num_days_lockdown'])

                policy_list.append(testing_policy)
                policy_list.append(lockdown_policy)


    def vaccine_policy_ui(self, dict):
        if(dict['Number of Vaccination Policies']):
            st.markdown("<ins>Vaccination parameters</ins>", unsafe_allow_html=True)

        for j in range(dict['Number of Vaccination Policies']):
            st.write("Vaccination policy {0}".format(j+1))
            try:
                cur_dict = dict['Vaccination'][j]
            except:
                dict['Vaccination'][j] = {'available_vaccines':{}, 'num_agents_per_step':100, 'num_vaccine_types':1}
                cur_dict = dict['Vaccination'][j]

            st.write("Vaccination parameters")
            cur_dict['num_agents_per_step']=st.slider("Number of Agents to vaccinate every day",0,1000,cur_dict['num_agents_per_step'],10,key=j)
            cur_dict['num_vaccine_types']=st.slider("Number of distinct vaccines",0,10,cur_dict['num_vaccine_types'],1,key=j)

            for i in range(cur_dict['num_vaccine_types']):
                try:
                    cur_dict_i = cur_dict['available_vaccines']['Vaccine'+str(i+1)]
                except:
                    cur_dict['available_vaccines']['Vaccine'+str(i+1)] = {'cost':1,'decay':1,'efficacy':1.0,'quantity':1}
                    cur_dict_i = cur_dict['available_vaccines']['Vaccine'+str(i+1)]

                st.text("Vaccine Type {0}".format(i+1))
                cur_dict_i['cost'] = st.slider("Cost of each vaccine",1,1000,cur_dict_i['cost'],1,key=(j,i))
                cur_dict_i['decay'] = st.slider("Decay days of each vaccine",1,100,cur_dict_i['decay'],1,key=(j,i))
                cur_dict_i['efficacy'] = st.slider("Efficacy of vaccine",0.0,1.0,cur_dict_i['efficacy'],0.1,key=(j,i))
                cur_dict_i['quantity'] = st.slider("Quantity of vaccines per day",1,1000,cur_dict_i['quantity'],1,key=(j,i))

    def update_vaccine_policy(self, dict, policy_list):
        for j in range(dict['Number of Vaccination Policies']):
            cur_dict = dict['Vaccination'][j]

            vaccinating_policy = Vaccination_policy.Vaccination_policy(lambda x:cur_dict['num_agents_per_step'])
            for vaccine in cur_dict['available_vaccines'].keys():
                vaccinating_policy.add_vaccination(vaccine,cur_dict['available_vaccines'][vaccine]['cost'],
                                                        cur_dict['available_vaccines'][vaccine]['decay'],cur_dict['available_vaccines'][vaccine]['efficacy'],
                                                        cur_dict['available_vaccines'][vaccine]['quantity'])
            policy_list.append(vaccinating_policy)

    def get_policy_items(self, dict):
        policy_list, event_restriction_fn = generate_policy()
        self.update_test_policy(dict,policy_list)
        self.update_vaccine_policy(dict,policy_list)
        return policy_list, event_restriction_fn
