import streamlit as st


def calcular_deduccion_imss(sdn, dias_trabajados, prima_riesgo):

    factor_integracion = 1.0493 # Factor de integración 2024
    uma = 108.57  # Unidad de Medida y Actualización 2024
    sdi = sdn * factor_integracion
    

    
    #calcular cuotas obrero patronales
    cuota_fija = uma * dias_trabajados * (20.4/100)
    prestaciones = sdi * dias_mes *  ((0.7/100)+(0.25/100)) if sdn <= (uma * 3) else sdi * dias_mes * (0.7/100)
    excedente = (sdi - uma * 3) * dias_mes * (1.1/100)) if sdi > (uma * 3) else 0
    gast_med_pen =  sdi * dias_mes * ((1.05/100) + (0.375/100)) if E13 <= F4 else F13 * C13 * K10


    

def app():

    with st.form(key='calculadora_imss'):
        dias_mes = st.number_input("Seleccione días mes", min_value=30, max_value=31, value=30)
        sdn = st.number_input("Ingrese su salario diario nominal", min_value=0.01)
        gas_med_pen = st.number_input("Ingrese gastos médicos pensionados (%)", min_value=0.0, max_value=100.0, value=3.8)

        submit_button = st.form_submit_button("Calcular Deducción")

        if st.form_submit_button("Calcular Deducción"):
            deduccion = calcular_deduccion_imss(sdn, dias_mes)
            st.write(f"La deducción del IMSS es: ${deduccion:.2f}")

            # Desglose de las deducciones
            st.write("Desglose de deducciones:")
            uma = 108.57
            if sbc > (uma * 3):
                st.write(f"- Enfermedades y Maternidad (en especie, cuota adicional): ${(sbc * 0.0040 * dias_trabajados / 30):.2f}")
            st.write(f"- Enfermedades y Maternidad (en dinero): ${(sbc * 0.0025 * dias_trabajados / 30):.2f}")
            st.write(f"- Enfermedades y Maternidad (gastos médicos pensionados): ${(sbc * 0.0038 * dias_trabajados / 30):.2f}")
            st.write(f"- Invalidez y Vida: ${(sbc * 0.0063 * dias_trabajados / 30):.2f}")