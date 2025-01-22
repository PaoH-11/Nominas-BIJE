import streamlit as st
from streamlit_option_menu import option_menu
import importlib

class MultiApp2:
    # Asegúrate de tener dos guiones bajos al inicio y al final
    def __init__(self):  
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    @staticmethod
    def run_user():
        st.sidebar.image("data/logo2.png")
        if 'username' in st.session_state:
            st.sidebar.write(f'Bienvenido, {st.session_state.username}')
        with st.sidebar:
            st.markdown(
                """
                <div style="background-color: ##154c79; border-radius: 5px; text-align: left; padding-left: 30px;">
                    <span style="color: #fff; font-size: 24px;">General</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            app = option_menu(
                menu_title=False,
                options=["Tables", "Data Presentation", "Layouts"],
                icons=["table", "bar-chart-line", "back"],
                menu_icon="heart-eyes-fill",
                default_index=1,
                styles={
                    "container": {"background-color": "#2a3f54"},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "17px", "text-align": "left", "margin": "0px"},
                    "nav-link-selected": {"background-color": "#2f4457"},
                }
            )
        # Diccionario para mapear la selección a los módulos
        app_modules = {
            'Tables': 'paginas.tables',
            'Data Presentation': 'paginas.datas',
            'Layouts': 'paginas.layout'
        }
        # Importar y ejecutar la función app del módulo correspondiente
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
                st.experimental_rerun()

        logout()
