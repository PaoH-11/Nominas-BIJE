import streamlit as st

def calcular_deduccion_imss(sbc, dias_trabajados, prima_riesgo):
    uma = 108.57  # Unidad de Medida y Actualización 2023
    
    # Cálculos para cada concepto
    def calcular_para_periodo(porcentaje):
        return (sbc * porcentaje / 100) * dias_trabajados / 30

    # Enfermedades y Maternidad
    em_especie_adicional = max(calcular_para_periodo(0.40), 0) if sbc > (uma * 3) else 0
    em_dinero = calcular_para_periodo(0.25)
    em_gastos_medicos = calcular_para_periodo(0.38)

    # Invalidez y Vida
    invalidez_vida = calcular_para_periodo(0.63)

    # Total de deducciones
    deduccion_total = em_especie_adicional + em_dinero + em_gastos_medicos + invalidez_vida

    return deduccion_total

# Interfaz de Streamlit
st.title("Calculadora de Deducción IMSS")

sbc = st.number_input("Ingrese su Salario Base de Cotización (SBC) diario", min_value=0.01)
dias_trabajados = st.number_input("Ingrese los días trabajados", min_value=1, max_value=31, value=30)
prima_riesgo = st.number_input("Ingrese la prima de riesgo de trabajo (%)", min_value=0.0, max_value=100.0, value=0.5)

if st.button("Calcular Deducción"):
    deduccion = calcular_deduccion_imss(sbc, dias_trabajados, prima_riesgo)
    st.write(f"La deducción del IMSS es: ${deduccion:.2f}")

    # Desglose de las deducciones
    st.write("Desglose de deducciones:")
    uma = 108.57
    if sbc > (uma * 3):
        st.write(f"- Enfermedades y Maternidad (en especie, cuota adicional): ${(sbc * 0.0040 * dias_trabajados / 30):.2f}")
    st.write(f"- Enfermedades y Maternidad (en dinero): ${(sbc * 0.0025 * dias_trabajados / 30):.2f}")
    st.write(f"- Enfermedades y Maternidad (gastos médicos pensionados): ${(sbc * 0.0038 * dias_trabajados / 30):.2f}")
    st.write(f"- Invalidez y Vida: ${(sbc * 0.0063 * dias_trabajados / 30):.2f}")