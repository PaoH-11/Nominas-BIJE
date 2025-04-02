import streamlit as st
import mysql.connector
import pandas as pd

# Función para conectar a la base de datos
def connect_to_database():
    try:
        connection_config = {
            'host': st.secrets["connections"]["mysql"]["host"],
            'user': st.secrets["connections"]["mysql"]["username"],
            'password': st.secrets["connections"]["mysql"]["password"],
            'database': st.secrets["connections"]["mysql"]["database"],
            'port': st.secrets["connections"]["mysql"]["port"], 
            'charset': st.secrets["connections"]["mysql"]["query"]["charset"]
        }
        conn = mysql.connector.connect(**connection_config)
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error al conectar a la base de datos: {e}")
        return None

# Función para cargar datos desde la BD
def cargar_datos_desde_bd():
    conn = connect_to_database()
    if conn:
        df = pd.DataFrame()  # Inicializamos el DataFrame vacío
        cursor = None
        
        try:
            query = "SELECT id, limite_inferior, limite_superior, cuota_fija, porcentaje FROM tarifas_isr ORDER BY limite_inferior"
            cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier access
            cursor.execute(query)
            rows = cursor.fetchall()

            # Crear DataFrame con los datos
            df = pd.DataFrame(rows)
            
            # Mostrar cuántos registros se encontraron para depuración
            st.info(f"Se encontraron {len(df)} registros en la base de datos")

        except mysql.connector.Error as e:
            st.error(f"Error al obtener los datos: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return df if not df.empty else None
    return None

# Función para actualizar los datos en la BD
def actualizar_datos_en_bd(id, limite_inferior, limite_superior, cuota_fija, porcentaje):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            UPDATE tarifas_isr
            SET limite_inferior = %s, limite_superior = %s, cuota_fija = %s, porcentaje = %s
            WHERE id = %s
            """
            cursor.execute(query, (limite_inferior, limite_superior, cuota_fija, porcentaje, id))
            conn.commit()
            st.success("Registro actualizado correctamente.✅")
            return True
        except mysql.connector.Error as e:
            st.error(f"Error al actualizar los datos: {e}")
            conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# Interfaz de Streamlit
def app():
    st.title("Tarifas ISR")

    # Mostrar los datos actuales en la BD
    st.subheader("Tarifas ISR Actuales en Base de Datos")
    df_actual = cargar_datos_desde_bd()
    
    if df_actual is not None and not df_actual.empty:
        # Crear encabezados
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 1, 1])
        with col1:
            st.write("ID")
        with col2:
            st.write("Límite Inferior")
        with col3:
            st.write("Límite Superior")
        with col4:
            st.write("Cuota Fija")
        with col5:
            st.write("Porcentaje")
        with col6:
            st.write("Acción")

        # Mostrar los datos de la tabla con un diseño en columnas
        for index, row in df_actual.iterrows():
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 1, 1])
            with col1:
                st.text(row['id'])
            with col2:
                st.text(row['limite_inferior'])
            with col3:
                st.text(row['limite_superior'])
            with col4:
                st.text(row['cuota_fija'])
            with col5:
                st.text(row['porcentaje'])
            with col6:
                #if st.button(f"Editar ✏️{row['id']}", key=f"editar_{row['id']}"):
                #    st.session_state.registro_a_editar = row.to_dict()  # Convertir a diccionario
                # Cambiar el texto del botón de "Editar" para incluir un emoji de lápiz
                if st.button(f"✏️ Editar", key=f"editar_{row['id']}"):
                    st.session_state.registro_a_editar = row.to_dict()  # Convertir a diccionario




        # Verificar si se ha seleccionado un registro para editar
        if 'registro_a_editar' in st.session_state:
            registro_a_editar = st.session_state.registro_a_editar
            st.subheader(f"Editar Registro ID {registro_a_editar['id']}")

            # Asegurarse de que los valores no sean None, si lo son, asignar un valor predeterminado
            limite_inferior = float(registro_a_editar.get('limite_inferior', 0.0))
            limite_superior = float(registro_a_editar.get('limite_superior', 0.0))
            cuota_fija = float(registro_a_editar.get('cuota_fija', 0.0))
            porcentaje = float(registro_a_editar.get('porcentaje', 0.0))

            # Crear formulario de edición
            limite_inferior = st.number_input("Límite Inferior", value=limite_inferior, step=1.0, key="limite_inferior")
            limite_superior = st.number_input("Límite Superior", value=limite_superior, step=1.0, key="limite_superior")
            cuota_fija = st.number_input("Cuota Fija", value=cuota_fija, step=0.01, key="cuota_fija")
            porcentaje = st.number_input("Porcentaje", value=porcentaje, step=0.01, key="porcentaje")

            if st.button("Guardar cambios", key="guardar_cambios"):
                # Actualizar el registro en la base de datos
                if actualizar_datos_en_bd(registro_a_editar['id'], limite_inferior, limite_superior, cuota_fija, porcentaje):
                    del st.session_state.registro_a_editar  # Eliminar registro de session_state
                    st.experimental_rerun()  # Recargar la página para mostrar los cambios