import streamlit as st
import pandas as pd
from io import BytesIO
from streamlit_gsheets import GSheetsConnection

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
def app():
    # Función para calcular la nómina

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
        

    def calcular_finiquito(salario_base, prem_punt_pct, prem_asis_pct, incluir_prima_dominical):
    # Función para calcular el finiquito con base en las reglas proporcionadas
        aguinaldo = round((salario_base * (15 / 365)), 2)
        vacaciones = round((salario_base * (12 / 365)), 2)
        prima_vacacional = round(vacaciones * 0.25, 2)  
        prima_dominical = round(((1 * 0.25) / 7) * salario_base, 2) if incluir_prima_dominical else 0
        prem_asis = round(salario_base * prem_punt_pct, 2)
        prem_punt = round(salario_base * prem_asis_pct, 2)
        sueldo_integrado = round(salario_base + aguinaldo + vacaciones + prima_vacacional + prima_dominical, 2)   
        fini = round((aguinaldo + vacaciones + prima_vacacional), 2)

        return aguinaldo, vacaciones, prima_vacacional, prima_dominical, prem_asis, prem_punt, sueldo_integrado, fini

    def calcular_nomina(eventos):
        resultados = []
        for evento in eventos:
            salario_base, salario_base_dos, salario_base_tres, prem_punt_pct1, prem_asis_pct1, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical1, incluir_prima_dominical2, incluir_prima_dominical3 = obtener_salario_y_premio(evento['puesto'], evento['zona'], evento['total_dias_t2'])

            # Calcula finiquitos y demás detalles
            aguinaldo, vacaciones, prima_vacacional, prima_dominical1, prem_asis, prem_punt, sueldo_integrado1, fini1 = calcular_finiquito(salario_base, prem_punt_pct1, prem_asis_pct1, incluir_prima_dominical1)

            if evento['total_dias_t2'] >= 1:
                aguinaldo2, vacaciones2, prima_vacacional2, prima_dominical2, prem_asis2, prem_punt2, sueldo_integrado2, fini2 = calcular_finiquito(salario_base_dos, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical2)
            else:
                aguinaldo2 = vacaciones2 = prima_vacacional2 = prima_dominical2 = prem_asis2 = prem_punt2 = sueldo_integrado2 = fini2 = 0
            if evento['total_dias_t3'] >= 1:
                aguinaldo3, vacaciones3, prima_vacacional3, prima_dominical3, prem_asis3, prem_punt3, sueldo_integrado3, fini3 = calcular_finiquito(salario_base_tres, prem_punt_pct1, prem_asis_pct1, incluir_prima_dominical3)
            else:
                aguinaldo3 = vacaciones3 = prima_vacacional3 = prima_dominical3 = prem_asis3 = prem_punt3 = sueldo_integrado3 = fini3 = 0

            # Calcular sueldo y total

            he = evento['horas_extra'] * 50

            sueldo_cotizacion1 = round(salario_base + prima_dominical1 + prem_asis + prem_punt, 2)
            sueldo_cotizacion2 = round(salario_base_dos + prima_dominical2 + prem_asis2 + prem_punt2, 2) if  evento['total_dias_t2'] >= 1 else 0
            sueldo_cotizacion3 = round(salario_base_tres + prima_dominical3 + prem_asis3 + prem_punt3, 2) if evento['total_dias_t3'] >= 1 else 0

            if  evento['total_dias_t2'] == 0:
                salario_base_dos = 0
            if  evento['total_dias_t3'] == 0:
                salario_base_tres = 0

            if  evento['dias_finiquito'] == 0:
                fini1 = 0
            if evento['dias_finiquito2'] == 0:
                fini2 = 0
            if evento['dias_finiquito3'] == 0:
                fini3 = 0

            total_uno = round(sueldo_cotizacion1 * evento['dias_trabajados'], 2) if evento['dias_finiquito'] == 0 else round(sueldo_cotizacion1 * evento['dias_trabajados'], 2) + round(fini1 * evento['dias_finiquito'], 2)
            total_dos = round(sueldo_cotizacion2 * evento['total_dias_t2'], 2) if evento['dias_finiquito2'] == 0 else round(sueldo_cotizacion2 * evento['total_dias_t2'] + round(fini2 * evento['dias_finiquito2']), 2)
            total_tres = round(sueldo_cotizacion3 * evento['total_dias_t3'], 2) if evento['dias_finiquito3'] == 0 else round(sueldo_cotizacion3 * evento['total_dias_t3'] + round(fini3 * evento['dias_finiquito3']), 2)
            

            if evento['dia_festivos_c'] == True:  
                dia_festivo = round(dia_festivos * 2, 2)              
                total_uno += dia_festivo 
            else:
                dia_festivo = 0

            total = round(total_uno + total_dos + total_tres + he, 2)

            resultados.append({
                'PUESTO': evento['puesto'],
                'ZONA': evento['zona'],
                'BODEGA': evento['bodega'],
                'EVENTO': evento['nombre_evento'],
                'PERIODO TRABAJADO': f"Del {evento['inicio']} al {evento['fin']}",
                'NOMBRE COMPLETO': evento['nombre'],
                'ESTATUS NOMINA': evento['estatus_nomina'],
                'ALTA SEGURO SOCIAL': evento['alta_seguro'],
                'HORARIO': evento['horario'],
                'HORAS EXTRA AUTORIZADAS': evento['horas_extra'],
                'TOTAL DE DÍAS TRABAJADOS': evento['dias_trabajados'],
                
                'TOTAL DE HORA EXTRA': he,
                'TOTAL CAPACITACION': "",
                'BANCO': "",
                'CUENTA': "",
                'TARJETA': "",
                'CLABE INTERBANCARIA': "",
                'RFC': "",
                ' ' : "",              
                'Días finiquito 1 evento': evento['dias_finiquito'],
                'Días trabajados 2 eventos': evento['total_dias_t2'],
                'Días finiquito 2 eventos': evento['dias_finiquito2'],

                "SALARIO DIARIO UN EVENTO (P001)": salario_base,
                "AGUINALDO (P002)": aguinaldo,
                "VACACIONES (P001)": vacaciones,
                "PRIMA VACACIONAL (P021)": prima_vacacional,
                "PRIMA DOMINICAL (P020)": prima_dominical1,
                "PREMIO ASISTENCIA (P049)": prem_asis,
                "PREMIO PUNTUALIDAD (P010)": prem_punt,
                "FINIQUITO UN EVENTO": fini1 * evento['dias_finiquito'],
                "SUELDO INTEGRADO (IMSS)": sueldo_integrado1,
                "SUELDO COTIZACIÓN S/F UN EVENTO": sueldo_cotizacion1 * evento['dias_trabajados'],
                
                "SUELDO POR COBRAR UN EVENTO": total_uno,

                "SALARIO DIARIO DOS EVENTOS (P001)": salario_base_dos,
                "AGUINALDO 2 (P002)": aguinaldo2,
                "VACACIONES 2 (P001)": vacaciones2,
                "PRIMA VACACIONAL 2 (P021)": prima_vacacional2,
                "PRIMA DOMINICAL 2 (P020)": prima_dominical2,
                "PREMIO ASISTENCIA 2 (P049)": prem_asis2,
                "PREMIO PUNTUALIDAD 2 (P010)": prem_punt2,
                "FINIQUITO DOS EVENTOS":fini2 * evento['dias_finiquito2'],
                "SUELDO INTEGRADO 2 (IMSS)": sueldo_integrado2,
                "SUELDO COTIZACIÓN S/F DOS EVENTOS": sueldo_cotizacion2 * evento['total_dias_t2'],
                
                "SUELDO POR COBRAR DOS EVENTOS": total_dos,

                "SALARIO DIARIO TRES EVENTOS (P001)": salario_base,
                "AGUINALDO 3 (P002)": aguinaldo3,
                "VACACIONES 3 (P001)": vacaciones3,
                "PRIMA VACACIONAL 3 (P021)": prima_vacacional3,
                "PRIMA DOMINICAL 3 (P020)": prima_dominical3,
                "PREMIO ASISTENCIA 3 (P049)": prem_asis3,
                "PREMIO PUNTUALIDAD 3 (P010)": prem_punt3,
                "FINIQUITO TRES EVENTOS": fini3 * evento['dias_finiquito3'],
                "SUELDO INTEGRADO 3 (IMSS)": sueldo_integrado3,
                "SUELDO COTIZACIÓN S/F TRES EVENTOS ": sueldo_cotizacion3 * evento['total_dias_t3'],
                
                "SUELDO POR COBRAR TRES EVENTOS": total_tres,

                "TOTAL DE LA NOMINA": total,
                'OBSERVACIONES': evento['observaciones'],
            })

        return resultados
    
    # Interfaz de Streamlit
    st.title("CALCULADORA DE NÓMINAS")   
    conn = st.connection("gsheets3", type=GSheetsConnection)

    df_aux = conn.read(worksheet="Datos", usecols=list(range(10)), ttl=5)
    df_aux = df_aux.dropna(how="all")

    NOMBRES = df_aux.iloc[:, 0].dropna().tolist()
    EVENTOS = df_aux.iloc[:, 1].dropna().tolist()
    BODEGA = df_aux.iloc[:, 2].dropna().tolist()
    PUESTO = df_aux.iloc[:, 3].dropna().tolist()
    SALARIOS = df_aux.iloc[:, 4].dropna().tolist()
    ZONA = ["INTERIOR", "FRONTERA", "ESPECIAL", "INTERIOR JOYERÍA Y DEGUSTACIÓN", "ESPECIAL JOYERÍA Y DEGUSTACIÓN"]
    HORARIO = ["9 A 4", "2 A 9", "COORDINACIÓN"]
    SEGURO = ["FINIQUITO", "NOMINA"]
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
            
        st.markdown("**Requerido*")
        submit_button = st.form_submit_button(label="Agregar evento")

        if 'eventos' not in st.session_state:
            st.session_state.eventos = []

        if submit_button:
            st.session_state.eventos.append({
            'nombre': nombre_empleado,
            'puesto': puesto,
            'nombre_evento': evento,
            'dias_trabajados': total_dias,
            'dias_finiquito': dias_finiquito,
            'bodega': bodega,
            'inicio': inicio,
            'alta_seguro': alta_seguro,
            'dia_festivo': dia_festivos,
            'horas_extra': horas_extra,
            'zona': zona,
            'horario': horario,
            'fin': fin,
            'dia_festivos_c': dia_festivos_c,
            'total_dias_t2': total_dias_t2,
            'dias_finiquito2': dias_finiquito2,
            'observaciones': observaciones,
            'estatus_nomina': estatus_nomina,
            'total_dias_t3': total_dias_t3,
            'dias_finiquito3': dias_finiquito3,
            })
        

        st.write("Eventos:")
        st.write(pd.DataFrame(st.session_state.eventos))

        # Calcular nómina y generar Excel
        

    if st.button('Calcular Nómina'):
        nomina = calcular_nomina(st.session_state.eventos)
        df_nomina = pd.DataFrame(nomina)
        st.session_state.eventos = []

        # Generar archivo Excel con fecha y hora
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_nomina.to_excel(writer, index=False, sheet_name='Nómina')
        output.seek(0)

        st.download_button(label="Descargar Nómina en Excel", data=output, file_name='nomina.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        st.write("Cálculo de nómina completado:")
        st.write(df_nomina) 

# Llamada a la función app para ejecutar la aplicación
if __name__ == "__main__":
    app()

    
