# Process-data split CSVs

These four files are unmodified exports from the earlier batch-wise split. The two Baseline ML result archives contain byte-identical copies, so they are stored once here.

| File | Rows | Batches | Original purpose |
|---|---:|---:|---|
| [train_normal_60_batches.csv](train_normal_60_batches.csv) | 67,820 | 60 | Fits the initial normal-operation models. |
| [validation_normal_15_batches.csv](validation_normal_15_batches.csv) | 17,510 | 15 | Compares candidate models before final testing. |
| [test_normal_15_batches.csv](test_normal_15_batches.csv) | 17,080 | 15 | Tests the selected baseline on unseen normal batches. |
| [test_fault_10_batches.csv](test_fault_10_batches.csv) | 11,525 | 10 | Tests the selected baseline on fault batches 91–100. |
| [manifest.json](manifest.json) | — | — | Lists the 41 column names, exact batch membership, source archives and checksums. |

The files cover 113,935 observations from 100 batches without overlap between the four batch groups. Each normal group is balanced across recipe, operator and APC regimes.

The target is Penicillin concentration(P:g/L). Batch_ID identifies the reconstructed complete batch; Data_Split records the original group. Fault reference and Fault flag remain diagnostic columns, not direct concentration-prediction inputs.

These are process-only exports, not the original full Raman dataset. In Main ML, all four files are combined before creating five normal folds and ten leave-one-fault-batch-out evaluations. Their old train/validation/test labels do not determine Main ML's folds.

[Input compatibility](../README.md) · [Dataset source and CC BY 4.0 licence](../../DATA_SOURCES.md)
