import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from config import DESCRIPCIONES_AREAS_EN

MONGO_URI = "mongodb+srv://martinjauma:sarAcademia@academiasar.pgsk3mr.mongodb.net/"
DB_NAME = "SAR"

def run_migration():
    print(f"Connecting to MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # 1. Migrar Usuarios y Credenciales
    print("1. Migrando usuarios...")
    df_users = pd.read_csv("credenciales_evaluadores.csv")
    users_col = db["users"]
    users_col.create_index("usuario", unique=True)
    for _, row in df_users.iterrows():
        user_doc = {
            "nombre": row["Nombre"],
            "area": row["Area"],
            "rol": row["Rol"],
            "usuario": row["Usuario"],
            "contrasena": str(row["Contrasena"]).strip(),
            "updatedAt": datetime.now()
        }
        users_col.update_one({"usuario": row["Usuario"]}, {"$set": user_doc}, upsert=True)
    print(f"   ✓ {len(df_users)} usuarios sincronizados.")

    # 2. Migrar Preguntas por Año y Área
    print("2. Migrando preguntas...")
    df_preguntas = pd.read_csv("preguntas_areas.csv")
    questions_col = db["questions"]
    questions_col.create_index([("year", 1), ("area", 1), ("numeroPregunta", 1)], unique=True)
    
    count_q = 0
    for _, row in df_preguntas.iterrows():
        year = int(row["Year"])
        area = row["Area"]
        num = int(row["Numero_Pregunta"])
        pregunta_es = str(row["Pregunta"]).strip()
        
        # Buscar traducción en inglés si existe
        pregunta_en = pregunta_es
        if area in DESCRIPCIONES_AREAS_EN:
            lista_en = DESCRIPCIONES_AREAS_EN[area]
            if num - 1 < len(lista_en):
                pregunta_en = lista_en[num - 1]

        q_doc = {
            "year": year,
            "area": area,
            "numeroPregunta": num,
            "preguntaEs": pregunta_es,
            "preguntaEn": pregunta_en,
            "updatedAt": datetime.now()
        }
        questions_col.update_one(
            {"year": year, "area": area, "numeroPregunta": num},
            {"$set": q_doc},
            upsert=True
        )
        count_q += 1
    print(f"   ✓ {count_q} preguntas sincronizadas.")

    # 3. Migrar Evaluadores por Año y Área
    print("3. Migrando evaluadores...")
    df_evaluadores = pd.read_csv("evaluadores_areas.csv")
    evaluators_col = db["evaluators"]
    evaluators_col.create_index([("year", 1), ("area", 1)], unique=True)

    count_ev = 0
    for _, row in df_evaluadores.iterrows():
        year = int(row["Year"])
        area = row["Area"]
        evaluador = str(row["Evaluador"]).strip()
        
        ev_doc = {
            "year": year,
            "area": area,
            "evaluador": evaluador,
            "updatedAt": datetime.now()
        }
        evaluators_col.update_one(
            {"year": year, "area": area},
            {"$set": ev_doc},
            upsert=True
        )
        count_ev += 1
    print(f"   ✓ {count_ev} evaluadores sincronizados.")

    # 4. Migrar Participantes
    print("4. Migrando participantes...")
    df_part = pd.read_csv("SAR 2024 ACADEMIA HP/Participantes x Areas.csv")
    participants_col = db["participants"]
    participants_col.create_index([("nombre", 1), ("area", 1), ("year", 1)], unique=True)

    count_p = 0
    for _, row in df_part.iterrows():
        nombre = str(row["NOMBRE"]).strip()
        union = str(row["UNION/FEDERACION"]).strip()
        email = str(row["EMAIL"]).strip() if pd.notna(row["EMAIL"]) else ""
        contacto = str(row["CONTACTO"]).strip() if pd.notna(row["CONTACTO"]) else ""
        area = str(row["AREA"]).strip()
        fecha = str(row["FECHA"]).strip() if pd.notna(row["FECHA"]) else "Noviembre, 2024"
        
        # Extraer año de la fecha o default a 2024
        year = 2024
        for y in [2023, 2024, 2025, 2026]:
            if str(y) in fecha:
                year = y
                break

        p_doc = {
            "nombre": nombre,
            "union": union,
            "email": email,
            "contacto": contacto,
            "area": area,
            "fecha": fecha,
            "year": year,
            "updatedAt": datetime.now()
        }
        participants_col.update_one(
            {"nombre": nombre, "area": area, "year": year},
            {"$set": p_doc},
            upsert=True
        )
        count_p += 1
    print(f"   ✓ {count_p} participantes sincronizados.")

    # 5. Configurar Encabezados por Año
    print("5. Configurando encabezados por año...")
    year_settings_col = db["year_settings"]
    year_settings_col.create_index("year", unique=True)
    
    headers = [
        {"year": 2023, "titulo": "SAR 2023", "headerImage": "/images/header_2023.png", "activo": True},
        {"year": 2024, "titulo": "SAR 2024", "headerImage": "/images/header_2024.png", "activo": True},
        {"year": 2025, "titulo": "SAR 2025", "headerImage": "/images/header_2025.png", "activo": True},
    ]
    for h in headers:
        year_settings_col.update_one(
            {"year": h["year"]},
            {"$set": h},
            upsert=True
        )
    print("   ✓ Encabezados por año configurados.")
    print("\n¡Migración completa exitosamente!")

if __name__ == "__main__":
    run_migration()

