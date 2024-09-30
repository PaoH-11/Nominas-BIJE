import streamlit as st
from streamlit_option_menu import option_menu
import importlib


def initialize_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'rol' not in st.session_state:
        st.session_state.rol = ""


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    @staticmethod
    def run_admin():
        
        st.set_page_config(
            page_title="MAVEN",
            page_icon="🗃",
            layout="wide",
            initial_sidebar_state="expanded",
            
        )
        st.sidebar.image("data/logo.jpg")
        
        if 'username' in st.session_state:
            st.sidebar.markdown(
                f"""
                <div style='text-align: center; font-weight: bold; font-size: 24px;'>
                    Bienvenido, {st.session_state.username}
                </div>
                """,
                unsafe_allow_html=True
            )

        with st.sidebar:
            st.markdown(
                """
                <div style="background-color: ##154c79; border-radius: 5px; text-align: left; padding-left: 15px;">
                    <span style="color: #F0602C; font-size: 24px;">Menú</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            app = option_menu(
                menu_title=False,
                options=["Nómina GoogleSheet","Nómina Temporal","Excel"],
                 icons=["calculator", "calculator", "calculator", "calculator"],
                menu_icon="heart-eyes-fill",
                default_index=0,
                styles={
                    "container": {"background-color": "#bcbcbc"},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "17px", "text-align": "left", "margin": "0px"},
                    "nav-link-selected": {"background-color": "#475570"},
                }
            )
        app_modules = {
            'Nómina GoogleSheet': 'paginas.calculadora_nomina',
            'Nómina Temporal': 'paginas.excel_temporal',
            'Excel': 'paginas.lector_excel',            
        }
        if app in app_modules:
            module = importlib.import_module(app_modules[app])
            module.app()  # Llamar a la función app() del módulo

        def logout():
            st.sidebar.markdown("""
            [![Logout](https://img.icons8.com/ios-filled/20/000000/logout-rounded.png)](#)
            """, unsafe_allow_html=True)

            if st.sidebar.button("Cerrar Sesión"):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.rol = ""
                st.rerun()

        logout()
