import streamlit as st

# Definir la función app()
def app():
    st.title("Calculadora de ISR México")

    base_isr = st.number_input("Ingrese su base ISR:", min_value=0.0, step=0.01)

    if st.button("Calcular ISR"):
        resultado = calcular_isr(base_isr)
        st.write(f"El ISR calculado para {base_isr} es: **${resultado}**")

# Función de cálculo ISR
def calcular_isr(base_isr):
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

    for tarifa in tarifas_isr:
        if tarifa["limite_inferior"] <= base_isr <= tarifa["limite_superior"]:
            isr = tarifa["cuota_fija"] + (base_isr - tarifa["limite_inferior"]) * tarifa["porcentaje"]
            return round(isr, 2)
    return 0.0
