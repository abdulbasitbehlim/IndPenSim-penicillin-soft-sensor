# ML3 — five additional experiments

Outputs of the follow-up sections in [baseline.ipynb](../../notebooks/baseline.ipynb). All five experiments and their original plots are retained.

## Experiment 1 — repeated complete-batch cross-validation

| File | Purpose |
|---|---|
| [experiment_1_repeated_batch_cv_fold_metrics.csv](experiment_1_repeated_batch_cv_fold_metrics.csv) | Scores and test-batch IDs for all 25 fold evaluations. |
| [experiment_1_repeated_batch_cv_summary.csv](experiment_1_repeated_batch_cv_summary.csv) | Mean, spread and range of the repeated-CV scores. |
| [figure_experiment_1_cv_distribution.png](figure_experiment_1_cv_distribution.png) | Distribution plot showing variation across those evaluations. |

## Experiment 2 — time and cumulative-feed ablation

| File | Purpose |
|---|---|
| [experiment_2_time_feed_ablation.csv](experiment_2_time_feed_ablation.csv) | Overall scores with all features, without time, without cumulative feed, and without both. |
| [experiment_2_time_feed_ablation_by_batch.csv](experiment_2_time_feed_ablation_by_batch.csv) | The same comparisons at individual-batch level. |
| [figure_experiment_2_time_feed_ablation.png](figure_experiment_2_time_feed_ablation.png) | Plot comparing the four feature sets. |

## Experiment 3 — fault-phase errors

| File | Purpose |
|---|---|
| [experiment_3_fault_onset_audit.csv](experiment_3_fault_onset_audit.csv) | Recorded fault-window timing for each fault batch. |
| [experiment_3_fault_phase_predictions.csv](experiment_3_fault_phase_predictions.csv) | Individual fault-batch predictions with their retrospective phase labels. |
| [experiment_3_fault_phase_by_batch.csv](experiment_3_fault_phase_by_batch.csv) | Errors before, within and after the fault window for each batch. |
| [experiment_3_fault_phase_overall.csv](experiment_3_fault_phase_overall.csv) | Pooled and equal-batch summary errors for each phase. |
| [figure_experiment_3_fault_phase_mae.png](figure_experiment_3_fault_phase_mae.png) | Individual-batch and mean MAE across the three phases. |

## Experiment 4 — model comparison

| File | Purpose |
|---|---|
| [experiment_4_model_comparison_validation.csv](experiment_4_model_comparison_validation.csv) | Validation scores for the compared regression models. |
| [experiment_4_model_comparison_test.csv](experiment_4_model_comparison_test.csv) | Overall normal-test and fault-test scores. |
| [experiment_4_model_comparison_by_batch.csv](experiment_4_model_comparison_by_batch.csv) | Test scores for each model and batch. |
| [experiment_4_fault_degradation.csv](experiment_4_fault_degradation.csv) | Change in performance between normal and fault conditions. |
| [figure_experiment_4_model_comparison.png](figure_experiment_4_model_comparison.png) | Pooled RMSE and R² comparison plot. |

## Experiment 5 — OOD and uncertainty

| File | Purpose |
|---|---|
| [experiment_5_early_ood_scores.csv](experiment_5_early_ood_scores.csv) | Early-batch OOD scores and thresholds at the evaluated time horizons. |
| [experiment_5_fault_ood_earliest_detection.csv](experiment_5_fault_ood_earliest_detection.csv) | Earliest evaluated warning horizon for each fault batch. |
| [experiment_5_ood_evaluation_summary.csv](experiment_5_ood_evaluation_summary.csv) | Summary of OOD warnings on normal and fault test data. |
| [experiment_5_ood_model_audit.csv](experiment_5_ood_model_audit.csv) | OOD reference/model setup audit. |
| [experiment_5_uncertainty_predictions.csv](experiment_5_uncertainty_predictions.csv) | Individual predictions and empirical uncertainty-related outputs. |
| [experiment_5_uncertainty_by_batch.csv](experiment_5_uncertainty_by_batch.csv) | Uncertainty summary for each batch. |
| [experiment_5_uncertainty_summary.csv](experiment_5_uncertainty_summary.csv) | Overall uncertainty summary. |
| [experiment_5_ood_uncertainty_by_batch.csv](experiment_5_ood_uncertainty_by_batch.csv) | Combined batch-level OOD, prediction-error and uncertainty information. |
| [figure_experiment_5_fault_ood_heatmap.png](figure_experiment_5_fault_ood_heatmap.png) | Heatmap of fault-batch OOD score margins over time horizons. |
| [figure_experiment_5_ood_vs_batch_rmse.png](figure_experiment_5_ood_vs_batch_rmse.png) | Scatter plot relating early OOD score to later batch RMSE. |

## Shared files

| File or folder | Purpose |
|---|---|
| [experiment_configuration.json](experiment_configuration.json) | Feature sets, model settings and experiment configuration. |
| [report_ready_results_summary.txt](report_ready_results_summary.txt) | Original automatically generated text summary; interpret alongside the results guide. |
| [notebook_outputs/](notebook_outputs/) | Original notebook-display versions of the six saved experiment plots. |

[Annotated experiment figures](../../docs/figures/EXPERIMENTS.md) · [Interpretation and limitations](../../docs/RESULTS_GUIDE.md)
