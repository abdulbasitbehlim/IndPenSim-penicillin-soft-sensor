# Running and checking the notebooks

## Choose the notebook and input

| Notebook | Study | Input |
|---|---|---|
| [main.ipynb](../notebooks/main.ipynb) | Main ML fault-aware comparison | The included [four split CSVs](../data/splits/README.md), or the original full CSV. |
| [baseline.ipynb](../notebooks/baseline.ipynb) | Baseline ML model selection and five experiments | The original concatenated CSV downloaded from the [IndPenSim record](https://doi.org/10.17632/pdnjz7zz5x.1), in original batch order. |

The earlier Baseline ML outputs are preserved in [results/baseline_earlier/](../results/baseline_earlier/README.md); a separate notebook for that earlier run was not supplied.

## Local Jupyter

Use a separate Python 3.12 environment for each notebook. From the repository root, create and activate an environment, install the selected requirements, then open Jupyter:

~~~bash
python -m venv .venv-main
~~~

On macOS/Linux, activate it with:

~~~bash
source .venv-main/bin/activate
~~~

On Windows PowerShell, activate it with:

~~~powershell
.venv-main\Scripts\Activate.ps1
~~~

Then run:

~~~bash
python -m pip install -r requirements/main.txt
python -m pip install "jupyterlab>=4,<5"
python -m jupyterlab notebooks/main.ipynb
~~~

In main.ipynb's path-setting cell, replace the DATA_PATH assignment with:

~~~python
DATA_PATH = str(PROJECT_ROOT / "data" / "splits")
~~~

Use RUN_MODE = "full" for all five normal folds and ten fault-batch holdouts. Smoke mode is only an installation check.

For the earlier study, create a separate environment, install [requirements/baseline.txt](../requirements/baseline.txt), open baseline.ipynb, and set DATA_PATH to the original full CSV. Do not install both requirement sets into the same environment.

## Google Colab

Open the chosen notebook in a fresh Colab session. Set the data path to the actual CSV or, for Main ML, to a folder containing all four included split CSVs. Google Drive mounting is optional. If package installation requests a runtime restart, restart before executing from the beginning.

## Outputs and recorded environments

New runs write to fresh folders under outputs/baseline/ or outputs/main/. Keep these separate from the archived [results/](../results/README.md). The notebooks save the numerical tables, plots, metadata and trained model.

The saved Main ML metadata records Python 3.13.15 and its scientific package versions. The baseline run recorded NumPy 2.1.3, pandas 2.2.3 and scikit-learn 1.6.1, but not a complete historical environment lock. The separate requirements files support reproduction; exact agreement must be checked after running.

## Evaluation boundaries

- The four included CSVs preserve the old 60/15/15/10 split. Main ML recombines them and creates its own complete-batch folds.
- Main ML tests normal batches in five folds and fault batches one at a time, learning from the other nine fault batches. This is not verified leave-one-fault-mechanism-out testing.
- The earlier repeated CV is five repeats of five normal folds, not 25 independent datasets.
- The earlier RF test and Main ML's HGB comparison use different training/evaluation designs. Compare methods within the same experiment.
- Adding fault examples and increasing their weight occur together in Main ML. The current comparison does not isolate the contribution of each change.
- The final model is refitted on all 100 labelled batches after evaluation. Its deployment diagnostics are not another held-out test.

## Automated checks

~~~bash
python -m unittest discover -s tests -v
~~~

The checks verify preserved notebook calculations, CSV integrity, split membership, agreement between input targets and held-out predictions, metric arithmetic, figure files and documentation links. They require no model training or external download.

The scientific notebook code and original result values remain unchanged by repository organisation. Machine-readable verification records are indexed in [docs/README.md](README.md). Passing checks confirm repository consistency, not publication readiness or independent scientific validation.
