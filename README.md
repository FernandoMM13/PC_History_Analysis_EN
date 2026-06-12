# Análisis PC History — Paquete de Reproducción

Cuaderno de análisis estadístico del rendimiento en tests inicial y final de alumnos de 5.º de Primaria en los centros **Pedro Duque** y **Juan Echegaray**, junto con las valoraciones de las actividades realizadas durante la intervención.

---

## Estructura del proyecto

```
Analysis_PC_History/
├── analisis_PC_history.ipynb   # Cuaderno principal de análisis
├── analisis_PC_history.pdf     # Informe en PDF (generado, sin código)
├── requirements.txt            # Dependencias Python
├── data/
│   └── Test_iniciales_v_finales.xlsx   # Datos fuente (no modificar)
└── outputs/
    ├── figures/                # Gráficos exportados (PNG y SVG)
    ├── tables/                 # Tablas exportadas (CSV y XLSX)
    └── logs/                   # Log de ejecución del pipeline
```

---

## Requisitos previos

| Requisito | Versión mínima | Notas |
|---|---|---|
| Python | 3.10 o superior | Probado con Python 3.14.2 |
| pip | incluido con Python | — |
| Git (opcional) | cualquiera | Solo si clonas desde un repositorio |

> **Windows:** Python se descarga desde [python.org](https://www.python.org/downloads/). Durante la instalación, marca la casilla **"Add Python to PATH"**.  
> **macOS/Linux:** Usa el gestor de paquetes del sistema (`brew install python` / `apt install python3`).

---

## Instalación paso a paso

### 1. Descarga o descomprime el paquete

Coloca la carpeta `Analysis_PC_History` en la ubicación que prefieras. Todos los pasos siguientes se ejecutan desde dentro de esa carpeta.

### 2. Abre una terminal en la carpeta del proyecto

- **Windows:** Pulsa `Shift + clic derecho` sobre la carpeta → *Abrir ventana de PowerShell aquí*  
  (o en el Explorador de archivos escribe `cmd` en la barra de direcciones).
- **macOS/Linux:** Abre Terminal y navega con `cd /ruta/a/Analysis_PC_History`.

### 3. Crea el entorno virtual

```bash
python -m venv .venv
```

### 4. Activa el entorno virtual

| Sistema | Comando |
|---|---|
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (CMD) | `.venv\Scripts\activate.bat` |
| macOS / Linux | `source .venv/bin/activate` |

Una vez activado, verás `(.venv)` al inicio de la línea de comandos.

### 5. Instala las dependencias

```bash
pip install -r requirements.txt
```

La instalación tarda entre 1 y 5 minutos según la velocidad de la conexión.

### 6. Registra el entorno en Jupyter

```bash
python -m ipykernel install --user --name pc_analysis_venv --display-name "Python (PC Analysis)"
```

---

## Ejecución del análisis

### Opción A — Jupyter Notebook (recomendada)

```bash
jupyter notebook analisis_PC_history.ipynb
```

Se abrirá el navegador automáticamente. Dentro del cuaderno:

1. Selecciona el kernel **"Python (PC Analysis)"** (*Kernel → Change kernel* si no aparece).
2. Ejecuta todas las celdas en orden: menú *Cell → Run All* (o `Ctrl+Shift+Enter` celda a celda).
3. Al finalizar, los resultados aparecen en la carpeta `outputs/`.

### Opción B — VS Code

1. Abre VS Code en la carpeta del proyecto.
2. Instala las extensiones **Python** y **Jupyter** si no las tienes.
3. Abre `analisis_PC_history.ipynb`.
4. Selecciona el kernel **"Python (PC Analysis)"** en la esquina superior derecha.
5. Pulsa *Run All* (▶▶) en la barra del cuaderno.

### Opción C — Ejecución desde terminal (sin interfaz)

```bash
jupyter nbconvert --to notebook --execute analisis_PC_history.ipynb --output analisis_PC_history_executed.ipynb
```

---

## Resultados esperados

Tras ejecutar el cuaderno completo encontrarás:

| Archivo | Descripción |
|---|---|
| `outputs/tables/paired_data.csv` | Tabla maestra de los 101 alumnos emparejados |
| `outputs/tables/pruebas_pareadas.xlsx` | t-test, Wilcoxon, Cohen's d y rank-biserial |
| `outputs/tables/analisis_items.xlsx` | Dificultad, discriminación y D27 por ítem |
| `outputs/tables/ranking_actividades.xlsx` | Ranking de actividades por valoración media |
| `outputs/figures/*.png / *.svg` | Boxplots, heatmaps, forest plot, scatter plots |
| `outputs/logs/run.log` | Log completo de la ejecución con timestamps |
| `requirements.txt` | Actualizado con versiones exactas del entorno |

La última celda del cuaderno (**Quality Gates**) ejecuta una verificación automática y muestra `✅ PASS` o `❌ FAIL` para cada archivo y condición esperada.

---

## Secciones del análisis

| Sección | Contenido |
|---|---|
| 1 · Setup | Importaciones, logger, rutas y constantes |
| 2 · Carga de datos | Lectura del Excel y vista preliminar de las hojas |
| 3 · Limpieza y validación | Imputación de NaN, reparación de totales, registro de correcciones |
| 4 · Identificación y emparejamiento | Construcción del ID alumno y cruce inicial–final |
| 5 · Normalización y ganancia de Hake | Cálculo de puntuaciones normalizadas y ganancia de aprendizaje |
| 6 · Estadísticos descriptivos | Medias, medianas, desviaciones, boxplots e histogramas |
| 7 · Pruebas pareadas y tamaño del efecto | t-test, Wilcoxon, Cohen's d, forest plot |
| 8 · ANOVA / Kruskal-Wallis por grupos | Comparación entre clases y centros, post-hoc Tukey / Dunn |
| 9 · Análisis por ítem | Dificultad p, discriminación pbis, índice D27, co-errores |
| 10 · Votaciones | Métricas de satisfacción por actividad y clase, ranking |
| 11 · Narrativa Edad Contemporánea | Contextualización pedagógica |
| 12 · Exportación completa | Guardado de tablas, figuras y actualización de `requirements.txt` |
| 13 · Quality Gates | Verificación automática de integridad de los resultados |

---

## Solución de problemas frecuentes

**`ModuleNotFoundError: No module named 'X'`**  
El entorno virtual no está activado o las dependencias no se instalaron.  
→ Activa `.venv` y ejecuta `pip install -r requirements.txt` de nuevo.

**El kernel "Python (PC Analysis)" no aparece en Jupyter**  
→ Ejecuta el paso 6 de la instalación (`ipykernel install`), reinicia Jupyter y refresca la página.

**`ValueError: assignment destination is read-only`**  
Este error fue corregido en el propio cuaderno (compatibilidad con pandas ≥ 3). Si aparece, asegúrate de estar usando la versión del archivo incluida en este paquete.

**Las gráficas no se muestran**  
→ Comprueba que `matplotlib` y `seaborn` se instalaron correctamente (`pip show matplotlib seaborn`).

**PowerShell bloquea la activación del entorno (Windows)**  
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Datos y privacidad

El archivo `data/Test_iniciales_v_finales.xlsx` contiene datos de rendimiento académico anonimizados (sin nombres ni DNI). No debe distribuirse fuera del equipo de investigación.

---

## Dependencias principales

| Paquete | Versión probada | Uso |
|---|---|---|
| pandas | 3.0.2 | Manipulación de datos |
| numpy | 2.4.4 | Cálculo numérico |
| scipy | 1.17.1 | Pruebas estadísticas |
| statsmodels | 0.14.6 | ANOVA, Tukey HSD |
| pingouin | 0.6.1 | Cohen's d, rank-biserial |
| seaborn | 0.13.2 | Visualización |
| matplotlib | — | Gráficos base |
| openpyxl | — | Lectura/escritura de Excel |
