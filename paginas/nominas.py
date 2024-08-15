import streamlit as st
from fpdf import FPDF
import os

# Definir una constante para el nombre del archivo PDF
PDF_FILENAME = "nomina_personalizada.pdf"

class PDF(FPDF):
    
    def header(self):
        # Agregar una imagen en la cabecera (lado izquierdo)
        image_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'logo.jpg')
        self.image(image_file, 20, 8, 33)        
        # Guardar la posición y alinear los títulos en el centro
        self.set_y(10)
        self.set_x(0)
        self.set_font("Arial", "B", 12)
        #self.set_fill_color(132, 139, 148)
        self.cell(0, 10, "Demo JIMTECH", ln=True, align="C")

        self.set_y(18)
        self.set_x(0)
        self.set_font("Arial", "", 7)
        self.cell(0, 2, "RFC: XAXX010101000 Reg Patronal:", ln=True, align="C")
        self.set_y(22)
        self.set_x(0)
        self.cell(0, 5, "C.P. 55721", ln=True, align="C")
        self.set_y(28)
        self.set_x(0)
        self.cell(0, 0, "Tel: 55555555555    Email:issac.mosquedag@gmail.com", ln=True, align="C")
        
        self.set_y(10)
        self.set_x(-65)  
        self.set_font("Arial", "B", 6)
        self.set_text_color(0, 0, 0)  # Establece el color del texto
        self.set_fill_color(236, 236, 236)  # Establece el color de fondo
        self.cell(60, 5, "Comprobante de nómina", ln=True, align="C", fill=True)

        # Primero, configuramos el color del borde gris claro
        self.set_draw_color(236, 236, 236)  # Color gris claro para el borde

        # Dibujamos el rectángulo
        self.rect(145, 15, 60, 18)  # (x, y, ancho, alto)

        # Ahora añadimos el contenido
        self.set_y(15)
        self.set_x(-65) 
        self.set_fill_color(255, 255, 255)  
        self.set_text_color(0, 0, 0)  
        self.cell(60, 4, "Folio:", ln=True, align="L", fill=False)

        self.set_y(19)
        self.set_x(-65) 
        self.cell(60, 4, "Fecha: 001", ln=True, align="L", fill=False)

        self.set_y(23)
        self.set_x(-65) 
        self.cell(60, 4, "Tipo de Recibo: 001", ln=True, align="L", fill=False)

        self.set_y(27)
        self.set_x(-65) 
        self.cell(60, 4, "Status: 001", ln=True, align="L", fill=False)

        self.ln(15)

    def footer(self):
        # Agregar un pie de página
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    def chapter_body(self):
        #Rectangulo Nominas
        self.set_font("Arial", "B", 8)
        self.set_y(40)  # Ajusta este valor según sea necesario
        self.set_x(10)  # Ajusta este valor según sea necesario
        self.set_fill_color(236, 236, 236)  # Color gris claro para el relleno    
        self.set_draw_color(236, 236, 236)  # Color un poco más oscuro para el borde
        self.rect(10, 40, 195, 7, style='DF') 

        self.set_y(40)
        self.set_x(25)  
        self.set_text_color(0, 0, 0)  
        self.cell(20, 7, "Empleado:", ln=True, align="L", fill=False)

        self.set_y(40)
        self.set_x(92)  
        self.set_text_color(0, 0, 0)  
        self.cell(20, 7, "Laboral:", ln=True, align="L", fill=False)

        self.set_y(40)
        self.set_x(165)  
        self.set_text_color(0, 0, 0)  
        self.cell(20, 7, "Pago:", ln=True, align="L", fill=False)
        
        self.set_y(100)  # Ajusta este valor según sea necesario
        self.set_x(10)  # Ajusta este valor según sea necesario
        self.set_draw_color(236, 236, 236)  # Color gris claro para el borde
        self.rect(10, 40, 195, 35)  # (x, y, ancho, alto)
    #Columna 1
        self.set_y(46)
        self.set_x(10)  
        self.set_text_color(0, 0, 0)  
        self.set_font("Arial", "B", 6)
        self.cell(0, 7, "VIRIDIANA MONTSERRAT MERCADO SERRATOS", ln=True, align="L", fill=False)

        self.set_y(49)       
        self.set_font("Arial", "", 6)
        self.cell(0, 7, "Núm.Empleado: 0002", ln=True, align="L", fill=False)

        self.set_y(52)       
        self.cell(0, 7, "RFC: ", ln=True, align="L", fill=False)

        self.set_y(55)       
        self.cell(0, 7, "CURP: ", ln=True, align="L", fill=False)

        self.set_y(58)
        self.cell(0, 7, "NSS: ", ln=True, align="L", fill=False)

        self.set_y(61)
        self.cell(0, 7, "Departamento: ", ln=True, align="L", fill=False)

        self.set_y(64)
        self.cell(0, 7, "Puesto: ", ln=True, align="L", fill=False)

        self.set_y(67)
        self.cell(0, 7, "Riesgo de puesto: ", ln=True, align="L", fill=False)
    #Columna 2
        self.set_y(46)
        self.set_x(80)  
        self.set_text_color(0, 0, 0)               
        self.set_font("Arial", "", 6)
        self.cell(0, 7, "Régimen:", ln=True, align="L", fill=False)

        self.set_y(49) 
        self.set_x(80) 
        self.cell(0, 7, "Contrato: ", ln=True, align="L", fill=False)

        self.set_y(52) 
        self.set_x(80)    
        self.cell(0, 7, "Jornada: ", ln=True, align="L", fill=False)

        self.set_y(55) 
        self.set_x(80)
        self.cell(0, 7, "Periodicidad: ", ln=True, align="L", fill=False)

        self.set_y(58)
        self.set_x(80)
        self.cell(0, 7, "Salario Diario: ", ln=True, align="L", fill=False)

        self.set_y(61)
        self.set_x(80)
        self.cell(0, 7, "Salario Integrado: ", ln=True, align="L", fill=False)
    #Columna 3
        self.set_y(46)
        self.set_x(145)
        self.set_text_color(0, 0, 0)  
        self.cell(0, 7, "Fecha de Inicio", ln=True, align="L", fill=False)

        self.set_y(49) 
        self.set_x(145)      
        self.cell(0, 7, "Fecha de Corte:", ln=True, align="L", fill=False)

        self.set_y(52) 
        self.set_x(145)       
        self.cell(0, 7, "Días Pagados: ", ln=True, align="L", fill=False)

        self.set_y(55) 
        self.set_x(145)      
        self.cell(0, 7, "Banco: ", ln=True, align="L", fill=False)

        self.set_y(58)
        self.set_x(145)
        self.cell(0, 7, "Cuenta: ", ln=True, align="L", fill=False)

        self.set_y(61)
        self.set_x(145)
        self.cell(0, 7, "Forma: ", ln=True, align="L", fill=False)

        self.ln()
    #Rectangulo Percepciones        
        self.set_y(80)
        self.set_x(10)
        self.set_fill_color(236, 236, 236)
        self.set_draw_color(236, 236, 236)
        self.rect(10, 80, 195, 7, style='DF')

        # Configuración de la fuente para los encabezados
        self.set_font("Arial", "B", 8)
        self.set_text_color(0, 0, 0)

        # Encabezados alineados en la misma fila
        self.set_y(80)
        self.set_x(10)
        self.cell(50, 7, "Percepciones", 0, 0, 'L')
        self.cell(40, 7, "Gravado", 0, 0, 'R')
        self.cell(15, 7, "Exento", 0, 0, 'R')
        self.cell(25, 7, "Deducciones", 0, 0, 'R')
        self.cell(47, 7, "Importe", 0, 0, 'R')  # El '1' al final crea un salto de línea

        self.set_font("Arial", "", 7)
        self.set_y(90)
        self.set_x(10)
        self.cell(50, 7, "Sueldos, Salarios Rayas y Jornales", 0, 0, 'L')
        self.cell(40, 7, "5,000.00", 0, 0, 'R')
        self.cell(15, 7, "0.00", 0, 0, 'R')
        self.cell(25, 7, " ", 0, 0, 'R')
        self.cell(47, 7, " ", 0, 0, 'R')

        self.rect(10, 87, 195, 10)

        self.set_font("Arial", "B", 8)
        self.set_y(100)
        self.set_x(10)
        self.cell(120, 7, "Cantidad con Letra", 0, 0, 'L')
        self.cell(40, 7, "Percepciones", 0, 0, 'C')
        self.set_font("Arial", "", 8)
        self.cell(25, 7, "5,000.00", 0, 1, 'C')  # El '1' al final crea un salto de línea
        
        self.set_y(108)
        self.set_x(10)
        self.cell(0, 7, "CINCO MIL PESOS 00/100 M:N", 0, 0, 'L')

        self.set_y(104)
        self.set_x(140)
        self.set_font("Arial", "B", 8)
        self.cell(0, 7, "Deducciones", 0, 0, 'L')

        self.set_y(108)
        self.set_x(140)
        self.cell(0, 7, "ISR", 0, 0, 'L')

        self.set_y(112)
        self.set_x(140)
        self.cell(0, 7, "Total", 0, 0, 'L')

        self.set_y(118)
        self.set_x(10)
        self.set_draw_color(200, 200, 200)  # Color gris para la línea
        self.line(10, 118, 130, 118)  # (x1, y1, x2, y2)

        self.ln()
    #Rectangulo QR
        self.set_y(120)
        self.set_x(10)
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(0, 0, 0)
        self.rect(10, 120, 25, 25, style='DF')

        self.set_font("Arial", "B", 7)
        self.set_y(120)
        self.set_x(38)
        self.cell(20, 7, "Folio Fiscal: ", 0, 0, 'L')
        self.cell(20, 7, "Fecha Timbrado: ", 0, 0, 'L')

        self.set_y(124)
        self.set_x(38)
        self.cell(29, 7, "Certificado Emisor: ", 0, 0, 'L')
        self.cell(20, 7, "Certificado SAT: ", 0, 0, 'L')

        self.set_y(128)
        self.set_x(38)
        self.cell(29, 7, "Sello del SAT: ", 0, 0, 'L')

        self.set_y(132)
        self.set_x(38)
        self.cell(29, 7, "Cadena Original del Complemento: ", 0, 0, 'L')
    #Recibí
        self.set_y(150)
        self.set_x(65)
        self.set_font("Arial", "", 7)
        self.cell(0, 7, "RECIBÍ DE: ", 0, 0, 'L')

        self.set_y(154)
        self.set_font("Arial", "B", 7)
        self.cell(0, 7, "DEMO JIMTECH: ", 0, 0, 'C')

        self.set_y(158)
        self.set_font("Arial", "", 7)
        self.cell(0, 7, "EL TOTAL NETO SEÑALADO Y ESTOY DE ACUERDO ", 0, 0, 'C')

        self.set_y(161)
        self.cell(0, 7, "CON LO INDICADO EN ESTE RECIBO", 0, 0, 'C')

        self.set_y(165)
        self.set_x(10)
        self.set_draw_color(200, 200, 200) 
        self.line(70, 175, 140, 175)  # (x1, y1, x2, y2)

        self.set_y(176)
        self.set_font("Arial", "b", 7)
        self.cell(0, 7, "VIRIDIANA MONTSERRAT MERCADO SERRATOS", 0, 0, 'C')

# Crear una función para generar el PDF con diseño personalizado
def generar_pdf():
    pdf = PDF()
    pdf.add_page()
    
    pdf.chapter_body()
    
    # Guardar el PDF
    pdf.output(PDF_FILENAME)

def app():

    # Generar el PDF
    generar_pdf()

    # Permitir que el usuario descargue el PDF
    with open(PDF_FILENAME, "rb") as pdf_file:
        st.download_button(label="Descargar Nómina Personalizada en PDF", data=pdf_file, file_name=PDF_FILENAME, mime='application/octet-stream')

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
