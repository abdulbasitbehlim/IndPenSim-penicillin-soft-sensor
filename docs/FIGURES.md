# Complete output-figure gallery

[Project overview](../README.md) · [Results guide](RESULTS_GUIDE.md) · [Figure provenance](figure_provenance.json)

For manuscript preparation, see the organized [high-resolution figure archive](../figures/README.md). Original result PNGs remain unchanged in `results/`.

The gallery contains **14 distinct plots** from the two completed studies. Figure F2 was regenerated from the unchanged saved results on 4 September 2026 to update its presentation labels; all other plots retain their original renderings. Six experiment plots also have a separate notebook-display rendering: both versions are retained, giving **20 PNG files** in total.

## Baseline ML: learning from normal batches

[Open the Baseline ML gallery](figures/BASELINE.md)

| Figure | Chart type | Question |
|---|---|---|
| B1 — Training trajectories | Line plot | Do normal batches follow the same production curve? |
| B2 — Random Forest predictions | Paired scatterplots | How does the selected model behave on unseen batches? |
| B3 — Feature importance | Horizontal bar chart | Which inputs does the forest rely on most? |

## Baseline ML experiments: investigating the weaknesses

[Open the experiment gallery](figures/EXPERIMENTS.md)

| Figure | Chart type | Question |
|---|---|---|
| E1 — Repeated batch validation | Boxplots and individual scores | How sensitive is performance to the split? |
| E2 — Time/feed ablation | Grouped bar chart | What happens when the dominant progress features are removed? |
| E3 — Fault-phase error | Batch lines and mean with bootstrap interval | When does error increase? |
| E4 — Model comparison | Paired grouped bar charts | Is the fault-related gap specific to Random Forest? |
| E5a — Early OOD warnings | Annotated heatmap | Which batch prefixes look unfamiliar? |
| E5b — OOD versus error | Scatterplot with threshold | Do early warnings identify high-error batches? |

## Main ML: improvements and remaining failures

[Open the Main ML gallery](figures/FAULT_INCLUSIVE.md)

| Figure | Chart type | Question |
|---|---|---|
| F1 — Overall RMSE | Grouped bar chart | Does including other fault batches help? |
| F2 — Per-fault-batch RMSE | Grouped bar chart | Do all ten fault batches improve? |
| F3 — Actual versus predicted | Paired scatterplots | Where do estimates depart from the true values? |
| F4 — Fault-risk scores | Boxplots | Does the warning score increase after onset? |
| F5 — Batch 100 trajectory | Time-series line plot | What does the unresolved failure look like? |

## Reading and reuse notes

- MAE and RMSE use g/L; lower is better. R² is not an accuracy percentage.
- Early OOD plots and final risk-score plots describe different methods. Neither proves a physical fault.
- Figure F2 has no plot title, uses **Batch ID** and **Batch RMSE (g/L)** as axis labels, and labels its series **Normal-only HGB** and **Fault-inclusive HGB**. Other figures retain their original labels.
- The studies use different evaluation designs; do not pool them as independent repetitions of one experiment.
- Every canonical image and retained display variant is linked in the gallery. [figure_provenance.json](figure_provenance.json) records current hashes, original source locations and the F2 presentation revision.

Retain the [IndPenSim attribution and data-derived material licence](../DATA_SOURCES.md) when reusing figures.
