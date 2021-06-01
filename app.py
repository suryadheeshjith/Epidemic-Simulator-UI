import streamlit as st
import UI
import Utils
import traceback
import streamlit as st
import os

def file_selector(folder_path='.'):
    filenames = Utils.get_example_names_list()
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

def main():
    st.set_page_config(page_title="Episimmer",page_icon="Data/Healthbadge_logo.png")
    st.markdown("""
    # :chart_with_upwards_trend: Welcome to our Epidemic Simulator!
    """)
    st.write("---")

    st.write("The implementation of this simulator is based on the [Episimmer](https://github.com/healthbadge/episimmer) simulator.")
    st.write("""
    To get started, choose your mode of data input. Do note that by choosing to upload your files directly, you harness the highest possible capability
    the simulator has to offer. Doing this through the website will only have limited capability.
    """)

    input_options = ['Upload files (Recommended)', 'Input data on the Website', 'Use templates']
    option = st.selectbox('Input Mode : ', input_options)

    # Session state
    state = Utils._get_state()
    state(first_run=True, run_id=0)
    if(state.first_run):
        state.first_run = False
        Utils.clear_files()

    # Options - Upload Files
    if(option=='Upload files (Recommended)'):
        st.markdown("""
            To use some pre-built examples, download some from [here](https://github.com/healthbadge/episimmer/tree/master/examples) and run the simulator.
            """)
        st.write("---")
        clear_button = st.button("Click here to clear all files")
        if(clear_button):
            Utils.clear_files()
            state.run_id += 1

        config_obj = Utils.get_uploaders(key=state.run_id)

        Utils.run_simulation_from_upload(config_obj)

    # Options - Input through website
    elif(option == 'Input data on the Website'):
        st.markdown("""
            Use the sidebar to navigate through the different pages to set your simulation parameters.
            """)
        st.write("---")
        app = Utils.MultiPage()
        defaults = {}

        all_pages_objects = [UI.UI_Simulation_Config(), UI.UI_Environment(), UI.UI_Model(), UI.UI_Policy(), UI.UI_Results()]

        for page_obj in all_pages_objects:
            name = page_obj.name
            defaults[name] = app.add_page(page_obj,state)

        state(params=defaults)
        app.execute_app(state)

    elif(option == 'Use templates'):
        st.markdown("""
            Select any of the templates below. All of them are from the /examples directory [here](https://github.com/healthbadge/episimmer).
            """)
        ls = Utils.get_example_names_list()
        choice = st.selectbox("Choose Template",ls)
        Utils.run_simulation_from_template(choice)




    st.sidebar.markdown("# :clipboard: About")
    st.sidebar.info("Make sure to check us out at [Episimmer](https://github.com/healthbadge/episimmer).\
     For any questions regarding the implementation, bring up an issue [here](https://github.com/suryadheeshjith/Epidemic-Simulator-UI)!")
    state.sync()


if __name__ == "__main__":
    try:

        filename = file_selector('examples')
        st.write('You selected `%s`' % filename)
        # main()
    except Exception as e:
        print(e)
        traceback.print_exc()
        st.error(e)
    # main()
