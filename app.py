import streamlit as st
from datetime import datetime
import pandas as pd
from config import DESCRIPCIONES_AREAS_EN, cargar_preguntas_desde_csv, cargar_evaluadores_desde_csv
from pymongo import MongoClient
from babel.dates import format_date
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from deep_translator import GoogleTranslator

# Función para formatear la fecha en español
def formatear_fecha(fecha):
    return format_date(fecha, format='MMMM yyyy', locale='es')

# Conexión a MongoDB usando la configuración desde st.secrets
client = MongoClient(st.secrets["mongo_uri"])
db = client[st.secrets["db_name"]]  # Usamos el nombre de la base de datos
collection = db[st.secrets["collection_name"]]  # Usamos el nombre de la colección
def cargar_evaluacion(nombre, area):
    evaluacion_guardada = collection.find_one(
        {"nombre": nombre, "area": area},
        sort=[("fecha", -1)]  # Ordenar por fecha descendente para obtener la más reciente
    )
    return evaluacion_guardada

# Guardar evaluación en MongoDB
def guardar_evaluacion(datos, evaluaciones, conclusion, evaluador, descripciones_areas):
    # Asegurarse de que todas las descripciones estén en evaluaciones, si no tienen calificación asignada se les da un 0
    for e in descripciones_areas[datos["area"]]: #MAJ las descripciones se pasan como parámetro
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

# Función para agregar número de páginas al pie de cada página
def add_page_number(canvas, doc):
    canvas.saveState()
    page_number = canvas.getPageNumber()  # Número de la página actual
    canvas.setFont("Helvetica", 8)
    canvas.drawString(520, 10, f"Página {page_number}")  # Coloca el número de página en el pie
    canvas.drawCentredString(300, 10, "Generado por el sistema de Evaluación SAR")  # Texto centrado
    canvas.restoreState()

# Generar PDF con ReportLab
def generar_pdf_con_reportlab(datos, evaluaciones, conclusion, evaluador, output_path, language='es', header_pdf_path=None):
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    # Estilos personalizados
    styles.add(ParagraphStyle(name="CustomTitle", fontSize=14, alignment=0, textColor=colors.HexColor("#0A0A45"), fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="CustomSubtitle", fontSize=11, spaceAfter=10, textColor=colors.goldenrod, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="CustomFooter", fontSize=10, alignment=2, textColor=colors.grey))
    styles.add(ParagraphStyle(name="TableCell", fontSize=8, alignment=0, leading=12))  # Tamaño de fuente para descripción y observaciones
    styles.add(ParagraphStyle(name="ClassificacionCell", fontSize=12, alignment=1, leading=12))  # Tamaño de fuente para clasificación (centrado)

    elements = []

    if header_pdf_path:
        try:
            img = Image(header_pdf_path, width=A4[0] - 80, height=(A4[0] - 80) * 0.2)  # Ajusta proporción
            elements.append(img)
        except IOError:
            elements.append(Paragraph("<b>Encabezado no disponible</b>", styles["Normal"]))

    # Título EVALUACIÓN con la fecha en la misma fila
    elements.append(Spacer(1, 5))

    # Obtener la fecha desde los datos y usarla como texto
    fecha_original = datos['fecha']
    
    if language == 'en':
        title_text = "EVALUATION"
        area_text = "Area"
        nombre_text = "Name"
        contacto_text = "Contact"
        celular_text = "Phone"
        union_text = "Union/Federation"
        table_header = ["Description", "Rating", "Observations"]
        total_text = "Total"
        conclusion_text = "Conclusion"
    else:
        title_text = "EVALUACIÓN"
        area_text = "Área"
        nombre_text = "Nombre"
        contacto_text = "Contacto"
        celular_text = "Celular"
        union_text = "Unión/Federación"
        table_header = ["Descripción", "Calificación", "Observaciones"]
        total_text = "Total"
        conclusion_text = "Conclusión"


    # Crear una tabla para el encabezado con EVALUACIÓN y Fecha
    header_table_data = [
        [Paragraph(f"<b>{title_text}</b>", styles["CustomTitle"]),
         Paragraph(f"{fecha_original}", ParagraphStyle(name="DateStyle", fontSize=11, alignment=2))]
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
    elements.append(Paragraph(f"<b>{area_text}:</b> {datos['area']}", styles["CustomSubtitle"]))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(f"<b>{nombre_text}:</b> {datos['nombre']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>{contacto_text}:</b> {datos['email']} | <b>{celular_text}:</b> {datos['celular']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>{union_text}:</b> {datos['uni']}", styles["Normal"]))

    # Tabla de evaluaciones
    elements.append(Spacer(1, 20))
    table_data = [table_header] + [
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
    elements.append(Paragraph(f"<b>{total_text}:</b> {total_calificaciones}", styles["CustomTitle"]))

    # Conclusión y Evaluador
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"<b>{conclusion_text}:</b> {conclusion}", styles["Normal"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"{evaluador}", styles["CustomFooter"]))

    # Agregar número de página al footer
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

# Aplicación principal de Streamlit
def main():
    
    #MAJ Ruta de la imagen del logo EN LA APP
    logo_path = "images/Hori_D_blanco_SAR.png"  # Cambia esta ruta si es necesario

    # Mostrar el logo en la barra lateral
    st.sidebar.image(logo_path, width=200)  # Ajusta el ancho de la imagen manualmente
    st.title("Generador de Evaluaciones")

    header_options = {
        "SAR 2025": "images/header_2025.png",
        "SAR 2024": "images/header_2024.png",
        "SAR 2023": "images/header_2023.png"
    }
    selected_header = st.sidebar.selectbox("Seleccionar Encabezado", list(header_options.keys()))
    header_pdf_path = header_options[selected_header]

    # Cargar datos antes de los tabs para que estén disponibles en ambos
    PARTICIPANTES_CSV_PATH = "SAR 2024 ACADEMIA HP/Participantes x Areas.csv" #MAJ CSV DE LOS PARTICIPANTES A EVALUAR
    df_participantes = pd.read_csv(PARTICIPANTES_CSV_PATH)

    # Filtrar por año seleccionado y cargar preguntas/evaluadores del año correspondiente
    year_to_filter = selected_header.split(" ")[-1]
    year_int = int(year_to_filter)
    df_participantes = df_participantes[df_participantes["FECHA"].str.contains(year_to_filter, na=False)]

    # Cargar preguntas y evaluadores para el año seleccionado
    DESCRIPCIONES_AREAS = cargar_preguntas_desde_csv(year=year_int)
    EVALUADORES_AREAS = cargar_evaluadores_desde_csv(year=year_int)

    area = st.sidebar.selectbox("Área de Evaluación", list(DESCRIPCIONES_AREAS.keys()))
    participantes_area = df_participantes[df_participantes["AREA"] == area]
    evaluador = EVALUADORES_AREAS.get(area, "Evaluador no asignado")
    st.sidebar.text_input("Evaluador", value=evaluador, disabled=True)
    nombre = st.sidebar.selectbox("Nombre del Evaluado", participantes_area["NOMBRE"].unique())

    # Limpiar session_state si cambió el participante o área
    current_selection = f"{nombre}_{area}"
    if "last_selection" not in st.session_state:
        st.session_state["last_selection"] = current_selection
    elif st.session_state["last_selection"] != current_selection:
        # Cambió el participante o área, limpiar session_state
        keys_to_delete = [k for k in st.session_state.keys() if k.startswith("cal_") or k.startswith("obs_") or k == "conclusion_guardada"]
        for k in keys_to_delete:
            del st.session_state[k]
        st.session_state["last_selection"] = current_selection

    if nombre:
        datos_participante = participantes_area[participantes_area["NOMBRE"] == nombre].iloc[0]
        contacto, celular, union, fecha_evaluacion = datos_participante["EMAIL"], datos_participante["CONTACTO"], datos_participante["UNION/FEDERACION"], datos_participante["FECHA"]
        st.sidebar.write(f"**Fecha de Evaluación:** {fecha_evaluacion}")
        evaluacion_guardada = cargar_evaluacion(nombre, area)

        # DEBUG: Mostrar si se encontró evaluación guardada
        if evaluacion_guardada:
            st.sidebar.success(f"✅ Evaluación encontrada en MongoDB")
            st.sidebar.write(f"📊 {len(evaluacion_guardada.get('evaluaciones', []))} preguntas guardadas")

            # Inicializar session_state con los datos guardados
            # IMPORTANTE: Siempre actualizar session_state con los datos de MongoDB
            # para asegurar que los widgets tengan los valores correctos
            for ev in evaluacion_guardada.get('evaluaciones', []):
                desc = ev.get('descripcion', '')
                key_cal = f"cal_{desc}"
                key_obs = f"obs_{desc}"
                # Solo actualizar si no existe en session_state (no fue editado por el usuario)
                if key_cal not in st.session_state:
                    st.session_state[key_cal] = str(ev.get('calificacion', ''))
                if key_obs not in st.session_state:
                    st.session_state[key_obs] = ev.get('observaciones', '')
            # Guardar conclusión
            if 'conclusion_guardada' not in st.session_state:
                st.session_state['conclusion_guardada'] = evaluacion_guardada.get('conclusion', '')
        else:
            st.sidebar.info("ℹ️ No hay evaluación previa guardada")
    else:
        contacto, celular, union, fecha_evaluacion = "", "", "", ""
        evaluacion_guardada = None

    # Crear placeholder para el total en el sidebar
    sidebar_total_placeholder = st.sidebar.empty()

    # Crear tabs después de cargar los datos
    tab1, tab2 = st.tabs(["Español", "English"])

    with tab1:
        st.header("Evaluación en Español")
        descripciones = DESCRIPCIONES_AREAS[area]
        evaluaciones = []
        suma_calificaciones = 0


        #MAJ CSS personalizado para aumentar el tamaño de las descripciones EN LA APP
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
        for i, descripcion in enumerate(descripciones):
            # Mostrar descripción con estilo personalizado
            st.markdown(f'<p class="descripcion-grande">{descripcion}</p>', unsafe_allow_html=True)

            # Los valores ahora vienen directamente de session_state (si existen) o quedan vacíos
            # Streamlit maneja automáticamente el valor con el key
            calificacion = st.text_input(f"Puntaje 0 al 5", key=f"cal_{descripcion}")
            observaciones = st.text_area(f"Observaciones", key=f"obs_{descripcion}")
            
            # Solo aceptar valores de "0", "1", "2", "3", "4", "5"
            if calificacion in ['0', '1', '2', '3', '4', '5']:
                evaluaciones.append({"descripcion": descripcion, "calificacion": int(calificacion), "observaciones": observaciones})
                suma_calificaciones += int(calificacion)
            elif calificacion != "":  # Mostrar advertencia si el valor no es permitido
                st.warning("Solo se permiten los valores 0, 1, 2, 3, 4, 5 para las calificaciones.")

            # Separar cada bloque con una línea
            st.markdown("---")
        
        # La conclusión también usa session_state
        conclusion = st.text_area("Conclusión de la Evaluación", key="conclusion_guardada")

        # Mostrar suma de calificaciones con colores condicionales en el placeholder
        if suma_calificaciones <= 29:
            color = "red"
        elif 30 <= suma_calificaciones <= 40:
            color = "yellow"
        else:
            color = "green"

        sidebar_total_placeholder.markdown(f"<h1 style='color:{color}; font-size: 30px;'>{suma_calificaciones} puntos</h1>", unsafe_allow_html=True)

        if st.button("Generar Evaluación (PDF) y Guardar"):
            datos = {
                "fecha": fecha_evaluacion,
                "area": area,
                "nombre": nombre,
                "uni": union,
                "email": contacto,
                "celular": celular,
            }
            output_path = "evaluacion_final.pdf"
            generar_pdf_con_reportlab(datos, evaluaciones, conclusion, evaluador, output_path, language='es', header_pdf_path=header_pdf_path)
            guardar_evaluacion(datos, evaluaciones, conclusion, evaluador, DESCRIPCIONES_AREAS)

            with open(output_path, "rb") as pdf_file:
                st.download_button(label="Descargar Evaluación (PDF)",
                                   data=pdf_file, file_name=f"{datos['area']}-{datos['nombre']}-{datos['uni']}.pdf",
                                   mime="application/pdf")

    with tab2:
        st.header("Evaluation in English")
        descripciones_en = DESCRIPCIONES_AREAS_EN.get(area, DESCRIPCIONES_AREAS[area])  # Fallback a español si no existe traducción
        descripciones_es = DESCRIPCIONES_AREAS[area]  # Necesitamos las descripciones en español para mapear

        evaluaciones_en = []
        suma_calificaciones_en = 0

        # CSS personalizado
        st.markdown(
            """
            <style>
            .descripcion-grande {
                font-size: 30px;
                font-weight: bold;
                color: #fff;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        for i, (descripcion_en, descripcion_es) in enumerate(zip(descripciones_en, descripciones_es)):
            # Cargar y traducir datos guardados si existen - BUSCAR POR DESCRIPCIÓN EXACTA
            calificacion_guardada = ""
            observaciones_traducidas = ""
            if evaluacion_guardada and 'evaluaciones' in evaluacion_guardada:
                # Buscar la evaluación que coincida con esta descripción en español
                for ev_guardada in evaluacion_guardada['evaluaciones']:
                    if ev_guardada.get('descripcion', '') == descripcion_es:
                        calificacion_guardada = ev_guardada.get('calificacion', "")
                        observaciones_originales = ev_guardada.get('observaciones', "")
                        if observaciones_originales:
                            try:
                                observaciones_traducidas = GoogleTranslator(source='es', target='en').translate(observaciones_originales)
                            except:
                                observaciones_traducidas = observaciones_originales
                        break

            st.markdown(f'<p class="descripcion-grande">{descripcion_en}</p>', unsafe_allow_html=True)
            calificacion_en = st.text_input(f"Score 0 to 5", value=str(calificacion_guardada), key=f"cal_en_{i}")
            observaciones_en = st.text_area(f"Observations", value=observaciones_traducidas, key=f"obs_en_{i}")

            # Validar y guardar evaluaciones
            if calificacion_en in ['0', '1', '2', '3', '4', '5']:
                evaluaciones_en.append({
                    "descripcion": descripcion_en,
                    "descripcion_es": descripcion_es,  # Guardamos la versión en español también
                    "calificacion": int(calificacion_en),
                    "observaciones": observaciones_en
                })
                suma_calificaciones_en += int(calificacion_en)
            elif calificacion_en != "":
                st.warning("Only values 0, 1, 2, 3, 4, 5 are allowed for ratings.")

            st.markdown("---")

        conclusion_traducida = ""
        if evaluacion_guardada and 'conclusion' in evaluacion_guardada and evaluacion_guardada['conclusion']:
            try:
                conclusion_traducida = GoogleTranslator(source='es', target='en').translate(evaluacion_guardada['conclusion'])
            except:
                conclusion_traducida = evaluacion_guardada['conclusion']

        conclusion_en = st.text_area("Conclusion", value=conclusion_traducida, key="conclusion_en")

        # Mostrar suma de calificaciones en el placeholder (sobrescribe el del tab español)
        if suma_calificaciones_en <= 29:
            color = "red"
        elif 30 <= suma_calificaciones_en <= 40:
            color = "yellow"
        else:
            color = "green"

        sidebar_total_placeholder.markdown(f"<h1 style='color:{color}; font-size: 30px;'>{suma_calificaciones_en} points</h1>", unsafe_allow_html=True)

        if st.button("Generate English Evaluation (PDF)"):
            datos = {
                "fecha": fecha_evaluacion,
                "area": area,
                "nombre": nombre,
                "uni": union,
                "email": contacto,
                "celular": celular,
            }
            output_path = "evaluacion_final_en.pdf"

            generar_pdf_con_reportlab(datos, evaluaciones_en, conclusion_en, evaluador, output_path, language='en', header_pdf_path=header_pdf_path)

            with open(output_path, "rb") as pdf_file:
                st.download_button(label="Download English Evaluation (PDF)",
                                   data=pdf_file, file_name=f"{datos['area']}-{datos['nombre']}-{datos['uni']}_EN.pdf",
                                   mime="application/pdf")

if __name__ == "__main__":
    main()
