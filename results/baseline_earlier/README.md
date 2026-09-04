# Baseline ML — earlier saved run

These are the original outputs from the earlier Baseline ML run. They are kept separate from the results associated with the current baseline notebook. A separate notebook for this earlier run was not supplied.

| File | Purpose |
|---|---|
| [validation_results.csv](validation_results.csv) | Validation MAE, RMSE and R² used to compare the candidate models. |
| [normal_and_fault_test_results.csv](normal_and_fault_test_results.csv) | Selected Random Forest's overall normal-test and fault-test metrics. |
| [normal_test_metrics_by_batch.csv](normal_test_metrics_by_batch.csv) | Prediction errors for each of the 15 normal test batches. |
| [fault_test_metrics_by_batch.csv](fault_test_metrics_by_batch.csv) | Prediction errors for each of the ten fault test batches. |
| [normal_test_predictions.csv](normal_test_predictions.csv) | Actual and predicted concentrations for the normal test rows. |
| [fault_test_predictions.csv](fault_test_predictions.csv) | Actual and predicted concentrations plus fault diagnostics for the fault test rows. |
| [Batch split definitions (JSON)](fault_aware_batch_split.json) | Batch-ID lists for the four original data groups. |
| [Batch split audit (CSV)](fault_aware_batch_split_table.csv) | Batch-by-batch split assignment and audit information. |
| [row_split_summary.csv](row_split_summary.csv) | Number of rows assigned to each of the four data groups. |
| [model_information.json](model_information.json) | Selected model, feature list, random seed, batch lists and final summary metrics. |

The shared input exports are in [data/splits/](../../data/splits/README.md). Both Baseline ML runs use identical split exports; minor numerical differences between their saved outputs do not represent a new dataset.

[Current Baseline ML results](../baseline/README.md) · [All result folders](../README.md)
