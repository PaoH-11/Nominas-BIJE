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
def calcular_finiquito(salario_base, dias_finiquito, prem_punt_pct, prem_asis_pct, incluir_prima_dominical):
    aguinaldo = round((salario_base * (15 / 365)), 2)
    vacaciones = round((salario_base * (12 / 365)), 2)
    prima_vacacional = round(vacaciones * 0.25, 2)  
    prima_dominical = round(((1 * 0.25) / 7) * salario_base, 2) if incluir_prima_dominical else 0
    prem_asis = round(salario_base * prem_punt_pct, 2)
    prem_punt = round(salario_base * prem_asis_pct, 2)
    sueldo_integrado = round(salario_base + aguinaldo + vacaciones + prima_vacacional + prima_dominical, 2)
    finiquito = round((aguinaldo + vacaciones + prima_vacacional + prima_dominical + prem_asis + prem_punt) * dias_finiquito, 2)
    
    return aguinaldo, vacaciones, prima_vacacional, prima_dominical, prem_asis, prem_punt, sueldo_integrado, finiquito

# Función para obtener el salario base y el porcentaje de la prima vacacional según el puesto y la zona

def obtener_salario_y_premio(puesto, zona, total_dias_t2):
    if puesto == 'DEMOSTRADOR':
        if zona == 'INTERIOR':
            return SALARIO_BASE[0], SALARIO_BASE[1], 0.1, 0.1, 0.1, 0.1, True, True
        elif zona == 'FRONTERA':
            if total_dias_t2 >= 1:
                return SALARIO_BASE[2], SALARIO_BASE[3], 0.068, 0.068, 0.1, 0.1, False, True
            else:
                return SALARIO_BASE[2], SALARIO_BASE[3], 0.068, 0.068, 0.1, 0.1, False, False       
        elif zona == 'ESPECIAL':
            return SALARIO_BASE[4], SALARIO_BASE[5], 0.1, 0.1, 0.1, 0.1, True, True
        elif zona == 'INTERIOR JOYERÍA Y DEGUSTACIÓN':
            return SALARIO_BASE[6], 0, 0.1, 0.1, 0.1, 0.1, True, True
        elif zona == 'ESPECIAL JOYERÍA Y DEGUSTACIÓN':
            return SALARIO_BASE[7], 0, 0.1, 0.1, 0.1, 0.1, True, True
    elif puesto == 'COORDINADOR':
        if zona == 'INTERIOR':
            return SALARIO_BASE[8],  0, 0, 0.1, 0, 0, True, True
        elif zona == 'FRONTERA':
            return SALARIO_BASE[11], 0, 0, 0, 0, 0, False, True
        elif zona == 'ESPECIAL':
            return SALARIO_BASE[13], 0, 0.1, 0.1 , 0, 0, True, True
        elif zona == 'INTERIOR JOYERÍA Y DEGUSTACIÓN':
            return SALARIO_BASE[15], 0, 0.1, 0.1, 0, 0, True, True
        elif zona == 'ESPECIAL JOYERÍA Y DEGUSTACIÓN':
            return SALARIO_BASE[16], 0, 0.1, 0.1 , 0, 0, True, True
    elif puesto == 'COORDINADOR Y DEMOSTRADOR':
        if zona == 'INTERIOR':
            return SALARIO_BASE[10], 0, 0.1, 0.1, 0, 0, True, True
        elif zona == 'FRONTERA':
            return SALARIO_BASE[12], 0, 0.1, 0.1, 0, 0, True, True
        elif zona == 'ESPECIAL':
            return SALARIO_BASE[14], 0, 0.1, 0.1, 0, 0, True, True

def procesar_datos(df_empleados):
    nuevos_registros = []
    
    for _, row in df_empleados.iterrows():
        puesto = row['puesto']
        zona = row['zona']
        total_dias = row['total días un evento']
        total_dias_t2 = row['total días dos eventos']
        dias_finiquito = row['total días finiquito uno']
        dias_finiquito2 = row['total días finiquito dos']
        horas_extra = row.get('horas extra', 0)
        cant_eventos = row.get('cant eventos', 0)
        observaciones = row.get('observaciones', '')
        
        # Obtener salario y premios según el puesto y la zona
        salario_base, salario_base_dos, prem_punt_pct1, prem_asis_pct1, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical1, incluir_prima_dominical2 = obtener_salario_y_premio(puesto, zona, total_dias_t2)
        
        # Calcular finiquitos para uno y dos eventos
        aguinaldo, vacaciones, prima_vacacional, prima_dominical1, prem_asis, prem_punt, sueldo_integrado1, finiquito = calcular_finiquito(salario_base, dias_finiquito, prem_punt_pct1, prem_asis_pct1, incluir_prima_dominical1)
        
        if total_dias_t2 >= 1:
            aguinaldo2, vacaciones2, prima_vacacional2, prima_dominical2, prem_asis2, prem_punt2, sueldo_integrado2, finiquito2 = calcular_finiquito(salario_base_dos, dias_finiquito2, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical2)
        else:
            aguinaldo2 = vacaciones2 = prima_vacacional2 = prima_dominical2 = prem_asis2 = prem_punt2 = sueldo_integrado2 = finiquito2 = 0

        he = horas_extra * 50

        sueldo_uno = round((salario_base * total_dias), 2)
        sueldo_dos = round(salario_base_dos * total_dias_t2, 2)
        sueldo_cotizacion1 = round(salario_base + prima_dominical1 + prem_asis + prem_punt, 2)
        sueldo_cotizacion2 = round(salario_base_dos + prima_dominical2 + prem_asis2 + prem_punt2, 2) if total_dias_t2 >= 1 else 0

        bono_coordinador = 0

        if puesto == 'COORDINADOR' and zona == 'INTERIOR':
            if cant_eventos == 0:  
                total_uno = round(sueldo_uno + finiquito, 2)
                bono_coordinador = 0
            elif cant_eventos == 1:
                total_uno = round((sueldo_uno + finiquito) * 2, 2)                  
                bono_coordinador = 250                
            elif cant_eventos == 2:
                total_uno = round((sueldo_uno + finiquito) * 3, 2)
                bono_coordinador = 500
        else:
            total_uno = round(sueldo_uno + finiquito, 2)

        if total_dias_t2 == 0:
            salario_base_dos = 0

        total_dos = round(sueldo_dos + finiquito2, 2)
        total = round(total_uno + total_dos + he, 2)

        nuevo_registro = {
            "Puesto": puesto,
            "Zona": zona,
            "TOTAL DE DIAS UN EVENTO": total_dias,
            "TOTAL DÍAS DOS EVENTOS": total_dias_t2,
            "TOTAL DÍAS FINIQUITO UN EVENTO": dias_finiquito,
            "TOTAL DÍAS FINIQUITO DOS EVENTOS": dias_finiquito2,
            "SALARIO DIARIO UN EVENTO (P001)": salario_base,
            "AGUINALDO (P002)": aguinaldo,
            "VACACIONES (P001)": vacaciones,
            "PRIMA VACACIONAL (P021)": prima_vacacional,
            "PRIMA DOMINICAL (P020)": prima_dominical1,
            "PREMIO ASISTENCIA (P049)": prem_asis,
            "PREMIO PUNTUALIDAD (P010)": prem_punt,
            "FINIQUITO UN EVENTO": finiquito,
            "SUELDO INTEGRADO (IMSS)": sueldo_integrado1,
            "SUELDO COTIZACIÓN": sueldo_cotizacion1,
            "SUELDO POR COBRAR UN EVENTO": total_uno,
            "SALARIO DIARIO DOS EVENTOS (P001)": salario_base_dos,
            "AGUINALDO 2 (P002)": aguinaldo2,
            "VACACIONES 2 (P001)": vacaciones2,
            "PRIMA VACACIONAL 2 (P021)": prima_vacacional2,
            "PRIMA DOMINICAL 2 (P020)": prima_dominical2,
            "PREMIO ASISTENCIA 2 (P049)": prem_asis2,
            "PREMIO PUNTUALIDAD 2 (P010)": prem_punt2,
            "FINIQUITO DOS EVENTOS": finiquito2,
            "SUELDO INTEGRADO 2 (IMSS)": sueldo_integrado2,
            "SUELDO COTIZACIÓN 2": sueldo_cotizacion2,
            "SUELDO POR COBRAR DOS EVENTOS": total_dos,
            "TOTAL DE LA NOMINA": total,
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