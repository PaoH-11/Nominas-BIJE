import streamlit as st
import pandas as pd
from io import BytesIO

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

# Función para obtener el salario base y el porcentaje de la prima vacacional según el puesto y la zona

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

def procesar_datos(df_empleados):
    nuevos_registros = []
    
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
        
        # Obtener salario y premios según el puesto y la zona
        salario_base, salario_base_dos, salario_base_tres, prem_punt_pct1, prem_asis_pct1, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical1, incluir_prima_dominical2, incluir_prima_dominical3 = obtener_salario_y_premio(puesto, zona, total_dias_t2)
        # Calcular finiquitos para uno y dos eventos
        aguinaldo, vacaciones, prima_vacacional, prima_dominical1, prem_asis, prem_punt, sueldo_integrado1, fini1  = calcular_finiquito(salario_base, prem_punt_pct1, prem_asis_pct1, incluir_prima_dominical1)
        
        if total_dias_t2 >= 1:
            aguinaldo2, vacaciones2, prima_vacacional2, prima_dominical2, prem_asis2, prem_punt2, sueldo_integrado2, fini2 = calcular_finiquito(salario_base_dos, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical2)
        else:
            aguinaldo2 = vacaciones2 = prima_vacacional2 = prima_dominical2 = prem_asis2 = prem_punt2 = sueldo_integrado2 = fini2 = 0

        if total_dias_t3 >= 1:
            aguinaldo3, vacaciones3, prima_vacacional3, prima_dominical3, prem_asis3, prem_punt3, sueldo_integrado3, fini3 = calcular_finiquito(salario_base_tres, prem_punt_pct1, prem_asis_pct1, incluir_prima_dominical3)
        else:
            aguinaldo3 = vacaciones3 = prima_vacacional3 = prima_dominical3 = prem_asis3 = prem_punt3 = sueldo_integrado3  = fini3 = 0

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
            
        total = round(total_uno + total_dos + total_tres + he, 2)

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

            "SALARIO DIARIO UN EVENTO (P001)": salario_base,
            "AGUINALDO (P002)": aguinaldo,
            "VACACIONES (P001)": vacaciones,
            "PRIMA VACACIONAL (P021)": prima_vacacional,
            "PRIMA DOMINICAL (P020)": prima_dominical1,
            "PREMIO ASISTENCIA (P049)": prem_asis,
            "PREMIO PUNTUALIDAD (P010)": prem_punt,
            "FINIQUITO UN EVENTO": fini1 * dias_finiquito,
            "SUELDO INTEGRADO (IMSS)": sueldo_integrado1,
            "SUELDO COTIZACIÓN S/F UN EVENTO": sueldo_cotizacion1 * total_dias,
            
            "SUELDO POR COBRAR UN EVENTO": total_uno,

            "SALARIO DIARIO DOS EVENTOS (P001)": salario_base_dos,
            "AGUINALDO 2 (P002)": aguinaldo2,
            "VACACIONES 2 (P001)": vacaciones2,
            "PRIMA VACACIONAL 2 (P021)": prima_vacacional2,
            "PRIMA DOMINICAL 2 (P020)": prima_dominical2,
            "PREMIO ASISTENCIA 2 (P049)": prem_asis2,
            "PREMIO PUNTUALIDAD 2 (P010)": prem_punt2,
            "FINIQUITO DOS EVENTOS": fini2 * dias_finiquito2,
            "SUELDO INTEGRADO 2 (IMSS)": sueldo_integrado2,
            "SUELDO COTIZACIÓN S/F DOS EVENTOS": sueldo_cotizacion2 * total_dias_t2,
            
            "SUELDO POR COBRAR DOS EVENTOS": total_dos,

            "SALARIO DIARIO TRES EVENTOS (P001)": salario_base_tres,
            "AGUINALDO 3 (P002)": aguinaldo3,
            "VACACIONES 3 (P001)": vacaciones3,
            "PRIMA VACACIONAL 3 (P021)": prima_vacacional3,
            "PRIMA DOMINICAL 3 (P020)": prima_dominical3,
            "PREMIO ASISTENCIA 3 (P049)": prem_asis3,
            "PREMIO PUNTUALIDAD 3 (P010)": prem_punt3,
            "FINIQUITO TRES EVENTOS": fini3 * dias_finiquito2,
            "SUELDO INTEGRADO 3 (IMSS)": sueldo_integrado3,
            "SUELDO COTIZACIÓN S/F TRES EVENTOS ": sueldo_cotizacion3 * total_dias_t3,
            
            "SUELDO POR COBRAR TRES EVENTOS": total_tres,
            
            "SUELDO POR COBRAR TOTAL": total,           
            "OBSERVACIONES": observaciones,
        }
        nuevos_registros.append(nuevo_registro)
    
    # Crear DataFrame con los nuevos registros
    df_resultado = pd.DataFrame(nuevos_registros)
    
    # Generar archivo Excel para descargar
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_resultado.to_excel(writer, index=False, sheet_name='Nómina Calculada')
    processed_file = output.getvalue()
    
    return processed_file

def app():
    st.title("CALCULADORA DE NÓMINAS")
    
    uploaded_file = st.file_uploader("Cargar archivo Excel con datos de empleados", type="xlsx")
    
    if uploaded_file is not None:
        df_empleados = pd.read_excel(uploaded_file)
        st.write("Datos cargados:")
        st.dataframe(df_empleados)
        
        if st.button("Procesar datos y descargar Nómina Calculada"):
            processed_file = procesar_datos(df_empleados)
            
            st.download_button(
                label="Descargar Nómina Calculada",
                data=processed_file,
                file_name="nomina_calculada.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    app()