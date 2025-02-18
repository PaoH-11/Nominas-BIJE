import streamlit as st
import mysql.connector
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from estructura.proceso_calculadora import calcular_nomina, calcular_isr, obtener_salario_y_premio
st.markdown(
    """
    <style>
    /* Degradado de fondo*/
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

    # Obtener valores únicos para la columna 'ZONA'
    if not data.empty:
        zonas_unicas = data['zona'].unique().tolist()
        puestos_unicos = data['puesto'].unique().tolist()
    else:
        zonas_unicas = ["INTERIOR", "EXTERIOR", "ESPECIAL"]
        puestos_unicos = ["DEMOSTRADOR", "COORDINADOR"]

    #Conexión a Google Sheets
    conn = st.connection("gsheets3", type=GSheetsConnection)
    df = conn.read(worksheet="Nómina", usecols=list(range(60)), ttl=5).dropna(how="all")
    df_aux = conn.read(worksheet="Datos", usecols=list(range(10)), ttl=5).dropna(how="all")
    df_aux2 = conn.read(worksheet="Nómina General", usecols=list(range(40)), ttl=5).dropna(how="all")
    df_aux3 = conn.read(worksheet="Nómina Doble Turno", usecols=list(range(40)), ttl=5).dropna(how="all")
    df_ret = conn.read(worksheet="Retención", usecols=[0, 1], ttl=5).dropna(how="all")
    
    #Obtener listas de nombres, eventos, bodegas, puestos y salarios
    NOMBRES = df_aux.iloc[:, 0].dropna().tolist()
    EVENTOS = df_aux.iloc[:, 1].dropna().tolist()
    BODEGA = df_aux.iloc[:, 2].dropna().tolist()
    PUESTO = puestos_unicos
    SALARIOS = df_aux.iloc[:, 4].dropna().tolist() 
    ZONA = zonas_unicas
    HORARIO = ["9 A 4", "2 A 9", "COORDINACIÓN"]
    SEGURO = ["FINIQUITO", "NOMINA", "CORTE"]
    NOMINA = ["FINIQUITO", "CORTE"]
    column_names = list(df_ret.columns)
    SALARIO_BASE_COL = column_names[0]  
    RETENCION_COL = column_names[1]

    if len(df_ret.columns) >= 2:
        SALARIO_BASE_COL = df_ret.columns[0]
        RETENCION_COL = df_ret.columns[1]
    else:
        st.error("El DataFrame 'Retención' no tiene suficientes columnas.")
        st.stop()
    
    #Formulario para ingresar los datos del empleado
    with st.form(key="empleado_form"):        
        c1, c2, c3 = st.columns(3)
        with c1:
            puesto = st.selectbox("Puesto*", PUESTO)
            evento = st.selectbox("Evento*", options=EVENTOS)
            observaciones = st.text_input(label="Observaciones")
            estatus_nomina = st.selectbox("Estatus de la nómina", options=NOMINA)
            st.write("Primer evento")
            total_dias = st.number_input(label="Total de días trabajados*", min_value=1, max_value=21, key="total_dias_1")
            dias_finiquito = st.number_input(label="Días Finiquito 1 Turno", min_value=0, max_value=21, key="dias_finiquito_1")
            dia_festivos_c = st.checkbox(label="Día festivo")
            dia_festivos = st.selectbox(label="Día festivo", options=SALARIOS) 
        with c2:
            bodega = st.selectbox("Bodega*", options=BODEGA)
            nombre_empleado = st.selectbox("Nombre completo", options=NOMBRES)
            inicio = st.date_input(label="Día inicio*")
            alta_seguro = st.selectbox("Alta del seguro social", options=SEGURO)
            st.write("Segundo evento")
            total_dias_t2 = st.number_input(label="Días trabajados con doble evento", min_value=0, max_value=21, key="total_dias_2")
            dias_finiquito2 = st.number_input(label="Días Finiquito", min_value=0, max_value=21, key="dias_finiquito_2")     
            efectivo = st.number_input(label="Efectivo", min_value=0, key="efectivo")           
        with c3:
            zona = st.selectbox("Zona*", ZONA)
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
            selected_sdi = st.selectbox(label="Seleccione su salario base", options=df_ret[SALARIO_BASE_COL].unique(), key="selected_sdi")
        
        retencion = df_ret[df_ret[SALARIO_BASE_COL] == selected_sdi][RETENCION_COL].values
        retencion = retencion[0] if len(retencion) > 0 else 0  
                    
        st.markdown("**Requerido*")

        submit_button = st.form_submit_button(label="Registrar")

    if submit_button:
        if puesto == 'Demostrador' and total_dias_t3 >= 1:
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
            retencion_dias = round((retencion/7) * total_dias, 2)
            deducciones = isr_calculado + infonavit + prestamo + retencion_dias

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
                        "EFECTIVO": efectivo,
                        "TOTAL DE LA NOMINA": total,
                        "BASE ISR": base_isr,
                        "ISR": isr_calculado,
                        "INFONAVIT": infonavit,
                        "PRESTAMO": prestamo,
                        "IMSS": retencion_dias,
                        "TOTAL A PAGAR": total - deducciones ,
                        "TOTAL SIN DEDUCCIONES": total,
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
                        "NOMBRE": nombre_empleado,
                        "FECHA ALTA": inicio,
                        "FECHA BAJA": fin,
                        "SEMANA NOI": " ",
                        "DIAS FINIQ": dias_finiquito,
                        "DIAS": total_dias,
                        "SBC": sueldo_integrado1,
                        "S.D.": salario_base,
                        "SUELDO": salario_base * total_dias,                     
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

                        "FINIQUITO": round(((fini*dias_finiquito) + (fini2*dias_finiquito2) + (fini3*dias_finiquito3)),2),
                        "EFECTIVO": efectivo,
                        "NETO A PAGAR": total - deducciones,
                        "TOTAL SIN DEDUCCIONES": total,
                        "STATUS": " ",
                        "DIFERENCIA": " ",
                        "COMENTARIOS": " ",
                    }                       
                ]
            )

            updated_df = pd.concat([df_aux2, nomina_uno_data], ignore_index=True)

            conn.update(worksheet="Nómina General", data=updated_df)
            
            nomina_dos_data = pd.DataFrame(
                    [
                        {
                            "BODEGA": bodega,
                            "EVENTO": evento,
                            "PERIODO TRABAJADO": f"{inicio.strftime('%Y-%m-%d')} al {fin.strftime('%Y-%m-%d')}",
                            "NOMBRE COMPLETO": nombre_empleado,    
                            "PRESTAMO": prestamo,   
                            "NÓMINA": total,
                            "FINIQUITO": round(((fini*dias_finiquito) + (fini2*dias_finiquito2) + (fini3*dias_finiquito3)),2),
                            "EFECTIVO": efectivo,    
                            "INFONAVIT": infonavit,  
                            "NETO A PAGAR": total - deducciones,                                                       
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
