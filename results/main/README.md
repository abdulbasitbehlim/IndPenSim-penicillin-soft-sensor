# ML4 — fault-aware soft sensor results

Saved outputs of the full ML4 run: five normal-batch folds and ten leave-one-fault-batch-out evaluations. Source notebook: [main.ipynb](../../notebooks/main.ipynb).

| File | Purpose |
|---|---|
| [cross_validated_overall_metrics.csv](cross_validated_overall_metrics.csv) | Pooled MAE, RMSE and R² for normal-only and fault-aware HGB on normal and fault batches. |
| [cross_validated_batch_metrics.csv](cross_validated_batch_metrics.csv) | MAE, RMSE and R² for each batch and each model. |
| [cross_validated_predictions.csv](cross_validated_predictions.csv) | Actual concentration, both predictions, fault phase, warning score and fold for all 113,935 held-out rows. |
| [paired_batch_bootstrap.csv](paired_batch_bootstrap.csv) | Paired batch-RMSE differences and descriptive bootstrap intervals. |
| [fault_risk_summary.csv](fault_risk_summary.csv) | Held-out normal warning rate, fault-affected sensitivity, pre-onset warning rate and fault-phase AUC. |
| [deployment_reliability_by_batch.csv](deployment_reliability_by_batch.csv) | Fault-risk and OOD diagnostics from the final refitted bundle; not an independent test. |
| [run_metadata.json](run_metadata.json) | Model settings, feature names, completed folds, interval radii and recorded software versions. |
| [RESULTS_SUMMARY.txt](RESULTS_SUMMARY.txt) | Original automatically saved text summary of the run. |
| [figure_1_rmse_comparison.png](figure_1_rmse_comparison.png) | Grouped bar chart comparing pooled normal and fault RMSE. |
| [figure_2_fault_batch_rmse.png](figure_2_fault_batch_rmse.png) | Grouped bar chart comparing the two models for each fault batch. |
| [figure_3_fault_actual_vs_predicted.png](figure_3_fault_actual_vs_predicted.png) | Scatter plots comparing actual and predicted fault-batch concentrations. |
| [figure_4_fault_risk_by_phase.png](figure_4_fault_risk_by_phase.png) | Box plots showing warning scores before and after fault onset and during normal operation. |
| [batch_100_held_out_trajectory.png](batch_100_held_out_trajectory.png) | Time-series plot showing the remaining prediction difficulty in batch 100. |

[Annotated figures](../../docs/figures/FAULT_INCLUSIVE.md) · [Results interpretation](../../docs/RESULTS_GUIDE.md)
