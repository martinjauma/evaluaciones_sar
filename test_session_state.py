"""
Script para simular lo que debería pasar en session_state
"""

# Simular datos de MongoDB
evaluacion_guardada = {
    'evaluaciones': [
        {
            'descripcion': 'Explicación ejercicios, dinámica, utilización tiempo.',
            'calificacion': 2,
            'observaciones': 'No fue claro en sus explicaciones a los jugadores...'
        },
        {
            'descripcion': 'Objetivo/s ejercicio.',
            'calificacion': 1,
            'observaciones': 'Los objetivos no fueron claros en los ejercicios...'
        }
    ],
    'conclusion': 'Conclusión de prueba'
}

# Simular session_state
session_state = {}

nombre = "Juan Giraldo"
area = "Coaching"

# El código actual
if f"loaded_{nombre}_{area}" not in session_state:
    session_state[f"loaded_{nombre}_{area}"] = True
    # Guardar los datos en session_state para cada pregunta
    for ev in evaluacion_guardada.get('evaluaciones', []):
        desc = ev.get('descripcion', '')
        session_state[f"cal_{desc}"] = str(ev.get('calificacion', ''))
        session_state[f"obs_{desc}"] = ev.get('observaciones', '')
    # Guardar conclusión
    session_state['conclusion_guardada'] = evaluacion_guardada.get('conclusion', '')

# Mostrar lo que se guardó
print("Session state después de cargar:")
for key, value in session_state.items():
    if len(str(value)) > 50:
        print(f"  {key}: {str(value)[:50]}...")
    else:
        print(f"  {key}: {value}")

# Verificar que las keys serían las mismas que los widgets
print("\nKeys de widgets esperados:")
print(f"  cal_Explicación ejercicios, dinámica, utilización tiempo.")
print(f"  obs_Explicación ejercicios, dinámica, utilización tiempo.")
print(f"  cal_Objetivo/s ejercicio.")
print(f"  obs_Objetivo/s ejercicio.")
print(f"  conclusion_guardada")
