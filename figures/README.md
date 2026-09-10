# High-resolution figure archive

The original scientific output PNGs under `results/` are preserved unchanged. This archive adds organized copies and manuscript-ready versions.

| Folder | Contents |
|---|---|
| `images_300_dpi/` | Organized 300-DPI copies of the previous/canonical code-output figures. |
| `images_600_dpi_original_code_output/` | 600-DPI archival versions preserving the original output appearance, plus a PowerPoint. |
| `publishable_images/` | Publication-ready 600-DPI figures generated from saved repository data/results, plus PowerPoint decks. |

`paper_figures_600dpi.py` regenerates the publication figures from checked-in results. `image_manifest.csv` records dimensions, DPI and SHA-256 hashes.

Scientific presentation notes: E5a uses three decimals; E5b is explicitly identified as the baseline RF/OOD experiment; F4 is labelled as an uncalibrated warning score and suppresses individual outlier markers only for visual clarity; F2 uses the requested fault-inclusive labels and no plot title.
