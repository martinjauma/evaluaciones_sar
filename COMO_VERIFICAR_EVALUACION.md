# Cómo Verificar que una Evaluación se Carga desde MongoDB

## 📋 Caso: Juan Giraldo - Coaching - 2024

### ✅ Datos Confirmados en MongoDB:

- **Nombre:** Juan Giraldo
- **Área:** Coaching
- **Fecha guardada:** 2024-12-07 08:16:45
- **Total preguntas:** 10
- **Evaluador:** D. Hourcade, L. Piña, P. Perez, R. Perez, R. Le Fort, Duran, P. Bouza, E. Meneses, Guzman.
- **Calificaciones:** 2, 1, 1, 1, 1, 3, 3, 1, 2, 2 (Total: 17 puntos)

---

## 🔍 Pasos para Verificar en la Aplicación:

### 1. **Abrir la Aplicación**
- Ir a: http://localhost:8501

### 2. **Seleccionar el Año Correcto**
- En el sidebar, seleccionar: **"SAR 2024"**

### 3. **Seleccionar el Área**
- En el sidebar, seleccionar: **"Coaching"**

### 4. **Seleccionar el Participante**
- En el dropdown "Nombre del Evaluado", seleccionar: **"Juan Giraldo"**

### 5. **Verificar Indicadores en el Sidebar**

Deberías ver:
```
✅ Evaluación encontrada en MongoDB
📊 10 preguntas guardadas
```

Si no ves esto, hay un problema con la carga desde MongoDB.

### 6. **Verificar los Campos de Entrada**

En el tab "Español", deberías ver:
- Los campos de "Puntaje 0 al 5" pre-llenados con las calificaciones guardadas
- Los campos de "Observaciones" pre-llenados con las observaciones guardadas
- El campo "Conclusión" pre-llenado con la conclusión guardada
- El total en el sidebar: **17 puntos** (en rojo porque es ≤ 29)

---

## 🚨 Problemas Comunes:

### Problema 1: "No hay evaluación previa guardada"

**Posibles causas:**
1. El nombre no coincide exactamente (espacios extra, mayúsculas/minúsculas)
2. El área no coincide exactamente
3. MongoDB no está conectado

**Solución:**
- Verificar que el nombre sea exactamente: `"Juan Giraldo"` (con espacio)
- Verificar que el área sea exactamente: `"Coaching"`
- Verificar conexión a MongoDB en `.streamlit/secrets.toml`

### Problema 2: Se encuentra la evaluación pero no se cargan los datos

**Posibles causas:**
1. La estructura del documento en MongoDB no coincide con lo esperado
2. Las descripciones de las preguntas cambiaron entre años

**Solución:**
- Las preguntas deben coincidir **exactamente** con las del CSV del año correspondiente
- Si cambiaste las preguntas en el CSV, los datos guardados pueden no coincidir

### Problema 3: Los datos se cargan pero no se muestran correctamente

**Posibles causas:**
1. Las keys de los campos de Streamlit causan conflictos
2. El índice de las evaluaciones no coincide

**Solución:**
- Recargar la página (F5)
- Limpiar la caché de Streamlit (Ctrl+C en el sidebar)

---

## 🛠️ Comando de Diagnóstico Rápido

Para verificar si Juan Giraldo está en MongoDB, ejecutar:

```bash
cd "/Users/martinjauma/Documents/CODIGO/ACADEMIA SAR"
source venv/bin/activate
python3 << EOF
from pymongo import MongoClient
import toml

with open('.streamlit/secrets.toml', 'r') as f:
    secrets = toml.load(f)

client = MongoClient(secrets["mongo_uri"])
db = client[secrets["db_name"]]
collection = db[secrets["collection_name"]]

ev = collection.find_one({"nombre": "Juan Giraldo", "area": "Coaching"})
if ev:
    print("✅ Evaluación encontrada")
    print(f"Fecha: {ev['fecha']}")
    print(f"Preguntas: {len(ev['evaluaciones'])}")
    print(f"Total puntos: {sum(e['calificacion'] for e in ev['evaluaciones'])}")
else:
    print("❌ No se encontró evaluación")
EOF
```

---

## 📊 Estructura Esperada en MongoDB

```json
{
  "nombre": "Juan Giraldo",
  "area": "Coaching",
  "fecha": "2024-12-07T08:16:45.206Z",
  "evaluador": "D. Hourcade, ...",
  "evaluaciones": [
    {
      "descripcion": "Explicación ejercicios, dinámica, utilización tiempo.",
      "calificacion": 2,
      "observaciones": "..."
    },
    ...10 elementos
  ],
  "conclusion": "..."
}
```

---

## ✅ Qué Debería Suceder:

1. Seleccionas "SAR 2024" → Carga preguntas de 2024
2. Seleccionas "Coaching" → Filtra participantes de Coaching
3. Seleccionas "Juan Giraldo" → Busca en MongoDB
4. MongoDB devuelve la evaluación guardada
5. Los campos se pre-llenan con los datos guardados
6. Puedes modificar y generar PDF nuevamente

---

## 📝 Notas Importantes:

- **Las preguntas deben coincidir:** Si cambias las preguntas en el CSV después de guardar, puede haber desajustes
- **El orden importa:** Las preguntas se cargan por índice (0-9)
- **Year independiente:** Los datos guardados no tienen campo "year", solo se usa para cargar las preguntas del CSV

---

Si aún tienes problemas, revisa la consola del servidor de Streamlit para ver si hay errores de MongoDB o prints de debug.
