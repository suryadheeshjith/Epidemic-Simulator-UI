import random
import copy
import numpy as np
import ReadFile

class Simulate():
	def __init__(self,config_obj,model,policy_list,event_restriction_fn,agents_obj,locations_obj):
		self.agents_obj=agents_obj
		self.locations_obj=locations_obj
		self.model=model
		self.policy_list=policy_list
		self.event_restriction_fn=event_restriction_fn
		self.config_obj=config_obj

	def onStartSimulation(self):

		#Intitialize state list
		self.state_list={}
		self.state_history={}
		for state in self.model.individual_state_types:
			self.state_list[state]=[]
			self.state_history[state]=[]

		#Initialize states
		self.model.initalize_states(self.agents_obj.agents)

		#Reset Policies
		for policy in self.policy_list:
			policy.reset()

		#Update State list
		for agent in self.agents_obj.agents.values():
			self.state_list[agent.state].append(agent.index)

		#Store state list
		self.store_state()

	def onStartTimeStep(self, interactionFiles_listOfList, eventFiles_listOfList, current_time_step):
		self.current_time_step=current_time_step

		for agent in self.agents_obj.agents.values():
			agent.new_time_step()

		for location in self.locations_obj.locations.values():
			location.new_time_step()

		# Initialize filenames
		interactions_filename = events_filename = None

		# Load interactions
		for interactionFiles_list in interactionFiles_listOfList:
			if interactionFiles_list != []:
				interactions_filename = interactionFiles_list[current_time_step % len(interactionFiles_list)]
				ReadFile.ReadInteractions(interactions_filename,self.config_obj,self.agents_obj)

		# Load Events
		for eventFiles_list in eventFiles_listOfList:
			if eventFiles_list != []:
				events_filename = eventFiles_list[current_time_step % len(eventFiles_list)]
				ReadFile.ReadEvents(events_filename,self.config_obj,self.locations_obj, self.agents_obj)

		#Enact policies by updating agent and location states.
		for policy in self.policy_list:
			policy.enact_policy(self.current_time_step, self.agents_obj.agents.values(), self.locations_obj.locations.values(), self.model)

		if events_filename != None:
			#Update event info to agents from location
			for location in self.locations_obj.locations.values():
				if not location.lock_down_state:
					for event_info in location.events:
						self.model.update_event_infection(event_info, location, self.agents_obj, self.current_time_step, self.event_restriction_fn)

	def handleTimeStepForAllAgents(self):
		#Too ensure concurrency we update agent.next_state in method handleTimeStepAsAgent
		#After every agent has updated next_state we update states of all agents in method handleTimeStep()

		for agent in self.agents_obj.agents.values():
			self.handleTimeStepAsAgent(agent)

		for agent in self.agents_obj.agents.values():
			self.convert_state(agent)

	def handleTimeStepAsAgent(self,agent):
		#Too ensure concurrency we update agent.next_state in method handleTimeStepAsAgent
		#After every agent has updated next_state we update states of all agents in method handleTimeStep()


		#Finding next_state
		agent.set_next_state(self.model.find_next_state(agent,self.agents_obj.agents,self.current_time_step))

	def endTimeStep(self):
		self.store_state()

	def endSimulation(self):
		return self.state_history

	def store_state(self):
		for state in self.state_history.keys():
			self.state_history[state].append(len(self.state_list[state]))

	def convert_state(self,agent):
		self.state_list[agent.state].remove(agent.index)
		agent.update_state()
		self.state_list[agent.state].append(agent.index)
