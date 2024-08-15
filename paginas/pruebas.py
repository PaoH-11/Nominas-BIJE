import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

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

def app():
    st.title("CALCULADORA DE NÓMINAS")
        # Agregar un cargador de archivos
    uploaded_file = st.file_uploader("Cargar archivo Excel con datos de empleados", type="xlsx")
    
    if uploaded_file is not None:
        # Leer el archivo Excel
        df_empleados = pd.read_excel(uploaded_file)
        
        # Mostrar el DataFrame cargado
        st.write("Datos cargados:")
        st.dataframe(df_empleados)
        
        # Botón para procesar los datos
        if st.button("Procesar datos y actualizar Nómina General"):
            procesar_datos(df_empleados)


    st.info('Rellenar los campos requeridos', icon="ℹ️")
    conn = st.connection("gsheets3", type=GSheetsConnection)

    df = conn.read(worksheet="Nómina", usecols=list(range(40)), ttl=5)
    df = df.dropna(how="all")

    df_aux = conn.read(worksheet="Datos", usecols=list(range(10)), ttl=5)
    df_aux = df_aux.dropna(how="all")

    df_aux2= conn.read(worksheet="Nómina General", usecols=list(range(40)), ttl=5)
    df_aux2 = df_aux2.dropna(how="all")

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

        submit_button = st.form_submit_button(label="Registrar")

    if submit_button:
        if not total_dias:
            st.warning("Asegúrese de llenar todos los campos requeridos")
            st.stop()
        else:
            salario_base, salario_base_dos, prem_punt_pct1, prem_asis_pct1, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical1, incluir_prima_dominical2 = obtener_salario_y_premio(puesto, zona, total_dias_t2)

            aguinaldo, vacaciones, prima_vacacional, prima_dominical1, prem_asis, prem_punt, sueldo_integrado1, finiquito = calcular_finiquito(salario_base, dias_finiquito, prem_punt_pct1, prem_asis_pct1, incluir_prima_dominical1)
            
            if total_dias_t2 >= 1:
                aguinaldo2, vacaciones2, prima_vacacional2, prima_dominical2, prem_asis2, prem_punt2, sueldo_integrado2, finiquito2 = calcular_finiquito(salario_base_dos, dias_finiquito2, prem_punt_pct2, prem_asis_pct2, incluir_prima_dominical2)
            else:
                aguinaldo2 = vacaciones2 = prima_vacacional2 = prima_dominical2 = prem_asis2 = prem_punt2 = sueldo_integrado2 = finiquito2 = 0

            he = horas_extra * 50

            sueldo_uno = round((salario_base * total_dias), 2)
            sueldo_dos = round(salario_base_dos * total_dias_t2, 2)
            sueldo_cotizacion1 = round(salario_base + prima_dominical1 + prem_asis + prem_punt, 2)
            sueldo_cotizacion2 = round(salario_base_dos + prima_dominical2 + prem_asis2 + prem_punt2, 2) if total_dias_t2 > 0 else 0

            if dia_festivos_c:  
                dia_festivo = round(dia_festivos * 2, 2)              
                sueldo_uno += dia_festivo
            else:
                dia_festivo = 0
                    
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
   
    st.dataframe(df_aux2)

def procesar_datos(df_empleados):
    conn = st.connection("gsheets3", type=GSheetsConnection)
    df_nomina_general = conn.read(worksheet="Nómina General", usecols=list(range(40)), ttl=5)
    df_nomina_general = df_nomina_general.dropna(how="all")
    
    nuevos_registros = []
    
    for _, row in df_empleados.iterrows():
        
        bodega = row['BODEGA']
        evento = row['EVENTO']
        periodo_trabajado = row['PERIODO TRABAJADO']
        nombre_empleado = row['NOMBRE COMPLETO']
        estatus_nomina = row['ESTATUS DE NÓMINA']
        alta_seguro = row['ALTA DEL SEGURO SOCIAL']
        horario = row['HORARIO']
        horas_extras_autorizadas = row['HORAS EXTRAS AUTORIZADAS']
        total_dias_trabajados = row['TOTAL DE DIAS TRABAJADOS']
        total_sueldo = row['TOTAL SUELDO']
        total_horas_extras = row['TOTAL DE HORAS EXTRAS']
        sueldo_por_cobrar = row['SUELDO POR COBRAR']
        banco = row['BANCO']
        cuenta = row['CUENTA']
        tarjeta = row['TARJETA']
        clabe_interbancaria = row['CLABE INTERBANCARIA']
        rfc = row['RFC']
        observaciones = row['OBSERVACIONES']    
        
        
        
        
        nuevo_registro = {
            "BODEGA": row.get('Bodega', ''),
            "EVENTO": row.get('Evento', ''),
            "PERIODO TRABAJADO": f"{row.get('Fecha Inicio', '')} al {row.get('Fecha Fin', '')}",
            "NOMBRE COMPLETO": nombre_empleado,
            "ESTATUS DE NÓMINA": row.get('Estatus de Nómina', ''),
            "ALTA DEL SEGURO SOCIAL": row.get('Alta del Seguro Social', ''),
            "HORARIO": row.get('Horario', ''),
            "HORAS EXTRAS AUTORIZADAS": row.get('Horas Extra', 0),
            "TOTAL DE DÍAS TRABAJADOS": dias_trabajados,
            "TOTAL SUELDO": 0,  # Calcular según tus fórmulas
            "TOTAL DE HORAS EXTRAS": 0,  # Calcular según tus fórmulas
            "TOTAL CAPACITACION PROPORCIONADA POR PROVEEDOR": 0,
            "BANCO": row.get('Banco', ''),
            "CUENTA": row.get('Cuenta', ''),
            "TARJETA": row.get('Tarjeta', ''),
            "CLABE INTERBANCARIA": row.get('CLABE', ''),
            "RFC": row.get('RFC', ''),
            "OBSERVACIONES": row.get('Observaciones', ''),
        }
        
        nuevos_registros.append(nuevo_registro)
    
    # Crear un DataFrame con los nuevos registros
    df_nuevos = pd.DataFrame(nuevos_registros)
    
    # Concatenar con los datos existentes
    df_actualizado = pd.concat([df_nomina_general, df_nuevos], ignore_index=True)
    
    # Actualizar la hoja de cálculo
    conn.update(worksheet="Nómina General", data=df_actualizado)
    
    st.success("Datos procesados y Nómina General actualizada exitosamente")

if __name__ == "__main__":
    app()
