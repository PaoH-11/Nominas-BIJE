import streamlit as st
import mysql.connector

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
            return True
        else:
            return False
    except mysql.connector.Error as e:
        st.error(f"Error al verificar las credenciales: {e}")
        return False
    finally:
        if conn is not None:
            conn.close()

def get_user_role(username):
    conn = None
    try:
        connection_config = {
            'host': st.secrets["connections"]["mysql"]["host"],
            'user': st.secrets["connections"]["mysql"]["username"],
            'password': st.secrets["connections"]["mysql"]["password"],
            'database': st.secrets["connections"]["mysql"]["database"],
            'charset': st.secrets["connections"]["mysql"]["query"]["charset"]
        }

        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()
        cursor.execute("SELECT rol FROM login WHERE usuario = %s", (username,))
        row = cursor.fetchone()

        if row:
            return row[0]
        else:
            return None
    except mysql.connector.Error as e:
        st.error(f"Error al obtener el rol del usuario: {e}")
        return None
    finally:
        if conn is not None:
            conn.close()