import streamlit as st
import pandas as pd
import io
from data.datos import SALARIO_BASE, tarifas_isr
from paginas.lector_excel import app
from paginas.cargador_tb_isr import cargar_datos_desde_bd

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
                return SALARIO_BASE[17], SALARIO_BASE[17], SALARIO_BASE[17], 0, 0, 0, 0, True, True, True
            elif zona == 'FRONTERA':
                return SALARIO_BASE[18], SALARIO_BASE[18], SALARIO_BASE[18], 0, 0, 0, 0, True, True, True
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

"""def calcular_isr(base_isr):
    for tarifa in tarifas_isr:
        if tarifa["limite_inferior"] <= base_isr <= tarifa["limite_superior"]:
            isr = tarifa["cuota_fija"] + (base_isr - tarifa["limite_inferior"]) * tarifa["porcentaje"]
            return round(isr, 2)        
    return 0.0"""

def calcular_isr(base_isr):
    # Obtener las tarifas desde la base de datos (como un DataFrame)
    df_tarifas_isr = cargar_datos_desde_bd()  #  esta función devuelve un DataFrame de lo que se eingresa en el cargador

    # Iterar sobre las filas del DataFrame
    #iterar : recorrer un conjunto de elementos uno por uno para realizar alguna acción sobre cada uno de esos elementos.
    for index, tarifa in df_tarifas_isr.iterrows():
        limite_inferior = tarifa["limite_inferior"]
        limite_superior = tarifa["limite_superior"]
        
        # Verificar si la base_isr está dentro del rango
        if limite_inferior <= base_isr <= limite_superior:
            cuota_fija = tarifa["cuota_fija"]
            porcentaje = tarifa["porcentaje"]
            
            # Calcular el ISR (dependiendo de tu fórmula)
            isr_calculado = cuota_fija + (base_isr - limite_inferior) * porcentaje
            return round(isr_calculado, 2)  # Retornar el ISR calculado

    # Si no se encuentra ningún rango, retornar 0
    return 0.0

