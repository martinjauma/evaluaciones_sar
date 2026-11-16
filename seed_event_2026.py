import toml
from pymongo import MongoClient
from datetime import datetime

secrets = toml.load('.streamlit/secrets.toml')
c = MongoClient(secrets['mongo_uri'])
db = c[secrets['db_name']]
event_col = db['academy_event_2026']

event_data = {
    "year": 2026,
    "asunto": "ACADEMIA HP SAR 2026",
    "lugar": "Rosario - Sta Fe / Argentina",
    "fecha": "06 al 12 de diciembre 2026",
    "hotel": "Solans Presidente",
    "hotelUrl": "https://www.solans.com/presidente",
    "traslados": "El traslado aeropuerto - hotel - aeropuerto es a cargo de cada participante / unión de origen. SAR no cubre estos costos.",
    "gerente": {
        "nombre": "DANIEL HOURCADE",
        "cargo": "GERENTE ALTO RENDIMIENTO SUDAMERICA RUGBY"
    },
    "disertantes": [
        {"nombre": "Daniel Hourcade", "area": "COACHING"},
        {"nombre": "Lucas Piña", "area": "COACHING"},
        {"nombre": "Ricardo Lefort", "area": "COACHING"},
        {"nombre": "Pablo Bouza", "area": "COACHING"},
        {"nombre": "Rodolfo Ambrosio", "area": "COACHING"},
        {"nombre": "Esteban Meneses", "area": "COACHING"},
        {"nombre": "Pablo Perez", "area": "COACHING"},
        {"nombre": "Raul Perez", "area": "COACHING"},
        {"nombre": "Gonzalo Santos", "area": "PF"},
        {"nombre": "Alejandro Pastor", "area": "PF"},
        {"nombre": "Martin Dominguez", "area": "PF"},
        {"nombre": "Fernando Aguilera", "area": "MEDICA"},
        {"nombre": "Juan Sylvestre", "area": "OFICIALES"},
        {"nombre": "Martin Jauma", "area": "VIDEO ANALISIS"},
        {"nombre": "Romina Garavaglia", "area": "NUTRICION"},
        {"nombre": "Martin Nuñez", "area": "FISIO"},
        {"nombre": "Pablo Perez Toranzo", "area": "TEAM MANAGER"},
        {"nombre": "Javier Sorbera Ferrer", "area": "UTILERIA"},
        {"nombre": "Paula Alejandra Mingot", "area": "UTILERIA"}
    ],
    "equipos": {
        "celeste": {
            "nombre": "STAFF CELESTE",
            "color": "bg-sky-600 text-white",
            "participantes": [
                {"nro": 1, "nombre": "Pedro Imhoff", "rol": "COACH (HC)"},
                {"nro": 2, "nombre": "Ignacio Basterra", "rol": "COACH"},
                {"nro": 3, "nombre": "Percy Rasmussen", "rol": "COACH"},
                {"nro": 4, "nombre": "Santiago García Botta", "rol": "COACH"},
                {"nro": 5, "nombre": "Ignacio Rodriguez", "rol": "COACH"},
                {"nro": 6, "nombre": "Maximiliano Soria", "rol": "PF"},
                {"nro": 7, "nombre": "Sebastián Golarte", "rol": "PF"},
                {"nro": 8, "nombre": "Danilo Trinidad", "rol": "MEDICO"},
                {"nro": 9, "nombre": "Florencia Gómez", "rol": "MEDICO"},
                {"nro": 10, "nombre": "Emmanuel Lorenzo", "rol": "MEDICO"},
                {"nro": 11, "nombre": "Luiz Felipe Silva", "rol": "VIDEO"},
                {"nro": 12, "nombre": "Florencia López Meyer", "rol": "NUTRI"},
                {"nro": 13, "nombre": "Triana Fernández", "rol": "NUTRI"},
                {"nro": 14, "nombre": "Leandro Pierucci", "rol": "FISIO"},
                {"nro": 15, "nombre": "Mateus Barbosa", "rol": "FISIO"},
                {"nro": 16, "nombre": "Germán Saavedra", "rol": "MANAGER"},
                {"nro": 17, "nombre": "Maria Gabriela Noya", "rol": "MANAGER"},
                {"nro": 18, "nombre": "Joaquín Zapata", "rol": "REFERATO"},
                {"nro": 19, "nombre": "Federico Bonesso", "rol": "LOGISTICA"}
            ]
        },
        "verde": {
            "nombre": "STAFF VERDE",
            "color": "bg-emerald-600 text-white",
            "participantes": [
                {"nro": 1, "nombre": "Diego Lamelas", "rol": "COACH (HC)"},
                {"nro": 2, "nombre": "Lucas Schonamsgruber", "rol": "COACH"},
                {"nro": 3, "nombre": "Martín Brancato", "rol": "COACH"},
                {"nro": 4, "nombre": "Felipe Caino / Carlos Caceres", "rol": "COACH"},
                {"nro": 5, "nombre": "Fernando Figueroa", "rol": "PF"},
                {"nro": 6, "nombre": "Joao Vicente Soares", "rol": "PF"},
                {"nro": 7, "nombre": "Thiago Macota", "rol": "MEDICO"},
                {"nro": 8, "nombre": "Santiago Cativiela", "rol": "MEDICO"},
                {"nro": 9, "nombre": "Nicolás Tapia", "rol": "VIDEO"},
                {"nro": 10, "nombre": "María Belén Britez Burro", "rol": "NUTRI"},
                {"nro": 11, "nombre": "Bruna Callegari", "rol": "NUTRI"},
                {"nro": 12, "nombre": "Agustina Muñiz", "rol": "NUTRI"},
                {"nro": 13, "nombre": "Felipe Galaz", "rol": "FISIO"},
                {"nro": 14, "nombre": "Silvana Mariel Luna", "rol": "FISIO"},
                {"nro": 15, "nombre": "Juan Ignacio Vattuone", "rol": "MANAGER"},
                {"nro": 16, "nombre": "Rafael Bianchi", "rol": "MANAGER"},
                {"nro": 17, "nombre": "Juan Luca Terra", "rol": "REFERATO"},
                {"nro": 18, "nombre": "Felipe Alonso", "rol": "LOGISTICA"}
            ]
        }
    },
    "cronograma": [
        {
            "id": "dia-1",
            "dia": "Domingo",
            "fecha": "6 de diciembre de 2026",
            "actividades": [
                {"hora": "13:00 A 14:00", "actividad": "ALMUERZO HOTEL", "lugar": "Hotel Presidente", "responsable": "Staff SAR", "notas": "Según arribos"},
                {"hora": "14:30 A 17:00", "actividad": "ARRIBO PARTICIPANTES HOTEL", "lugar": "Hotel Presidente", "responsable": "Team Managers", "notas": "Check-in"},
                {"hora": "19:00 A 20:00", "actividad": "BIENVENIDA PARTICIPANTES", "lugar": "Salón Hotel", "responsable": "Daniel Hourcade & Staff SAR", "notas": "Apertura oficial"},
                {"hora": "20:30", "actividad": "CENA HOTEL", "lugar": "Hotel Presidente", "responsable": "Todos", "notas": ""}
            ]
        },
        {
            "id": "dia-2",
            "dia": "Lunes",
            "fecha": "7 de diciembre de 2026",
            "actividades": [
                {"hora": "07:30 A 08:30", "actividad": "DESAYUNO HOTEL", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "09:00 A 09:30", "actividad": "SALIDA A PRACTICA CON EQUIPOS", "lugar": "Hacia Campo", "responsable": "Logística / Managers", "notas": ""},
                {"hora": "09:30 A 10:30", "actividad": "PRACTICA CON EQUIPOS 1 Y 2 X STAFF", "lugar": "Campo de Juego", "responsable": "Coaches & PF", "notas": "Bloque 1"},
                {"hora": "10:30 A 11:30", "actividad": "PRACTICA CON EQUIPOS 1 Y 2 X STAFF", "lugar": "Campo de Juego", "responsable": "Coaches & PF", "notas": "Bloque 2"},
                {"hora": "12:30 A 13:30", "actividad": "ALMUERZO HIPODROMO", "lugar": "Hipódromo", "responsable": "Nutrición / Logística", "notas": ""},
                {"hora": "13:30 A 13:45", "actividad": "REGRESO HOTEL", "lugar": "Traslado", "responsable": "Managers", "notas": ""},
                {"hora": "13:45 A 15:00", "actividad": "DESCANSO", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "16:00 A 16:30", "actividad": "CHARLA STAFF SAR HOTEL", "lugar": "Salón Hotel", "responsable": "Disertantes SAR", "notas": ""},
                {"hora": "17:00 A 18:30", "actividad": "CHARLA STAFF SAR HOTEL", "lugar": "Salón Hotel", "responsable": "Disertantes SAR", "notas": ""},
                {"hora": "18:30 A 19:00", "actividad": "CHARLA STAFF SAR HOTEL", "lugar": "Salón Hotel", "responsable": "Disertantes SAR", "notas": ""},
                {"hora": "19:00 A 19:45", "actividad": "REUNIÓN STAFF X GRUPOS CADA EQUIPO 1", "lugar": "Salas Designadas", "responsable": "Equipo Celeste", "notas": ""},
                {"hora": "19:45 A 20:30", "actividad": "REUNIÓN STAFF X GRUPOS CADA EQUIPO 2", "lugar": "Salas Designadas", "responsable": "Equipo Verde", "notas": ""},
                {"hora": "20:30 A 21:00", "actividad": "CIERRE DEL DÍA CON RESPONSABLES SAR", "lugar": "Salón Hotel", "responsable": "Daniel Hourcade", "notas": "Reflexión final y programa del día siguiente"},
                {"hora": "21:00", "actividad": "CENA HOTEL", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "A designar", "actividad": "CHARLA LEGADO - STAFF", "lugar": "A designar", "responsable": "Staff SAR", "notas": ""}
            ]
        },
        {
            "id": "dia-3",
            "dia": "Martes",
            "fecha": "8 de diciembre de 2026",
            "actividades": [
                {"hora": "07:30 A 08:30", "actividad": "DESAYUNO HOTEL", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "09:00 A 09:30", "actividad": "SALIDA A PRACTICA CON EQUIPOS", "lugar": "Traslado", "responsable": "Managers", "notas": ""},
                {"hora": "09:30 A 10:00", "actividad": "PRACTICA CON EQUIPOS 1 Y 2 X STAFF", "lugar": "Campo", "responsable": "Coaches", "notas": ""},
                {"hora": "10:00 A 11:00", "actividad": "PRACTICA CON EQUIPOS 1 Y 2 X STAFF", "lugar": "Campo", "responsable": "Coaches", "notas": ""},
                {"hora": "12:30 A 13:30", "actividad": "ALMUERZO HIPODROMO + JUGADORES EQUIPOS", "lugar": "Hipódromo", "responsable": "Todos", "notas": "Integración"},
                {"hora": "13:30 A 13:45", "actividad": "REGRESO HOTEL", "lugar": "Traslado", "responsable": "Managers", "notas": ""},
                {"hora": "13:45 A 15:00", "actividad": "DESCANSO", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "15:00 A 17:30", "actividad": "CHARLA STAFF SAR HOTEL", "lugar": "Salón Hotel", "responsable": "Disertantes SAR", "notas": ""},
                {"hora": "17:30 A 18:00", "actividad": "CHARLA STAFF SAR HOTEL", "lugar": "Salón Hotel", "responsable": "Disertantes SAR", "notas": ""},
                {"hora": "18:00 A 20:00", "actividad": "REUNIÓN STAFF X GRUPOS CADA EQUIPO 1", "lugar": "Salas Designadas", "responsable": "Equipo Celeste", "notas": ""},
                {"hora": "20:00 A 20:30", "actividad": "REUNIÓN STAFF X GRUPOS CADA EQUIPO 2", "lugar": "Salas Designadas", "responsable": "Equipo Verde", "notas": ""},
                {"hora": "20:30 A 21:00", "actividad": "CIERRE DEL DÍA CON RESPONSABLES SAR", "lugar": "Salón Hotel", "responsable": "Daniel Hourcade", "notas": "Reflexión final"},
                {"hora": "21:00", "actividad": "CENA HOTEL", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "A designar", "actividad": "CHARLA LEGADO - STAFF", "lugar": "A designar", "responsable": "Staff SAR", "notas": ""}
            ]
        },
        {
            "id": "dia-4",
            "dia": "Miércoles",
            "fecha": "9 de diciembre de 2026",
            "actividades": [
                {"hora": "07:30 A 08:30", "actividad": "DESAYUNO HOTEL", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "09:30 A 10:00", "actividad": "CHARLA STAFF SAR", "lugar": "Salón Hotel", "responsable": "Disertantes SAR", "notas": ""},
                {"hora": "10:00 A 10:15", "actividad": "PREGUNTAS", "lugar": "Salón Hotel", "responsable": "Todos", "notas": "Q&A"},
                {"hora": "10:15 A 10:30", "actividad": "CIERRE DEL DÍA CON RESPONSABLES SAR", "lugar": "Salón Hotel", "responsable": "Daniel Hourcade", "notas": ""},
                {"hora": "10:30 A 12:00", "actividad": "RECUPERACIÓN - FEED BACK INTERNO STAFF", "lugar": "Salas Hotel", "responsable": "Staff SAR", "notas": "Evaluaciones"},
                {"hora": "12:30 A 13:30", "actividad": "ALMUERZO HOTEL", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "13:30 A 15:00", "actividad": "DESCANSO", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "15:00 A 19:00", "actividad": "RECUPERACIÓN - FEED BACK INTERNO STAFF", "lugar": "Salas Hotel", "responsable": "Staff SAR", "notas": "Bloque tarde"},
                {"hora": "19:30 A 20:30", "actividad": "LIBRE", "lugar": "Libre", "responsable": "Participantes", "notas": ""},
                {"hora": "20:30 A 23:00", "actividad": "CENA LIBRE A CARGO DE PARTICIPANTES", "lugar": "Rosario", "responsable": "Participantes", "notas": "Salida libre"}
            ]
        },
        {
            "id": "dia-5",
            "dia": "Jueves",
            "fecha": "10 de diciembre de 2026",
            "actividades": [
                {"hora": "07:30 A 08:30", "actividad": "DESAYUNO HOTEL", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "09:00 A 09:30", "actividad": "SALIDA A PRACTICA CON EQUIPOS", "lugar": "Traslado", "responsable": "Managers", "notas": ""},
                {"hora": "09:30 A 10:00", "actividad": "PRACTICA CON EQUIPOS 1 Y 2 X STAFF", "lugar": "Campo", "responsable": "Coaches", "notas": ""},
                {"hora": "10:00 A 11:00", "actividad": "PRACTICA CON EQUIPOS 1 Y 2 X STAFF", "lugar": "Campo", "responsable": "Coaches", "notas": ""},
                {"hora": "12:30 A 13:30", "actividad": "ALMUERZO HIPODROMO", "lugar": "Hipódromo", "responsable": "Todos", "notas": ""},
                {"hora": "13:30 A 13:45", "actividad": "REGRESO HOTEL", "lugar": "Traslado", "responsable": "Managers", "notas": ""},
                {"hora": "13:45 A 15:00", "actividad": "DESCANSO", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "15:00 A 17:30", "actividad": "CHARLA STAFF SAR HOTEL", "lugar": "Salón Hotel", "responsable": "Disertantes SAR", "notas": ""},
                {"hora": "17:30 A 18:00", "actividad": "CHARLA STAFF SAR HOTEL", "lugar": "Salón Hotel", "responsable": "Disertantes SAR", "notas": ""},
                {"hora": "18:00 A 20:00", "actividad": "REUNIÓN STAFF X GRUPOS CADA EQUIPO 1", "lugar": "Salas Designadas", "responsable": "Equipo Celeste", "notas": ""},
                {"hora": "20:00 A 20:30", "actividad": "REUNIÓN STAFF X GRUPOS CADA EQUIPO 2", "lugar": "Salas Designadas", "responsable": "Equipo Verde", "notas": ""},
                {"hora": "20:30 A 21:00", "actividad": "CIERRE DEL DÍA CON RESPONSABLES SAR", "lugar": "Salón Hotel", "responsable": "Daniel Hourcade", "notas": ""},
                {"hora": "21:00", "actividad": "CENA HOTEL", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "A designar", "actividad": "CHARLA LEGADO - STAFF", "lugar": "A designar", "responsable": "Staff SAR", "notas": ""}
            ]
        },
        {
            "id": "dia-6",
            "dia": "Viernes",
            "fecha": "11 de diciembre de 2026",
            "actividades": [
                {"hora": "07:00 A 08:00", "actividad": "DESAYUNO HOTEL", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "08:00", "actividad": "SALIDA STAFF AL PARTIDO", "lugar": "Traslado", "responsable": "Managers", "notas": ""},
                {"hora": "08:30", "actividad": "EQUIPOS Y STAFF", "lugar": "Cancha", "responsable": "Todos", "notas": "Llegada al estadio"},
                {"hora": "09:15 A 09:55", "actividad": "CALENTAMIENTO", "lugar": "Campo de Juego", "responsable": "PFs", "notas": "Pre-match"},
                {"hora": "10:00", "actividad": "🏉 KICK OFF PARTIDO (CELESTE VS VERDE)", "lugar": "Estadio", "responsable": "Referees & Teams", "notas": "Partido Oficial Academia"},
                {"hora": "11:30", "actividad": "FIN PARTIDO", "lugar": "Campo", "responsable": "Todos", "notas": ""},
                {"hora": "12:30 A 13:30", "actividad": "TERCER TIEMPO", "lugar": "Club / Quincho", "responsable": "Staff + Jugadores + SAR", "notas": "Tradición Rugby"},
                {"hora": "14:30 A 14:45", "actividad": "DESPEDIDA Y AGRADECIMIENTO A LOS JUGADORES", "lugar": "Club", "responsable": "Staff SAR", "notas": ""},
                {"hora": "15:00", "actividad": "REGRESO HOTEL", "lugar": "Traslado", "responsable": "Managers", "notas": ""},
                {"hora": "16:00 A 19:00", "actividad": "TRABAJO X EQUIPOS PARA PRESENTACIÓN FINAL", "lugar": "Salas Hotel", "responsable": "Equipos 1 y 2", "notas": "Preparación conclusiones"},
                {"hora": "20:30 A 21:30", "actividad": "CENA HOTEL", "lugar": "Hotel", "responsable": "Todos", "notas": ""}
            ]
        },
        {
            "id": "dia-7",
            "dia": "Sábado",
            "fecha": "12 de diciembre de 2026",
            "actividades": [
                {"hora": "08:30 A 09:30", "actividad": "DESAYUNO HOTEL", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "09:30 A 11:30", "actividad": "PRESENTACIÓN FINAL EQUIPO 1", "lugar": "Salón Auditorio", "responsable": "Equipo Celeste", "notas": "Defensa de trabajo"},
                {"hora": "11:30 A 13:30", "actividad": "PRESENTACIÓN FINAL EQUIPO 2", "lugar": "Salón Auditorio", "responsable": "Equipo Verde", "notas": "Defensa de trabajo"},
                {"hora": "13:00", "actividad": "ALMUERZO", "lugar": "Hotel", "responsable": "Todos", "notas": ""},
                {"hora": "13:30 A 14:00", "actividad": "DESPEDIDA Y CIERRE OFICIAL", "lugar": "Salón Hotel", "responsable": "Daniel Hourcade & Staff SAR", "notas": "Fin de Academia SAR 2026"}
            ]
        }
    ],
    "updatedAt": datetime.now()
}

event_col.update_one({"year": 2026}, {"$set": event_data}, upsert=True)
print("¡Colección academy_event_2026 guardada en MongoDB Atlas exitosamente!")

