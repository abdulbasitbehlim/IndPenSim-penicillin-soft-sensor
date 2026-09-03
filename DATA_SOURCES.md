# Data sources and licences

## Original IndPenSim data

Goldrick, S. (2019). *Data for: Modern day monitoring and control challenges outlined on an industrial-scale benchmark fermentation process* (Version 1) [Data set]. Mendeley Data. https://doi.org/10.17632/pdnjz7zz5x.1

The original dataset is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

## Included data

| Path | Relationship to the source data |
|---|---|
| [data/splits/](data/splits/README.md) | Process-column exports from the source CSV, with reconstructed Batch_ID and Data_Split columns. Four complete-batch partitions are included; Raman spectra are not. |
| [results/](results/README.md) | Derived model predictions, metrics and plots from the supplied completed runs. These are analysis outputs, not newly collected experimental measurements. |
| [data/raw/](data/raw/README.md) | Location for a separately downloaded original full CSV; the full process-plus-Raman file was not present in the supplied result archives. |

The four split CSVs are preserved byte-for-byte from the supplied Baseline ML exports. Their transformations relative to the original dataset are process-column selection, batch identification, split labelling and partitioning. Checksums and exact column names are recorded in [data/splits/manifest.json](data/splits/manifest.json).

## Licence scope

| Material | Licence or terms |
|---|---|
| Original repository code and documentation | [MIT](LICENSE). |
| Source-derived input CSVs, result tables and plots | CC BY 4.0 with the IndPenSim attribution above; the MIT licence does not override these data terms. |
| Third-party dependencies | Their respective software licences. |

Preserve the dataset citation, licence link and indication of changes when redistributing source-derived material.

## Source publications

Goldrick, S., Ştefan, A., Lovett, D., Montague, G., & Lennox, B. (2015). The development of an industrial-scale fed-batch fermentation simulation. *Journal of Biotechnology, 193*, 70–82. https://doi.org/10.1016/j.jbiotec.2014.10.029

Goldrick, S., Duran-Villalobos, C. A., Jankauskas, K., Lovett, D., Farid, S. S., & Lennox, B. (2019). Modern day monitoring and control challenges outlined on an industrial-scale benchmark fermentation process. *Computers & Chemical Engineering, 130*, 106471. https://doi.org/10.1016/j.compchemeng.2019.05.037
