from markdown2pdf import convert
import os

def generate_pdf():
    input_file = "documentacion.md"
    output_file = "Documentacion_Balanceate.pdf"
    
    try:
        # Convertir markdown a PDF
        convert(input_file, output_file)
        print(f"PDF generado exitosamente: {output_file}")
    except Exception as e:
        print(f"Error al generar el PDF: {str(e)}")

if __name__ == "__main__":
    generate_pdf()
