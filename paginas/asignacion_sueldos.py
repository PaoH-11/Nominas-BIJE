import streamlit as st
import mysql.connector
import pandas as pd

st.markdown(
    """
    <style>
    /* Degradado de fondo */
    .stApp {
        background-image: radial-gradient(circle at 34.8%, #bad4ee 0, #97bee6 25%, #70a8dd 50%, #4192d4 75%, #007dcc 100%);
        height: 100vh;
        padding: 0;
    }    
    </style>
    """,
    unsafe_allow_html=True
)       

def app():
    st.title("ASIGNACIÓN DE SALARIOS")
    st.markdown("""
    <style>
    .stAlert {
        background-color: #1E3A8A; 
        border-radius: 10px;
        color: white;  
    }
    </style>
    """, unsafe_allow_html=True)

    # Función para conectar a la base de datos
    def connect_to_database():
        try:
            connection_config = {
                'host': st.secrets["connections"]["mysql"]["host"],
                'user': st.secrets["connections"]["mysql"]["username"],
                'password': st.secrets["connections"]["mysql"]["password"],
                'database': st.secrets["connections"]["mysql"]["database"],
                'charset': st.secrets["connections"]["mysql"]["query"]["charset"]
            }
            conn = mysql.connector.connect(**connection_config)
            return conn
        except mysql.connector.Error as e:
            st.error(f"Error al conectar a la base de datos: {e}")
            return None

    # Función para realizar consultas
    def fetch_data(query, params=None):
        conn = connect_to_database()
        if conn is None:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            return pd.DataFrame(results)
        except mysql.connector.Error as e:
            st.error(f"Error al ejecutar la consulta: {e}")
            return None
        finally:
            conn.close()

    # Función para ejecutar operaciones (INSERT, UPDATE, DELETE)
    def execute_query(query, params=None):
        conn = connect_to_database()
        if conn is None:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return True
        except mysql.connector.Error as e:
            st.error(f"Error al ejecutar la operación: {e}")
            return False
        finally:
            conn.close()

    # Mostrar tabla de datos
    query = "SELECT idsalarios, puesto AS PUESTO, zona AS ZONA, salario_base AS SALARIO, p_asis AS ASISTENCIA, p_punt AS PUNTUALIDAD FROM salarios"
    data = fetch_data(query)

    if data is not None and not data.empty:
        # Crear encabezados manuales
        cols = st.columns([1.5, 1.5, 1.5, 1, 1, 1, 1])  
        cols[0].write("Puesto")
        cols[1].write("Zona")
        cols[2].write("Salario Base")
        cols[3].write("Bono Asistencia")
        cols[4].write("Bono Puntualidad")
        cols[5].write("Editar")
        cols[6].write("Eliminar")

        # Mostrar datos fila por fila
        for index, row in data.iterrows():
            cols = st.columns([1.5, 1.5, 1.5, 1, 1, 1, 1])
            cols[0].write(row["PUESTO"])
            cols[1].write(row["ZONA"])
            cols[2].write(row["SALARIO"])
            cols[3].write(row["ASISTENCIA"])
            cols[4].write(row["PUNTUALIDAD"])

            # Botón para editar
            if cols[5].button("✏️", key=f"edit_{row['idsalarios']}"):
                st.session_state["edit_id"] = row["idsalarios"]
                st.session_state["edit_row"] = row

            # Botón para eliminar
            if cols[6].button("❌", key=f"delete_{row['idsalarios']}"):
                delete_query = "DELETE FROM salarios WHERE idsalarios = %s"
                if execute_query(delete_query, (row["idsalarios"],)):
                    st.success(f"Registro eliminado exitosamente.")
                    st.experimental_rerun()

        # Mostrar formulario de edición si se seleccionó un registro
        if "edit_id" in st.session_state:
            st.subheader("Editar Registro")
            edit_id = st.session_state["edit_id"]
            edit_row = st.session_state["edit_row"]

            edit_puesto = st.text_input("Puesto", edit_row["PUESTO"])
            edit_zona = st.text_input("Zona", edit_row["ZONA"])
            edit_salario = st.number_input("Salario Base", min_value=0.0, value=edit_row["SALARIO"], step=0.01)
            edit_asis = st.number_input("Bono de Asistencia", min_value=0.0, value=edit_row["ASISTENCIA"], step=0.01)
            edit_punt = st.number_input("Bono de Puntualidad", min_value=0.0, value=edit_row["PUNTUALIDAD"], step=0.01)

            if st.button("Guardar Cambios"):
                update_query = """
                    UPDATE salarios
                    SET puesto = %s, zona = %s, salario_base = %s, p_asis = %s, p_punt = %s
                    WHERE idsalarios = %s
                """
                if execute_query(update_query, (edit_puesto, edit_zona, edit_salario, edit_asis, edit_punt, edit_id)):
                    st.success("Registro actualizado exitosamente.")
                    del st.session_state["edit_id"]
                    del st.session_state["edit_row"]
                    st.experimental_rerun()
                else:
                    st.error("No se pudo actualizar el registro.")
    else:
        st.write("No se encontraron datos o hubo un error.")

    # Funcionalidad de agregar nuevo registro
    with st.expander("Agregar salario nuevo"):
        st.subheader("Agregar Nuevo Registro")
        new_puesto = st.text_input("Puesto")

        # Obtener valores únicos para la columna 'ZONA'
        if not data.empty:
            zonas_unicas = data["ZONA"].unique().tolist()
        else:
            zonas_unicas = ["Interior", "Exterior", "Especial"]  # Opciones por defecto si no hay datos

        # Usar selectbox para seleccionar la zona
        new_zona = st.selectbox("Zona", zonas_unicas)
        #new_zona = st.text_input("Zona")
        new_salario = st.number_input("Salario Base", min_value=0.0, step=0.01)
        new_asis = st.number_input("Bono de Asistencia", min_value=0.0, step=0.01)
        new_punt = st.number_input("Bono de Puntualidad", min_value=0.0, step=0.01)
        
        new_aguinaldo = 0.0411
        new_vacaciones = 0.0329
        new_pvac = 0.082
        new_pdom = 0.0357

        if st.button("Agregar Registro"):
            insert_query = """
                    INSERT INTO salarios (puesto, zona, salario_base, p_asis, p_punt, aguinaldo, vacaciones, p_vac, p_dom)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            if execute_query(insert_query, (new_puesto, new_zona, new_salario, new_asis, new_punt, new_aguinaldo, new_vacaciones, new_pvac, new_pdom)):
                st.success("Nuevo registro agregado exitosamente.")
            else:
                st.error("No se pudo agregar el registro.")

if __name__ == "__main__":
    app()
