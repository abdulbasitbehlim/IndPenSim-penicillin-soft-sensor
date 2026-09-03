# Reading the saved results

The CSVs are outputs of completed runs. Opening a notebook or passing the repository checks does not retrain the models.

## Which study is which?

| Results | Meaning |
|---|---|
| [ML2](../results/ml2/README.md) | Earlier baseline run, retained separately. |
| [ML3 baseline](../results/baseline/README.md) | Fixed-split model selection and the selected Random Forest's normal/fault tests. |
| [ML3 experiments](../results/experiments/README.md) | Five diagnostic studies of generalisation and reliability. |
| [ML4](../results/main/README.md) | Normal-only versus fault-aware HGB under complete-batch evaluation. |

ML2 and ML3 use the same split data; they are not independent validation datasets. Do not substitute one run's predictions for another run's metric tables.

## Metric meanings

| Metric | Interpretation |
|---|---|
| MAE | Average absolute concentration error, in g/L; lower is better. |
| RMSE | Concentration error with extra weight on large mistakes, in g/L; lower is better. |
| R² | Explained target variation relative to a mean reference; not an accuracy percentage and may be negative. |
| Pooled result | Calculated over all time rows together; longer batches contribute more rows. |
| Mean batch result | Calculated for each batch first, then averaged with equal batch weight. |

## ML4 concentration results

Source: [cross_validated_overall_metrics.csv](../results/main/cross_validated_overall_metrics.csv).

| Condition | Model | MAE (g/L) | RMSE (g/L) | R² |
|---|---|---:|---:|---:|
| Normal | Normal-only HGB | 1.2095 | 1.9806 | 0.9607 |
| Normal | Fault-aware HGB | 1.2063 | 1.9830 | 0.9606 |
| Fault | Normal-only HGB | 2.0763 | 3.1946 | 0.8580 |
| Fault | Fault-aware HGB | 1.4405 | 2.5644 | 0.9085 |

Fault-aware training reduced pooled fault RMSE by 19.73%, with little change in normal RMSE. Eight of ten fault batches improved. Batch 100 remained poorly predicted: RMSE 6.631 g/L and R² −2.4837.

The saved files use the label Fault-aware HGB. Some figure captions use fault-inclusive HGB to describe the same strategy. Neither name means every fault is predicted correctly.

## Reading the five experiment plots

1. **Repeated batch CV:** 25 scores come from five repeats over the same 90 normal batches. Their spread describes split sensitivity, not freedom from bias. Earlier feature-usability screening was not fully nested within these repeats.
2. **Time/feed ablation:** compare against the ablation's own all-input reference. The refit's row order differs from the initial RF final fit, which can slightly change a seeded tree model. Removing these two variables does not remove every possible batch-progress proxy; feature importance is not causation.
3. **Fault-phase errors:** the plot uses equal-batch mean MAE: 0.061, 1.485 and 4.721 g/L before, within and after the recorded fault window. Pooled row MAEs are 0.112, 2.170 and 4.708 g/L. Only nine batches contribute an after-window segment. The first-to-last window can include inactive gaps, and a cleared flag is not proof of recovery.
4. **Model comparison:** the figure shows pooled RMSE and pooled R², not mean batch RMSE. The earlier HGB comparator uses different settings from ML4; rankings also depend on the metric chosen.
5. **Early OOD:** the heatmap shows score minus the horizon-specific threshold. The 24-hour scatter plot uses the raw OOD score. For batches 91 and 100, warnings at 24 h occur after the recorded onset at 20 h. These prefix-summary detectors differ from ML4's row-level detector.

[Annotated figures](FIGURES.md) link each plot to its result files. The original automatically generated text summaries are retained as outputs, not as replacements for these distinctions.

## ML4 warning scores and uncertainty

At a risk-score threshold of 0.5, warnings occurred on 13.86% of normal rows, 4.64% of pre-onset fault-batch rows and 49.26% of onset/after rows. The AUC of 0.8434 compares pre-onset with onset/after rows within fault batches; it is not an all-normal-versus-all-fault-batches AUC.

The risk score is uncalibrated despite the original column name Probability. It labels all rows from the first recorded fault onset onward, including later rows after the active flag clears. Risk and OOD warnings do not prove a physical fault and do not alter the concentration point prediction.

The final OOD threshold is the fitted normal reference's 99th percentile, not a verified 1% warning rate on unseen batches. The final-bundle diagnostic table is calculated after refitting and is not an independent OOD evaluation.

The empirical error range combines held-out absolute-error quantiles and widens by 25% on OOD flags. It is a heuristic range, not guaranteed 90% coverage. Some raw concentration estimates are negative; the reported metrics retain them and the regressor is unconstrained.

## Scope of the findings

This is current-time concentration estimation on simulated IndPenSim batches, not future forecasting or external validation on physical fermentations. The benchmark informed development, so the final comparison is exploratory rather than an untouched confirmatory test. Fault examples and their training weight change together. Only ten fault batches are available, and bootstrap summaries across overlapping fold fits do not represent independent campaigns.

The results support a benchmark-level improvement, not complete fault robustness. A full-run flag or green repository check is not a certificate of publication readiness. Trained joblib binaries are not included; rerunning the notebooks creates them.
