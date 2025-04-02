import streamlit as st
import pandas as pd
import mysql.connector

# Función para conectar a MySQL
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

# Función para guardar o actualizar el único registro
def guardar_o_actualizar_datos(uma, tope_isubsidio, subsidio_diario, subsidio_empleo, excedente, prest_dinero, prest_especie, invy_vida, cesa_vejz):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()

        # Verificar si ya existe un registro
        cursor.execute("SELECT COUNT(*) FROM conf_imss")
        total_registros = cursor.fetchone()[0]

        if total_registros == 0:
            # Insertar si no hay registros"""
            cursor.execute("""
                INSERT INTO conf_imss (`uma`, `tope_isubsidio`, `subsidio_diario`, `subsidio_empleo`, `excedente`, `prest_dinero`, `prest_especie`, `invy_vida`, `cesa_vejz`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (uma, tope_isubsidio, subsidio_diario, subsidio_empleo, excedente, prest_dinero, prest_especie, invy_vida, cesa_vejz))

        else:
            # Actualizar si ya hay un registro
            cursor.execute("""
                UPDATE conf_imss 
                SET `uma`=%s, `tope_isubsidio`=%s, `subsidio_diario`=%s, `subsidio_empleo`=%s, `excedente`=%s, 
                    `prest_dinero`=%s, `prest_especie`=%s, `invy_vida`=%s, `cesa_vejz`=%s
                WHERE id = (SELECT id FROM conf_imss ORDER BY id LIMIT 1)
            """, (uma, tope_isubsidio, subsidio_diario, subsidio_empleo, excedente, prest_dinero, prest_especie, invy_vida, cesa_vejz))
        conn.commit()
        conn.close()
        return True
    return False

def obtener_datos():
    conn = connect_to_database()
    if conn:
        
        df = pd.read_sql("SELECT * FROM conf_imss LIMIT 1", conn)
        conn.close()
        return df
    return pd.DataFrame()


# Interfaz en Streamlit
def app():
    st.title("Configuración de parámetros para IMSS")

    # Cargar datos existentes (si hay)
    datos_actuales = obtener_datos()

    # Variables con valores por defecto si ya hay datos
    valores_por_defecto = datos_actuales.iloc[0] if not datos_actuales.empty else {}

    with st.form("formulario_nomina"):
        col1, col2 = st.columns(2)  # Crear dos columnas

        with col1:
            uma = st.number_input("UMA", min_value=0.0, format="%.4f", value=valores_por_defecto.get("uma", 0.0))
            #uma = st.number_input("UMA", min_value=0.0, format="%.4f", value=float(valores_por_defecto.get("uma", 0.0)))

            tope_isubsidio = st.number_input("TOPE DE INGRESOS PARA SUBSIDIO", min_value=0.0, format="%.4f", value=valores_por_defecto.get("tope_isubsidio", 0.0))
            subsidio_diario = st.number_input("SUBSIDIO DIARIO", min_value=0.0, format="%.4f", value=valores_por_defecto.get("subsidio_diario", 0.0))
            subsidio_empleo = st.number_input("(%) SUBSIDIO AL EMPLEO", min_value=0.0, format="%.4f", value=valores_por_defecto.get("subsidio_empleo", 0.0))
            excedente = st.number_input("(%) EXCEDENTE", min_value=0.0, format="%.4f", value=valores_por_defecto.get("excedente", 0.0))
            
        with col2:
            prest_dinero = st.number_input("(%) PRESTACIONES EN DINERO", min_value=0.0, format="%.4f", value=valores_por_defecto.get("prest_dinero", 0.0))
            prest_especie = st.number_input("(%) PRESTACIONES EN ESPECIE", min_value=0.0, format="%.4f", value=valores_por_defecto.get("prest_especie", 0.0))
            invy_vida = st.number_input("(%) INVALIDEZ Y VIDA", min_value=0.0, format="%.4f", value=valores_por_defecto.get("invy_vida", 0.0))
            cesa_vejz = st.number_input("(%) CESANTÍA Y VEJEZ", min_value=0.0, format="%.4f", value=valores_por_defecto.get("cesa_vejz", 0.0))

        submit = st.form_submit_button("Guardar Datos")

    if submit:
        if guardar_o_actualizar_datos(uma, tope_isubsidio, subsidio_diario, subsidio_empleo, excedente, prest_dinero, prest_especie, invy_vida, cesa_vejz):
            st.success("Datos guardados correctamente ✅")
        else:
            st.error("Error al guardar los datos ❌")

    # Mostrar datos guardados
    st.subheader("Datos Registrados")
    df = obtener_datos()

    if not df.empty:
        with st.expander("📋 Ver registro actual"):
            st.dataframe(df)
    else:
        st.warning("No hay datos registrados.")

if __name__ == "__main__":
    app() 