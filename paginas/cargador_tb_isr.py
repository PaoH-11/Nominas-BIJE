import streamlit as st
import mysql.connector
import pandas as pd
import io

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

# Función para guardar datos en la BD
def guardar_datos_en_bd(df):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tarifas_isr")  # Limpiar datos anteriores

        query = """
        INSERT INTO tarifas_isr (limite_inferior, limite_superior, cuota_fija, porcentaje) 
        VALUES (%s, %s, %s, %s)
        """
        data = df.values.tolist()
        cursor.executemany(query, data)

        conn.commit()
        cursor.close()
        conn.close()
        return True
    return False

# Función para cargar datos desde la BD
def cargar_datos_desde_bd():
    conn = connect_to_database()
    if conn:
        query = "SELECT limite_inferior, limite_superior, cuota_fija, porcentaje FROM tarifas_isr"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    return None

# Función para procesar y validar los datos antes de guardarlos
def procesar_datos(df):
    required_columns = ["limite_inferior", "limite_superior", "cuota_fija", "porcentaje"]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Faltan las siguientes columnas en el archivo: {', '.join(missing_columns)}")

    for col in required_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()
    return df

# Interfaz de Streamlit
def app():
    st.title("Cargador de Tarifas ISR")

    # Mostrar los datos actuales en la BD
    st.subheader("Tarifas ISR Actuales en la Base de Datos")
    df_actual = cargar_datos_desde_bd()
    
    if df_actual is not None and not df_actual.empty:
        st.dataframe(df_actual)
    else:
        st.warning("No hay datos en la base de datos.")

    # Subir nuevo archivo
    uploaded_file = st.file_uploader("Cargar archivo Excel con tarifas ISR", type="xlsx")

    if uploaded_file is not None:
        df_tarifas = pd.read_excel(uploaded_file)
        st.write("Datos cargados:")
        st.dataframe(df_tarifas)

        if st.button("Guardar en BD"):
            try:
                df_procesado = procesar_datos(df_tarifas)
                if guardar_datos_en_bd(df_procesado):
                    st.success("Datos guardados en la base de datos correctamente.")
                    st.experimental_rerun()  # Recargar la página
            except Exception as e:
                st.error(f"Error al procesar los datos: {e}")

if __name__ == "__main__":
    app()
