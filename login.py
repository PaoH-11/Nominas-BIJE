import streamlit as st

@st.cache_resource(ttl=3600)
def get_session_state():
    return {"logged_in": False, "username": "", "rol": ""}

def initialize_session_state():
    if "logged_in" not in st.session_state:
        session_state = get_session_state()
        st.session_state.logged_in = session_state["logged_in"]
        st.session_state.username = session_state["username"]
        st.session_state.rol = session_state["rol"]
        st.session_state.logout_requested = False

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.rol = ""
    st.session_state.logout_requested = True
    st.cache_data.clear()
    st.experimental_rerun()

# Inicializar el estado de la sesión
initialize_session_state()

# Mostrar el estado de la sesión
st.write("Logged in:", st.session_state.logged_in)
st.write("Username:", st.session_state.username)
st.write("Role:", st.session_state.rol)

# Botón para hacer logout
if st.button('Logout'):
    logout()

# Simulación de inicio de sesión para propósitos de demostración
if st.button('Login'):
    st.session_state.logged_in = True
    st.session_state.username = "user123"
    st.session_state.rol = "admin"
    st.experimental_rerun()

# Mensaje para indicar que se ha solicitado el logout
if st.session_state.logout_requested:
    st.write("You have been logged out.")
