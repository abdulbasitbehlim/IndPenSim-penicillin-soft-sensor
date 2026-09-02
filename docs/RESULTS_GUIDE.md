# Reading the saved results

These folders contain existing completed-run outputs. They are not produced by opening a notebook or running repository checks.

## Earlier notebook: `results/baseline/` and `results/experiments/`

The baseline folder records the fixed split, validation comparison, selected Random Forest's normal/fault errors and individual-batch scores. The experiments folder records all five diagnostic studies and their original PNG figures.

The five repeated CV folds contain 18 normal test batches each. They are repeated five times using the same 90 normal batches. Mean, SD and range summarise sensitivity to those splits; they do not prove freedom from model bias.

The fault-phase plot is a line plot with individual-batch lines and a mean with a bootstrap interval. Its means are **mean per-batch MAE**: 0.061, 1.485 and 4.721 g/L before, within and after the first-to-last recorded fault window. The pooled row MAEs are different: 0.112, 2.170 and 4.708 g/L. Do not label one as the other. Only nine batches contribute an after-window segment.

The comparator figure has pooled RMSE on the left and pooled R² on the right. It is not a plot of mean batch RMSE. The earlier HGB model improves fault RMSE relative to RF, but has slightly worse fault MAE; ranking depends on the metric.

The early OOD heatmap shows **score minus its horizon-specific threshold**. Positive entries are warnings. The 24-hour OOD-versus-error scatterplot instead uses the **raw OOD score** on its x-axis; its dashed vertical line is the threshold. These prefix-summary detectors are different from the final `main.ipynb` row-level detector. For batches 91 and 100, a warning at 24 h occurs after their recorded 20-h onset.

## Final notebook: `results/main/`

| File | What it means |
|---|---|
| `cross_validated_overall_metrics.csv` | Primary pooled normal/fault MAE, RMSE and R² for both training strategies |
| `cross_validated_batch_metrics.csv` | 200 rows: two strategies for each of 100 held-out batches |
| `cross_validated_predictions.csv` | 113,935 held-out observation rows, with both predictions and the separate risk score |
| `paired_batch_bootstrap.csv` | Differences between paired batch RMSEs; negative means fault-inclusive is lower |
| `fault_risk_summary.csv` | Held-out warning rates and the within-fault-batch phase AUC |
| `deployment_reliability_by_batch.csv` | Diagnostics from the final refitted bundle; not another held-out test |
| `run_metadata.json` | Run mode, completed folds, feature names, settings and recorded environment |
| `figure_1_rmse_comparison.png` | Grouped bar chart of pooled normal and fault RMSE |
| `figure_2_fault_batch_rmse.png` | Grouped bar chart for each held-out fault batch |
| `figure_3_fault_actual_vs_predicted.png` | Two scatterplots against the equality line |
| `figure_4_fault_risk_by_phase.png` | Original boxplots of the separate warning scores |
| `batch_100_held_out_trajectory.png` | Actual and predicted concentration over time for the unresolved failure |

The saved files use `Fault-aware HGB`; the README calls it **fault-inclusive HGB** to describe what the regressor learns from. These names refer to the same saved strategy, not different models.

MAE and RMSE are in g/L. Lower is better. R² is not an accuracy percentage and may be negative. Pooled row metrics weight longer batches more heavily than an equal-batch mean.

### Warnings are not concentration accuracy

At a risk-score threshold of 0.5, 13.86% of normal rows, 4.64% of pre-onset fault-batch rows and 49.26% of onset/after rows were warned. The reported AUC of 0.8434 compares pre-onset with onset/after rows within the ten fault batches; it is not an all-normal-versus-all-fault-batches AUC.

The column and original figure use the term `Probability`, but the class-weighted score has not been independently probability-calibrated. Read it as a risk score. It does not prove a physical fault and does not correct the concentration estimate.

The final OOD reference is fitted on normal inputs with a fitted-reference 99th-percentile threshold. That is not a demonstrated 1% false-warning rate for unseen batches. An input may look familiar while its target prediction is poor: batch 100 illustrates this limitation.

The final empirical range combines held-out absolute-error quantiles and widens by 25% on OOD flags. It is heuristic, not a guaranteed 90% interval. The final bundle's diagnostics involve refitting after evaluation and cannot establish independent interval coverage.

### Main conclusion and remaining failure

Fault-inclusive training reduced pooled fault RMSE from 3.1946 to 2.5644 g/L, with little change in normal RMSE. Eight of ten fault batches improved. Batch 100 still had RMSE 6.631 g/L and R² −2.4837. These results support a benchmark-level improvement, not a claim that all faults are now predicted correctly.

No trained `joblib` model is bundled. Run the notebook to create your own, and never load a pickle/joblib file from a source you do not trust.
