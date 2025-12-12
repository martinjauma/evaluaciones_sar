# Sistema de Evaluaciones por Año - Academia SAR

## 📋 Resumen

El sistema ahora soporta **preguntas y evaluadores diferentes por año**. Los datos se cargan automáticamente según el año seleccionado en el encabezado del documento.

---

## 🗂️ Archivos de Configuración

### 1. **preguntas_areas.csv**
Contiene todas las preguntas de evaluación organizadas por año y área.

**Estructura:**
```csv
Year,Area,Pregunta,Numero_Pregunta
2023,Coaching,Explicación ejercicios, dinámica, utilización tiempo.,1
2024,Coaching,Explicación ejercicios, dinámica, utilización tiempo.,1
2025,Coaching,Explicación ejercicios, dinámica, utilización tiempo.,1
```

**Columnas:**
- `Year`: Año de la evaluación (2023, 2024, 2025, etc.)
- `Area`: Nombre del área (Coaching, Fisio, Médico, etc.)
- `Pregunta`: Texto de la pregunta en castellano
- `Numero_Pregunta`: Número de orden (1-10)

### 2. **evaluadores_areas.csv**
Contiene los evaluadores asignados a cada área por año.

**Estructura:**
```csv
Year,Area,Evaluador
2023,Coaching,"D. Hourcade, L. Piña, P. Perez, R. Le Fort, P. Bouza, E. Meneses."
2024,Coaching,"D. Hourcade, L. Piña, P. Perez, R. Le Fort, P. Bouza, E. Meneses."
2025,Coaching,"D. Hourcade, L. Piña, P. Perez, R. Le Fort, P. Bouza, E. Meneses."
```

**Columnas:**
- `Year`: Año de la evaluación
- `Area`: Nombre del área
- `Evaluador`: Nombre(s) del/los evaluador(es)

---

## 🔧 Cómo Funciona

### En la Aplicación (app.py):

1. **El usuario selecciona el encabezado** (SAR 2023, SAR 2024, SAR 2025)
2. **El sistema extrae el año** del encabezado seleccionado
3. **Carga automáticamente:**
   - Las preguntas del CSV para ese año
   - Los evaluadores del CSV para ese año
4. **Muestra los datos** correspondientes al año seleccionado

### Flujo de Datos:

```
Usuario selecciona "SAR 2024"
    ↓
Sistema extrae: year = 2024
    ↓
Carga preguntas_areas.csv filtrando Year = 2024
    ↓
Carga evaluadores_areas.csv filtrando Year = 2024
    ↓
Muestra formulario con preguntas y evaluadores de 2024
```

---

## ✏️ Cómo Modificar Preguntas o Evaluadores

### Para cambiar preguntas de un año específico:

1. Abrir **preguntas_areas.csv**
2. Buscar las filas con el año que quieres modificar
3. Editar el texto en la columna `Pregunta`
4. Guardar el archivo
5. ✅ Los cambios se verán automáticamente al reiniciar la app o recargar

### Para cambiar evaluadores de un año específico:

1. Abrir **evaluadores_areas.csv**
2. Buscar las filas con el año que quieres modificar
3. Editar el texto en la columna `Evaluador`
4. Guardar el archivo
5. ✅ Los cambios se verán automáticamente

### Para agregar un nuevo año (ej: 2026):

1. **En preguntas_areas.csv:**
   - Copiar todas las filas de un año existente
   - Cambiar la columna `Year` a 2026
   - Modificar las preguntas si es necesario

2. **En evaluadores_areas.csv:**
   - Copiar todas las filas de un año existente
   - Cambiar la columna `Year` a 2026
   - Modificar los evaluadores si es necesario

3. **En app.py** (líneas 185-187):
   - Agregar: `"SAR 2026": "images/header_2026.png"`
   - Crear la imagen del header en la carpeta `images/`

---

## 📊 Áreas Soportadas

Actualmente el sistema soporta **9 áreas**:

1. Video & Análisis
2. Coaching
3. Fisio
4. Logística & Utilería
5. Match Official
6. Médico
7. Preparación Física
8. Team Manager
9. Nutrición

Cada área tiene **10 preguntas** de evaluación.

---

## 🔍 Ventajas del Nuevo Sistema

✅ **Flexibilidad:** Preguntas diferentes por año sin cambiar código
✅ **Mantenibilidad:** Todo en archivos CSV fáciles de editar
✅ **Escalabilidad:** Agregar nuevos años es muy simple
✅ **Trazabilidad:** Los documentos antiguos mantienen sus preguntas originales
✅ **Retrocompatibilidad:** Los datos en MongoDB siguen funcionando

---

## 🚨 Importante

- **No eliminar columnas** de los CSV, solo editar valores
- **Mantener el formato CSV** con las comillas en textos que contienen comas
- **Guardar con encoding UTF-8** para preservar caracteres especiales
- **Cada área debe tener exactamente 10 preguntas** por año

---

## 📝 Ejemplo de Uso

**Escenario:** Queremos cambiar la primera pregunta de Coaching para 2025

1. Abrir `preguntas_areas.csv`
2. Buscar la línea:
   ```
   2025,Coaching,"Explicación ejercicios, dinámica, utilización tiempo.",1
   ```
3. Cambiar a:
   ```
   2025,Coaching,"Presentación y explicación de ejercicios.",1
   ```
4. Guardar el archivo
5. Recargar la aplicación
6. Seleccionar "SAR 2025" → La nueva pregunta aparecerá

---

## 🐛 Troubleshooting

**Problema:** No aparecen las preguntas
- **Solución:** Verificar que el CSV tiene la columna `Year` correctamente

**Problema:** Aparecen preguntas de otro año
- **Solución:** Verificar que el año en el CSV coincide con el seleccionado

**Problema:** Error al cargar CSV
- **Solución:** Verificar que las comillas están correctamente escapadas en textos con comas

---

## 📞 Contacto

Para soporte técnico o consultas, contactar al equipo de desarrollo.

**Última actualización:** Diciembre 2024
