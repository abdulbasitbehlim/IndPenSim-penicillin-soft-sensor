# ML2 — earlier baseline run

These are the original outputs supplied in the ML2 results archive. They are kept separate from the later ML3 baseline outputs. A separate ML2 notebook is not included in this repository.

| File | Purpose |
|---|---|
| [validation_results.csv](validation_results.csv) | Validation MAE, RMSE and R² used to compare the candidate models. |
| [normal_and_fault_test_results.csv](normal_and_fault_test_results.csv) | Selected Random Forest's overall normal-test and fault-test metrics. |
| [normal_test_metrics_by_batch.csv](normal_test_metrics_by_batch.csv) | Prediction errors for each of the 15 normal test batches. |
| [fault_test_metrics_by_batch.csv](fault_test_metrics_by_batch.csv) | Prediction errors for each of the ten fault test batches. |
| [normal_test_predictions.csv](normal_test_predictions.csv) | Actual and predicted concentrations for the normal test rows. |
| [fault_test_predictions.csv](fault_test_predictions.csv) | Actual and predicted concentrations plus fault diagnostics for the fault test rows. |
| [fault_aware_batch_split.json](fault_aware_batch_split.json) | Batch-ID lists for the four original data groups. |
| [fault_aware_batch_split_table.csv](fault_aware_batch_split_table.csv) | Batch-by-batch split assignment and audit information. |
| [row_split_summary.csv](row_split_summary.csv) | Number of rows assigned to each of the four data groups. |
| [model_information.json](model_information.json) | Selected model, feature list, random seed, batch lists and final summary metrics. |

The shared input exports are in [data/splits/](../../data/splits/README.md). The ML2 and ML3 splits are identical; minor numerical differences between their saved outputs do not represent a new dataset.

[Later baseline results](../baseline/README.md) · [All result folders](../README.md)
