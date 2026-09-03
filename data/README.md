# Dataset files

| Path | Purpose |
|---|---|
| [splits/](splits/README.md) | Four included process-data CSVs covering all 100 batches. |
| [splits/manifest.json](splits/manifest.json) | Exact column names, batch IDs, row counts and file checksums. |
| [raw/](raw/README.md) | Location for the optional original full CSV downloaded from IndPenSim. |

## Which notebook reads which data?

| Notebook | Accepted input |
|---|---|
| [main.ipynb](../notebooks/main.ipynb) | The included directory containing all four split CSVs, or the original full CSV. |
| [baseline.ipynb](../notebooks/baseline.ipynb) | The original concatenated IndPenSim CSV in batch order. It does not directly accept the four-file split directory. |

For a local Main ML run, set DATA_PATH in the notebook's path cell to:

~~~python
DATA_PATH = str(PROJECT_ROOT / "data" / "splits")
~~~

For Colab, place all four files in one folder and use that folder's actual path. The notebooks' calculation code has not been changed.

The split CSVs are model inputs, not prediction outputs. They preserve the process-variable exports with Batch_ID and Data_Split. They are not a reconstruction of the full 2,239-column raw file: Raman spectra are absent.

Source and redistribution terms: [DATA_SOURCES.md](../DATA_SOURCES.md). Run instructions: [REPRODUCIBILITY.md](../docs/REPRODUCIBILITY.md).
