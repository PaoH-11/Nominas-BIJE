import streamlit as st
import pandas as pd
from io import BytesIO
from streamlit_gsheets import GSheetsConnection
from pandas import ExcelWriter
import io

SALARIO_BASE = [265.6,  #INTERIOR DEMOSTRADOR UN EVENTO     [0]
                455,    #INTERIOR DEMOSTRADOR DOS EVENTOS   [1]
                374.89, #FRONTERA DEMOSTRADOR UN EVENTO     [2]
                594,    #FRONTERA DEMOSTRADOR DOS EVENTOS   [3]
                298.2,  #ESPECIAL DEMOSTRADOR UN EVENTO     [4]
                510,    #ESPECIAL DEMOSTRADOR DOS EVENTOS   [5]
                304,    #INTERIOR DEMOSTRADOR JOYERÍA Y DEGUSTACIÓN UN EVENTO [6]
                326,    #ESPECIAL DEMOSTRADOR JOYERÍA Y DEGUSTACIÓN UN EVENTO [7]
                205.27, #INTERIOR COORDINADOR UN EVENTO     [8]
                468.00, #INTERIOR COORDINADOR TRES EVENTOS  [9]
                455,    #INTERIOR COORDINADOR Y DEMOSTRADOR UN EVENTO [10]
                284,    #FRONTERA COORDINADOR UN EVENTO     [11]
                580,    #FRONTERA COORDINADOR Y DEMOSTRADOR UN EVENTO [12]
                209,    #ESPECIAL COORDINADOR UN EVENTO     [13]
                507,    #ESPECIAL COORDINADOR Y DEMOSTRADOR UN EVENTO [14]
                228,    #INTERIOR DEMOSTRADOR JOYERÍA Y DEGUSTACIÓN UN EVENTO [15]
                239,    #ESPECIAL DEMOSTRADOR JOYERÍA Y DEGUSTACIÓN UN EVENTO [16]                    
                ]
tarifas_isr = [
    {"limite_inferior": 0.01, "limite_superior": 171.78, "cuota_fija": 0.00, "porcentaje": 0.0192},
    {"limite_inferior": 171.78, "limite_superior": 1458.03, "cuota_fija": 3.29, "porcentaje": 0.0640},
    {"limite_inferior": 1458.03, "limite_superior": 2562.35, "cuota_fija": 85.61, "porcentaje": 0.1088},
    {"limite_inferior": 2562.35, "limite_superior": 2978.64, "cuota_fija": 205.80, "porcentaje": 0.16},
    {"limite_inferior": 2978.64, "limite_superior": 3566.22, "cuota_fija": 272.37, "porcentaje": 0.1792},
    {"limite_inferior": 3566.22, "limite_superior": 7192.64, "cuota_fija": 377.65, "porcentaje": 0.2136},
    {"limite_inferior": 7192.64, "limite_superior": 11336.57, "cuota_fija": 1152.27, "porcentaje": 0.2352},
    {"limite_inferior": 11336.57, "limite_superior": 21643.30, "cuota_fija": 2126.95, "porcentaje": 0.30},
    {"limite_inferior": 21643.30, "limite_superior": 28857.78, "cuota_fija": 5218.92, "porcentaje": 0.32},
    {"limite_inferior": 28857.78, "limite_superior": 86573.34, "cuota_fija": 7527.59, "porcentaje": 0.34},
    {"limite_inferior": 86573.34, "limite_superior": float("inf"), "cuota_fija": 27150.83, "porcentaje": 0.35}
]
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

def obtener_salario_y_premio(puesto, zona, total_dias_t2):
    if puesto == 'DEMOSTRADOR':
        if zona == 'INTERIOR':
            return SALARIO_BASE[0], SALARIO_BASE[1], 0, 0.1, 0.1, 0.1, 0.1, True, True, False
        elif zona == 'FRONTERA':
            if total_dias_t2 >= 1:
                return SALARIO_BASE[2], SALARIO_BASE[3], 0, 0.068, 0.068, 0.1, 0.1, False, True, False
            else:
                return SALARIO_BASE[2], SALARIO_BASE[3], 0, 0.068, 0.068, 0.1, 0.1, False, False, False
        elif zona == 'ESPECIAL':
            return SALARIO_BASE[4], SALARIO_BASE[5], 0, 0.1, 0.1, 0.1, 0.1, True, True, False
        elif zona == 'INTERIOR JOYERÍA Y DEGUSTACIÓN':
            return SALARIO_BASE[6], 0, 0, 0.1, 0.1, 0.1, 0.1, True, False, False
        elif zona == 'ESPECIAL JOYERÍA Y DEGUSTACIÓN':
            return SALARIO_BASE[7], 0, 0, 0.1, 0.1, 0.1, 0.1, True, False, False
    elif puesto == 'COORDINADOR':
        if zona == 'INTERIOR':
            return SALARIO_BASE[8], SALARIO_BASE[8], SALARIO_BASE[8], 0, 0.1, 0, 0.1, True, True, True
        elif zona == 'FRONTERA':
            return SALARIO_BASE[11], SALARIO_BASE[11], SALARIO_BASE[11], 0, 0, 0, 0, False, False, False
        elif zona == 'ESPECIAL':
            return SALARIO_BASE[13], SALARIO_BASE[13], SALARIO_BASE[13], 0.1, 0.1, 0.1, 0.1, True, True, True
        elif zona == 'INTERIOR JOYERÍA Y DEGUSTACIÓN':
            return SALARIO_BASE[15], SALARIO_BASE[15], SALARIO_BASE[15], 0.1, 0.1, 0.1, 0.1, True, True, True
        elif zona == 'ESPECIAL JOYERÍA Y DEGUSTACIÓN':
            return SALARIO_BASE[16], SALARIO_BASE[16], SALARIO_BASE[16], 0.1, 0.1, 0.1, 0.1, True, True, True
    elif puesto == 'COORDINADOR Y DEMOSTRADOR':
        if zona == 'INTERIOR':
            return SALARIO_BASE[10], 0, 0, 0.1, 0.1, 0, 0, True, False, False
        elif zona == 'FRONTERA':
            return SALARIO_BASE[12], 0, 0, 0.1, 0.1, 0, 0, True, False, False
        elif zona == 'ESPECIAL':
            return SALARIO_BASE[14], 0, 0, 0.1, 0.1, 0, 0, True, False, False
    
    # Si no se encuentra una combinación válida, devolver valores por defecto
    return 0, 0, 0, 0, 0, 0, 0, False, False, False

def procesar_datos(df_empleados, df_ret):
    nuevos_registros = []
    nomina_uno_data = []

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
            "FECHA ALTA": " ",
            "FECHA BAJA": " ",
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
    
    # Crear DataFrame con los nuevos registros
    df_resultado = pd.DataFrame(nuevos_registros)
    df_nomina_uno = pd.DataFrame(nomina_uno_data)

    return df_resultado, df_nomina_uno
    
    # Generar archivo Excel para descargar
def to_excel_con_sheets(df1, df2):
    if not isinstance(df1, pd.DataFrame) or not isinstance(df2, pd.DataFrame):
        raise ValueError("Se esperaban objetos DataFrame, pero se recibió un tipo incorrecto.")
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df1.to_excel(writer, index=False, sheet_name='Nuevo Registro')
        df2.to_excel(writer, index=False, sheet_name='Nómina Uno')
    return output.getvalue()

def app():
    st.title("CALCULADORA DE NÓMINAS")
    conn = st.connection("gsheets3", type=GSheetsConnection)

    df_ret = conn.read(worksheet="Retención", usecols=[0, 1], ttl=5).dropna(how="all")

    if len(df_ret.columns) < 2:
        st.error("El DataFrame 'Retención' no tiene suficientes columnas.")
        st.stop()
    
    uploaded_file = st.file_uploader("Cargar archivo Excel con datos de empleados", type="xlsx")
    
    if uploaded_file is not None:
        df_empleados = pd.read_excel(uploaded_file)
        st.write("Datos cargados:")
        with st.expander("Nóminas"): 
            st.dataframe(df_empleados)
        
        if st.button("Procesar datos"):
            df_resultado, df_nomina_uno = procesar_datos(df_empleados, df_ret)
            
            # Store the processed DataFrames in session state
            st.session_state['df_resultado'] = df_resultado
            st.session_state['df_nomina_uno'] = df_nomina_uno
            
            st.success("Datos procesados. Ahora puedes descargar los archivos.")

    # Only show download buttons if data has been processed
    if 'df_resultado' in st.session_state and 'df_nomina_uno' in st.session_state:
        if st.download_button(
            label="Descargar Nómina Completa",
            data=to_excel_con_sheets(st.session_state['df_resultado'], st.session_state['df_nomina_uno']),
            file_name="nomina_completa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            st.success("Nómina Completa descargada exitosamente.")

if __name__ == "__main__":
    app()