import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
st.markdown(
    """
    <style>
    /* Estilo para el fondo de la aplicación con degradado */
    .stApp {
        background-image: radial-gradient(circle at 34.8%, #bad4ee 0, #97bee6 25%, #70a8dd 50%, #4192d4 75%, #007dcc 100%);
        height: 100vh;
        padding: 0;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)
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
def calcular_nomina(salario_base, prem_punt_pct, prem_asis_pct, incluir_prima_dominical):
    aguinaldo = round((salario_base * (15 / 365)), 2)
    vacaciones = round((salario_base * (12 / 365)), 2)
    prima_vacacional = round(vacaciones * 0.25, 2)  
    prima_dominical = round(((1 * 0.25) / 7) * salario_base, 2) if incluir_prima_dominical else 0
    prem_asis = round(salario_base * prem_punt_pct, 2)
    prem_punt = round(salario_base * prem_asis_pct, 2)
    sueldo_integrado = round(salario_base + aguinaldo + vacaciones + prima_vacacional + prima_dominical, 2)
    fini = round(aguinaldo + vacaciones + prima_vacacional, 2)
 
    return aguinaldo, vacaciones, prima_vacacional, prima_dominical, prem_asis, prem_punt, sueldo_integrado, fini

# Función para obtener el salario base y el porcentaje de la prima vacacional según el puesto y la zona
def calcular_isr(base_isr):
    for tarifa in tarifas_isr:
        if tarifa["limite_inferior"] <= base_isr <= tarifa["limite_superior"]:
            isr = tarifa["cuota_fija"] + (base_isr - tarifa["limite_inferior"]) * tarifa["porcentaje"]
            return round(isr, 2)        
    return 0.0

def obtener_salario_y_premio(puesto, zona, total_dias_t2):
    if puesto == 'DEMOSTRADOR':
        if zona == 'INTERIOR':
            return SALARIO_BASE[0], SALARIO_BASE[1], 0, 0.1, 0.1, 0.1, 0.1, True, True, False
        elif zona == 'FRONTERA':
            if total_dias_t2 >= 1:
                return SALARIO_BASE[2], SALARIO_BASE[3], 0, 0.068, 0.068, 0.1, 0.1, False, True, False
            elif total_dias_t2 == 0:
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

def app():
    st.title("CALCULADORA DE NÓMINAS")
    st.markdown("""
    <style>
    .stAlert {
        background-color: #1E3A8A; 
        border-radius: 10px;
        color: white;  
    }
    </style>
    """, unsafe_allow_html=True)

    st.info('Rellenar los campos requeridos', icon="ℹ️")
    conn = st.connection("gsheets3", type=GSheetsConnection)

    df = conn.read(worksheet="Nómina", usecols=list(range(60)), ttl=5)
    df = df.dropna(how="all")

    df_aux = conn.read(worksheet="Datos", usecols=list(range(10)), ttl=5)
    df_aux = df_aux.dropna(how="all")

    df_aux2= conn.read(worksheet="Nómina General", usecols=list(range(40)), ttl=5)
    df_aux2 = df_aux2.dropna(how="all")

    df_aux3= conn.read(worksheet="Nómina Doble Turno", usecols=list(range(40)), ttl=5)
    df_aux3 = df_aux3.dropna(how="all")

    NOMBRES = df_aux.iloc[:, 0].dropna().tolist()
    EVENTOS = df_aux.iloc[:, 1].dropna().tolist()
    BODEGA = df_aux.iloc[:, 2].dropna().tolist()
    PUESTO = df_aux.iloc[:, 3].dropna().tolist()
    SALARIOS = df_aux.iloc[:, 4].dropna().tolist()
    ZONA = ["INTERIOR", "FRONTERA", "ESPECIAL", "INTERIOR JOYERÍA Y DEGUSTACIÓN", "ESPECIAL JOYERÍA Y DEGUSTACIÓN"]
    HORARIO = ["9 A 4", "2 A 9", "COORDINACIÓN"]
    SEGURO = ["FINIQUITO", "NOMINA", "CORTE"]
    NOMINA = ["FINIQUITO", "CORTE"]

    with st.form(key="empleado_form"):
        
        c1, c2, c3 = st.columns(3)
        with c1:
            puesto = st.selectbox("Puesto*", options=PUESTO)
            evento = st.selectbox("Evento*", options=EVENTOS)
            observaciones = st.text_input(label="Observaciones")
            estatus_nomina = st.selectbox("Estatus de la nómina", options=NOMINA)
            st.write("Primer evento")
            total_dias = st.number_input(label="Total de días trabajados*", min_value=1, max_value=21, key="total_dias_1")
            dias_finiquito = st.number_input(label="Días Finiquito 1 Turno", min_value=0, max_value=21, key="dias_finiquito_1")
            dia_festivos_c = st.checkbox(label="Día festivo")
        with c2:
            bodega = st.selectbox("Bodega*", options=BODEGA)
            nombre_empleado = st.selectbox("Nombre completo", options=NOMBRES)
            inicio = st.date_input(label="Día inicio*")
            alta_seguro = st.selectbox("Alta del seguro social", options=SEGURO)
            st.write("Segundo evento")
            total_dias_t2 = st.number_input(label="Días trabajados con doble evento", min_value=0, max_value=21, key="total_dias_2")
            dias_finiquito2 = st.number_input(label="Días Finiquito", min_value=0, max_value=21, key="dias_finiquito_2")     
            dia_festivos = st.selectbox(label="Día festivo", options=SALARIOS)            
        with c3:
            zona = st.selectbox("Zona*", options=ZONA)
            horario = st.selectbox("Horario", options=HORARIO)
            fin = st.date_input(label="Día fin*")
            horas_extra = st.number_input(label="Horas extra", max_value=8, min_value=0, key="horas_extra")  
            st.write("Tercer evento")
            total_dias_t3 = st.number_input(label="Días trabajados con tres eventos", min_value=0, max_value=21, key="total_dias_3")
            dias_finiquito3 = st.number_input(label="Días Finiquito", min_value=0, max_value=21, key="dias_finiquito_3") 
            bono = st.number_input(label="Bono", min_value=0, key="bono")   
        st.subheader("Deducciones")
        
        c4, c5, c6 = st.columns(3)  
        
        with c4:            
            infonavit = st.number_input(label="Infonavit", min_value=0, key="infonavit")
           
        with c5:
            prestamo = st.number_input(label="Prestamo", min_value=0, key="prestamo")
        with c6:            
            imss = st.number_input(label="IMSS", min_value=0, key="imss")      
            
        st.markdown("**Requerido*")

        submit_button = st.form_submit_button(label="Registrar")

    if submit_button:
        if puesto == 'DEMOSTRADOR' and total_dias_t3 >= 1:
            st.warning("Demostrador no puede tener tres eventos")
            st.stop()            
        else:
            salario_base, salario_base_dos, salario_base_tres, prem_punt_pct1, prem_asis_pct1, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical1, incluir_prima_dominical2, incluir_prima_dominical3 = obtener_salario_y_premio(puesto, zona, total_dias_t2)

            aguinaldo, vacaciones, prima_vacacional, prima_dominical1, prem_asis, prem_punt, sueldo_integrado1, fini = calcular_nomina(salario_base, prem_punt_pct1, prem_asis_pct1, incluir_prima_dominical1)
            
            if total_dias_t2 >= 1:
                aguinaldo2, vacaciones2, prima_vacacional2, prima_dominical2, prem_asis2, prem_punt2, sueldo_integrado2, fini2 = calcular_nomina(salario_base_dos, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical2)
            else:
                aguinaldo2 = vacaciones2 = prima_vacacional2 = prima_dominical2 = prem_asis2 = prem_punt2 = sueldo_integrado2 = fini2 =0
            
            if total_dias_t3 >= 1:
                aguinaldo3, vacaciones3, prima_vacacional3, prima_dominical3, prem_asis3, prem_punt3, sueldo_integrado3, fini3 = calcular_nomina(salario_base_tres, prem_punt_pct1, prem_asis_pct1, incluir_prima_dominical3)
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
                fini = 0
            if dias_finiquito2 == 0:
                fini2 = 0
            if dias_finiquito3 == 0:
                fini3 = 0

            total_uno = round(sueldo_cotizacion1 * total_dias, 2) if dias_finiquito == 0 else round(sueldo_cotizacion1 * total_dias + (fini * dias_finiquito), 2)
            total_dos = round(sueldo_cotizacion2 * total_dias_t2, 2) if dias_finiquito2 == 0 else round(sueldo_cotizacion2 * total_dias_t2 + (fini2 * dias_finiquito2), 2)
            total_tres = round(sueldo_cotizacion3 * total_dias_t3, 2) if dias_finiquito3 == 0 else round(sueldo_cotizacion3 * total_dias_t3 + (fini3 * dias_finiquito3), 2)
            
            if dia_festivos_c:  
                dia_festivo = round(dia_festivos * 2, 2)              
                total_uno += dia_festivo 
            else:
                dia_festivo = 0

            if bono > 0:
                total_uno += bono                
            base_isr = round((salario_base + prem_asis + prem_punt) * total_dias + ((he / 2) + dia_festivo + bono + (vacaciones * dias_finiquito)),2) 
            total = round(total_uno + total_dos + total_tres + he, 2)

            isr_calculado = calcular_isr(base_isr)        

            empleado_data = pd.DataFrame(
                [
                    {
                        "BODEGA": bodega,
                        "EVENTO": evento,
                        "NOMBRE COMPLETO": nombre_empleado,
                        "STATUS DE NOMINA": estatus_nomina,
                        "ALTA DEL SEGURO SOCIAL": alta_seguro,
                        "PERIODO":  f"{inicio.strftime('%Y-%m-%d')} al {fin.strftime('%Y-%m-%d')}",                        
                        "HORARIO": horario,  
                        "DÍAS FESTIVOS": dia_festivo,                      
                        "BONO": he,                        
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
                        "FINIQUITO UN EVENTO": fini * dias_finiquito,
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
                        "FINIQUITO DOS EVENTOS":fini2 * dias_finiquito2,
                        "SUELDO INTEGRADO 2 (IMSS)": sueldo_integrado2 * total_dias_t2,
                        "SUELDO COTIZACIÓN S/F DOS EVENTOS": sueldo_cotizacion2 * total_dias_t2,
                       
                        "SUELDO POR COBRAR DOS EVENTOS": total_dos,

                        "SALARIO BASE TRES EVENTOS": salario_base_tres,
                        "SALARIO DIARIO TRES EVENTOS (P001)": salario_base_tres * total_dias_t3,
                        "AGUINALDO 3 (P002)": aguinaldo3 * dias_finiquito3,
                        "VACACIONES 3 (P001)": vacaciones3  * dias_finiquito3,
                        "PRIMA VACACIONAL 3 (P021)": prima_vacacional3 * dias_finiquito3,
                        "PRIMA DOMINICAL 3 (P020)": prima_dominical3 * total_dias_t3,
                        "PREMIO ASISTENCIA 3 (P049)": prem_asis3 * total_dias_t3,
                        "PREMIO PUNTUALIDAD 3 (P010)": prem_punt3 * total_dias_t3,
                        "FINIQUITO TRES EVENTOS": fini3 * dias_finiquito3,
                        "SUELDO INTEGRADO 3 (IMSS)": sueldo_integrado3 * total_dias_t3,
                        "SUELDO COTIZACIÓN S/F TRES EVENTOS ": sueldo_cotizacion3 * total_dias_t3,
                       
                        "SUELDO POR COBRAR TRES EVENTOS": total_tres,

                        "TOTAL DE LA NOMINA": total,
                        "BASE ISR": base_isr,
                        "ISR": isr_calculado,
                        "INFONAVIT": infonavit,
                        "PRESTAMO": prestamo,
                        "IMSS": imss,
                        "TOTAL A PAGAR": total - isr_calculado - infonavit - prestamo - imss,

                        "OBSERVACIONES": observaciones,
                    }
                ]
            )

            updated_df = pd.concat([df, empleado_data], ignore_index=True)

            conn.update(worksheet="Nómina", data=updated_df)

            nomina_uno_data = pd.DataFrame(
                [
                    {
                        "BODEGA": bodega,
                        "EVENTO": evento,
                        "PERIODO TRABAJADO": f"{inicio.strftime('%Y-%m-%d')} al {fin.strftime('%Y-%m-%d')}",
                        "NOMBRE COMPLETO ": nombre_empleado,
                        "ESTATUS DE NÓMINA": estatus_nomina,
                        "ALTA DEL SEGURO SOCIAL ": alta_seguro,                        
                        "HORARIO": horario,  
                        "HORAS EXTRAS AUTORIZADAS": horas_extra,
                        "TOTAL DE DÍAS TRABAJADOS": total_dias,
                        "TOTAL SUELDO": total_uno,                    
                        "TOTAL DE HORAS EXTRAS": he,
                        "TOTAL CAPACITACION PROPORCIONADA POR PROVEEDOR": 0, 
                        "ISR": isr_calculado,
                        "BANCO": " ",
                        "CUENTA": " ",
                        "TARJETA": " ",
                        "CLABE INTERBANCARIA": " ",
                        "RFC": " ",
                        "OBSERVACIONES": observaciones,                      
                    }
                ]
            )

            updated_df = pd.concat([df_aux2, nomina_uno_data], ignore_index=True)

            conn.update(worksheet="Nómina General", data=updated_df)
            if total_dias_t2 > 0:
                nomina_dos_data = pd.DataFrame(
                    [
                        {
                            "BODEGA": bodega,
                            "EVENTO": evento,
                            "PERIODO TRABAJADO": f"{inicio.strftime('%Y-%m-%d')} al {fin.strftime('%Y-%m-%d')}",
                            "NOMBRE COMPLETO": nombre_empleado,
                            "ESTATUS DE NÓMINA": estatus_nomina,
                            "ALTA DEL SEGURO SOCIAL": alta_seguro,                        
                            "HORARIO": horario,  
                            "HORAS EXTRAS AUTORIZADAS": horas_extra,
                            "TOTAL DE DÍAS DOBLES TRABAJADOS": total_dias_t2,
                            "TOTAL SUELDO": total_dos,                    
                            "TOTAL DE HORAS EXTRAS": he,
                            "TOTAL CAPACITACION PROPORCIONADA POR PROVEEDOR": 0, 
                            "BANCO": " ",
                            "CUENTA": " ",
                            "TARJETA": " ",
                            "CLABE INTERBANCARIA": " ",
                            "RFC": " ",
                            "OBSERVACIONES": observaciones,                      
                        }
                    ]
                )

                updated_df = pd.concat([df_aux3, nomina_dos_data], ignore_index=True)

                conn.update(worksheet="Nómina Doble Turno", data=updated_df)

            st.success(f"Datos de {nombre_empleado} registrados correctamente.")
    with st.expander("Nóminas"):    
        st.dataframe(df)


if __name__ == "__main__":
    app()
