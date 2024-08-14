import streamlit as st
import pandas as pd
from io import BytesIO

def app():
    # Función para calcular la nómina
    def calcular_nomina(eventos):
        resultados = []
        for evento in eventos:
            if evento['puesto'] == 'Demostrador':
                sueldo = 350 * (evento['horas_trabajadas'] // 4)
                pago_extra = evento['horas_extra'] * 250
            elif evento['puesto'] == 'Coordinador':
                sueldo = 250 * (evento['horas_trabajadas'] // 3)
                horas_cubiertas = min(5, max(0, evento['horas_trabajadas'] - 3))
                pago_cubierto = horas_cubiertas * 350
                pago_extra = evento['horas_extra'] * 120
            total = sueldo + pago_extra + (pago_cubierto if evento['puesto'] == 'Coordinador' else 0)
            resultados.append({'Nombre': evento['nombre'], 'Puesto': evento['puesto'], 'Evento': evento['nombre_evento'], 'Total': total})
        return resultados

    # Interfaz de Streamlit
    st.title('Cálculo de Nómina')
    st.write("Ingrese los detalles del evento:")

    # Ingreso de datos
    nombre = st.text_input("Nombre del empleado")
    puesto = st.selectbox("Puesto", ["Demostrador", "Coordinador"])
    nombre_evento = st.text_input("Nombre del evento")
    horas_trabajadas = st.number_input("Horas trabajadas", min_value=1)
    horas_extra = st.number_input("Horas extra", min_value=0)

    # Almacenar los eventos ingresados
    if 'eventos' not in st.session_state:
        st.session_state.eventos = []

    if st.button('Agregar evento'):
        st.session_state.eventos.append({'nombre': nombre, 'puesto': puesto, 'nombre_evento': nombre_evento, 'horas_trabajadas': horas_trabajadas, 'horas_extra': horas_extra})
        st.success(f"Evento agregado para {nombre} en el evento {nombre_evento}")

    # Mostrar eventos agregados
    st.write("Eventos:")
    st.write(pd.DataFrame(st.session_state.eventos))

    # Calcular nómina y generar Excel
    if st.button('Calcular Nómina'):
        nomina = calcular_nomina(st.session_state.eventos)
        df_nomina = pd.DataFrame(nomina)

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
