import streamlit as st

SALARIO_BASE = [278.8,      #INTERIOR DEMOSTRADOR UN EVENTO         [0] Salario anterior 265.6
                455,        #INTERIOR DEMOSTRADOR DOS EVENTOS       [1]
                419.88,     #FRONTERA DEMOSTRADOR UN EVENTO         [2] Salario anterior 374.89
                594,        #FRONTERA DEMOSTRADOR DOS EVENTOS       [3]
                298.2,      #ESPECIAL DEMOSTRADOR UN EVENTO         [4]
                510,        #ESPECIAL DEMOSTRADOR DOS EVENTOS       [5]
                298.2,      #INTERIOR DEMOSTRADOR JOYERÍA Y DEGUSTACIÓN UN EVENTO [6] Salario anterior 278.8
                278.8,      #INTERIOR DEMOSTRADOR JOYERÍA           [19]
                298.2,      #ESPECIAL DEMOSTRADOR JOYERÍA Y DEGUSTACIÓN UN EVENTO [7]
                278.8,      #INTERIOR COORDINADOR UN EVENTO         [8] Salario anterior 205.27
                468.00,     #INTERIOR COORDINADOR TRES EVENTOS      [9]
                455,        #INTERIOR COORDINADOR Y DEMOSTRADOR UN EVENTO [10]
                419.88,     #FRONTERA COORDINADOR UN EVENTO         [11] Salario anterior 284
                580,        #FRONTERA COORDINADOR Y DEMOSTRADOR UN EVENTO [12]
                278.80,     #ESPECIAL COORDINADOR UN EVENTO         [13] Salario anterior 209
                507,        #ESPECIAL COORDINADOR Y DEMOSTRADOR UN EVENTO [14]
                298.2,      #INTERIOR COORDINADOR JOYERÍA Y DEGUSTACIÓN UN EVENTO [15] Salario anterior 228
                239,        #ESPECIAL DEMOSTRADOR JOYERÍA Y DEGUSTACIÓN UN EVENTO [16]      
                278.8,      #INTERIOR COORDINADOR                   [17]  
                419.88,     #FRONTERA COORDINADOR                   [18] Salaio anterior 374.89        
                ]

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