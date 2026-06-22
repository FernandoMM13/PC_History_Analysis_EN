# PC History Analysis — Reproduction Package

Statistical analysis notebook for initial and final test performance of 5th Grade Primary students at **Pedro Duque** and **Juan Echegaray** schools, together with ratings of activities carried out during the intervention.

---

## Project Structure

```
Analysis_PC_History/
├── PC_History_Analysis_EN.ipynb    # Main analysis notebook (English)
├── analisis_completo_PC_Historia.ipynb  # Original notebook (Spanish)
├── requirements.txt                # Python dependencies
├── data/
│   └── Test_iniciales_v_finales.xlsx   # Source data (do not modify)
└── outputs/
    ├── figures/en/             # Exported charts — English version (PNG)
    ├── figures/                # Exported charts — Spanish version (PNG)
    ├── tables/                 # Exported tables (CSV)
    └── logs/                   # Execution log of the pipeline
```

---

## Prerequisites

| Requirement | Minimum version | Notes |
|---|---|---|
| Python | 3.10 or higher | Tested with Python 3.14.2 |
| pip | bundled with Python | — |
| Git (optional) | any | Only if cloning from a repository |

> **Windows:** Download Python from [python.org](https://www.python.org/downloads/). During installation, tick **"Add Python to PATH"**.  
> **macOS/Linux:** Use the system package manager (`brew install python` / `apt install python3`).

---

## Step-by-step Installation

### 1. Download or unzip the package

Place the `Analysis_PC_History` folder wherever you like. All steps below are run from inside that folder.

### 2. Open a terminal in the project folder

- **Windows:** Press `Shift + right-click` on the folder → *Open PowerShell window here*  
  (or type `cmd` in the address bar of File Explorer).
- **macOS/Linux:** Open Terminal and navigate with `cd /path/to/Analysis_PC_History`.

### 3. Create the virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

| System | Command |
|---|---|
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (CMD) | `.venv\Scripts\activate.bat` |
| macOS / Linux | `source .venv/bin/activate` |

Once activated, you will see `(.venv)` at the start of the command line.

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

Installation takes between 1 and 5 minutes depending on connection speed.

### 6. Register the environment in Jupyter

```bash
python -m ipykernel install --user --name pc_analysis_venv --display-name "Python (PC Analysis)"
```

---

## Running the Analysis

### Option A — Jupyter Notebook (recommended)

```bash
jupyter notebook PC_History_Analysis_EN.ipynb
```

The browser will open automatically. Inside the notebook:

1. Select the **"Python (PC Analysis)"** kernel (*Kernel → Change kernel* if it does not appear).
2. Run all cells in order: menu *Cell → Run All* (or `Ctrl+Shift+Enter` cell by cell).
3. When finished, results appear in the `outputs/` folder.

### Option B — VS Code

1. Open VS Code in the project folder.
2. Install the **Python** and **Jupyter** extensions if you haven't already.
3. Open `PC_History_Analysis_EN.ipynb`.
4. Select the **"Python (PC Analysis)"** kernel in the top-right corner.
5. Press *Run All* (▶▶) in the notebook toolbar.

### Option C — Terminal execution (no GUI)

```bash
jupyter nbconvert --to notebook --execute PC_History_Analysis_EN.ipynb --output PC_History_Analysis_EN_executed.ipynb
```

---

## Expected Results

After running the complete notebook you will find:

| File | Description |
|---|---|
| `outputs/tables/pc_limpio_por_alumno.csv` | Cleaned CT data per student |
| `outputs/tables/historia_hake_por_clase.csv` | Group Hake gain per class |
| `outputs/tables/historia_efectos.csv` | Effect sizes — History (Cohen's d) |
| `outputs/tables/votaciones_ranking_actividades.csv` | Activity ranking by mean satisfaction |
| `outputs/figures/en/*.png` | All charts in English (histograms, heatmaps, boxplots, forest plots) |
| `outputs/logs/data_quality.log` | Full execution log with timestamps |

The last cell of the notebook (**Quality Gates**) runs an automatic verification and shows `✅ PASS` or `❌ FAIL` for each expected file and condition.

---

## Notebook Sections

| Section | Content |
|---|---|
| 0 · Setup | Imports, logger, paths, constants and utility functions |
| 1 · Loading & Audit | Robust loading of all datasets; data-quality audit table exported |
| 2 · CT Test: Format + Correct Answers | Automatic format detection; score per student, task and concept |
| 3 · CT Descriptives | Global and group distribution; items × class heatmap; barplots by concept |
| 4 · CT Contrasts | Significant differences by Gender and SEN; automatic methodological decision |
| 5 · Self-Perception | Self-perception vs. actual performance at aggregate group level |
| 6 · CT Level by Class | Tertile classification (Low/Medium/High) as moderating variable |
| 7 · History | Pre-post analysis (independent samples); group Hake gain; ANOVA; OLS model |
| 8 · Ratings | Activity satisfaction × CT level; ranking; rating–gain correlation |
| 9 · Methodological Reflection | The five pillars of CT applied to the analysis pipeline |
| 10 · Quality Gates | Automatic verification of all outputs and data invariants |

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'X'`**  
The virtual environment is not activated or dependencies were not installed.  
→ Activate `.venv` and run `pip install -r requirements.txt` again.

**The "Python (PC Analysis)" kernel does not appear in Jupyter**  
→ Run step 6 of the installation (`ipykernel install`), restart Jupyter and refresh the page.

**`ValueError: assignment destination is read-only`**  
This error was corrected in the notebook itself (pandas ≥ 3 compatibility). Make sure you are using the file version included in this package.

**Charts are not displayed**  
→ Check that `matplotlib` and `seaborn` were installed correctly (`pip show matplotlib seaborn`).

**PowerShell blocks virtual environment activation (Windows)**  
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Data and Privacy

The file `data/Test_iniciales_v_finales.xlsx` contains anonymised academic performance data (no names or ID numbers). It must not be distributed outside the research team.

---

## Main Dependencies

| Package | Tested version | Use |
|---|---|---|
| pandas | 3.0.2 | Data manipulation |
| numpy | 2.4.4 | Numerical computation |
| scipy | 1.17.1 | Statistical tests |
| statsmodels | 0.14.6 | ANOVA, Tukey HSD |
| pingouin | 0.6.1 | Cohen's d, rank-biserial |
| seaborn | 0.13.2 | Visualisation |
| matplotlib | — | Base charts |
| openpyxl | — | Excel read/write |
