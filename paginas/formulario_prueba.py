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
        

    def calcular_finiquito(salario_base, dias_finiquito, prem_punt_pct, prem_asis_pct, incluir_prima_dominical):
    # Función para calcular el finiquito con base en las reglas proporcionadas
        aguinaldo = round((salario_base * (15 / 365)) * dias_finiquito, 2)
        vacaciones = round((salario_base * (12 / 365)) * dias_finiquito, 2)
        prima_vacacional = round(vacaciones * 0.25, 2)
        prima_dominical = round(((1 * 0.25) / 7) * salario_base * dias_finiquito, 2) if incluir_prima_dominical else 0
        prem_asis = round(salario_base * prem_punt_pct * dias_finiquito, 2)
        prem_punt = round(salario_base * prem_asis_pct * dias_finiquito, 2)
        sueldo_integrado = round(salario_base + aguinaldo + vacaciones + prima_vacacional + prima_dominical, 2)
        finiquito = round(aguinaldo + vacaciones + prima_vacacional + prima_dominical + prem_asis + prem_punt, 2)
        return aguinaldo, vacaciones, prima_vacacional, prima_dominical, prem_asis, prem_punt, sueldo_integrado, finiquito

    def calcular_nomina(eventos):
        resultados = []
        for evento in eventos:
            salario_base, salario_base_dos, prem_punt_pct1, prem_asis_pct1, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical1, incluir_prima_dominical2 = obtener_salario_y_premio(evento['puesto'], evento['zona'], evento['total_dias_t2'])

            # Calcula finiquitos y demás detalles
            aguinaldo, vacaciones, prima_vacacional, prima_dominical1, prem_asis, prem_punt, sueldo_integrado1, finiquito = calcular_finiquito(salario_base, evento['dias_finiquito'], prem_punt_pct1, prem_asis_pct1, incluir_prima_dominical1)

            if evento['total_dias_t2'] >= 1:
                aguinaldo2, vacaciones2, prima_vacacional2, prima_dominical2, prem_asis2, prem_punt2, sueldo_integrado2, finiquito2 = calcular_finiquito(salario_base_dos, evento['dias_finiquito2'], prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical2)
            else:
                aguinaldo2 = vacaciones2 = prima_vacacional2 = prima_dominical2 = prem_asis2 = prem_punt2 = sueldo_integrado2 = finiquito2 = 0

            # Calcular sueldo y total
            sueldo_uno = round(salario_base * evento['dias_trabajados'], 2)
            sueldo_dos = round(salario_base_dos * evento['total_dias_t2'], 2)
            he = evento['horas_extra'] * 50

            # Inicializar bono de coordinador
            bono_coordinador = 0

            # Lógica para calcular el bono del coordinador en el total_uno
            if evento['puesto'] == 'COORDINADOR' and evento['zona'] == 'INTERIOR':
                if evento['cant_eventos'] == 0:
                    total_uno = round(sueldo_uno + finiquito, 2)
                    bono_coordinador = 0
                elif evento['cant_eventos'] == 1:
                    total_uno = round((sueldo_uno + finiquito) * 2, 2)
                    bono_coordinador = 250
                elif evento['cant_eventos'] == 2:
                    total_uno = round((sueldo_uno + finiquito) * 3, 2)
                    bono_coordinador = 500
            else:
                total_uno = round(sueldo_uno + finiquito, 2)

            total_dos = round(sueldo_dos + finiquito2, 2)
            total = round(total_uno + total_dos + he, 2)

            resultados.append({
                'Nombre': evento['nombre'],
                'Puesto': evento['puesto'],
                'Zona': evento['zona'],
                'Evento': evento['nombre_evento'],
                'Bodega': evento['bodega'],
                'Días trabajados': evento['dias_trabajados'],
                'Días finiquito 1 evento': evento['dias_finiquito'],
                'Días trabajados 2 eventos': evento['total_dias_t2'],
                'Días finiquito 2 eventos': evento['dias_finiquito2'],
                'Bonos Coordinador': bono_coordinador,
                'Aguinaldo 1': aguinaldo,
                'Vacaciones 1': vacaciones,
                'Prima vacacional 1': prima_vacacional,
                'Prima dominical 1': prima_dominical1,
                'Premio asistencia 1': prem_asis,
                'Premio puntualidad 1': prem_punt,
                'Sueldo integrado 1': sueldo_integrado1,
                'Finiquito 1': finiquito,
                'Aguinaldo 2': aguinaldo2,
                'Vacaciones 2': vacaciones2,
                'Prima vacacional 2': prima_vacacional2,
                'Prima dominical 2': prima_dominical2,
                'Premio asistencia 2': prem_asis2,
                'Premio puntualidad 2': prem_punt2,
                'Sueldo integrado 2': sueldo_integrado2,
                'Finiquito 2': finiquito2,
                'Horas extra': he,
                'Sueldo 1': sueldo_uno,
                'Total': total
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
            puesto = st.selectbox("Puesto", options=PUESTO)
            evento = st.selectbox("Evento", options=EVENTOS)
            observaciones = st.text_input(label="Observaciones")
            estatus_nomina = st.selectbox("Estatus de la nómina", options=NOMINA)
            st.write("Primer evento")
            total_dias = st.number_input(label="Total de días trabajados*", min_value=1, max_value=21)
            dias_finiquito = st.number_input(label="Días Finiquito 1 Turno", min_value=0, max_value=21)
        with c2:
            bodega = st.selectbox("Bodega*", options=BODEGA)
            nombre_empleado = st.selectbox("Nombre completo", options=NOMBRES)
            inicio = st.date_input(label="Día inicio*")
            alta_seguro = st.selectbox("Alta del seguro social", options=SEGURO)
            dia_festivos_c = st.checkbox(label="Día festivo")
            dia_festivos = st.selectbox(label="Día festivo", options=SALARIOS)
            horas_extra = st.number_input(label="Horas extra", max_value=8, min_value=0)      
            
        with c3:
            zona = st.selectbox("Zona*", options=ZONA)
            horario = st.selectbox("Horario", options=HORARIO)
            fin = st.date_input(label="Día fin*")            
            st.write("Segundo evento")
            total_dias_t2 = st.number_input(label="Días trabajados con doble turno", min_value=0, max_value=21)
            dias_finiquito2 = st.number_input(label="Días Finiquito 2 Turnos", min_value=0, max_value=21)
            cant_eventos = st.number_input("Bonos de coordinador", min_value=0, max_value=2)

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
            'cant_eventos': cant_eventos,
            'zona': zona,
            'horario': horario,
            'fin': fin,
            
            'total_dias_t2': total_dias_t2,
            'dias_finiquito2': dias_finiquito2,
            'observaciones': observaciones,
            'estatus_nomina': estatus_nomina
            })
        

        st.write("Eventos:")
        st.write(pd.DataFrame(st.session_state.eventos))

        # Calcular nómina y generar Excel
        

    if st.button('Calcular Nómina'):
        nomina = calcular_nomina(st.session_state.eventos)
        df_nomina = pd.DataFrame(nomina)
        st.session_state.eventos = []
        # Generar archivo Excel
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
