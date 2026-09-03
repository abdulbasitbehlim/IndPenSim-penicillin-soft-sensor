# Saved result files

| Folder | Run | Purpose |
|---|---|---|
| [ml2/](ml2/README.md) | Earlier ML2 baseline | Original baseline tables and predictions from the earlier run. |
| [baseline/](baseline/README.md) | ML3 baseline | Model selection, normal/fault test results, predictions and baseline figures. |
| [experiments/](experiments/README.md) | ML3 extensions | All five diagnostic experiments, including detailed row-level outputs. |
| [main/](main/README.md) | Full ML4 run | Fault-aware model comparison, complete-batch results, reliability diagnostics and figures. |

Each folder's README lists every result file and its purpose. Shared input CSVs are stored once in [data/splits/](../data/splits/README.md).

ML2 and ML3 are separate saved runs, not independent datasets; their shared split exports are identical. Existing result values are preserved rather than overwritten with values from a different run.

[All output figures](../docs/FIGURES.md) · [Interpretation and limitations](../docs/RESULTS_GUIDE.md)

Duplicate ZIPs and trained joblib binaries are not included in the result folders. The notebooks regenerate trained models; the large original Random Forest binary exceeds the normal GitHub file limit. Source-data attribution is in [DATA_SOURCES.md](../DATA_SOURCES.md).
