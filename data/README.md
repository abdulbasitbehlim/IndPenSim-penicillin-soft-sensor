# Obtaining and locating the data

Download `100_Batches_IndPenSim_V3.csv` from the [original IndPenSim record](https://doi.org/10.17632/pdnjz7zz5x.1). Extract the dataset archive before use. Neither notebook reads the dataset directly from a ZIP.

## Local computer

Place the raw CSV at:

```text
data/raw/100_Batches_IndPenSim_V3.csv
```

Run Jupyter from the repository root or its `notebooks/` directory. The path cells then find the default location. If your file lives elsewhere, set `DATA_PATH` to its full path. Windows users can use a raw string, for example:

```python
DATA_PATH = r"C:\Research\IndPenSim\100_Batches_IndPenSim_V3.csv"
```

The earlier `baseline.ipynb` expects the original concatenated CSV in original batch order, not a shuffled table. It reconstructs batch IDs from time resets.

## Four existing process-data files: `main.ipynb` only

`main.ipynb` also accepts a directory containing **all four** exports from the earlier notebook:

- `train_normal_60_batches.csv`
- `validation_normal_15_batches.csv`
- `test_normal_15_batches.csv`
- `test_fault_10_batches.csv`

Place them in `data/splits/` and set:

```python
DATA_PATH = str(PROJECT_ROOT / "data" / "splits")
```

`main.ipynb` combines them, preserves verified `Batch_ID` values and constructs its own outer evaluation. Their old train/validation/test names do not determine the `main.ipynb` folds. Do not rename arbitrary CSVs to imitate these files.

## Google Colab

The default example path is:

```python
DATA_PATH = "/content/drive/MyDrive/IndPenSim_Data/100_Batches_IndPenSim_V3.csv"
```

Use your own file's actual path. If you set `MOUNT_GOOGLE_DRIVE = False`, choose a CSV in Colab session storage instead. No Google password, access token or private share link belongs in a notebook.

## Keep data and generated files out of ordinary commits

The source dataset remains separately licensed; see [DATA_SOURCES.md](../DATA_SOURCES.md). Raw files and newly generated outputs are ignored by local Git. Keep credentials and private data out of the repository. Completed runs should be reviewed before selecting outputs for the research archive.

The checked-in `results/main/cross_validated_predictions.csv` contains derived evaluation rows from simulated data. It is not a copy of the full raw process/Raman dataset.
