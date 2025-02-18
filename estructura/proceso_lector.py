import streamlit as st
import mysql.connector
import pandas as pd
import io
from data.datos import SALARIO_BASE, tarifas_isr

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
        #st.error(f"Error al ejecutar la consulta: {e}")
        return None
    finally:
        conn.close()

# Función para calcular el finiquito
def calcular_finiquito(salario_base, prem_punt_pct, prem_asis_pct, incluir_prima_dominical):
    aguinaldo = round((salario_base * (15 / 365)), 2)
    vacaciones = round((salario_base * (12 / 365)), 2)
    prima_vacacional = round(vacaciones * 0.25, 2)  
    prima_dominical = round(((1 * 0.25) / 7) * salario_base, 2) if incluir_prima_dominical else 0
    prem_asis = round(salario_base * prem_punt_pct, 2)
    prem_punt = round(salario_base * prem_asis_pct, 2)
    sueldo_integrado = round(salario_base + aguinaldo + vacaciones + prima_vacacional + prima_dominical, 2)   
    fini = round((aguinaldo + vacaciones + prima_vacacional), 2)

    return aguinaldo, vacaciones, prima_vacacional, prima_dominical, prem_asis, prem_punt, sueldo_integrado, fini

def calcular_isr(base_isr):
    for tarifa in tarifas_isr:
        if tarifa["limite_inferior"] <= base_isr <= tarifa["limite_superior"]:
            isr = tarifa["cuota_fija"] + (base_isr - tarifa["limite_inferior"]) * tarifa["porcentaje"]
            return round(isr, 2)        
    return 0.0

# Función para obtener el salario base y el porcentaje de la prima vacacional según el puesto y la zona
def calcular_retencion(sdi, df_ret):
    # Definir los nombres de las columnas
    SALARIO_BASE_COL = 'Salario Base'  # Reemplaza con el nombre real de la columna de salario base
    RETENCION_COL = 'Retención'  # Reemplaza con el nombre real de la columna de retención
    
    # Ordenar el DataFrame por el salario base en orden ascendente
    df_ret = df_ret.sort_values(by=SALARIO_BASE_COL)
    
    # Buscar la fila correspondiente al SDI
    for index, row in df_ret.iterrows():
        if sdi <= row[SALARIO_BASE_COL]:
            return row[RETENCION_COL]

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
    
    # Si no se encuentra una combinación válida, devolver valores por defecto
    return 0, 0, 0, 0, 0, 0, 0, False, False, False

def procesar_datos(df_empleados, df_ret):
    nuevos_registros = []
    nomina_uno_data = []
    nomina_dos_data = []

    for _, row in df_empleados.iterrows():
        puesto = row['PUESTO']
        zona = row['ZONA']
        nombre_completo = row['NOMBRE COMPLETO']
        bodega = row['BODEGA']
        evento = row['EVENTO']
        horario = row['HORARIO']
        periodo = row['PERIODO TRABAJADO']
        total_dias = row['TOTAL DE DIAS TRABAJADOS UN EVENTO']
        total_dias_t2 = row.get('TOTAL DE DIAS TRABAJADOS DOS EVENTOS', 0)
        total_dias_t3 = row.get('TOTAL DE DIAS TRABAJADOS TRES EVENTOS', 0)
        dias_finiquito = row.get('TOTAL DE DIAS FINIQUITO', 0)
        dias_finiquito2 = row.get('TOTAL DE DIAS FINIQUITO DOS EVENTOS', 0)
        dias_finiquito3 = row.get('TOTAL DE DIAS FINIQUITO TRES EVENTOS', 0)
        horas_extra = row.get('TOTAL DE HORAS EXTRAS', 0)
        dia_festivo = row.get('DÍA FESTIVO', 0)
        observaciones = row.get('OBSERVACIONES', '')
        infonavit = row.get('INFONAVIT', 0)
        prestamo = row.get('PRÉSTAMO', 0)
        sdi = row.get('SDI', 0)
        retencion = calcular_retencion(sdi, df_ret)
        bono = row.get('BONO', 0)
        efectivo = row.get('EFECTIVO', 0)

        
        # Obtener salario y premios según el puesto y la zona
        salario_base, salario_base_dos, salario_base_tres, prem_punt_pct1, prem_asis_pct1, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical1, incluir_prima_dominical2, incluir_prima_dominical3 = obtener_salario_y_premio(puesto, zona, total_dias_t2)
        # Calcular finiquitos para uno y dos eventos
        aguinaldo, vacaciones, prima_vacacional, prima_dominical1, prem_asis, prem_punt, sueldo_integrado1, fini1 = calcular_finiquito(salario_base, prem_punt_pct1, prem_asis_pct1, incluir_prima_dominical1)
        
        if total_dias_t2 >= 1:
            aguinaldo2, vacaciones2, prima_vacacional2, prima_dominical2, prem_asis2, prem_punt2, sueldo_integrado2, fini2 = calcular_finiquito(salario_base_dos, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical2)
        else:
            aguinaldo2 = vacaciones2 = prima_vacacional2 = prima_dominical2 = prem_asis2 = prem_punt2 = sueldo_integrado2 = fini2 = 0

        if total_dias_t3 >= 1:
            aguinaldo3, vacaciones3, prima_vacacional3, prima_dominical3, prem_asis3, prem_punt3, sueldo_integrado3, fini3 = calcular_finiquito(salario_base_tres, prem_punt_pct1, prem_asis_pct1, incluir_prima_dominical3)
        else:
            aguinaldo3 = vacaciones3 = prima_vacacional3 = prima_dominical3 = prem_asis3 = prem_punt3 = sueldo_integrado3 = fini3 = 0

        he = horas_extra * 50
        
        sueldo_cotizacion1 = round(salario_base + prima_dominical1 + prem_asis + prem_punt, 2)
        sueldo_cotizacion2 = round(salario_base_dos + prima_dominical2 + prem_asis2 + prem_punt2, 2) if total_dias_t2 >= 1 else 0
        sueldo_cotizacion3 = round(salario_base_tres + prima_dominical3 + prem_asis3 + prem_punt3, 2) if total_dias_t3 >= 1 else 0

        if total_dias_t2 == 0:
            salario_base_dos = 0
        if total_dias_t3 == 0:
            salario_base_tres = 0

        if dias_finiquito == 0:
            fini1 = 0
        if dias_finiquito2 == 0:
            fini2 = 0
        if dias_finiquito3 == 0:
            fini3 = 0

        total_uno = round(sueldo_cotizacion1 * total_dias, 2) if dias_finiquito == 0 else round(sueldo_cotizacion1 * total_dias + (fini1 * dias_finiquito), 2)
        total_dos = round(sueldo_cotizacion2 * total_dias_t2, 2) if dias_finiquito2 == 0 else round(sueldo_cotizacion2 * total_dias_t2 + (fini2 * dias_finiquito2), 2)
        total_tres = round(sueldo_cotizacion3 * total_dias_t3, 2) if dias_finiquito3 == 0 else round(sueldo_cotizacion3 * total_dias_t3 + (fini3 * dias_finiquito3), 2)

        if dia_festivo >= 1:
            total_uno += dia_festivo * 2
        
        base_isr = round((salario_base + prem_asis + prem_punt) * total_dias + ((he / 2) + dia_festivo + bono + (vacaciones * dias_finiquito)),2) 
        total = round(total_uno + total_dos + total_tres + he, 2)
        retencion_dias = round((retencion/7) * total_dias, 2)
        isr_calculado = calcular_isr(base_isr)   
        deducciones = isr_calculado + infonavit + prestamo + retencion_dias

        nuevo_registro = {
            "PUESTO": puesto,
            "ZONA": zona,
            "NOMBRE COMPLETO": nombre_completo,
            "BODEGA": bodega,
            "EVENTO": evento,
            "HORARIO": horario,
            "PERIODO": periodo,
            "TOTAL DE DIAS UN EVENTO": total_dias,
            "TOTAL DÍAS DOS EVENTOS": total_dias_t2,
            "TOTAL DÍAS TRES EVENTOS": total_dias_t3,
            "TOTAL DÍAS FINIQUITO UN EVENTO": dias_finiquito,
            "TOTAL DÍAS FINIQUITO DOS EVENTOS": dias_finiquito2,
            "TOTAL DÍAS FINIQUITO TRES EVENTOS": dias_finiquito3,
            "SALARIO BASE": salario_base,
            "SALARIO DIARIO UN EVENTO (P001)": salario_base * total_dias,
            "AGUINALDO (P002)": aguinaldo * dias_finiquito,
            "VACACIONES (P001)": vacaciones * dias_finiquito,
            "PRIMA VACACIONAL (P021)": prima_vacacional * dias_finiquito,
            "PRIMA DOMINICAL (P020)": prima_dominical1 * total_dias,
            "PREMIO ASISTENCIA (P049)": prem_asis * total_dias,
            "PREMIO PUNTUALIDAD (P010)": prem_punt * total_dias,
            "FINIQUITO UN EVENTO": fini1 * dias_finiquito,
            "SUELDO INTEGRADO (IMSS)": sueldo_integrado1 * total_dias,
            "SUELDO COTIZACIÓN S/F UN EVENTO": sueldo_cotizacion1 * total_dias,
            
            "SUELDO POR COBRAR UN EVENTO": total_uno,

            "SALARIO BASE DOS EVENTOS": salario_base_dos,
            "SALARIO DIARIO DOS EVENTOS (P001)": salario_base_dos * total_dias_t2,
            "AGUINALDO 2 (P002)": aguinaldo2 * dias_finiquito2,
            "VACACIONES 2 (P001)": vacaciones2 * dias_finiquito2,
            "PRIMA VACACIONAL 2 (P021)": prima_vacacional2 * dias_finiquito2,
            "PRIMA DOMINICAL 2 (P020)": prima_dominical2 * total_dias_t2,
            "PREMIO ASISTENCIA 2 (P049)": prem_asis2 * total_dias_t2,
            "PREMIO PUNTUALIDAD 2 (P010)": prem_punt2 * total_dias_t2,
            "FINIQUITO DOS EVENTOS": fini2 * dias_finiquito2,
            "SUELDO INTEGRADO 2 (IMSS)": sueldo_integrado2 * total_dias_t2,
            "SUELDO COTIZACIÓN S/F DOS EVENTOS": sueldo_cotizacion2 * total_dias_t2,
            
            "SUELDO POR COBRAR DOS EVENTOS": total_dos,

            "SALARIO DIARIO TRES EVENTOS (P001)": salario_base_tres * total_dias_t3,
            "AGUINALDO 3 (P002)": aguinaldo3 * dias_finiquito2,
            "VACACIONES 3 (P001)": vacaciones3 * dias_finiquito2,
            "PRIMA VACACIONAL 3 (P021)": prima_vacacional3 * dias_finiquito2,
            "PRIMA DOMINICAL 3 (P020)": prima_dominical3 * total_dias_t3,
            "PREMIO ASISTENCIA 3 (P049)": prem_asis3 * total_dias_t3,
            "PREMIO PUNTUALIDAD 3 (P010)": prem_punt3 * total_dias_t3,
            "FINIQUITO TRES EVENTOS": fini3 * dias_finiquito2,
            "SUELDO INTEGRADO 3 (IMSS)": sueldo_integrado3 * total_dias_t3,
            "SUELDO COTIZACIÓN S/F TRES EVENTOS ": sueldo_cotizacion3 * total_dias_t3,
            
            "SUELDO POR COBRAR TRES EVENTOS": total_tres,
            
            "TOTAL DE LA NOMINA SIN DEDUCCIONES": total,
            "EFECTIVO": efectivo,
            "BASE ISR": base_isr,
            "ISR": isr_calculado,
            "INFONAVIT": infonavit,
            "PRESTAMO": prestamo,
            "IMSS": retencion_dias,
            "TOTAL NETO A PAGAR": total - deducciones,

            "OBSERVACIONES": observaciones,
        }
        nuevos_registros.append(nuevo_registro)

        
        nomina_uno_registro = {
            "BODEGA": bodega,
            "EVENTO": evento,
            "NOMBRE": nombre_completo,
            "PERIODO": periodo,
            "SEMANA NOI": " ",
            "DIAS FINIQ": dias_finiquito + dias_finiquito2 + dias_finiquito3,
            "DIAS": total_dias + total_dias_t2 + total_dias_t3,
            "SBC": sueldo_integrado1,
            "S.D.": salario_base,
            "SUELDO": salario_base * total_dias, 
            "TOTAL HORAS EXTRA": horas_extra,                    
            "PASIST": prem_asis * total_dias,
            "PPUNT": prem_punt * total_dias,
            "HRS EXT": he,
            "TIME EXT DOBLE": " ",
            "PRIMA DOM IMPORTE": prima_dominical1 * total_dias,
            "DIA FESTIVO": dia_festivo,
            "BONO": bono,
            "AGUI DIAS": "15",
            "AGUI IMPORTE": aguinaldo * dias_finiquito,
            "VAC DIAS": "12",
            "VAC IMPORTE": vacaciones * dias_finiquito,
            "P.V. %": "25%",
            "P.VAC IMPORTE": prima_vacacional * dias_finiquito,
            "PERCEPCIÓN TOTAL": total_uno,
            "BASE ISR": base_isr,
            "IMSS": retencion_dias,
            "ISR (SUBSIDIO)": isr_calculado,
            "PRESTAMO": prestamo,
            "CREDITO INFONAVIT": infonavit,
            "DEDUCCIÓN TOTAL": deducciones,
            "NOMINA NETA": total - deducciones,
            "NOMINA": " ",
            "FINIQUITO": total - deducciones,
            "EFECTIVO": efectivo,
            "NETO A PAGAR": total - deducciones,
            "STATUS": " ",
            "DIFERENCIA": " ",
            "COMENTARIOS": " ",
        }
        nomina_uno_data.append(nomina_uno_registro)

        nomina_dos_registro = {
            "BODEGA": bodega,
            "EVENTO": evento,
            "PERIODO TRABAJADO": periodo,
            "NOMBRE COMPLETO": nombre_completo,
            "NOMINA": total,
            "FINIQUITO": round(((fini1*dias_finiquito) + (fini2*dias_finiquito2) + (fini3*dias_finiquito3)),2),
            "PRESTAMO": prestamo,
            "EFECTIVO": efectivo,
            "NETO A PAGAR": total - deducciones,
        }
        nomina_dos_data.append(nomina_dos_registro)
    
    # Crear DataFrame con los nuevos registros
    df_resultado = pd.DataFrame(nuevos_registros)
    df_nomina_uno = pd.DataFrame(nomina_uno_data)
    df_nomina_dos = pd.DataFrame(nomina_dos_data)

    return df_resultado, df_nomina_uno, df_nomina_dos
    
# Generar archivo Excel para descargar
def to_excel_con_sheets(df1, df2, df3):
    if not isinstance(df1, pd.DataFrame) or not isinstance(df2, pd.DataFrame) or not isinstance(df3, pd.DataFrame):
        raise ValueError("Se esperaban objetos DataFrame, pero se recibió un tipo incorrecto.")
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df1.to_excel(writer, index=False, sheet_name='Nuevo Registro')
        df2.to_excel(writer, index=False, sheet_name='Nómina Uno')
        df3.to_excel(writer, index=False, sheet_name='Nómina Dos')
    return output.getvalue()