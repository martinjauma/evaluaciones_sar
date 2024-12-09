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

# Función para formatear la fecha en español
def formatear_fecha(fecha):
    return format_date(fecha, format='MMMM yyyy', locale='es')

# Conexión a MongoDB usando la configuración desde config_mongo.py
client = MongoClient(config_mongo.MONGO_URI)
db = client[config_mongo.DB_NAME]  # Usamos el nombre de la base de datos
collection = db[config_mongo.COLLECTION_NAME]  # Usamos el nombre de la colección

# Guardar evaluación en MongoDB
def guardar_evaluacion(datos, evaluaciones, conclusion, evaluador):
    evaluacion_doc = {
        "nombre": datos["nombre"],
        "area": datos["area"],
        "fecha": datetime.now(),
        "evaluador": evaluador,
        "evaluaciones": evaluaciones,
        "conclusion": conclusion
    }
    collection.insert_one(evaluacion_doc)
    print("Evaluación guardada en MongoDB")

# Generar PDF con ReportLab
def generar_pdf_con_reportlab(datos, evaluaciones, conclusion, evaluador, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    # Estilos personalizados
    styles.add(ParagraphStyle(name="CustomTitle", fontSize=14, alignment=0, textColor=colors.HexColor("#0A0A45")))
    styles.add(ParagraphStyle(name="CustomSubtitle", fontSize=12, spaceAfter=10, textColor=colors.black))
    styles.add(ParagraphStyle(name="CustomFooter", fontSize=8, alignment=2, textColor=colors.grey))
    styles.add(ParagraphStyle(name="TableCell", fontSize=10, alignment=0, leading=12))

    elements = []

    # Encabezado con imagen
    header_image = "images/encSARAca.jpeg"
    try:
        img = Image(header_image, width=A4[0] - 80, height=(A4[0] - 80) * 0.2)  # Ajusta proporción
        elements.append(img)
    except IOError:
        elements.append(Paragraph("<b>Encabezado no disponible</b>", styles["Normal"]))

    # Título EVALUACIÓN
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("EVALUACIÓN", styles["CustomTitle"]))

    # Información del evaluado
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"<b>Área:</b> {datos['area']}", styles["CustomSubtitle"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"<b>Contacto:</b> {datos['email']} | <b>Celular:</b> {datos['celular']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Unión/Federación:</b> {datos['uni']}", styles["Normal"]))

    # Tabla de evaluaciones
    elements.append(Spacer(1, 20))
    table_data = [["Descripción", "Calificación", "Observaciones"]] + [
        [Paragraph(e["descripcion"], styles["TableCell"]),
         Paragraph(str(e["calificacion"]), styles["TableCell"]),
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

    # Conclusión y Evaluador
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"<b>Conclusión:</b> {conclusion}", styles["Normal"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"<b>Evaluador:</b> {evaluador}", styles["CustomFooter"]))

    doc.build(elements)
    print(f"PDF generado en {output_path}")

# Aplicación principal de Streamlit
def main():
    st.title("Generador de Evaluaciones")
    PARTICIPANTES_CSV_PATH = "SAR 2024 ACADEMIA HP/Participantes x Areas.csv"
    df_participantes = pd.read_csv(PARTICIPANTES_CSV_PATH)

    area = st.sidebar.selectbox("Área de Evaluación", list(DESCRIPCIONES_AREAS.keys()))
    participantes_area = df_participantes[df_participantes["AREA"] == area]
    nombre = st.sidebar.selectbox("Nombre del Evaluado", participantes_area["NOMBRE"].unique())

    if nombre:
        datos_participante = participantes_area[participantes_area["NOMBRE"] == nombre].iloc[0]
        contacto, celular, union = datos_participante["EMAIL"], datos_participante["CONTACTO"], datos_participante["UNION/FEDERACION"]
    else:
        contacto, celular, union = "", "", ""

    evaluador = EVALUADORES_AREAS.get(area, "Evaluador no asignado")
    st.sidebar.text_input("Evaluador", value=evaluador, disabled=True)

    descripciones = DESCRIPCIONES_AREAS[area]
    evaluaciones = []
    suma_calificaciones = 0

    for descripcion in descripciones:
        calificacion = st.number_input(f"Calificación ({descripcion})", 0, 5, key=f"cal_{descripcion}")
        observaciones = st.text_area(f"Observaciones ({descripcion})", key=f"obs_{descripcion}")
        evaluaciones.append({"descripcion": descripcion, "calificacion": calificacion, "observaciones": observaciones})
        suma_calificaciones += calificacion

    st.sidebar.write(f"**Total de Calificaciones: {suma_calificaciones} puntos**")

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
            st.download_button(label="Descargar Evaluación (PDF)", data=pdf_file, file_name="EvaluacionFinal.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
