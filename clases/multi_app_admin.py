import streamlit as st
from streamlit_option_menu import option_menu
import importlib
import mysql.connector


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
        st.sidebar.image("data/logo_maven_azul_s.png")

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
            
            app = option_menu(
                menu_title=False,
                options=["Nómina GoogleSheet","Nómina Temporal","Excel", "Salarios"],
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

        # Módulos de aplicaciones
        app_modules = {
            'Nómina GoogleSheet': 'paginas.calculadora_nomina',
            'Nómina Temporal': 'paginas.excel_temporal',
            'Excel': 'paginas.lector_excel',
            'Salarios': 'paginas.asignacion_sueldos',  
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
        
    #Usuarios    
    def run_user():
        st.set_page_config(
            page_title="MAVEN",
            page_icon="🗃",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.sidebar.image("data/logo_maven_azul_s.png")

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
            
            app = option_menu(
                menu_title=False,
                options=["Nómina GoogleSheet","Nómina Temporal"],
                icons=["calculator", "calculator"],
                menu_icon="heart-eyes-fill",
                default_index=0,
                styles={
                    "container": {"background-color": "#bcbcbc"},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "17px", "text-align": "left", "margin": "0px"},
                    "nav-link-selected": {"background-color": "#475570"},
                }
            )

        # Módulos de aplicaciones
        app_modules = {
            'Nómina GoogleSheet': 'paginas.calculadora_nomina',
            'Nómina Temporal': 'paginas.excel_temporal', 
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



def verify_credentials(username, password):
    conn = None
    try:
        # Conectar a MySQL usando los secrets de Streamlit
        connection_config = {
            'host': st.secrets["connections"]["mysql"]["host"],
            'user': st.secrets["connections"]["mysql"]["username"],
            'password': st.secrets["connections"]["mysql"]["password"],
            'database': st.secrets["connections"]["mysql"]["database"],
            'charset': st.secrets["connections"]["mysql"]["query"]["charset"]
        }
        
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM login WHERE usuario = %s AND clave = %s", (username, password))
        row = cursor.fetchone()
        
        if row:
            st.session_state.logged_in = True
            st.session_state.username = row['nombre']
            st.session_state.rol = row['rol']
            return True
        else:
            return False
    except mysql.connector.Error as e:
        st.error(f"Error al verificar las credenciales: {e}")
        return False
    finally:
        if conn is not None:
            conn.close()


def login_page():
    st.markdown("<h1>INICIAR SESIÓN</h1>", unsafe_allow_html=True)
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        if verify_credentials(username, password):
            st.success("Inicio de sesión exitoso!")
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")


def main():
    initialize_session_state()
    if st.session_state.logged_in:
        if st.session_state.rol == "Admin":
            MultiApp.run_admin()
        if st.session_state.rol == "User":
            MultiApp.run_user()  
        else:    
            st.error("No tienes permisos para acceder.")
    else:
        login_page()


if __name__ == "__main__":
    main()
