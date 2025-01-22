import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from estructura.proceso_lector import procesar_datos, to_excel_con_sheets

def app():
    st.title("CALCULADORA DE NÓMINAS")
    conn = st.connection("gsheets3", type=GSheetsConnection)

    df_ret = conn.read(worksheet="Retención", usecols=[0, 1], ttl=5).dropna(how="all")

    if len(df_ret.columns) < 2:
        st.error("El DataFrame 'Retención' no tiene suficientes columnas.")
        st.stop()
    
    uploaded_file = st.file_uploader("Cargar archivo Excel con datos de empleados", type="xlsx")
    
    if uploaded_file is not None:
        df_empleados = pd.read_excel(uploaded_file)
        st.write("Datos cargados:")
        with st.expander("Nóminas"): 
            st.dataframe(df_empleados)
        
        if st.button("Procesar datos"):
            df_resultado, df_nomina_uno = procesar_datos(df_empleados, df_ret)
            
            # Store the processed DataFrames in session state
            st.session_state['df_resultado'] = df_resultado
            st.session_state['df_nomina_uno'] = df_nomina_uno
            
            st.success("Datos procesados. Ahora puedes descargar los archivos.")

    # Only show download buttons if data has been processed
    if 'df_resultado' in st.session_state and 'df_nomina_uno' in st.session_state:
        if st.download_button(
            label="Descargar Nómina Completa",
            data=to_excel_con_sheets(st.session_state['df_resultado'], st.session_state['df_nomina_uno']),
            file_name="nomina_completa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            st.success("Nómina Completa descargada exitosamente.")

if __name__ == "__main__":
    app()