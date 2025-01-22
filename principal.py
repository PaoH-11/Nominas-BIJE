import streamlit as st
import os
from streamlit_lottie import st_lottie
from clases.multi_app_admin import MultiApp as MultiAppAdmin
from clases.multi_app_user import MultiApp2 as MultiAppUser

from utils.autenticacion import verify_credentials, get_user_role
from utils.configuracion import initialize_session_state, hide_sidebar, set_wide_layout_and_center_title

logo = os.path.join(os.path.dirname(__file__), 'data', 'logo_maven_azul.png')

def login_page():
    hide_sidebar()
    set_wide_layout_and_center_title()
    st.markdown("<h1>INICIAR SESIÓN</h1>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 2])

    with col1:
        st.image(logo, width=450)

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)        
        username = st.text_input(" ", placeholder="Ingrese su usuario")
        st.markdown("<br>", unsafe_allow_html=True)
        password = st.text_input(" ", type="password", placeholder="Ingrese su contraseña")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Iniciar Sesión"):
            if verify_credentials(username, password):
                st.success("Inicio de sesión exitoso!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.rol = get_user_role(username)
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

def logout():
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.rol = ""
        st.experimental_rerun()

def main():
    initialize_session_state()
    if st.session_state.logged_in and st.session_state.rol == "Admin":
        multi_app = MultiAppAdmin()
        multi_app.run_admin()
    elif st.session_state.logged_in and st.session_state.rol == "Usuario":
        multi_app2 = MultiAppUser()
        multi_app2.run_user()
    else:
        login_page()

if __name__ == "__main__":
    main()