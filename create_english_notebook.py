#!/usr/bin/env python3
"""
Generates PC_History_Analysis_EN.ipynb from analisis_completo_PC_Historia.ipynb.
- Translates all markdown cells to English.
- Translates all visible output strings in code cells (plot labels, print, logger, captions).
- Redirects figures to outputs/figures/en/ subfolder.
"""
import json, re, pathlib

SRC  = pathlib.Path("analisis_completo_PC_Historia.ipynb")
DEST = pathlib.Path("PC_History_Analysis_EN.ipynb")

with open(SRC, encoding="utf-8") as f:
    nb = json.load(f)

# ─────────────────────────────────────────────────────────────────
# 1. FULL MARKDOWN CELL TRANSLATIONS  (keyed by first non-empty line)
# ─────────────────────────────────────────────────────────────────
MD_BY_ID = {
"971903fc": """\
# Complete Analysis: Computational Thinking + History
## Project: CT and History Assessment — Juan Echegaray School

---

| Metadata | Value |
|----------|-------|
| **School** | Juan Echegaray Elementary School |
| **Grade** | 5th Grade Primary — 4 classes (A, B, C, D) |
| **CT Test** | 28 multiple-choice items (A/B/C/D) |
| **History pre-test** | 8 binary-response items (P1–P8) |
| **History post-test** | 11 binary-response items (P1–P11) |
| **Data** | `./data/{test_inicial_pc_echegaray.csv, especificacion_items.csv, autoperception_test_inicial_pc_echegaray.csv, Test_iniciales_v_finales.xlsx}` |
| **Outputs** | `./outputs/{tables/, figures/en/, logs/}` |
| **Seed** | `numpy.random.seed(42)` |

---

### Analysis Objectives

1. **Describe the initial CT performance** of Echegaray students: global distribution, by class, gender and SEN; psychometric item analysis by computational concept and required task.
2. **Examine students' self-perception** about their performance and its relationship with actual performance (at aggregate group level, given the absence of individual ID).
3. **Classify classes by CT level** (Low / Medium / High using tertiles on the class mean) to use as a moderating variable in sections 7 and 8.
4. **Analyse History learning** (pre-post design, **independent samples** by class): Hake **group-level gain** per class (without individual matching) and the effect of CT level on the gain.
5. **Explore satisfaction ratings** for activities, crossed with the CT level of the class, and their possible relationship with learning gain.
6. **Export and verify** all outputs through automatic quality gates that guarantee reproducibility of the analysis.

---

### Notebook Structure

| Section | Content |
|---------|-----------|
| **0 · Setup** | Libraries, seed, paths, logger, utility functions and table-styling helper |
| **1 · Loading & Audit** | Robust loading of all datasets; data-quality audit table exported |
| **2 · CT Test: Format + Correct Answers** | Automatic detection of response format; score per student, task and concept |
| **3 · CT Descriptives** | Global and group distribution; items × class heatmap; barplots by concept |
| **4 · CT Contrasts** | Significant differences by Gender and SEN; automatic methodological decision |
| **5 · Self-Perception** | Self-perception vs. actual performance contrast at aggregate group level |
| **6 · CT Level by Class** | Tertile classification (Low/Medium/High) as moderating variable |
| **7 · History** | Pre-post analysis (independent samples); group Hake gain per class; ANOVA; OLS model |
| **8 · Ratings** | Activity satisfaction by activity × CT level; ranking; rating–gain correlation |
| **9 · Methodological Reflection** | The five pillars of CT applied to the analysis pipeline |
| **10 · Quality Gates** | Automatic verification of all outputs and data invariants |

---

### Key Methodological Note

> **History — independent samples design:** The `Student` index in the data represents the response order, not the same student across both tests. Therefore, **individual observations cannot be paired**. The Hake gain is calculated at the **class** level (over group means):
>
> $$g = \\frac{\\text{pct\\_fin} - \\text{pct\\_ini}}{1 - \\text{pct\\_ini}}$$
>
> **CT level as moderator:** The level (Low/Medium/High) is assigned at the **class** level, not the individual student level. It is only applied to Echegaray classes to avoid imputing levels to schools without CT data.
>
> **Self-perception — explicit limitation:** Without an ID column in the self-perception dataset, comparison with actual performance is only possible at the group mean level. No individual correlations are performed.

### Reproducibility Note

> This notebook is **self-contained**. Install dependencies with `pip install -r requirements.txt`.
> Running all cells in order (with seed `np.random.seed(42)`) fully regenerates all outputs in `./outputs/`.
> **Section 10 (Quality Gates)** automatically verifies the integrity of each output file.
""",

"97e86b5f": """\
## 0. Setup and Configuration

**What this section does:** Imports all libraries, fixes the random seed (`np.random.seed(42)`), creates output directories, configures the data-quality logger and defines shared utility functions: robust CSV/Excel reading, normality detection, Hedges g, rank-biserial, bootstrap CI and permutation test. Finally adds the `style_table()` helper for uniform-style tables throughout the notebook.

**Why:** Centralising configuration and functions in the first block guarantees exact reproducibility (same seed → same results in bootstrap and permutations) and allows reusing utilities in any section without duplicating code.
""",

"9cd42f98": """\
## 1. Load + Audit of All Data

**What this section does:** Loads all project files — CT CSV, item specification, self-perception, History Excel with all its sheets and `category_questions.xlsx` — using robust functions with automatic separator and encoding detection. Shows the first rows of each dataset and calls the audit function.

**Why:** Before any analysis it is essential to know the data quality: dimensions, column types, presence of NaN and outliers. Robust loading avoids silent errors due to separator differences (`,` vs `;`) or encoding (`utf-8` vs `latin-1`).
""",

"c6570400": """\
### 1.2 Dataset Audit

**What this subsection does:** For each loaded dataset, calculates quality statistics: number of rows/columns, NaN percentage per column, unique values per variable and min–max range for numeric ones. Records the result in `auditoria_datasets.csv` and in the quality log.

**Why:** The audit is the first quality control of the pipeline. Detecting columns with excess NaN, unexpected duplicates or out-of-range values at this stage prevents data errors from contaminating all subsequent analyses and makes any cleaning decision traceable.
""",

"390935ae": """\
## 2. Initial CT Test: Format Detection + Correct Answers

**What this section does:** Standardises column names, automatically detects the response format of the CT test (binary `{0,1}` or letters `A/B/C/D`), converts responses to correct/incorrect by comparing against the correction key (`especificacion_items.csv`) and calculates the total score per student, plus scores broken down by **required task** (Sequencing, Completion, Debugging) and **computational concept** (Directions, Loops, Conditionals, Functions).

**Why:** The CT CSV may come in two different formats depending on the export process. Automatically detecting the format makes the notebook robust to different file versions. The breakdown by task and concept allows identifying in which dimension of computational thinking students show more or less mastery, guiding potential pedagogical interventions.
""",

"b327e4b9": """\
## 3. Initial CT Descriptives

**What this section does:** Generates the complete descriptive analysis of CT test performance: histograms with KDE of the global score, box/violin plots by class, gender and SEN with 95% bootstrap CI, descriptive statistics tables globally and by group, heatmap of % correct by item × class, and barplots by required task and computational concept.

**Why:** Descriptive statistics is the essential step before any inference: it allows seeing the distribution, detecting outliers, visually comparing groups and identifying which concepts or tasks are more difficult for students, before applying formal significance tests.
""",

"30a68d15": """\
## 4. Significant CT Differences: Gender and SEN

**What this section does:** Contrasts the CT score between Boys and Girls, and between students with and without SEN. The statistical test selection (Welch's t or Mann-Whitney U) is performed automatically based on normality (Shapiro-Wilk) and homoscedasticity (Levene). Calculates effect sizes (Hedges g or rank-biserial) with 95% bootstrap CI and permutation test for robustness. Documents the methodological decision in an exportable table.

**Why:** Verifying whether differences by gender or SEN exist is an educational equity question. Automatic test selection guarantees that the statistically appropriate method is applied in each case, which is especially critical when the SEN group has very few students (N < 10), a situation in which the p-value is highly unstable and an explicit warning is issued.
""",

"a4562645": """\
## 5. Self-Perception vs Actual Performance (CT)

**What this section does:** Contrasts students' self-perception about their CT performance with their actual performance. As the self-perception dataset has no individual ID column, the comparison is performed at **aggregate group level** (by gender, SEN or CT level): the group's mean self-perception is calculated and compared against its mean real CT score, identifying whether the group overestimates, underestimates or is well-calibrated.

**Why:** Metacognitive calibration (knowing one's own level well) is a key factor in learning. Students who overestimate themselves may not make sufficient effort; students who underestimate themselves may exhibit low self-efficacy. This section identifies groups with systematic self-perception mismatches.

> **Explicit limitation:** Without individual ID, student-to-student correlations cannot be calculated. All analyses are performed at group mean level and reported as such.
""",

"1fc140f4": """\
## 6. CT Level by Class: Low / Medium / High (Tertiles)

**What this section does:** Calculates the mean `pct_pc` of each class, ranks them and assigns a categorical level (**Low / Medium / High**) using tertiles with `pd.qcut`. If there are ties, it falls back to a dense ranking with manual cutoffs. The level is merged into the student CT dataset and becomes the moderating variable for sections 7 (History) and 8 (Ratings).

**Why:** With only 4 classes, the CT level cannot be used as a continuous quantitative variable between groups. Categorisation into tertiles allows analysing whether classes with higher CT performance also learn more History or rate activities differently. The assignment is only applied to Echegaray classes to avoid imputing levels to other schools without CT data.
""",

"c35b6343": """\
## 7. History (Excel): Enriched Analysis + CT Level + Categories

**What this section does:** Performs the complete analysis of History learning in a pre-post design with **independent samples**. The `Student` index in the data represents the response order — it does not identify the same student across initial and final tests — so individual observations cannot be paired.

| Subsection | Content |
|-----------|-----------|
| **7.1–7.2** | Preparation and cleaning of initial and final tests; independent samples design by class |
| **7.3** | Calculation of absolute gain per class and group Hake (over class means, not individual) |
| **7.4** | Enrichment with class CT level (Echegaray only) and item thematic categories |
| **7.5** | Global and per-class descriptives; boxplots, histograms, category × CT level heatmap |
| **7.6–7.8** | Inference: Welch-t / Mann-Whitney U (initial vs final, indep.); ANOVA/KW by CT level; OLS model |
| **7.9–7.14** | Item psychometrics (difficulty, discrimination, co-errors); between-class comparisons |

**Why:** Integrating CT level as a moderator of History gain allows answering whether classes with better computational thinking also learn more History, which would reveal a possible transfer of cognitive capacities between domains. Hake gain corrects the ceiling effect and allows comparing classes with different starting levels.
""",

"82564f10": """\
## 7 → 8 · History Section Summary

### What was done and why?

**7.1–7.5  Preparation (pre-post design, independent samples)**
The two History tests (Initial and Final) were cleaned and standardised. Upon confirming that the `Student` index represents the response order and does not identify the same student, an **independent samples** design was adopted: initial/final distributions are compared by class without individual pairing. Group Hake by class and Cohen's d on independent samples were calculated.

**7.6  Metrics by thematic category × CT Level**
To detect whether History learning is mediated by the computational thinking level, thematic item categories were crossed with each student's CT level. The heatmap facilitates reading strengths and gaps by theme.

**7.7–7.8  Descriptives and basic visualisations**
Histograms, boxplot of gain by CT level and bar plots of means by class (same as the reference notebook).

**7.9  Inference: Welch-t / Mann-Whitney U global + ANOVA/KW + OLS model**
Tested whether initial and final means differ (Welch-t or Mann-Whitney U depending on normality, independent samples), whether gain by class differs between CT levels (ANOVA/KW + post-hoc) and whether the model `gain_abs ~ pct_ini + ct_level + School` has explanatory power.

**7.10  Group Hake gain per class**
Equivalent to Section 5 of the reference notebook: calculates Hake gain at class level and categorises teaching effectiveness (Low/Medium/High). Exported to `historia_hake_por_clase.csv`.

**7.11  Box plots ini/fin by class + mean ± SD + global histogram**
Direct reproduction of Section 6 of the reference notebook: complete distribution visualisations with individual stripplot overlaid on the group boxplot, and bars with confidence intervals.

**7.12  Cohen's d (independent samples) + forest plot (95% bootstrap CI)**
Quantifies the magnitude of the learning effect (not just its statistical significance). Calculated for the global set and by class, with 95% CI obtained by bootstrap. Exported to `historia_efectos.csv`.

**7.13  Between-class comparison (ANOVA/KW + Bonferroni post-hoc)**
Equivalent to Section 8 of the reference notebook: tests whether there are inter-class differences at baseline, at the final score and in the gain. If the omnibus test is significant, post-hoc is applied. Exported to `historia_omnibus_clases.csv`.

**7.14  Item psychometrics (difficulty, pbis, D27, co-errors)**
Equivalent to Section 9 of the reference notebook: identifies items that are too easy/difficult or with low discrimination, and shows which pairs of items are systematically failed together.

## 8. Ratings + CT Level
""",

"f7cdd8a3": """\
### 8 · Ratings Section Summary

#### What was done and why?

**8.1–8.2  Ratings unification and enrichment**
All rating sheets are consolidated into a single long dataset and the CT level of each class is incorporated by joining with `df_nivel_clase`. Ratings outside the [0, 10] range are recorded as anomalies and excluded from analysis.

**8.3  Summary by Activity × CT level**
Allows seeing whether activities are rated differently depending on the CT level of the students. Exported to `votos_resumen_por_actividad_y_nivelpc.csv`.

**8.3b  Global activity ranking**
Lists activities from highest to lowest mean satisfaction with CI (±SD), equivalent to Section 10 of the reference notebook. Useful for prioritising which activities to repeat or reformulate. Exported to `votaciones_ranking_actividades.csv`.

**8.3c  Heatmap of mean ratings by Activity × Class**
Facilitates visual comparison between classes and detects whether an activity is rated very differently between groups. Exported as `votaciones_heatmap_clase.png`.

**8.4  Boxplots of ratings by activity × CT level**
Shows the complete distribution of ratings for each activity separated by CT level, detecting outliers and asymmetries.

**8.5  Satisfaction vs learning correlation (by class)**
Compares the class mean rating with its History gain and its group Hake gain. If the correlation is positive, the highest-rated activities are also those that produce the greatest learning. Exported as `votos_vs_ganancia_clase.png`.
""",

"a700796f": """\
### 9.1 Problem Decomposition

The problem is decomposed into nested layers:

**A) Student level (CT):** Each of the 97 Echegaray students took a 28-item test
whose responses (letters A/B/C/D) were compared against the correction key
(`especificacion_items.csv`), generating a continuous score `score_pc ∈ [0, 28]`.

**B) Class level (CT → History):** The means of `pct_pc` by class were ranked using
tertiles to assign a qualitative level {Low, Medium, High}. This level is "exported"
to the History data (Juan Echegaray) via the mapping `CT Class → History Class`.
For any other school present in the History data, the level remains NaN
to avoid imputation.

**C) Item level (History):** Each History item (P1-P8 initial, P1-P11 final)
has a thematic category (Algorithmics, Prehistory, Middle Ages…) extracted from
`category_questions.xlsx`. Converting to long format allows calculating difficulty
by category, timepoint and CT level simultaneously.

**D) Activity level (Ratings):** The 7 activities are unified into a single long format;
the CT level of the class is joined to compare ratings between groups.
""",

"b75d3380": """\
### 9.2 Detected Patterns

**Difficult items (% correct < 33%):** Visible in the heatmap `pc_heatmap_items_clase.png`.
Items with the highest difficulty tend to coincide with concepts of greater abstraction
(complex Conditionals, Functions). The `pct_Debugging` dimension tends to score
lower than `pct_Sequencing`, which is consistent with the literature on CT in Primary Education.

**Profiles by CT level:**
- **High**-level classes show more compact distributions (lower SD) and skewed
  towards high scores, suggesting internal homogeneity.
- **Low**-level classes show greater variance, with extreme students in both directions.

**Frequent co-errors:** Items in the Conditionals block (items 13-24 per spec)
show positive correlations with each other, indicating a shared error pattern.
This may reflect insufficient instruction in that concept or inherent cognitive difficulty
at this age.
""",

"a71603e3": """\
### 9.3 Abstraction

Three levels of abstraction have been created for CT performance:

1. **Raw score** (`score_pc`): direct sum of correct answers, scale 0-28.
2. **Proportion** (`pct_pc`): normalised to [0,1]; facilitates comparisons between tests
   with different numbers of items.
3. **Class level** (`nivel_pc` ∈ {Low, Medium, High}): tertile on class mean;
   categorical abstraction for cross-analyses with History and Ratings.

In History:
- `pct_hist_ini` and `pct_hist_fin`: proportions over 8 and 11 items respectively.
- `ganancia_abs`: class mean difference (`pct_fin_class − pct_ini_class`) — calculated at **class** level, not individual student, given the independent samples design.
- `hake_g`: group Hake gain (`g = (μ_fin − μ_ini) / (1 − μ_ini)`) calculated on class means; avoids ceiling effect.
""",

"30b99148": """\
### 9.4 Pipeline Algorithm and Decision Rules

The pipeline follows these coded rules:

```
FOR EACH two-group contrast:
  IF N(group) < 3 → skip Shapiro, use MWU
  IF N(SEN=Yes) < 10 → prioritise descriptive + bootstrap CI + warning
  ELSE:
    Shapiro on each group:
      IF both p_shapiro > 0.05 AND N < 50 → Welch-t; effect = Hedges g
      ELSE → Mann-Whitney; effect = rank-biserial
  ALWAYS: permutation test (5000 iterations) for robustness

FOR CT Level by class:
  TRY pd.qcut(q=3) → if fails due to duplicates → dense ranking + manual cutoffs

FOR History (independent samples):
  df_ini = Initial test (one row per student; Student = response order)
  df_fin = Final test  (different N per class — NOT individually pairable)
  ct_level: join by Class only if School contains "Echegaray"; else NaN (DO NOT impute)
  Hake: calculated on class means (g = (μ_fin - μ_ini) / (1 - μ_ini))
```
""",

"af71d65e": """\
### 9.5 Analysis Evaluation / Debugging

**Quality audit:**
- All datasets pass through `audit_df()` which reports %NaN by column, ranges and duplicates.
- Corrections (out-of-range values, recalculated TOTAL, Gender/SEN encodings)
  are written to `outputs/logs/data_quality.log`.

**SEN imbalance:**
- With N(SEN=Yes) ≈ 8, the p-value of any test is highly unstable.
  It is explicitly reported that strong conclusions should not be drawn.
  The permutation test is more robust than the asymptotic one in this scenario,
  but the effect size with bootstrap CI is the most reliable information.

**Self-perception without ID:**
- Since there is no ID column in the self-perception dataset, the relationship with actual
  performance can only be established at group aggregate level (group mean vs mean pct_pc
  of the same Gender/SEN group). This is declared as an **explicit limitation** and NO
  individual correlations are performed.

**CT level with few classes:**
- With only 4 classes, the tertiles collapse to ranges: the class with the lowest mean → Low,
  the central one (if 4, the second) → Medium, etc. The exact distribution
  is recorded in the log and in `nivel_pc_por_clase.csv`.
""",

"a738ed21": """\
## 10. Quality Gates — Automatic Output Verification

**What this section does:** Runs a battery of automatic checks on the existence and size of each expected output file (CSV tables and PNG figures), and verifies key data invariants: N students in initial and final History tests (independent samples), group Hake gain per class, presence of the CT level column in all datasets that require it, number of unique activities in ratings.

**Why:** A reproducible analysis does not end with the last code cell: it must verify that *all* its outputs are complete and intact. If any gate fails, the message indicates exactly which file or invariant is missing, allowing relaunching only the corresponding section without repeating the entire notebook.

> **PASS on all gates** → The analysis is correct, complete and reproducible.
> **FAIL on any gate** → Review and re-run the section indicated in the error message.
""",
}

# ─────────────────────────────────────────────────────────────────
# 2. CODE-CELL STRING SUBSTITUTIONS  (ordered – longer strings first)
# ─────────────────────────────────────────────────────────────────
# Each entry is (old, new).  Applied in order via str.replace().
CODE_SUBS = [
    # ── Figures path ──────────────────────────────────────────────
    ('FIGS   = OUT / "figures"',             'FIGS   = OUT / "figures" / "en"'),

    # ── Logger section headers ────────────────────────────────────
    ('"=== Inicio del análisis PC + Historia ==="',  '"=== Start of CT + History Analysis ==="'),
    ('"--- SECCIÓN 1: Carga de datos ---"',          '"--- SECTION 1: Data Loading ---"'),
    ('"--- SECCIÓN 2: Detección de formato PC + cálculo de aciertos ---"',
                                                     '"--- SECTION 2: CT Format Detection + Correct Answers ---"'),
    ('"--- SECCIÓN 3: Descriptivo PC ---"',          '"--- SECTION 3: CT Descriptives ---"'),
    ('"--- SECCIÓN 4: Contrastes género y NEE ---"', '"--- SECTION 4: Gender and SEN Contrasts ---"'),
    ('"--- SECCIÓN 5: Autopercepción ---"',          '"--- SECTION 5: Self-Perception ---"'),
    ('"--- SECCIÓN 6: Nivel PC por clase ---"',      '"--- SECTION 6: CT Level by Class ---"'),
    ('"--- SECCIÓN 7: Historia (muestras independientes) ---"',
                                                     '"--- SECTION 7: History (independent samples) ---"'),
    ('"--- SECCIÓN 8: Votaciones ---"',              '"--- SECTION 8: Ratings ---"'),
    ('"--- SECCIÓN 10: Quality Gates ---"',          '"--- SECTION 10: Quality Gates ---"'),
    ('"=== Análisis completado ==="',                '"=== Analysis completed ==="'),

    # ── Docstrings & comments ─────────────────────────────────────
    ('"""Lee CSV con detección automática de separador y encoding."""',
     '"""Reads CSV with automatic separator and encoding detection."""'),
    ('"""Lee hoja Excel con manejo de errores."""',
     '"""Reads Excel sheet with error handling."""'),
    ('"""Convierte a numérico; valores inválidos → NaN."""',
     '"""Converts to numeric; invalid values → NaN."""'),
    ('"""Fuerza a {0,1,NaN}; cualquier valor fuera → NaN."""',
     '"""Forces to {0,1,NaN}; any value outside → NaN."""'),
    ('"""Registra una anomalía en el log."""',
     '"""Records an anomaly in the log."""'),
    ('"""IC bootstrap percentil para una estadística."""',
     '"""Percentile bootstrap CI for a statistic."""'),
    ("""\"\"\"Hedges g con IC 95 % aproximado (Borenstein 2009).\"\"\"""",
     "\"\"\"Hedges g with approximate 95% CI (Borenstein 2009).\"\"\""""),
    ('"""Correlación biserial de rangos (Cliff\'s delta) para Mann-Whitney."""',
     '"""Rank-biserial correlation (Cliff\'s delta) for Mann-Whitney."""'),
    ('"""Prueba de permutación sobre diferencia de medias."""',
     '"""Permutation test on mean difference."""'),
    ('"""True si no se rechaza normalidad (N < 50) o si N >= 50 (no aplicable)."""',
     '"""True if normality not rejected (N < 50) or N >= 50 (not applicable)."""'),
    ('"""Selecciona t de Welch o Mann-Whitney según supuestos."""',
     '"""Selects Welch t or Mann-Whitney based on assumptions."""'),
    ('"""Genera tabla de auditoría para un DataFrame."""',
     '"""Generates audit table for a DataFrame."""'),
    ('"""Calcula estadísticos + IC95% bootstrap."""',
     '"""Calculates statistics + 95% bootstrap CI."""'),
    ('"""Construye tabla descriptiva para una lista de columnas pct_*."""',
     '"""Builds descriptive table for a list of pct_* columns."""'),
    ('"""Contraste automático entre dos grupos:',
     '"""Automatic contrast between two groups:'),
    ('    Retorna un dict con todos los resultados.',
     '    Returns a dict with all results.'),
    ('"""Limpia y prepara un test de historia."""',
     '"""Cleans and prepares a history test."""'),
    ('"""Une nivel_pc por clase. Si otro centro, deja NaN."""',
     '"""Joins ct_level by class. If another school, leaves NaN."""'),
    ('"""Convierte a formato largo. nivel_pc ya incluido en df."""',
     '"""Converts to long format. ct_level already included in df."""'),
    ('"""Dificultad y discriminación para ítems de Historia."""',
     '"""Difficulty and discrimination for History items."""'),
    ('"""Bootstrap CI para estadísticos de dos muestras independientes."""',
     '"""Bootstrap CI for two independent samples statistics."""'),
    ('"""Cohen\'s d para muestras independientes (pooled SD)."""',
     '"""Cohen\'s d for independent samples (pooled SD)."""'),

    # ── safe_read logger messages ─────────────────────────────────
    ('f"CSV cargado: {path.name} | enc={enc} sep=\'{sep}\' | {df.shape}"',
     'f"CSV loaded: {path.name} | enc={enc} sep=\'{sep}\' | {df.shape}"'),
    ('f"CSV cargado (fallback python engine): {path.name} | {df.shape}"',
     'f"CSV loaded (fallback python engine): {path.name} | {df.shape}"'),
    ('f"Excel cargado: {path.name} hoja=\'{sheet_name}\' | {df.shape}"',
     'f"Excel loaded: {path.name} sheet=\'{sheet_name}\' | {df.shape}"'),
    ('f"Error leyendo {path.name} hoja={sheet_name}: {e}"',
     'f"Error reading {path.name} sheet={sheet_name}: {e}"'),
    ('f"  \'{col_name}\': {n_bad} valores no numéricos → NaN"',
     'f"  \'{col_name}\': {n_bad} non-numeric values → NaN"'),
    ('f"  \'{col_name}\': {mask_invalid.sum()} valores ∉ {{0,1}} → NaN"',
     'f"  \'{col_name}\': {mask_invalid.sum()} values ∉ {{0,1}} → NaN"'),
    ('[ANOMALÍA]', '[ANOMALY]'),

    # ── Setup prints ──────────────────────────────────────────────
    ('print("Setup completo OK")', 'print("Setup complete OK")'),

    # ── Section 0 style_table docstring ──────────────────────────
    ('    Devuelve un pandas Styler con estilos consistentes para display en el cuaderno.\n    Parámetros\n    ----------\n    caption          : str   – Título que aparece sobre la tabla.\n    fmt_float        : str   – Formato para columnas float (default 3 decimales).\n    fmt_cols         : dict  – Sobreescribe formato para columnas específicas.\n    bar_col          : str   – Nombre de columna donde añadir barra de progreso.\n    bar_range        : tuple – (vmin, vmax) para la barra de progreso.\n    pval_cols        : list  – Columnas de p-valor; se resaltan en verde si < 0.05.\n    highlight_max_col: str   – Columna cuyo máximo se resalta en amarillo.\n    highlight_min_col: str   – Columna cuyo mínimo se resalta en rojo claro.\n    hide_index       : bool  – Ocultar el índice del DataFrame (default True).\n    ',
     '    Returns a pandas Styler with consistent styles for notebook display.\n    Parameters\n    ----------\n    caption          : str   – Title shown above the table.\n    fmt_float        : str   – Format for float columns (default 3 decimals).\n    fmt_cols         : dict  – Overrides format for specific columns.\n    bar_col          : str   – Column name where to add a progress bar.\n    bar_range        : tuple – (vmin, vmax) for the progress bar.\n    pval_cols        : list  – p-value columns; highlighted in green if < 0.05.\n    highlight_max_col: str   – Column whose maximum is highlighted in yellow.\n    highlight_min_col: str   – Column whose minimum is highlighted in light red.\n    hide_index       : bool  – Hide the DataFrame index (default True).\n    '),

    # ── Section 1 prints ──────────────────────────────────────────
    ('print(f"\\nHojas en {xl_path.name}:")',
     'print(f"\\nSheets in {xl_path.name}:")'),
    ('print(f"\\nHojas de votaciones: {voting_sheets}")',
     'print(f"\\nRating sheets: {voting_sheets}")'),
    ('f"Hojas category_questions.xlsx: {xl_cat.sheet_names}"',
     'f"Sheets category_questions.xlsx: {xl_cat.sheet_names}"'),

    # ── Audit ─────────────────────────────────────────────────────
    ('"columna"',       '"column"'),
    ('"n_no_nulos"',    '"n_non_null"'),
    ('"n_unicos"',      '"n_unique"'),
    ('f"[AUDITORÍA] {name}: {n_rows} filas × {n_cols} cols | "',
     'f"[AUDIT] {name}: {n_rows} rows × {n_cols} cols | "'),
    ('print(f"Auditoría guardada → {TABS / \'auditoria_datasets.csv\'}")',
     'print(f"Audit saved → {TABS / \'auditoria_datasets.csv\'}")'),
    ('"\\nResumen por dataset:"',             '"\\nSummary by dataset:"'),
    ('"% NaN por dataset (máximo y media)"',  '"% NaN by dataset (max and mean)"'),

    # ── Section 2 ─────────────────────────────────────────────────
    ('f"Columnas de preguntas detectadas: {len(pregunta_cols)}/28"',
     'f"Question columns detected: {len(pregunta_cols)}/28"'),
    ('print(f"Columnas de preguntas encontradas: {len(pregunta_cols)}")',
     'print(f"Question columns found: {len(pregunta_cols)}")'),
    # gender mapping values
    ('"chico": "Chico", "masculino": "Chico", "hombre": "Chico", "m": "Chico",',
     '"chico": "Boy", "masculino": "Boy", "hombre": "Boy", "m": "Boy",'),
    ('"chica": "Chica", "femenino": "Chica", "mujer": "Chica", "f": "Chica",',
     '"chica": "Girl", "femenino": "Girl", "mujer": "Girl", "f": "Girl",'),
    # NEE mapping values
    ('"si": "Sí", "sí": "Sí", "yes": "Sí", "1": "Sí",',
     '"si": "Yes", "sí": "Yes", "yes": "Yes", "1": "Yes",'),
    ('print("Distribución de grupos:")',  'print("Group distribution:")'),
    ('fmt_detected = "BINARIO (0/1)"',   'fmt_detected = "BINARY (0/1)"'),
    ('fmt_detected = "LETRAS (A/B/C/D)"','fmt_detected = "LETTERS (A/B/C/D)"'),
    ('f"Formato PC detectado: {fmt_detected} → convirtiendo a 0/1"',
     'f"CT format detected: {fmt_detected} → converting to 0/1"'),
    ('f"Formato PC detectado: {fmt_detected}"',
     'f"CT format detected: {fmt_detected}"'),
    ('print(f"\\nFormato detectado: {fmt_detected}")',
     'print(f"\\nDetected format: {fmt_detected}")'),
    ('print(f"Conversiones realizadas: {n_conversiones}")',
     'print(f"Conversions performed: {n_conversiones}")'),
    ('print("\\nVariables construidas:")',         'print("\\nConstructed variables:")'),
    ('print(f"  Tarea_requerida : {tarea_pct_cols}")',  'print(f"  Required_Task   : {tarea_pct_cols}")'),
    ('print(f"  Conceptos       : {concepto_pct_cols}")', 'print(f"  Concepts        : {concepto_pct_cols}")'),
    ('print(f"\\nResumen score_pc:")',              'print(f"\\nScore summary:")'),
    ('"Estadísticos descriptivos: score PC inicial"', '"Descriptive statistics: initial CT score"'),
    ('.rename(columns={"index": "estadístico"})', '.rename(columns={"index": "statistic"})'),
    ('print(f"\\nExportado → {TABS / \'pc_limpio_por_alumno.csv\'}")',
     'print(f"\\nExported → {TABS / \'pc_limpio_por_alumno.csv\'}")'),

    # ── Section 3 histograms ──────────────────────────────────────
    ('"Puntuación (0-28)"',                         '"Score (0-28)"'),
    ('"% aciertos (0-1)"',                          '"% correct (0-1)"'),
    ('"Frecuencia"',                                '"Frequency"'),
    ('f"Distribución {col}"',                       'f"Distribution {col}"'),
    ('"Distribución global del Test Inicial PC"',   '"Global Distribution of Initial CT Test"'),
    ('print("Figura guardada: pc_histograma_global.png")',
     'print("Figure saved: pc_histograma_global.png")'),
    # violin groups
    ('"Clase (A/B/C/D)"',                           '"Class (A/B/C/D)"'),
    ('"Necesidad Educativa Especial"',               '"Special Educational Needs (SEN)"'),
    ('"Chico": "#59A14F", "Chica": "#B07AA1",',     '"Boy": "#59A14F", "Girl": "#B07AA1",'),
    ('"Sí": "#FF9DA7", "No": "#9C755F"',            '"Yes": "#FF9DA7", "No": "#9C755F"'),
    ('"Score PC (0-28)"',                           '"CT Score (0-28)"'),
    ('f"Score PC por {gvar}"',                      'f"CT Score by {gvar}"'),
    ('"Score PC inicial por grupos"',               '"Initial CT Score by groups"'),
    ('print("Figura guardada: pc_violin_por_grupo.png")',
     'print("Figure saved: pc_violin_por_grupo.png")'),
    # descriptive tables
    ('"Estadísticos descriptivos globales — PC inicial"',
     '"Global Descriptive Statistics — Initial CT"'),
    ('"Descriptivos PC por grupo (Clase / Género / NEE)"',
     '"CT Descriptives by Group (Class / Gender / SEN)"'),
    ('"Grupo" if grupo_col else "Global"', '"Group" if grupo_col else "Global"'),
    ('"\\nDescriptivo por grupos:"',  '"\\nDescriptives by group:"'),
    ('"Descriptivo global:"',         '"Global descriptives:"'),
    # item table
    ('print(f"\\nTabla de ítems guardada → {TABS / \'pc_por_item_y_clase.csv\'}")',
     'print(f"\\nItem table saved → {TABS / \'pc_por_item_y_clase.csv\'}")'),
    ('"% Acierto por ítem y clase"',                '"% Correct by item and class"'),
    # heatmap
    ('"Heatmap % acierto por Pregunta × Clase (+ Global)"',
     '"Heatmap % correct by Question × Class (+ Global)"'),
    ('cbar_kws={"label": "% acierto"}',            'cbar_kws={"label": "% correct"}'),
    ('print("Figura guardada: pc_heatmap_items_clase.png")',
     'print("Figure saved: pc_heatmap_items_clase.png")'),
    # tarea/concepto tables
    ('"Tarea_requerida"',  '"Required_Task"'),
    ('print(f"\\nTabla por Tarea_requerida → {TABS / \'pc_por_tarea_requerida.csv\'}")',
     'print(f"\\nTable by Required Task → {TABS / \'pc_por_tarea_requerida.csv\'}")'),
    ('"Score PC por tarea requerida"',     '"CT Score by Required Task"'),
    ('print(f"\\nTabla por Concepto Computacional → {TABS / \'pc_por_concepto_computacional.csv\'}")',
     'print(f"\\nTable by Computational Concept → {TABS / \'pc_por_concepto_computacional.csv\'}")'),
    ('"Score PC por concepto computacional"', '"CT Score by Computational Concept"'),
    ('"Concepto"', '"Concept"'),
    # barplots
    ('"% acierto medio"',                           '"Mean % correct"'),
    ('"% Acierto por Tarea Requerida (Test PC Inicial)"',
     '"% Correct by Required Task (Initial CT Test)"'),
    ('print("Figura guardada: pc_acierto_por_tarea_requerida.png")',
     'print("Figure saved: pc_acierto_por_tarea_requerida.png")'),
    ('"% Acierto por Concepto Computacional (Test PC Inicial)\\n"',
     '"% Correct by Computational Concept (Initial CT Test)\\n"'),
    ('"Direcciones · Bucles · Condicionales · Funciones"',
     '"Directions · Loops · Conditionals · Functions"'),
    ('print("Figura guardada: pc_acierto_por_concepto.png")',
     'print("Figure saved: pc_acierto_por_concepto.png")'),
    # nota10 histogram
    ('"Aprobado (5)"',                              '"Pass (5)"'),
    ('"Nota (escala 0-10)"',                        '"Grade (scale 0-10)"'),
    ('"Distribución del Test Inicial PC — Escala 0-10"',
     '"Distribution of Initial CT Test — Scale 0-10"'),
    ('print("Figura guardada: pc_histograma_nota10.png")',
     'print("Figure saved: pc_histograma_nota10.png")'),
    ('"Nota (0-10)"',                               '"Grade (0-10)"'),
    ('f"Nota PC (0-10) por {gvar}"',               'f"CT Grade (0-10) by {gvar}"'),
    ('"Score PC inicial en escala 0-10 por grupos"',
     '"Initial CT Score (scale 0-10) by groups"'),
    ('print("Figura guardada: pc_violin_nota10_por_grupo.png")',
     'print("Figure saved: pc_violin_nota10_por_grupo.png")'),

    # ── Section 4 contrasts ───────────────────────────────────────
    ('"Normalidad score_pc por Género"',            '"Normality of score_pc by Gender"'),
    ('"=== Contraste Género ==="',                  '"=== Gender Contrast ==="'),
    ('"=== Contraste NEE ==="',                     '"=== SEN Contrast ==="'),
    ('f"  N(NEE=Sí)={n_nee_si}  N(NEE=No)={n_nee_no}"',
     'f"  N(SEN=Yes)={n_nee_si}  N(SEN=No)={n_nee_no}"'),
    ('f"[NEE] Desequilibrio muestral severo: N(Sí)={n_nee_si}. "',
     'f"[SEN] Severe sample imbalance: N(Yes)={n_nee_si}. "'),
    ('"Se prioriza descriptivo + bootstrapping. Conclusiones de p-valor con CAUTELA EXTREMA."',
     '"Prioritising descriptive + bootstrapping. p-value conclusions with EXTREME CAUTION."'),
    ('f"[!] **ADVERTENCIA:** El grupo NEE=Sí tiene solo {n_nee_si} alumnos. "',
     'f"[!] **WARNING:** The SEN=Yes group has only {n_nee_si} students. "'),
    ('"Los p-valores son extremadamente poco fiables en muestras tan pequeñas. "',
     '"p-values are extremely unreliable in such small samples. "'),
    ('"Se reportan descriptivos, tamaño de efecto con IC bootstrap y prueba de permutación. "',
     '"Reporting descriptives, effect size with bootstrap CI and permutation test. "'),
    ('"NO deben extraerse conclusiones fuertes sobre significación estadística."',
     '"Strong conclusions about statistical significance should NOT be drawn."'),
    ('"MWU + permutación + IC bootstrap (N<10 en NEE=Sí)"',
     '"MWU + permutation + bootstrap CI (N<10 in SEN=Yes)"'),
    ('"Selección automática Shapiro + Levene"',
     '"Automatic selection Shapiro + Levene"'),
    ('"metodo"',        '"method"'),
    ('"advertencia"',   '"warning"'),
    # contraste result keys in dict literals
    ('"estadístico":',  '"statistic":'),
    ('"p_valor":',      '"p_value":'),
    ('"tipo_efecto":',  '"effect_type":'),
    ('"test_elegido":', '"chosen_test":'),
    ('"efecto":',       '"effect":'),
    ('"Requiere exactamente 2 grupos"', '"Requires exactly 2 groups"'),
    # decision table
    ('"Contraste": "Género (Chico vs Chica)"', '"Contrast": "Gender (Boy vs Girl)"'),
    ('"Contraste": "NEE (Sí vs No)"',          '"Contrast": "SEN (Yes vs No)"'),
    ('"Tipo_efecto"',   '"Effect_Type"'),
    ('"Test_elegido"',  '"Chosen_Test"'),
    ('"N_grupo1"',      '"N_group1"'),
    ('"N_grupo2"',      '"N_group2"'),
    ('"Decisión"',      '"Decision"'),
    ('"Decisión metodológica: Género y NEE"',
     '"Methodological Decision: Gender and SEN"'),
    # boxplot IC
    ('"Contraste Score PC por Género y NEE\\n(* = media; barras = IC95% bootstrap)"',
     '"CT Score Contrast by Gender and SEN\\n(* = mean; bars = 95% bootstrap CI)"'),
    ('f"Score PC por {glabel}"',  'f"CT Score by {glabel}"'),
    ('print("Figura guardada: pc_contraste_grupos.png")',
     'print("Figure saved: pc_contraste_grupos.png")'),
    # norm10 boxplot
    ('"Contraste Score PC normalizado (0-10) por Género y NEE\\n"',
     '"Normalised CT Score Contrast (0-10) by Gender and SEN\\n"'),
    ('"(◆ = media; barras = IC95% bootstrap)"',
     '"(◆ = mean; bars = 95% bootstrap CI)"'),
    ('f"Score PC (0-10) por {glabel}"',  'f"CT Score (0-10) by {glabel}"'),
    ('"Score PC (0-10)"',               '"CT Score (0-10)"'),
    ('print("Figura guardada: pc_contraste_grupos_norm10.png")',
     'print("Figure saved: pc_contraste_grupos_norm10.png")'),
    # QQ-plots
    ('"Normalidad score_pc por NEE"', '"Normality of score_pc by SEN"'),
    ('"Normalidad score_pc por Género"', '"Normality of score_pc by Gender"'),
    # print results
    ('print("Resultados NEE:")', 'print("SEN results:")'),

    # ── Section 5 self-perception ─────────────────────────────────
    ('"Estadísticos descriptivos: autopercepción"',
     '"Descriptive Statistics: self-perception"'),
    ('"[!]  Sin ID común → Análisis AGREGADO por grupo (no individual)."',
     '"[!]  No common ID → AGGREGATE analysis by group (not individual)."'),
    ('"   LIMITACIÓN: La comparación autopercepción vs rendimiento real"',
     '"   LIMITATION: The self-perception vs actual performance comparison"'),
    ('"   se realiza a nivel de media de grupo, NO a nivel de alumno."',
     '"   is performed at group mean level, NOT at student level."'),
    ('"[AUTOPERCEPCIÓN] Se encontró ID común → emparejamiento individual"',
     '"[SELF-PERCEPTION] Common ID found → individual pairing"'),
    ('f"  Emparejados: {len(df_merged)} alumnos"',
     'f"  Paired: {len(df_merged)} students"'),
    ('"[AUTOPERCEPCIÓN] No hay columna ID común con PC. "',
     '"[SELF-PERCEPTION] No common ID column with CT. "'),
    ('"No se realizará emparejamiento individual. "',
     '"Individual pairing will not be performed. "'),
    ('"Análisis EXCLUSIVAMENTE agregado por grupo. "',
     '"EXCLUSIVELY aggregate analysis by group. "'),
    ('"LIMITACIÓN: no es posible relacionar autopercepción con rendimiento a nivel individuo."',
     '"LIMITATION: it is not possible to relate self-perception with performance at individual level."'),
    ('"Agrupación"',    '"Grouping"'),
    ('"Grupo"',         '"Group"'),
    ('"Variable"',      '"Variable"'),
    ('"Descriptivos autopercepción por grupo"',
     '"Self-Perception Descriptives by Group"'),
    ('"Variable_agrupacion"',           '"Grouping_Variable"'),
    ('"diferencia_agregada"',           '"aggregate_difference"'),
    ('"nota": "Comparación a nivel de grupo, NO individual"',
     '"note": "Comparison at group level, NOT individual"'),
    ('"Comparación agregada por grupo (sin emparejamiento individual):"',
     '"Aggregate comparison by group (no individual pairing):"'),
    ('"Comparación agregada autopercepción vs rendimiento real"',
     '"Aggregate comparison self-perception vs actual performance"'),
    ('print(f"\\nContrastes autopercepción → {TABS / \'autopercepcion_contrastes.csv\'}")',
     'print(f"\\nSelf-perception contrasts → {TABS / \'autopercepcion_contrastes.csv\'}")'),
    ('"Autopercepción y Dificultad por Género"',
     '"Self-Perception and Difficulty by Gender"'),
    ('"Puntuación (0-10)"',             '"Score (0-10)"'),
    ('"Rendimiento real (pct_pc)"',     '"Actual performance (pct_pc)"'),
    ('"Autopercepción norm."',          '"Self-perception norm."'),
    ('"Proporción (0-1)"',              '"Proportion (0-1)"'),
    ('"Autopercepción vs Rendimiento Real (medias por grupo)"',
     '"Self-Perception vs Actual Performance (group means)"'),
    ('"[!] Comparación agregada por grupo, NO individual"',
     '"[!] Aggregate comparison by group, NOT individual"'),
    ('print("Figuras autopercepción guardadas OK")',
     'print("Self-perception figures saved OK")'),
    ('"autopercepcion_norm"',           '"self_perception_norm"'),
    ('"error_calibracion"',             '"calibration_error"'),
    ('f"\\nCorrelaciones (N={len(df_merged)}):"',
     'f"\\nCorrelations (N={len(df_merged)}):"'),
    ('"Autopercepción normalizada"',    '"Normalised self-perception"'),
    ('"Autopercepción vs Rendimiento Real (individual)"',
     '"Self-Perception vs Actual Performance (individual)"'),

    # ── Section 6 CT level ────────────────────────────────────────
    ('"Media pct_pc por Clase:"',                   '"Mean pct_pc by Class:"'),
    ('"Media pct_pc por clase"',                    '"Mean pct_pc by class"'),
    # CT level labels (as list literal)
    ('labels=["Bajo", "Medio", "Alto"]',            'labels=["Low", "Medium", "High"]'),
    # CT level logger
    ('"[NIVEL_PC] Pocas clases para terciles; usando ranking denso"',
     '"[CT_LEVEL] Few classes for tertiles; using dense ranking"'),
    ('"[NIVEL_PC] qcut falló (valores repetidos). Usando ranking denso + cortes manuales."',
     '"[CT_LEVEL] qcut failed (repeated values). Using dense ranking + manual cutoffs."'),
    ('f"  Clase={row[\'Clase\']} mean_pct={row[\'mean_pct_pc\']:.3f} nivel={row[\'nivel_pc\']}"',
     'f"  Class={row[\'Clase\']} mean_pct={row[\'mean_pct_pc\']:.3f} level={row[\'nivel_pc\']}"'),
    ('print(f"\\nNivel PC por clase → {TABS / \'nivel_pc_por_clase.csv\'}")',
     'print(f"\\nCT level by class → {TABS / \'nivel_pc_por_clase.csv\'}")'),
    ('"Nivel PC asignado por clase (terciles)"',    '"CT Level assigned by class (tertiles)"'),
    ('"\\nDistribución nivel_pc en alumnos PC:"',   '"\\nCT level distribution in CT students:"'),
    ('"Alumnos PC por nivel de clase"',             '"CT students by class level"'),
    ('"Media % aciertos PC"',                       '"Mean % correct CT"'),
    ('"Nivel PC por Clase (terciles sobre media de clase)"',
     '"CT Level by Class (tertiles on class mean)"'),
    ('"Nivel PC"',      '"CT Level"'),
    ('{"Bajo": "#E15759", "Medio": "#F28E2B", "Alto": "#59A14F"}',
     '{"Low": "#E15759", "Medium": "#F28E2B", "High": "#59A14F"}'),
    ('print("Figura guardada: pc_nivel_por_clase.png")',
     'print("Figure saved: pc_nivel_por_clase.png")'),
    # Hake category labels
    ('"Baja (<0.30)"',       '"Low (<0.30)"'),
    ('"Media (0.30–0.70)"',  '"Medium (0.30–0.70)"'),
    ('"Alta (>0.70)"',       '"High (>0.70)"'),

    # ── Section 7 History ─────────────────────────────────────────
    ('f"  Historia {tipo}: columna TOTAL renombrada desde \'{total_col}\'"',
     'f"  History {tipo}: TOTAL column renamed from \'{total_col}\'"'),
    ('f"  Historia {tipo}: {df.shape[0]} filas, {len(p_cols)} ítems"',
     'f"  History {tipo}: {df.shape[0]} rows, {len(p_cols)} items"'),
    ('print(f"Historia Inicial: {df_ini.shape} | ítems: {p_cols_ini}")',
     'print(f"History Initial: {df_ini.shape} | items: {p_cols_ini}")'),
    ('print(f"Historia Final:   {df_fin.shape} | ítems: {p_cols_fin}")',
     'print(f"History Final:   {df_fin.shape} | items: {p_cols_fin}")'),
    ('"Une nivel_pc por clase. Si otro centro, deja NaN."',
     '"Joins ct_level by class. If another school, leaves NaN."'),
    ('f"  nivel_pc asignado: {n_asig} | sin asignar: {n_nan}"',
     'f"  ct_level assigned: {n_asig} | unassigned: {n_nan}"'),
    ('f"\\nHistoria Inicial: N={len(df_ini)} | media={df_ini[\'pct_hist\'].mean():.3f}"',
     'f"\\nHistory Initial: N={len(df_ini)} | mean={df_ini[\'pct_hist\'].mean():.3f}"'),
    ('" SD={df_ini[\'pct_hist\'].std():.3f}"',
     '" SD={df_ini[\'pct_hist\'].std():.3f}"'),
    ('f"Historia Final:   N={len(df_fin)} | media={df_fin[\'pct_hist\'].mean():.3f}"',
     'f"History Final:   N={len(df_fin)} | mean={df_fin[\'pct_hist\'].mean():.3f}"'),
    ('"\\n⚠ Diseño: MUESTRAS INDEPENDIENTES — sin emparejamiento individual por alumno"',
     '"\\n⚠ Design: INDEPENDENT SAMPLES — no individual student pairing"'),
    ('"\\nnivel_pc — Inicial:"',  '"\\nCT level — Initial:"'),
    ('"\\nnivel_pc — Final:"',    '"\\nCT level — Final:"'),
    ('"Distribución nivel PC — Historia Inicial"',  '"CT Level Distribution — History Initial"'),
    ('"Distribución nivel PC — Historia Final"',    '"CT Level Distribution — History Final"'),
    ('print("\\nMapa categorías Inicial:", cat_ini_map)',
     'print("\\nInitial category map:", cat_ini_map)'),
    ('print("Mapa categorías Final:  ", cat_fin_map)',
     'print("Final category map:  ", cat_fin_map)'),
    # to_long column names
    ('"Momento"',       '"Timepoint"'),
    ('"Acierto"',       '"Correct"'),
    ('"Categoria"',     '"Category"'),
    ('"Desconocida"',   '"Unknown"'),
    ('"Desconocido"',   '"Unknown"'),
    ('f"\\nDataset largo historia: {df_long.shape}"',
     'f"\\nLong history dataset: {df_long.shape}"'),
    # cat stats
    ('print(f"\\nTabla categoría×nivel_pc → {TABS / \'historia_categoria_stats.csv\'}")',
     'print(f"\\nTable category×CT_level → {TABS / \'historia_categoria_stats.csv\'}")'),
    ('f"% Acierto por Categoría × Nivel PC — {momento}"',
     'f"% Correct by Category × CT Level — {momento}"'),
    ('f"Figura guardada: historia_heatmap_cat_nivel_{momento.lower()}.png"',
     'f"Figure saved: historia_heatmap_cat_nivel_{momento.lower()}.png"'),
    # hist resumen
    ('"Momento"',       '"Timepoint"'),   # duplicate – harmless
    ('print(f"\\nResumen historia → {TABS / \'historia_resumen_por_grupo.csv\'}")',
     'print(f"\\nHistory summary → {TABS / \'historia_resumen_por_grupo.csv\'}")'),
    ('"Resumen descriptivo global — Historia (inicial y final)"',
     '"Global Descriptive Summary — History (initial and final)"'),
    # Section 7.7 figures
    ('"Distribución Test Historia — Inicial vs Final (muestras independientes)"',
     '"History Test Distribution — Initial vs Final (independent samples)"'),
    ('"% aciertos"',                                '"% correct"'),
    ('"Nivel PC (asignado por clase)"',             '"CT Level (assigned by class)"'),
    ('"Puntuación normalizada (0–1)"',              '"Normalised score (0–1)"'),
    ('"Historia Inicial vs Final por Nivel PC\\n(muestras independientes)"',
     '"History Initial vs Final by CT Level\\n(independent samples)"'),
    ('"Rendimiento Historia por Clase — Inicial vs Final\\n(muestras independientes)"',
     '"History Performance by Class — Initial vs Final\\n(independent samples)"'),
    ('print("Figuras 7.7 guardadas OK")', 'print("Figures 7.7 saved OK")'),
    # 7.8 inference
    ('"  Inferencia historia (muestras independientes)..."',
     '"  History inference (independent samples)..."'),
    ('"Contraste global ini vs fin (indep.)"', '"Global contrast ini vs fin (indep.)"'),
    ('"N_ini"',      '"N_ini"'),
    ('"N_fin"',      '"N_fin"'),
    ('"media_ini"',  '"mean_ini"'),
    ('"media_fin"',  '"mean_fin"'),
    ('"diff_medias"', '"diff_means"'),
    ('"Estadístico"', '"Statistic"'),
    ('f"\\nTest global ini vs fin ({test_name_g}): stat={stat_g:.4f} p={p_g:.4f}"',
     'f"\\nGlobal test ini vs fin ({test_name_g}): stat={stat_g:.4f} p={p_g:.4f}"'),
    ('f"  Δ medias (fin−ini): {diff_means_g:+.3f}  IC95=[{ci_lo_g:.3f}, {ci_hi_g:.3f}]"',
     'f"  Δ means (fin−ini): {diff_means_g:+.3f}  CI95=[{ci_lo_g:.3f}, {ci_hi_g:.3f}]"'),
    ('"Final por Nivel PC (omnibus)"',   '"Final by CT Level (omnibus)"'),
    ('"Inicial por Nivel PC (omnibus)"', '"Initial by CT Level (omnibus)"'),
    ('"=== Modelo Lineal: pct_hist(Final) ~ nivel_pc + Colegio ==="',
     '"=== Linear Model: pct_hist(Final) ~ ct_level + School ==="'),
    # Hake
    ('"=== Ganancia de Hake grupal por clase (Historia — muestras indep.) ==="',
     '"=== Group Hake Gain per Class (History — independent samples) ==="'),
    ('"Ganancia de Hake grupal por clase — Historia"',
     '"Group Hake Gain by Class — History"'),
    ('"umbral bajo (0.30)"',  '"low threshold (0.30)"'),
    ('"umbral alto (0.70)"',  '"high threshold (0.70)"'),
    ('"Ganancia de Hake g"',  '"Hake Gain g"'),
    ('"Ganancia de Hake grupal por clase — Historia\\n(muestras independientes)"',
     '"Group Hake Gain by Class — History\\n(independent samples)"'),
    ('print("Figura guardada: historia_hake_por_clase.png")',
     'print("Figure saved: historia_hake_por_clase.png")'),
    # 7.10
    ('"Distribución Historia por clase — Inicial vs Final\\n(muestras independientes)"',
     '"History Distribution by Class — Initial vs Final\\n(independent samples)"'),
    ('print("Figura guardada: historia_boxplot_ini_fin_clase.png")',
     'print("Figure saved: historia_boxplot_ini_fin_clase.png")'),
    ('"Media Inicial"',  '"Initial Mean"'),
    ('"Media Final"',    '"Final Mean"'),
    ('"Puntuación normalizada media (± SD)"', '"Mean normalised score (± SD)"'),
    ('"Media Historia Inicial vs Final por clase (± SD)\\n(muestras independientes)"',
     '"Mean History Initial vs Final by Class (± SD)\\n(independent samples)"'),
    ('print("Figura guardada: historia_medias_ini_fin_clase.png")',
     'print("Figure saved: historia_medias_ini_fin_clase.png")'),
    ('"Histograma global Historia — Inicial vs Final\\n(muestras independientes)"',
     '"Global History Histogram — Initial vs Final\\n(independent samples)"'),
    ('print("Figura guardada: historia_histograma_global.png")',
     'print("Figure saved: historia_histograma_global.png")'),
    # 7.11 Cohen's d
    ('"GLOBAL"',     '"GLOBAL"'),
    ('"Cohen_d"',    '"Cohen_d"'),
    ('"pequeño (0.2)"',  '"small (0.2)"'),
    ('"mediano (0.5)"',  '"medium (0.5)"'),
    ('"grande (0.8)"',   '"large (0.8)"'),
    ('"Cohen\'s d  (muestras indep.; positivo = Final > Inicial)"',
     '"Cohen\'s d  (independent samples; positive = Final > Initial)"'),
    ('"Tamaños de efecto Historia ini→fin (IC95% bootstrap)"',
     '"History Effect Sizes ini→fin (95% bootstrap CI)"'),
    ('"Tamaños de efecto — Historia (Cohen\'s d)"',
     '"Effect Sizes — History (Cohen\'s d)"'),
    ('print("Figura guardada: historia_effect_sizes.png")',
     'print("Figure saved: historia_effect_sizes.png")'),
    # 7.12 ANOVA
    ('"Inicial — entre clases"',     '"Initial — between classes"'),
    ('"Final — entre clases"',       '"Final — between classes"'),
    ('"Método"',    '"Method"'),
    ('"Comparaciones entre clases — Historia (ANOVA / Kruskal-Wallis)"',
     '"Between-class comparisons — History (ANOVA / Kruskal-Wallis)"'),
    ('"=== Comparaciones entre clases (Historia) ==="',
     '"=== Between-class comparisons (History) ==="'),
    ('f"=== Post-hoc Mann-Whitney + Bonferroni: {lbl_ph} ==="',
     'f"=== Post-hoc Mann-Whitney + Bonferroni: {lbl_ph} ==="'),
    ('"Post-hoc entre clases (Bonferroni)"',
     '"Post-hoc between classes (Bonferroni)"'),
    ('f"\\n→ {lbl_ph}: p ≥ 0.05 — sin diferencias significativas entre clases."',
     'f"\\n→ {lbl_ph}: p ≥ 0.05 — no significant differences between classes."'),
    ('"Comparación entre clases — Historia (Inicial / Final)"',
     '"Between-class comparison — History (Initial / Final)"'),
    ('print("Figura guardada: historia_comparacion_clases.png")',
     'print("Figure saved: historia_comparacion_clases.png")'),
    # 7.13 items
    ('"=== Análisis psicométrico por ítem — Historia ==="',
     '"=== Psychometric item analysis — History ==="'),
    ('"Análisis psicométrico por ítem — Historia"',
     '"Psychometric item analysis — History"'),
    ('"Test Historia Inicial"',   '"Initial History Test"'),
    ('"Test Historia Final"',     '"Final History Test"'),
    ('"Indicador"',   '"Indicator"'),
    ('"Ítem"',        '"Item"'),
    ('"Dificultad y Discriminación por Ítem — Historia"',
     '"Difficulty and Discrimination by Item — History"'),
    ('print("Figura guardada: historia_heatmap_items.png")',
     'print("Figure saved: historia_heatmap_items.png")'),
    ('"Co-errores Inicial"',  '"Co-errors Initial"'),
    ('"Co-errores Final"',    '"Co-errors Final"'),
    ('"Matriz de Co-errores — Historia (veces que dos ítems fallan juntos)"',
     '"Co-error Matrix — History (times two items fail together)"'),
    ('print("Figura guardada: historia_coerror_matrix.png")',
     'print("Figure saved: historia_coerror_matrix.png")'),

    # ── Section 8 Ratings ─────────────────────────────────────────
    ('"% Missing votos por actividad:"',    '"% Missing ratings by activity:"'),
    ('"% Missing votos por actividad"',     '"% Missing ratings by activity"'),
    ('f"Votaciones \'{sh_name}\': {out_range.sum()} votos fuera [0,10] → NaN"',
     'f"Ratings \'{sh_name}\': {out_range.sum()} ratings outside [0,10] → NaN"'),
    ('"Voto"',       '"Rating"'),
    ('f"\\nVotaciones con nivel_pc asignado: {df_votes[\'nivel_pc\'].notna().sum()}/{len(df_votes)}"',
     'f"\\nRatings with ct_level assigned: {df_votes[\'nivel_pc\'].notna().sum()}/{len(df_votes)}"'),
    ('"Distribución de votos por nivel PC"', '"Rating distribution by CT level"'),
    ('"media_voto"',     '"mean_rating"'),
    ('"mediana_voto"',   '"median_rating"'),
    ('"sd_voto"',        '"sd_rating"'),
    ('print(f"\\nResumen votos → {TABS / \'votos_resumen_por_actividad_y_nivelpc.csv\'}")',
     'print(f"\\nRatings summary → {TABS / \'votos_resumen_por_actividad_y_nivelpc.csv\'}")'),
    ('"Resumen votos por actividad × nivel PC"', '"Ratings summary by activity × CT level"'),
    ('"n_votos"',        '"n_ratings"'),
    ('"media_global"',   '"global_mean"'),
    ('"std_global"',     '"global_std"'),
    ('"mediana"',        '"median"'),
    ('"=== Ranking global de actividades ==="', '"=== Global activity ranking ==="'),
    ('"Ranking global de actividades por satisfacción media"',
     '"Global activity ranking by mean satisfaction"'),
    ('"Voto medio (0–10)"',  '"Mean rating (0–10)"'),
    ('"Ranking global de actividades por satisfacción media (± SD)"',
     '"Global activity ranking by mean satisfaction (± SD)"'),
    ('print("Figura guardada: votaciones_ranking_actividades.png")',
     'print("Figure saved: votaciones_ranking_actividades.png")'),
    ('"Voto medio por Actividad × Clase"', '"Mean rating by Activity × Class"'),
    ('print("Figura guardada: votaciones_heatmap_clase.png")',
     'print("Figure saved: votaciones_heatmap_clase.png")'),
    ('"Votos por Actividad × Nivel PC"', '"Ratings by Activity × CT Level"'),
    ('"Voto (0-10)"',     '"Rating (0-10)"'),
    ('print("Figura guardada: votos_por_actividad_nivel_pc.png")',
     'print("Figure saved: votos_por_actividad_nivel_pc.png")'),
    # vote vs gain
    ('"media_voto_clase"', '"mean_rating_class"'),
    ('f"\\nCorrelación Spearman voto_clase vs ganancia_clase: ρ={r_sp:.3f} p={p_sp:.4f}"',
     'f"\\nSpearman correlation rating_class vs gain_class: ρ={r_sp:.3f} p={p_sp:.4f}"'),
    ('"  (N clases muy pequeño → interpretación orientativa)"',
     '"  (N classes very small → indicative interpretation)"'),
    ('"Ganancia media historia (pct_fin − pct_ini)"',
     '"Mean history gain (pct_fin − pct_ini)"'),
    ('"Ganancia de Hake g grupal"',   '"Group Hake Gain g"'),
    ('"Voto medio de la clase (0–10)"',  '"Class mean rating (0–10)"'),
    ('"Satisfacción vs Aprendizaje (por clase)"',
     '"Satisfaction vs Learning (by class)"'),
    ('"Relación Votos × Ganancia Historia — por clase"',
     '"Rating × History Gain Relationship — by class"'),
    ('print("Figura guardada: votos_vs_ganancia_clase.png")',
     'print("Figure saved: votos_vs_ganancia_clase.png")'),
    ('"Insuficientes clases con datos voto+ganancia para correlación voto-ganancia"',
     '"Insufficient classes with rating+gain data for rating-gain correlation"'),

    # ── Section 10 Quality Gates ──────────────────────────────────
    ('"QUALITY GATES: Verificación de outputs"',    '"QUALITY GATES: Output verification"'),
    ('"✗ FALTA"',    '"✗ MISSING"'),
    ('f"[ TABLAS — {len(expected_tables)} esperadas ]"',
     'f"[ TABLES — {len(expected_tables)} expected ]"'),
    ('f"[ FIGURAS — {len(expected_figures)} esperadas ]"',
     'f"[ FIGURES — {len(expected_figures)} expected ]"'),
    ('"Tipo"',       '"Type"'),
    ('"Archivo"',    '"File"'),
    ('"Estado"',     '"Status"'),
    ('"Tabla"',      '"Table"'),
    ('"Figura"',     '"Figure"'),
    ('"Quality Gates — Estado de todos los outputs esperados"',
     '"Quality Gates — Status of all expected outputs"'),
    ('"RESUMEN FINAL"',  '"FINAL SUMMARY"'),
    ('"PC Test Inicial:"',  '"Initial CT Test:"'),
    ('"\\nNivel PC por Clase:"',    '"\\nCT Level by Class:"'),
    ('"\\nHistoria (muestras independientes):"',
     '"\\nHistory (independent samples):"'),
    ('"  Ganancia abs. media por clase (pct_fin − pct_ini):"',
     '"  Mean abs. gain by class (pct_fin − pct_ini):"'),
    ('"  Hake grupal global      : g={global_hake_qg:+.3f}"',
     '"  Global group Hake       : g={global_hake_qg:+.3f}"'),
    ('"\\nVotaciones:"',  '"\\nRatings:"'),
    ('"ANOMALÍAS Y DECISIONES METODOLÓGICAS REGISTRADAS"',
     '"ANOMALIES AND METHODOLOGICAL DECISIONS RECORDED"'),
    ('"  Ver log completo en: {log_path.resolve()}"',
     '"  See full log in: {log_path.resolve()}"'),
    ('"MWU+bootstrap; sin conclusiones fuertes"',
     '"MWU+bootstrap; no strong conclusions"'),
    ('"test automático"',    '"automatic test"'),
    ('"Autopercepción: SIN ID común → solo análisis agregado por grupo"',
     '"Self-perception: NO common ID → aggregate group analysis only"'),
    ('"Nivel PC: terciles sobre media de clase " +',
     '"CT level: tertiles on class mean " +'),
    ('"(ranking denso, pocas clases)"',  '"(dense ranking, few classes)"'),
    ('"Historia: TOTAL recalculado donde discrepante"',
     '"History: TOTAL recalculated where discrepant"'),
    ('"Historia: nivel_pc=NaN para clases fuera de Echegaray"',
     '"History: ct_level=NaN for classes outside Echegaray"'),
    ('"Votaciones: valores fuera [0,10] → NaN"',
     '"Ratings: values outside [0,10] → NaN"'),
    ('"  ✓ TODOS LOS OUTPUTS VERIFICADOS CORRECTAMENTE"',
     '"  ✓ ALL OUTPUTS VERIFIED CORRECTLY"'),
    ('"  [!] ALGUNOS OUTPUTS NO ENCONTRADOS (ver detalle arriba)"',
     '"  [!] SOME OUTPUTS NOT FOUND (see details above)"'),
    ('print(f"\\nLog completo: {log_path.resolve()}")',
     'print(f"\\nFull log: {log_path.resolve()}")'),
    # final prints in summary
    ('f"  N total PC              : {n_pc_total}"',
     'f"  Total N CT              : {n_pc_total}"'),
    ('f"  Género Chico            : {n_chico}"',
     'f"  Gender Boy              : {n_chico}"'),
    ('f"  Género Chica            : {n_chica}"',
     'f"  Gender Girl             : {n_chica}"'),
    ('f"  NEE = Sí                : {n_nee_si_final}"',
     'f"  SEN = Yes              : {n_nee_si_final}"'),
    ('f"  NEE = No                : {n_nee_no_final}"',
     'f"  SEN = No               : {n_nee_no_final}"'),
    ('f"  N Inicial               : {len(df_ini)}"',
     'f"  N Initial              : {len(df_ini)}"'),
    ('f"  N Final                 : {len(df_fin)}"',
     'f"  N Final               : {len(df_fin)}"'),
    ('f"  % missing global        : {pct_miss_tot:.1f}%"',
     'f"  % global missing       : {pct_miss_tot:.1f}%"'),
    ('f"  N registros             : {len(df_votes)}"',
     'f"  N records              : {len(df_votes)}"'),

    # ── Categorical value runtime references ─────────────────────
    ('niv_order = ["Bajo", "Medio", "Alto"]',  'niv_order = ["Low", "Medium", "High"]'),
    ('group_labels=["Chico", "Chica"])',         'group_labels=["Boy", "Girl"])'),
    ('df_pc["Género"] == "Chico")',              'df_pc["Género"] == "Boy")'),
    ('df_pc["Género"] == "Chica")',              'df_pc["Género"] == "Girl")'),
    ('df_pc["NEE"] == "Sí")',                    'df_pc["NEE"] == "Yes")'),
    ('group_labels=["Sí", "No"])',               'group_labels=["Yes", "No"])'),
    # Also filter expressions with .sum()
    ('== "Chico").sum()',   '== "Boy").sum()'),
    ('== "Chica").sum()',   '== "Girl").sum()'),
    ('== "Sí").sum()',      '== "Yes").sum()'),
    # QQ-plot loop literals
    ('for gen in zip(axes, ["Chico", "Chica"])',  'for gen in zip(axes, ["Boy", "Girl"])'),
    ('for nee_val in zip(axes, ["Sí", "No"])',    'for nee_val in zip(axes, ["Yes", "No"])'),
    # actual patterns from code
    ('for ax, gen in zip(axes, ["Chico", "Chica"])', 'for ax, gen in zip(axes, ["Boy", "Girl"])'),
    ('for ax, nee_val in zip(axes, ["Sí", "No"])',   'for ax, nee_val in zip(axes, ["Yes", "No"])'),
    # OLS numeric mapping
    ('{"Bajo": 0, "Medio": 1, "Alto": 2}',        '{"Low": 0, "Medium": 1, "High": 2}'),

    # ── Generic remaining Spanish ─────────────────────────────────
    ('"Figura guardada:', '"Figure saved:'),
    ('"figura guardada:', '"figure saved:'),
    ('"Exportado →',     '"Exported →'),
    ('"exportado →',     '"exported →'),
    # Misc axis labels
    ('"% acierto"',      '"% correct"'),
    ('"% aciertos"',     '"% correct"'),
    ('ylabel("% aciertos")', 'ylabel("% correct")'),
    ('ylabel("% acierto")',  'ylabel("% correct")'),
    ('"Puntuación normalizada"', '"Normalised score"'),
    ('"Frecuencia"',     '"Frequency"'),
    # Spanish strings that appear in prints
    ('print("\\n[!] Comparación agregada por grupo, NO individual")',
     'print("\\n[!] Aggregate comparison by group, NOT individual")'),
    ('"Formato detectado"',  '"Detected format"'),
]

# ─────────────────────────────────────────────────────────────────
# 3. Apply translations
# ─────────────────────────────────────────────────────────────────
for cell in nb["cells"]:
    cell_id = cell.get("id", "")
    src = cell["source"]
    joined = "".join(src) if isinstance(src, list) else src

    if cell["cell_type"] == "markdown":
        if cell_id in MD_BY_ID:
            new_src = MD_BY_ID[cell_id]
            cell["source"] = new_src.splitlines(keepends=True)
        # else leave as is

    elif cell["cell_type"] == "code":
        for old, new in CODE_SUBS:
            joined = joined.replace(old, new)
        cell["source"] = joined.splitlines(keepends=True)

# ─────────────────────────────────────────────────────────────────
# 4. Update notebook metadata title
# ─────────────────────────────────────────────────────────────────
nb.setdefault("metadata", {})["title"] = "PC History Analysis (English)"

# ─────────────────────────────────────────────────────────────────
# 5. Write output
# ─────────────────────────────────────────────────────────────────
with open(DEST, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"✓  Written: {DEST}")
print(f"   Markdown cells translated: {sum(1 for c in nb['cells'] if c['cell_type'] == 'markdown')}")
print(f"   Code cells processed:      {sum(1 for c in nb['cells'] if c['cell_type'] == 'code')}")
