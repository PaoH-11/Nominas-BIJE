import streamlit as st
import pandas as pd
import mysql.connector
import io
from data.datos import SALARIO_BASE, tarifas_isr
from paginas.cargador_tb_isr import cargar_datos_desde_bd

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

# Mostrar tabla de datos
query = "SELECT * FROM salarios"
data = fetch_data(query)

# Función para calcular el nomina
def calcular_nomina(salario_base, prem_punt_pct, prem_asis_pct, incluir_prima_dominical):
    aguinaldo = round((salario_base * (15 / 365)), 2)
    vacaciones = round((salario_base * (12 / 365)), 2)
    prima_vacacional = round(vacaciones * 0.25, 2)  
    prima_dominical = round(((1 * 0.25) / 7) * salario_base, 2) if incluir_prima_dominical else 0
    prem_asis = round(salario_base * prem_asis_pct, 2)
    prem_punt = round(salario_base * prem_punt_pct, 2)
    sueldo_integrado = round(salario_base + aguinaldo + vacaciones + prima_vacacional + prima_dominical, 2)
    fini = round(aguinaldo + vacaciones + prima_vacacional, 2)
 
    return aguinaldo, vacaciones, prima_vacacional, prima_dominical, prem_asis, prem_punt, sueldo_integrado, fini

# Función para obtener el salario base y el porcentaje de la prima vacacional según el puesto y la zona
"""def calcular_isr(base_isr):
    for tarifa in tarifas_isr:
        if tarifa["limite_inferior"] <= base_isr <= tarifa["limite_superior"]:
            isr = tarifa["cuota_fija"] + (base_isr - tarifa["limite_inferior"]) * tarifa["porcentaje"]
            return round(isr, 2)        
    return 0.0"""

def calcular_isr(base_isr):
    # Obtener las tarifas desde la base de datos (como un DataFrame)
    df_tarifas_isr = cargar_datos_desde_bd()  #  esta función devuelve un DataFrame de lo que se eingresa en el cargador

    # Iterar sobre las filas del DataFrame
    #iterar : recorrer un conjunto de elementos uno por uno para realizar alguna acción sobre cada uno de esos elementos.
    for index, tarifa in df_tarifas_isr.iterrows():
        limite_inferior = tarifa["limite_inferior"]
        limite_superior = tarifa["limite_superior"]
        
        # Verificar si la base_isr está dentro del rango
        if limite_inferior <= base_isr <= limite_superior:
            cuota_fija = tarifa["cuota_fija"]
            porcentaje = tarifa["porcentaje"]
            
            # Calcular el ISR (dependiendo de tu fórmula)
            isr_calculado = cuota_fija + (base_isr - limite_inferior) * porcentaje
            return round(isr_calculado, 2)  # Retornar el ISR calculado

    # Si no se encuentra ningún rango, retornar 0
    return 0.0

# Función para obtener el salario base y premios según el puesto y la zona
def obtener_salario_y_premio(puesto, zona, total_dias_t2):
    conn = connect_to_database()
    if conn is None:
        st.error("No se pudo conectar a la base de datos.")
        return None
    
    try:
        cursor = conn.cursor()
        # Consulta el salario base, premio de asistencia y premio dominical según el puesto y la zona
        query = """
            SELECT salario_base, salario_base2, salario_base3, p_asis, p_punt, p_dom
            FROM salarios
            WHERE puesto = %s AND zona = %s
        """
        cursor.execute(query, (puesto, zona))
        resultado = cursor.fetchone()
        
        if not resultado:
            raise ValueError(f"No se encontraron datos para el puesto '{puesto}' y la zona '{zona}'")

        salario_base, salario_base2, salario_base3, p_asis, p_punt, p_dom = resultado
        
        #PRIMERAS TRES VARIABLES SON SALARIOS BASE (las que estan en cero  son para el tercer evento)
        #LAS SIGUIENTES CUATRO SON PREMIOS DE ASISTENCIA Y PUNTUALIDAD
        #ULTIMA VARIABLE ES PARA SABER SI SE INCLUYE PRIMA DOMINICAL USANDO TODAS EN TRUE YA QUE AL ASIGAR SALARIOS SE INDICA SI TIENEN O NO   
        if puesto == 'DEMOSTRADOR':
            return salario_base, salario_base2, salario_base3, p_asis, p_punt, 0.1, 0.1,  p_dom, True, False
        elif puesto == 'COORDINADOR':
            return salario_base, salario_base2, salario_base3, p_asis, p_punt, 0.1, 0.1,  p_dom, True, True
        elif puesto == 'COORDINADOR Y DEMOSTRADOR':
            return salario_base, salario_base2, salario_base3, p_asis, p_punt, 0.1, 0.1,  p_dom, False, False
        else:
            raise ValueError(f"Puesto '{puesto}' no reconocido")
    except mysql.connector.Error as e:
        st.error(f"Error al ejecutar la consulta: {e}")
    finally:
        conn.close()
