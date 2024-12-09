from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generar_prueba_posiciones(pdf_path):
    """
    Genera un PDF con una cuadrícula de prueba para ajustar posiciones.
    """
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Dibujar una cuadrícula de referencia
    for x in range(0, int(width), 50):
        c.drawString(x, height - 10, str(x))
        c.line(x, 0, x, height)
    for y in range(0, int(height), 50):
        c.drawString(5, height - y, str(y))
        c.line(0, height - y, width, height - y)

    c.drawString(100, height - 100, "Ajusta las coordenadas aquí")
    c.save()

# Generar el PDF de prueba
generar_prueba_posiciones("prueba_posiciones.pdf")
