# Roadmap del proyecto
## 1. Vision del proyecto

Crear un Dashboard Inteligente que permita subir CSV o Excel y obtener análisis, visualizaciones e inicio de predicciones para evolucionar luego a modelos avanzados y redes neuronales.

## 2. Objetivo de la versión 1 (MVP)
    - 1 - Subir archivo CSV o Excel.
    - 2 - Limpiar y validar datos básicos.
    - 3 - Mostrar métricas principales.
    - 4 - Mostrar gráficos iniciales.
    - 5 - Guardar resultados de análisis.
    - 6 - Mostrar una predicción básica.

## 3. Reglas de trabajo
    - 1 - Cada sprint dura 1 o 2 semanas.
    - 2 - Cada sprint debe terminar con una demo funcional.
    - 3 - No avanzar a otro sprint sin criterios de cierre.
    - 4 - Documentar aprendizajes técnicos en cada sprint.

## 4. Sprints iniciales
### Sprint 0: Preparación y base

Objetivo: dejar el entorno listo para construir sin fricción.
Entregables:

    - 1 - Estructura de carpetas del proyecto.
    - 2 - Entorno Python configurado.
    - 3 - Repositorio con control de versiones.
    - 4 - README con roadmap y objetivos.
    Criterio de cierre:
    - 5 - Proyecto corre localmente y tiene estructura clara.

### Sprint 1: Ingesta de datos

Objetivo: recibir y leer archivos reales.
Entregables:

    - 1 - Carga de CSV y Excel.
    - 2 - Validación de columnas y tipos.
    - 3 - Manejo de errores de archivo inválido.
    - 4 - Resumen de dataset cargado.
    Criterio de cierre:
    - 5 - Subes archivo y el sistema devuelve datos estructurados sin romperse.

### Sprint 2: Análisis descriptivo

Objetivo: generar valor inmediato con estadísticas.
Entregables:

    - 1 - Total, promedio, mínimo, máximo.
    - 2 - Detección de nulos y duplicados.
    - 3 - Insights básicos automáticos.
    - 4 - Respuesta lista para frontend.
    Criterio de cierre:
    - 5 - Cada archivo cargado produce un análisis consistente.

### Sprint 3: Visualización del dashboard

Objetivo: mostrar resultados de forma clara para usuarios no técnicos.
Entregables:

    - 1 - Vista de KPIs.
    - 2 - Gráfico de evolución temporal.
    - 3 - Tabla con datos limpios.
    - 4 - Sección de insights.
    Criterio de cierre:
    - 5 - Usuario puede entender el estado del dataset sin leer código.

### Sprint 4: API y persistencia inicial

Objetivo: pasar de prototipo a app con historial.
Entregables:

    - 1 - Endpoints de subida y consulta.
    - 2 - Base de datos con usuarios, archivos y análisis.
    - 3 - Guardado de historial por análisis.
    - 4 - Estado de procesamiento por registro.
    Criterio de cierre:
    - 5 - Puedes consultar análisis anteriores desde la aplicación.

### Sprint 5: Predicción básica versión 1

Objetivo: incorporar primer modelo predictivo real.
Entregables:

    - 1 - Predicción con regresión lineal.
    - 2 - Métricas iniciales de desempeño.
    - 3 - Registro de resultados de predicción.
    - 4 - Visualización del valor predicho.
    Criterio de cierre:
    - 5 - El sistema predice y muestra resultado con métricas básicas.

______________________________________________________________________________
______________________________________________________________________________

# Proceso

## Sprint 0 - Preparación y base (completado)

### Qué se hizo
1. Se instaló Python 3.12.10.
2. Se creó la estructura inicial del proyecto:
   - backend/
   - backend/app/
   - backend/tests/
   - frontend/
   - data/
   - docs/
   - scripts/
3. Se creó entorno virtual `.venv` y se activó.
4. Se instalaron dependencias base:
   - fastapi
   - uvicorn
   - pandas
   - openpyxl
   - python-multipart
   - scikit-learn
   - pytest
5. Se generó `backend/requirements.txt` con `pip freeze`.
6. Se implementó API mínima en `backend/app/main.py` con endpoint `/health`.
7. Se validó ejecución local con Uvicorn.
8. Se inicializó Git y se subió el repositorio a GitHub.

### Resultado técnico
1. El proyecto corre localmente.
2. La estructura está clara para continuar con Sprint 1.
3. El repositorio ya tiene control de versiones y remoto en GitHub.

### Problema encontrado y solución
1. Error de sintaxis en `return` dentro de `main.py`.
2. Causa: faltaba indentación dentro de la función.
3. Solución: aplicar 4 espacios antes de `return`.

### Evidencia de funcionamiento
1. `GET /health` responde: `{"status":"ok"}`
2. Swagger disponible en `/docs`.

__________________________________________________________________________________________

## Sprint 1 - Ingesta de datos (completado)

### Qué se hizo
1. Se construyo:
    - Endpoint de subida de archivos CSV/Excel.
    - Validación de formato y archivo vacío.
    - Lectura con pandas.
    - Resumen inicial del dataset:
        • nombre de archivo
        • filas
        • columnas
        • nombres de columnas
    - Tests mínimos para salud y validación de extensión.

### Evidencia de validación manual

1. Se probó carga de archivo Excel real con 2 columnas y 5 registros.
2. El endpoint de upload respondió código 200.
3. La API devolvió correctamente:
    • nombre de archivo
    • cantidad de filas y columnas
    • nombres de columnas normalizados
    • columnas numéricas detectadas
    • tipos de columnas
    • nulos por columna
    • lista de warnings vacía

### Resultado

1. La ingesta CSV/Excel funciona correctamente.
2. La validación de formato y contenido está operativa.
3. El sistema ya está listo para iniciar Sprint 2 (análisis descriptivo).

### Mejora detectada

1. Unificar el formato de nombres en nulls_by_column para que coincida siempre con column_names normalizadas.

### Cierre final

1. Se verificó la normalización consistente de columnas en toda la respuesta del endpoint.
2. Se validó carga de archivo Excel real con respuesta 200.
3. Se confirmó detección correcta de columnas numéricas y tipos.
4. Resultado: Sprint 1 completado y listo para iniciar Sprint 2.

__________________________________________________________________________________________

## Sprint 2: Análisis descriptivo (En curso)

### Qué se hizo
1. Cree las hojas de excel para realizar las pruebas
    • Cree excel con datos correctos
    • Cree excel con datos incorrectos
2. 
