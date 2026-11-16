import json
import pandas as pd
from config import DESCRIPCIONES_AREAS_EN

users = pd.read_csv('credenciales_evaluadores.csv').to_dict(orient='records')
evaluators = pd.read_csv('evaluadores_areas.csv').to_dict(orient='records')
preguntas_raw = pd.read_csv('preguntas_areas.csv').to_dict(orient='records')

questions = []
for p in preguntas_raw:
    year = int(p['Year'])
    area = p['Area']
    num = int(p['Numero_Pregunta'])
    pes = str(p['Pregunta']).strip()
    pen = pes
    if area in DESCRIPCIONES_AREAS_EN:
        lista_en = DESCRIPCIONES_AREAS_EN[area]
        if num - 1 < len(lista_en):
            pen = lista_en[num - 1]
    questions.append({
        'year': year,
        'area': area,
        'numeroPregunta': num,
        'preguntaEs': pes,
        'preguntaEn': pen
    })

part_df = pd.read_csv('SAR 2024 ACADEMIA HP/Participantes x Areas.csv')
participants = []
for _, row in part_df.iterrows():
    f = str(row['FECHA']) if pd.notna(row['FECHA']) else 'Noviembre, 2024'
    y = 2024
    for check_y in [2023, 2024, 2025, 2026]:
        if str(check_y) in f:
            y = check_y
            break
    participants.append({
        'nombre': str(row['NOMBRE']).strip(),
        'union': str(row['UNION/FEDERACION']).strip(),
        'email': str(row['EMAIL']).strip() if pd.notna(row['EMAIL']) else '',
        'contacto': str(row['CONTACTO']).strip() if pd.notna(row['CONTACTO']) else '',
        'area': str(row['AREA']).strip(),
        'fecha': f,
        'year': y
    })

year_settings = [
    {'year': 2023, 'titulo': 'SAR 2023', 'headerImage': '/images/header_2023.png', 'activo': True},
    {'year': 2024, 'titulo': 'SAR 2024', 'headerImage': '/images/header_2024.png', 'activo': True},
    {'year': 2025, 'titulo': 'SAR 2025', 'headerImage': '/images/header_2025.png', 'activo': True},
]

users_list = [{
    'nombre': u['Nombre'],
    'area': u['Area'],
    'rol': u['Rol'],
    'usuario': u['Usuario'],
    'contrasena': str(u['Contrasena']).strip()
} for u in users]

evaluators_list = [{
    'year': int(e['Year']),
    'area': e['Area'],
    'evaluador': str(e['Evaluador']).strip()
} for e in evaluators]

out = "import { User, Participant, Question, Evaluator, YearSetting } from '@/types';\n\n"
out += f"export const INITIAL_USERS: User[] = {json.dumps(users_list, ensure_ascii=False, indent=2)};\n\n"
out += f"export const INITIAL_YEAR_SETTINGS: YearSetting[] = {json.dumps(year_settings, ensure_ascii=False, indent=2)};\n\n"
out += f"export const INITIAL_EVALUATORS: Evaluator[] = {json.dumps(evaluators_list, ensure_ascii=False, indent=2)};\n\n"
out += f"export const INITIAL_QUESTIONS: Question[] = {json.dumps(questions, ensure_ascii=False, indent=2)};\n\n"
out += f"export const INITIAL_PARTICIPANTS: Participant[] = {json.dumps(participants, ensure_ascii=False, indent=2)};\n"

with open('sar-web/src/lib/initialData.ts', 'w') as f:
    f.write(out)

print("Generated sar-web/src/lib/initialData.ts successfully!")

