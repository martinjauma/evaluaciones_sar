# config.py
import pandas as pd
import os
from datetime import datetime

# Función para cargar las preguntas desde el CSV por año
def cargar_preguntas_desde_csv(year=None, archivo_csv="preguntas_areas.csv"):
    """
    Carga las preguntas de evaluación desde un archivo CSV filtradas por año.

    Args:
        year: Año de las preguntas (None = año actual)
        archivo_csv: Ruta al archivo CSV con las preguntas

    Returns:
        dict: Diccionario con las áreas como keys y listas de preguntas como values
    """
    try:
        # Si no se proporciona año, usar el año actual
        if year is None:
            year = datetime.now().year

        # Obtener la ruta absoluta del archivo
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_completa = os.path.join(ruta_base, archivo_csv)

        # Leer el CSV
        df = pd.read_csv(ruta_completa)

        # Filtrar por año
        df_year = df[df['Year'] == year]

        # Si no hay datos para ese año, usar el año más reciente disponible
        if df_year.empty:
            max_year = df['Year'].max()
            print(f"⚠️ No hay preguntas para el año {year}. Usando año {max_year}")
            df_year = df[df['Year'] == max_year]

        # Crear diccionario agrupando por área
        preguntas_dict = {}
        for area in df_year['Area'].unique():
            preguntas = df_year[df_year['Area'] == area].sort_values('Numero_Pregunta')['Pregunta'].tolist()
            preguntas_dict[area] = preguntas

        return preguntas_dict
    except Exception as e:
        print(f"Error al cargar preguntas desde CSV: {e}")
        # Si falla, retornar diccionario vacío para que la app no se rompa
        return {}

# Función para cargar evaluadores desde el CSV por año
def cargar_evaluadores_desde_csv(year=None, archivo_csv="evaluadores_areas.csv"):
    """
    Carga los evaluadores desde un archivo CSV filtrados por año.

    Args:
        year: Año de los evaluadores (None = año actual)
        archivo_csv: Ruta al archivo CSV con los evaluadores

    Returns:
        dict: Diccionario con las áreas como keys y nombres de evaluadores como values
    """
    try:
        # Si no se proporciona año, usar el año actual
        if year is None:
            year = datetime.now().year

        # Obtener la ruta absoluta del archivo
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_completa = os.path.join(ruta_base, archivo_csv)

        # Leer el CSV
        df = pd.read_csv(ruta_completa)

        # Filtrar por año
        df_year = df[df['Year'] == year]

        # Si no hay datos para ese año, usar el año más reciente disponible
        if df_year.empty:
            max_year = df['Year'].max()
            print(f"⚠️ No hay evaluadores para el año {year}. Usando año {max_year}")
            df_year = df[df['Year'] == max_year]

        # Crear diccionario con área y evaluador
        evaluadores_dict = {}
        for _, row in df_year.iterrows():
            evaluadores_dict[row['Area']] = row['Evaluador']

        return evaluadores_dict
    except Exception as e:
        print(f"Error al cargar evaluadores desde CSV: {e}")
        # Si falla, retornar diccionario vacío
        return {}

# Descripciones por área (cargadas desde CSV)
# MAJ: Ahora las preguntas se cargan desde preguntas_areas.csv con soporte para años
# Para modificar las preguntas, editar el archivo preguntas_areas.csv
# Por defecto, carga las del año actual
DESCRIPCIONES_AREAS = cargar_preguntas_desde_csv()

# Evaluadores por área (cargados desde CSV)
# MAJ: Ahora los evaluadores se cargan desde evaluadores_areas.csv con soporte para años
# Para modificar los evaluadores, editar el archivo evaluadores_areas.csv
# Por defecto, carga los del año actual
EVALUADORES_AREAS = cargar_evaluadores_desde_csv()

DESCRIPCIONES_AREAS_EN = {
    "Video & Análisis": [
        "Creativity / Proactivity.",
        "Decision making / Problem solving.",
        "Punctuality and commitment.",
        "Communication skills.",
        "Teamwork, with peers, other staff.",
        "Visual communication.",
        "Data and statistics.",
        "Knowledge of the game.",
        "Able to solve technology outside of video analysis.",
        "Video capture - Real Time coding.",
    ],
    "Coaching": [
        "Exercise explanation, dynamics, time utilization.",
        "Exercise objective(s).",
        "Correction and transmission.",
        "Feedback.",
        "Decision making - problem solving.",
        "Receptivity.",
        "Relationship with other coaches, other staff and players.",
        "Team analysis capacity.",
        "Analysis capacity during the match.",
        "Analysis capacity after the match.",
    ],
    "Fisio": [
        "Creativity / Proactivity.",
        "Decision making / Problem solving.",
        "Punctuality and commitment.",
        "Communication skills with Players, Staff, Extras.",
        "Teamwork, with peers, other staff.",
        "Organization and Planning.",
        "Management of physio room, gym and field.",
        "Interpretation of planning.",
        "Management of technological tools, GPS, evaluations.",
        "Knowledge of the game.",
    ],
    "Logística & Utilería": [
        "Teamwork.",
        "Planning.",
        "Order.",
        "Creativity.",
        "Punctuality.",
        "Decision making - problem solving.",
        "Knowledge of the game.",
        "Predisposition / Energy.",
        "Ability to work and learn.",
        "Proactive.",
    ],
    "Match Official": [
        "Commitment / Punctuality.",
        "Personal training objective(s).",
        "Demonstration of tools for game management.",
        "Feedback.",
        "Decision making - problem solving.",
        "Receptivity.",
        "Relationship with other coaches, other staff and players.",
        "Team analysis capacity.",
        "Analysis capacity during the match.",
        "Analysis capacity after the match.",
    ],
    "Médico": [
        "Creativity / Proactivity.",
        "Decision making / Problem solving.",
        "Punctuality / Commitment.",
        "Communication skills with Players / Staff, etc.",
        "Teamwork with peers, other staff.",
        "Organization and Planning.",
        "Management of physio room, gym and field.",
        "Interpretation of planning.",
        "Management of technological tools, GPS, evaluations and HIA video review.",
        "Knowledge of the game.",
    ],
    "Preparación Física": [
        "Commitment / Punctuality.",
        "Level of training and previous experience.",
        "Planning / Setting objectives.",
        "Teamwork, with peers, other staff.",
        "Communication skills with players, staff, extras.",
        "Creativity / Proactivity.",
        "Decision making / Problem solving.",
        "Leadership of activities.",
        "Control and organization of activities and work times.",
        "Interpretation, analysis and use of data.",
    ],
    "Team Manager": [
        "Commitment / Punctuality.",
        "Previous experience.",
        "Planning / Setting objectives.",
        "Field work.",
        "Communication skills (players, staff, extras).",
        "Creativity / Proactivity.",
        "Decision making / Problem solving.",
        "Leadership of activities.",
        "Teamwork, with peers, other staff.",
        "Control and organization of activities.",
    ],
    "Nutrición":[
        "Creativity / Proactivity",
        "Decision making / Problem solving",
        "Time management and commitment",
        "Communication skills with Players, Staff, Extras",
        "Teamwork, with peers, other staff",
        "Level of training in Sports Nutrition",
        "Management of ISAK 2 protocol for measurement",
        "Anthropometric interpretation",
        "Management of technological, computer, etc. tools.",
        "Knowledge of the game and physical preparation",
    ],
}