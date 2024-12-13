import streamlit as st
from datetime import date, datetime
import pandas as pd
from config import DESCRIPCIONES_AREAS, EVALUADORES_AREAS
from pymongo import MongoClient
import config_mongo  # Importamos la configuración de MongoDB
from babel.dates import format_date
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image
from reportlab.pdfgen import canvas
#asdfasd

# Función para formatear la fecha en español
def formatear_fecha(fecha):
    return format_date(fecha, format='MMMM yyyy', locale='es')

# Conexión a MongoDB usando la configuración desde config_mongo.py
client = MongoClient(config_mongo.MONGO_URI)
db = client[config_mongo.DB_NAME]  # Usamos el nombre de la base de datos
collection = db[config_mongo.COLLECTION_NAME]  # Usamos el nombre de la colección

# Guardar evaluación en MongoDB
def guardar_evaluacion(datos, evaluaciones, conclusion, evaluador):
    # Asegurarse de que todas las descripciones estén en evaluaciones, si no tienen calificación asignada se les da un 0
    for e in DESCRIPCIONES_AREAS[datos["area"]]:
        if not any(ev["descripcion"] == e for ev in evaluaciones):
            evaluaciones.append({"descripcion": e, "calificacion": 0, "observaciones": ""})
    
    evaluacion_doc = {
        "nombre": datos["nombre"],
        "area": datos["area"],
        "fecha": datetime.now(),
        "evaluador": evaluador,
        "evaluaciones": evaluaciones,  # Incluye las calificaciones y observaciones
        "conclusion": conclusion
    }
    collection.insert_one(evaluacion_doc)
    print("Evaluación guardada en MongoDB")

# Función para agregar número de páginas al pie de cada página
def add_page_number(canvas, doc):
    canvas.saveState()
    page_number = canvas.getPageNumber()  # Número de la página actual
    total_pages = canvas.getPageNumber()  # Este valor lo mantenemos igual hasta el final
    canvas.setFont("Helvetica", 8)
    canvas.drawString(520, 10, f"Página {page_number} de {total_pages}")  # Coloca el número de página en el pie
    canvas.drawCentredString(300, 10, "Generado por el sistema de Evaluación SAR |")  # Texto centrado
    canvas.restoreState()

# Generar PDF con ReportLab
def generar_pdf_con_reportlab(datos, evaluaciones, conclusion, evaluador, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    # Estilos personalizados
    styles.add(ParagraphStyle(name="CustomTitle", fontSize=14, alignment=0, textColor=colors.HexColor("#0A0A45"), fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="CustomSubtitle", fontSize=11, spaceAfter=10, textColor=colors.goldenrod, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="CustomFooter", fontSize=10, alignment=2, textColor=colors.grey))
    styles.add(ParagraphStyle(name="TableCell", fontSize=8, alignment=0, leading=12))  # Tamaño de fuente para descripción y observaciones
    styles.add(ParagraphStyle(name="ClassificacionCell", fontSize=12, alignment=1, leading=12))  # Tamaño de fuente para clasificación (centrado)

    elements = []

    # Encabezado con imagen
    header_image = "images/encSARAca.jpeg"
    try:
        img = Image(header_image, width=A4[0] - 80, height=(A4[0] - 80) * 0.2)  # Ajusta proporción
        elements.append(img)
    except IOError:
        elements.append(Paragraph("<b>Encabezado no disponible</b>", styles["Normal"]))

    # Título EVALUACIÓN con la fecha en la misma fila
    elements.append(Spacer(1, 5))

    # Obtener la fecha desde los datos y formatearla en español
    fecha_original = datos['fecha']  # Asume que 'fecha' está en formato "DD/MM/YYYY"
    fecha_objeto = datetime.strptime(fecha_original, "%d/%m/%Y")
    fecha_formateada = fecha_objeto.strftime("%B, %Y")  # "diciembre, 2024" en español

    # Convertir el mes a español utilizando babel (si es necesario)
    fecha_formateada = format_date(fecha_objeto, format='MMMM yyyy', locale='es').capitalize()

    # Crear una tabla para el encabezado con EVALUACIÓN y Fecha
    header_table_data = [
        [Paragraph("<b>EVALUACIÓN</b>", styles["CustomTitle"]),
         Paragraph(f"{fecha_formateada}", ParagraphStyle(name="DateStyle", fontSize=11, alignment=2))]
    ]

    header_table = Table(header_table_data, colWidths=[300, 200])  # Ajusta el ancho de las columnas
    header_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (0, 0), "LEFT"),  # Alinear "EVALUACIÓN" a la izquierda
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),  # Alinear fecha a la derecha
        ("LEFTPADDING", (0, 0), (-1, -1), 0),  # Sin relleno izquierdo
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),  # Sin relleno derecho
        ("VALIGN", (0, 0), (-1, -1), "TOP"),  # Alinear verticalmente en la parte superior
        ("TOPPADDING", (0, 0), (-1, -1), 0),  # Sin espacio superior
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),  # Sin espacio inferior
    ]))

    elements.append(header_table)  # Agregar la tabla
    elements.append(Spacer(1, 5))  # Espacio reducido entre "EVALUACIÓN" y "ÁREA"

    # Información del evaluado
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(f"<b>Área:</b> {datos['area']}", styles["CustomSubtitle"]))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(f"<b>Nombre:</b> {datos['nombre']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Contacto:</b> {datos['email']} | <b>Celular:</b> {datos['celular']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Unión/Federación:</b> {datos['uni']}", styles["Normal"]))

    # Tabla de evaluaciones
    elements.append(Spacer(1, 20))
    table_data = [["Descripción", "Calificación", "Observaciones"]] + [
        [Paragraph(e["descripcion"], styles["TableCell"]),
         Paragraph(str(e["calificacion"]), styles["ClassificacionCell"]),  # Centrado y más grande
         Paragraph(e["observaciones"], styles["TableCell"])] for e in evaluaciones
    ]
    table = Table(table_data, colWidths=[200, 100, 200])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0A0A45")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    # Total de calificaciones (más grande)
    elements.append(Spacer(1, 10))
    total_calificaciones = sum(e["calificacion"] for e in evaluaciones)
    elements.append(Paragraph(f"<b>Total:</b> {total_calificaciones}", styles["CustomTitle"]))

    # Conclusión y Evaluador
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"<b>Conclusión:</b> {conclusion}", styles["Normal"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"{evaluador}", styles["CustomFooter"]))

    # Agregar número de página al footer
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF generado en {output_path}")

# Aplicación principal de Streamlit
def main():
    
    # Ruta de la imagen del logo
    logo_path = "images/Hori_D_blanco_SAR.png"  # Cambia esta ruta si es necesario

    # Mostrar el logo en la barra lateral
    st.sidebar.image(logo_path, width=200)  # Ajusta el ancho de la imagen manualmente
    st.title("Generador de Evaluaciones")
    PARTICIPANTES_CSV_PATH = "SAR 2024 ACADEMIA HP/Participantes x Areas.csv"
    df_participantes = pd.read_csv(PARTICIPANTES_CSV_PATH)

    area = st.sidebar.selectbox("Área de Evaluación", list(DESCRIPCIONES_AREAS.keys()))
    participantes_area = df_participantes[df_participantes["AREA"] == area]
    evaluador = EVALUADORES_AREAS.get(area, "Evaluador no asignado")
    st.sidebar.text_input("Evaluador", value=evaluador, disabled=True)
    nombre = st.sidebar.selectbox("Nombre del Evaluado", participantes_area["NOMBRE"].unique())

    if nombre:
        datos_participante = participantes_area[participantes_area["NOMBRE"] == nombre].iloc[0]
        contacto, celular, union = datos_participante["EMAIL"], datos_participante["CONTACTO"], datos_participante["UNION/FEDERACION"]
    else:
        contacto, celular, union = "", "", ""

    descripciones = DESCRIPCIONES_AREAS[area]
    evaluaciones = []
    suma_calificaciones = 0


    # CSS personalizado para aumentar el tamaño de las descripciones
    st.markdown(
        """
        <style>
        .descripcion-grande {
            font-size: 30px; /* Cambia el tamaño según tu preferencia */
            font-weight: bold;
            color: #fff; /* Ajusta el color si es necesario */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    for descripcion in descripciones:
        # Mostrar descripción con estilo personalizado
        st.markdown(f'<p class="descripcion-grande">{descripcion}</p>', unsafe_allow_html=True)
        # Cambiar input de número a texto (solo aceptando 0, 1, 2, 3, 4, 5)
        calificacion = st.text_input(f"Puntaje 0 al 5", value="", key=f"cal_{descripcion}")
        observaciones = st.text_area(f"Observaciones", key=f"obs_{descripcion}")
        
        # Solo aceptar valores de "0", "1", "2", "3", "4", "5"
        if calificacion in ['0', '1', '2', '3', '4', '5']:
            evaluaciones.append({"descripcion": descripcion, "calificacion": int(calificacion), "observaciones": observaciones})
            suma_calificaciones += int(calificacion)
        elif calificacion != "":  # Mostrar advertencia si el valor no es permitido
            st.warning("Solo se permiten los valores 0, 1, 2, 3, 4, 5 para las calificaciones.")

        # Separar cada bloque con una línea
        st.markdown("---")

    # Mostrar suma de calificaciones con colores condicionales
    if suma_calificaciones <= 29:
        color = "red"
    elif 30 <= suma_calificaciones <= 40:
        color = "yellow"
    else:
        color = "green"
        
    # Información del evaluado en el sidebar
    st.sidebar.write(f"**Correo Electrónico:** {contacto}")
    st.sidebar.write(f"**Número de Celular:** {celular}")
    st.sidebar.write(f"**Unión/Federación:** {union}")

    # Mostrar la suma de calificaciones con el KPI en el sidebar
    st.sidebar.markdown(f"<h1 style='color:{color}; font-size: 30px;'>{suma_calificaciones} puntos</h1>", unsafe_allow_html=True)

    conclusion = st.text_area("Conclusión de la Evaluación")

    if st.button("Generar Evaluación (PDF)"):
        datos = {
            "fecha": date.today().strftime('%d/%m/%Y'),
            "area": area,
            "nombre": nombre,
            "uni": union,
            "email": contacto,
            "celular": celular,
        }
        output_path = "evaluacion_final.pdf"
        generar_pdf_con_reportlab(datos, evaluaciones, conclusion, evaluador, output_path)

        guardar_evaluacion(datos, evaluaciones, conclusion, evaluador)

        with open(output_path, "rb") as pdf_file:
            st.download_button(label="Descargar Evaluación (PDF)", data=pdf_file, file_name=f"{datos['area']}-{datos['nombre']}-{datos['uni']}.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
