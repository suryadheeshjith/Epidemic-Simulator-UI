import streamlit as st

class MultiPage():

    def __init__(self):
        self.pages = {}

    def add_page(self, object):
        self.pages[object.name] = object
        return object.get_defaults_dict()

    def execute_app(self, state):
        st.sidebar.write("# Navigation")
        radio = st.sidebar.radio("",list(self.pages.keys()))
        self.pages[radio].run(state)
        button = st.button("Reset to defaults")
        if(button):
            state.params[self.pages[radio].name] = self.pages[radio].get_defaults_dict()
