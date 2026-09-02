# IndPenSim Penicillin Soft Sensor

This repository contains two stages of a study of penicillin-concentration estimation in simulated fermentation. The first notebook establishes a normal-trained baseline and investigates where it fails. The second tests whether including other fault-affected batches during training improves predictions for a held-out batch.

The target is **current penicillin concentration in g/L**, not a future concentration forecast. This is an exploratory soft-sensor study using IndPenSim, not a validated plant-control system or a complete digital twin.

Suggested GitHub repository name: **`penicillin-soft-sensor`**. Start with **`notebooks/main.ipynb`** for the final study. For upload decisions, see [UPLOAD_CHECKLIST.md](UPLOAD_CHECKLIST.md).

## Which notebook should I open?

| Notebook | Purpose | What it contains |
|---|---|---|
| [notebooks/baseline.ipynb](notebooks/baseline.ipynb) | Original study | Linear Regression, Random Forest and a median baseline; selection of Random Forest; five follow-up experiments |
| [notebooks/main.ipynb](notebooks/main.ipynb) | Final fault-inclusive study | Normal-only versus fault-inclusive HistGradientBoosting; batch-held-out evaluation; a separate risk classifier, OOD scoring and empirical prediction ranges |

**`main.ipynb` is self-contained. You do not need to run `baseline.ipynb` first.** Use separate fresh environments for the two notebooks because their recorded NumPy and scikit-learn versions differ.

The repository copies have cleared outputs and portable setup cells. The scientific code is unchanged; setup adaptations are documented in [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md). Completed-run CSVs and figures are in `results/`. Running a notebook writes to a new timestamped location, not over those archived results.

## Dataset

The source is the [public IndPenSim dataset, version 1](https://doi.org/10.17632/pdnjz7zz5x.1), created by Stephen Goldrick. These are simulated industrial-scale fermentation trajectories, not experiments newly conducted by this repository's author.

| Item | Study data |
|---|---|
| Original CSV | `100_Batches_IndPenSim_V3.csv` |
| Batches / observations | 100 / 113,935 |
| Normal operating groups | Batches 1–30: recipe; 31–60: operator; 61–90: advanced process control |
| Documented deviation group | Batches 91–100 |
| Original columns | 39 process/metadata columns and 2,200 Raman columns |
| Inputs used in the final regressor | 36: 20 current/base, 15 history-based and one cumulative-feed input |
| Risk / OOD inputs in `main.ipynb` | 34; time and cumulative feed are omitted |
| Raman spectra | Not used |

Raw data are **not bundled**. Download them from the original record and follow [data/README.md](data/README.md). Dataset attribution and licensing are in [DATA_SOURCES.md](DATA_SOURCES.md).

History features use only current and preceding input measurements within a batch. No lagged penicillin target is used. Cumulative feed is in **litres of feed**, not sugar mass. The 36 exact names are preserved in [run_metadata.json](results/ml4/run_metadata.json).

## What the two studies test

### 1. Normal-trained models and five diagnostic experiments

The initial split used 60 normal training batches, 15 normal validation batches, 15 normal test batches and all ten fault batches as a separate stress test. Random Forest was selected by validation RMSE and refitted on the 75 normal development batches.

| Initial validation model | MAE (g/L) | RMSE (g/L) | R² |
|---|---:|---:|---:|
| Median baseline | 8.851 | 10.175 | approximately 0 |
| Linear Regression | 1.817 | 2.539 | 0.938 |
| Random Forest | 1.228 | 2.034 | 0.960 |

The selected Random Forest had normal-test RMSE **2.181 g/L** and fault-test RMSE **4.321 g/L**. The five additional experiments examined:

1. **Repeated complete-batch validation:** five folds repeated five times, giving 25 normal-batch evaluations. Mean RF RMSE was 2.050 g/L, with SD 0.286 g/L. The same 90 batches are reused; these are not 25 independent datasets.
2. **Time/feed ablation:** removing both variables increased normal RMSE by 11.53% and fault RMSE by 2.44%, relative to that experiment's all-input refit. Performance did not collapse.
3. **Fault-phase analysis:** errors increased within and after the recorded fault window. The plotted equal-batch mean MAEs differ from pooled row MAEs; see [the results guide](docs/RESULTS_GUIDE.md).
4. **A stronger comparator:** normal-trained HGB also had larger fault than normal errors. The difficulty was not confined to Random Forest.
5. **Early OOD and uncertainty:** at 24 h, the earlier detector flagged 6/10 fault batches and 2/15 normal-test batches. Ranges targeting 90% coverage achieved 84.89% normal and 70.41% fault row coverage.

The fixed-split and experiment results are in [results/baseline](results/baseline/) and [results/experiments](results/experiments/). They are development evidence, not independent confirmations of the later `main.ipynb` comparison.

### 2. Fault-inclusive HGB: the primary comparison

Both regressors use the same feature definitions and HGB settings. Training gives each batch equal total weight before a multiplier of three is applied to fault-development batches. The fault-inclusive model receives other fault examples; it does not see the batch being tested.

| Evaluation | Normal-only training | Fault-inclusive training | Held-out test |
|---|---|---|---|
| Five normal folds | 72 normal batches | Same 72 normal + all 10 fault batches | 18 normal batches per fold; six per regime |
| Ten fault folds | All 90 normal batches | Same 90 normal + the other nine fault batches | One complete fault batch per fold |

| Held-out group | Training strategy | MAE (g/L) | RMSE (g/L) | R² |
|---|---|---:|---:|---:|
| Normal | Normal-only HGB | 1.2095 | 1.9806 | 0.9607 |
| Normal | Fault-inclusive HGB | 1.2063 | 1.9830 | 0.9606 |
| Fault | Normal-only HGB | 2.0763 | 3.1946 | 0.8580 |
| Fault | Fault-inclusive HGB | 1.4405 | 2.5644 | 0.9085 |

Source: [cross_validated_overall_metrics.csv](results/ml4/cross_validated_overall_metrics.csv). The saved code calls the second strategy **“Fault-aware HGB”**; “fault-inclusive” describes the training change more precisely.

Fault RMSE decreased by **19.73%**, while normal RMSE changed little. Eight of ten fault batches improved in RMSE. **Batch 100 remained a failure:** fault-inclusive RMSE was 6.631 g/L and R² was −2.4837. Holding out a batch does not establish generalisation to a fault mechanism absent from training.

![Pooled held-out normal and fault RMSE for the two HGB training strategies](results/ml4/figure_1_rmse_comparison.png)

*Pooled RMSE, not a mean across independent training repetitions. Shorter bars mean smaller error.*

![Held-out RMSE for every fault batch](results/ml4/figure_2_fault_batch_rmse.png)

*Per-batch results retain adverse outcomes, including batches 92 and 93 that worsened and batch 100 that remained difficult.*

The risk classifier and OOD detector provide **separate warnings**. They do not change the concentration point prediction and do not prove a physical fault. The empirical ranges are not guaranteed 90% confidence intervals. See [docs/RESULTS_GUIDE.md](docs/RESULTS_GUIDE.md) before interpreting them.

## Run in Google Colab

1. Put the downloaded CSV in your own Drive, for example `MyDrive/IndPenSim_Data/100_Batches_IndPenSim_V3.csv`.
2. Open [Google Colab](https://colab.research.google.com/), choose **File → Upload notebook**, and select either notebook from `notebooks/`. After publishing this repository, Colab can also open it through its GitHub tab.
3. Start a fresh CPU session. Run the setup cell; it installs the notebook's own dependency versions in Colab. Restart the session if instructed, then rerun from the start.
4. Run the optional Drive connection and set `DATA_PATH` in the path cell. No credentials belong in the code.
5. For `main.ipynb`, try `RUN_MODE = "smoke"` to check installation, then use `"full"` for the planned evaluation. Smoke mode uses one normal fold, fault batch 91 and 50 boosting iterations. It is not a research result.
6. Run the remaining cells in order. `main.ipynb` full mode uses five normal folds, ten fault folds and 180 iterations. Keep the fault multiplier at 3.0 to reproduce the recorded configuration.
7. Review and save the new result directory. `main.ipynb` can create a result ZIP; automatic download is optional.

The setup defaults to ordinary example Drive paths, not the original author's personal folders. If using session storage instead, set `MOUNT_GOOGLE_DRIVE = False` and change `DATA_PATH` to the uploaded file. Session storage can disappear when the runtime ends.

## Run in local Jupyter

Use **Python 3.12** and open a terminal in the repository root. Create a separate environment for each notebook. Do not install both scientific requirement files into one environment.

### Final `main.ipynb` notebook

```bash
python -m venv .venv-main
```

Activate it on Windows PowerShell:

```powershell
.\.venv-main\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv-main/bin/activate
```

Then install and launch:

```bash
python -m pip install -r requirements.txt
python -m pip install "jupyterlab>=4,<5"
python -m jupyterlab notebooks/main.ipynb
```

Place the raw CSV in `data/raw/`. `main.ipynb` can alternatively read the directory of the four process-split CSVs; set `DATA_PATH` to that directory as explained in [data/README.md](data/README.md).

### Earlier baseline notebook

Start another terminal, create and activate `.venv-baseline` in the same way, then run:

```bash
python -m pip install -r requirements/baseline.txt
python -m pip install "jupyterlab>=4,<5"
python -m jupyterlab notebooks/baseline.ipynb
```

The local setup cell checks versions but does not automatically install packages. Drive is skipped locally. Paths default to the repository's `data/raw/` and `outputs/` folders when Jupyter starts in the root or `notebooks/` directory. An explicit path always takes precedence.

New outputs are written to `outputs/baseline/<timestamp>/` or `outputs/main/<mode>_<timestamp>/`. Those generated directories are ignored by Git. Preserve a completed run before deciding which results to add to a release.

## Repository organisation

| Path | Contents |
|---|---|
| `notebooks/` | The two canonical notebooks; scientific code preserved, saved cell outputs cleared |
| `requirements.txt` | Default dependencies for `main.ipynb` |
| `requirements/` | Separate dependency files for the earlier and final studies |
| `data/` | Download/location instructions; no raw data |
| `results/baseline/` | Original split and Random Forest baseline results |
| `results/experiments/` | Five diagnostic experiments, tables and figures |
| `results/ml4/` | Original full-run metrics, 113,935 held-out prediction rows, configuration and figures |
| `docs/` | GitHub upload guide, reproducibility notes, results guide and notebook provenance |
| `tests/` | Lightweight repository checks; no raw-data download or model training |
| `.github/workflows/` | Optional-on-upload GitHub Actions checks on pushes and pull requests |
| `DATA_SOURCES.md` | Dataset/publication attribution and licensing boundaries |
| `CITATION.cff` | Software citation metadata |
| `LICENSE` | MIT licence for original code/documentation; see the exclusions below |

Run the lightweight checks from the root:

```bash
python -m unittest discover -s tests -v
```

They check notebook syntax, preserved scientific-source hashes, clean outputs, result-table arithmetic and held-out prediction membership. **They do not retrain either study** and do not prove absence of data leakage in every future modification.

For upload instructions, see [docs/GITHUB_UPLOAD_GUIDE.md](docs/GITHUB_UPLOAD_GUIDE.md). Extract the supplied ZIP and upload the repository contents, not the ZIP itself.

## Limits and responsible interpretation

- This is a simulation benchmark, not external validation on physical fermentations.
- The benchmark informed development. The final comparison is exploratory, not an untouched confirmatory study.
- `main.ipynb` holds out complete batches, not independently verified fault mechanisms. Inclusion and weighting change together; no isolated weight-multiplier ablation was completed.
- Earlier feature-usability screening was not fully nested inside repeated CV. The 25 earlier scores are dependent and do not prove that a model is unbiased.
- The original RF importance assigned about 92.1% to time and cumulative feed, but ablation did not remove every possible progress proxy or establish causation.
- Fault-phase windows may include inactive gaps. Error after a flag clears is not evidence of recovery.
- The `main.ipynb` risk score is uncalibrated. At 0.5, normal-row warnings were 13.86% and onset/after sensitivity was 49.26%. These are different quantities from pooled R².
- Final-bundle OOD and risk diagnostics are not an additional held-out regression test. Refitting on all 100 batches occurs after evaluation.
- Some raw concentration estimates are negative. They were retained in reported metrics, and the final model remains unconstrained.
- `run_metadata.json` uses `reportable: true` to denote full computational coverage; this is not a certification of publication readiness.

## Citation and licence

Project author: **Abdul Basit Behlim**. This package is prepared as software version **0.1.0**; a public Git tag or release has not been created by this preparation step. Use [CITATION.cff](CITATION.cff), identify the actual commit/release used, and cite the original IndPenSim dataset and publications in [DATA_SOURCES.md](DATA_SOURCES.md). No manuscript DOI is claimed.

Original code and accompanying documentation use the [MIT licence](LICENSE). It permits reuse, modification and distribution, including commercial use, while retaining its copyright and licence notice. The original dataset and derived data retain the applicable **CC BY 4.0** attribution terms; third-party articles and dependencies retain their own licences. Confirm institutional and contributor permissions before making the repository public.

AI tools assisted with code drafting and documentation. The project author is responsible for reviewing the code, results and scientific claims. No publication acceptance or fault-detection guarantee is implied.
