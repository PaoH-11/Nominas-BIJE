import streamlit as st
import psycopg2
import toml
from clases.multi_app_admin import MultiApp as MultiAppAdmin
from clases.multi_app_user import MultiApp2 as MultiAppUser
import os
import json
from streamlit_lottie import st_lottie

def initialize_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'rol' not in st.session_state:
        st.session_state.rol = ""

def hide_sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
            [data-testid="collapsedControl"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def set_wide_layout_and_center_title():
    st.markdown(
        """
        <style>
            .main .block-container {
                max-width: 1200px;
                padding-left: 5%;
                padding-right: 5%;
            }
            h1 {
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def verify_credentials(username, password, connection_string):
    conn = None
    try:
        conn = psycopg2.connect(connection_string)
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM login WHERE usuario = %s AND contraseña = %s", (username, password))
            row = cursor.fetchone()
            if row:
                return True
            else:
                return False
    except psycopg2.Error as e:
        st.error(f"Error al verificar las credenciales: {e}")
        return False
    finally:
        if conn is not None:
            conn.close()

def get_user_role(username, connection_string):
    conn = None
    try:
        conn = psycopg2.connect(connection_string)
        with conn.cursor() as cursor:
            cursor.execute("SELECT rol FROM login WHERE usuario = %s", (username,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
    except psycopg2.Error as e:
        st.error(f"Error al obtener el rol del usuario: {e}")
        return None
    finally:
        if conn is not None:
            conn.close()


def load_lottieur(path: str):
    with open(path, encoding='utf-8') as f:
       data = json.load(f)
    return data

lottie_file = 'C:\\Users\\repet\\OneDrive\\Escritorio\\Nominas\\data\\maven_icon01.json'
lottie_json = load_lottieur(lottie_file)

def login_page(connection_string):
    hide_sidebar()
    set_wide_layout_and_center_title()
    st.markdown("<h1>INICIAR SESIÓN</h1>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 2])  # Cambia los tamaños de las columnas aquí

    with col1:
        st_lottie(lottie_json,width=450)  # Ajustar el tamaño de la animación con el parámetro height

    with col2:        
        st.markdown(
            """
            <style>
                .stTextInput {
                    margin-top: 30px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Iniciar Sesión"):
            if verify_credentials(username, password, connection_string):
                st.success("Inicio de sesión exitoso!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.rol = get_user_role(username, connection_string)
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

def logout():
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.rol = ""
        st.rerun()

def main(connection_string):
    initialize_session_state()
    if st.session_state.logged_in and st.session_state.rol == "admin":
        multi_app = MultiAppAdmin()
        multi_app.run_admin()
    elif st.session_state.logged_in and st.session_state.rol == "usuario":
        multi_app2 = MultiAppUser()
        multi_app2.run_user()
    else:
        login_page(connection_string)

if __name__ == "__main__":
    try:
        file_path = os.path.join(os.path.dirname(__file__), '.streamlit', 'secrets.toml')
        secrets = toml.load(file_path)
        connection_string = secrets["database"]["connection_string"]
    except FileNotFoundError:
        st.error("El archivo secrets.toml no se encontró. Asegúrate de que está en el directorio correcto.")
        st.stop()
    except KeyError:
        st.error("El archivo secrets.toml no tiene el formato correcto.")
        st.stop()

    main(connection_string)
