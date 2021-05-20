import streamlit as st

class MultiPage():

    def __init__(self):
        self.pages = {}

    def add_page(self, object, state):
        self.pages[object.name] = object
        return object.get_defaults_dict(state)

    def execute_app(self, state):
        st.sidebar.markdown("# :hammer_and_pick: Navigation")
        radio = st.sidebar.radio("",list(self.pages.keys()))
        str_header = "### "+self.pages[radio].name
        st.markdown(str_header)
        self.pages[radio].run(state)
        if(self.pages[radio].requires_reset):
            button = st.button("Reset to defaults")
            if(button):
                state.params[self.pages[radio].name] = self.pages[radio].get_defaults_dict(state)
