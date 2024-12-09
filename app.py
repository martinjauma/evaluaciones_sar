import streamlit as st
from datetime import date
import pandas as pd
import pdfkit
from config import DESCRIPCIONES_AREAS, EVALUADORES_AREAS
from datetime import datetime
import locale
from pymongo import MongoClient
import config_mongo  # Importamos la configuración de MongoDB

# Cambiar la configuración regional a español (español de España)
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Esto puede cambiar dependiendo de tu sistema operativo

# Conexión a MongoDB usando la configuración desde config_mongo.py
client = MongoClient(config_mongo.MONGO_URI)
db = client[config_mongo.DB_NAME]  # Usamos el nombre de la base de datos
collection = db[config_mongo.COLLECTION_NAME]  # Usamos el nombre de la colección

def guardar_evaluacion(datos, evaluaciones, conclusion, evaluador):
    # Crear un documento de evaluación
    evaluacion_doc = {
        "nombre": datos["nombre"],
        "area": datos["area"],
        "fecha": datetime.now(),
        "evaluador": evaluador,
        "evaluaciones": evaluaciones,
        "conclusion": conclusion
    }
    # Insertar el documento en la colección de MongoDB
    collection.insert_one(evaluacion_doc)
    print("Evaluación guardada en MongoDB")

def generar_pdf_con_html(datos, evaluaciones, conclusion, evaluador, output_path):
    # Formateamos la fecha al estilo solicitado (solo mes y año)
    fecha_formateada = datetime.strptime(datos['fecha'], "%d/%m/%Y").strftime("%B, %Y").capitalize()

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                font-size: 12px;
                line-height: 1.4;
                color: #333;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .header img {{
                width: 100%;
                height: auto;
            }}
            .evaluation-title {{
                display: flex;
                justify-content: space-between;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 20px;
                width: 100%;
            }}
            .evaluation-title h1 {{
                color: #0a0a45;
                font-size: 18px;
                margin: 0;
                text-align: left;  /* Alinea EVALUACIÓN a la izquierda */
            }}
            .evaluation-title .date {{
                font-size: 12px;
                color: #555;
                text-align: right;  /* Alinea FECHA a la derecha */
            }}
            .area {{
                margin-bottom: 20px;
                font-size: 18px;
            }}
            .info {{
                margin-bottom: 20px;
            }}
            .info p {{
                margin: 5px 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #0a0a45;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .total {{
                margin-top: 20px;
                font-weight: bold;
                text-align: right;
            }}
            .conclusion {{
                margin-top: 30px;
                font-size: 12px;
            }}
            .conclusion .evaluador {{
                text-align: right;
                margin-top: 10px;
            }}
            .date-footer {{
                text-align: right;
                font-size: 12px;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <img src="images/encSARAca.jpeg" alt="Encabezado">
        </div>
        <div class="evaluation-title">
            <h1>EVALUACIÓN</h1>
        </div>
        <div class="area">
            <p><strong>Área:</strong> {datos['area']}</p>
        </div>
        <div class="info">
            <p><strong>Nombre:</strong> {datos['nombre']}</p>
            <p><strong>Contacto:</strong> {datos['email']} | <strong>Celular:</strong> {datos['celular']}</p>
            <p><strong>Unión/Federación:</strong> {datos['uni']}</p>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Descripción</th>
                    <th>Calificación</th>
                    <th>Observaciones</th>
                </tr>
            </thead>
            <tbody>
                {"".join(f"<tr><td>{e['descripcion']}</td><td>{e['calificacion']}</td><td>{e['observaciones']}</td></tr>" for e in evaluaciones)}
            </tbody>
        </table>
        <div class="total">
            Total Calificaciones: {sum(e['calificacion'] for e in evaluaciones)}
        </div>
        <div class="conclusion">
            <p><strong>Conclusión:</strong> {conclusion}</p>
            <p class="evaluador">{evaluador}</p>
        </div>
        <div class="date-footer">
            <strong>FECHA:</strong> {fecha_formateada}
        </div>
    </body>
    </html>
    """
    
    # Configuramos pdfkit para que use tamaño A4 y agregamos la opción para mostrar el número de páginas
    pdfkit.from_string(
        html_content,
        output_path,
        options={
            'enable-local-file-access': True,
            'page-size': 'A4',  # Aseguramos que el tamaño de página sea A4
            'footer-center': 'Generado por el sistema de Evaluación SAR |',  # Pie de página centrado
            'footer-right': 'Páginas: [page] de [topage]',  # Muestra el número de páginas en el pie de página
            'footer-font-size': '8',  # Ajustamos el tamaño de la fuente del pie de página a 10px
        }
    )
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

    # Mostrar en el sidebar el nombre del evaluador basado en el área seleccionada
    evaluador = EVALUADORES_AREAS.get(area, "Evaluador no asignado")
    st.sidebar.text_input("Evaluador", value=evaluador, disabled=True)

    st.sidebar.text_input("Correo Electrónico", value=contacto, disabled=True)
    st.sidebar.text_input("Número de Celular", value=celular, disabled=True)
    st.sidebar.text_input("Unión/Federación", value=union, disabled=True)

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
        generar_pdf_con_html(datos, evaluaciones, conclusion, evaluador, output_path)

        # Guardar en MongoDB
        guardar_evaluacion(datos, evaluaciones, conclusion, evaluador)

        with open(output_path, "rb") as pdf_file:
            st.download_button(label="Descargar Evaluación (PDF)", data=pdf_file, file_name="EvaluacionFinal.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
