# ML3 — original baseline results

Outputs of the initial normal-trained comparison in [baseline.ipynb](../../notebooks/baseline.ipynb). The notebook compares Linear Regression and Random Forest with a Dummy baseline, selects Random Forest, and tests it on normal and fault batches.

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
| [figures/training_batch_trajectories.png](figures/training_batch_trajectories.png) | Penicillin concentration trajectories from the training batches. |
| [figures/actual_vs_predicted.png](figures/actual_vs_predicted.png) | Scatter plots of actual versus predicted normal and fault concentrations. |
| [figures/feature_importance.png](figures/feature_importance.png) | Random Forest feature-importance bar chart. |

The four input CSVs are in [data/splits/](../../data/splits/README.md). The notebook's five follow-up experiments are in [results/experiments/](../experiments/README.md).

[Annotated baseline figures](../../docs/figures/BASELINE.md) · [Earlier ML2 run](../ml2/README.md)
