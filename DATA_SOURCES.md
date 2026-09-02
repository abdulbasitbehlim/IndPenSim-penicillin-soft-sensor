# Data sources, attribution and licensing boundaries

## Original dataset

Goldrick, S. (2019). *Data for: Modern day monitoring and control challenges outlined on an industrial-scale benchmark fermentation process* (Version 1) [Data set]. Mendeley Data. https://doi.org/10.17632/pdnjz7zz5x.1

The [dataset record](https://data.mendeley.com/datasets/pdnjz7zz5x/1) identifies the licence as **Creative Commons Attribution 4.0 International**. Consult the [CC BY 4.0 terms](https://creativecommons.org/licenses/by/4.0/). Credit the creators, link the licence and indicate changes when sharing adaptations.

The source CSV used here is `100_Batches_IndPenSim_V3.csv`. The notebooks select its process-variable subset, reconstruct or retain batch IDs, construct history/feed features and calculate model outputs. The original CSV and Raman measurements are not redistributed in this package.

## Source publications

Goldrick, S., Ştefan, A., Lovett, D., Montague, G., & Lennox, B. (2015). The development of an industrial-scale fed-batch fermentation simulation. *Journal of Biotechnology, 193*, 70–82. https://doi.org/10.1016/j.jbiotec.2014.10.029

Goldrick, S., Duran-Villalobos, C. A., Jankauskas, K., Lovett, D., Farid, S. S., & Lennox, B. (2019). Modern day monitoring and control challenges outlined on an industrial-scale benchmark fermentation process. *Computers & Chemical Engineering, 130*, 106471. https://doi.org/10.1016/j.compchemeng.2019.05.037

## What this repository adds

The original code implements concentration models, complete-batch evaluation, diagnostic experiments and result visualisation. The checked-in CSVs and plots are outputs of those analyses of simulated data. They are not newly collected fermentation measurements, nor evidence that the repository author created IndPenSim.

The `results/` directories contain selected outputs of the supplied completed runs. In particular, `results/ml4/cross_validated_predictions.csv` includes source-derived target values together with held-out predictions, so dataset attribution remains relevant when sharing it. The supplied result values were not replaced by a new packaging run.

## Licence scope

- `LICENSE` contains the MIT terms for the repository's original software and accompanying documentation. MIT does not transfer ownership of IndPenSim or override its attribution requirements.
- The source data and redistributed data-derived material in `results/` are provided with the original dataset's CC BY 4.0 attribution. Preserve this notice when redistributing them.
- Third-party software dependencies retain their own licences; they are installed as dependencies, not vendored here.
- Third-party paper PDFs, personal presentation files and unapproved manuscript drafts are not included. Do not add them without checking redistribution rights and author approval.

The proposed copyright holder is Abdul Basit Behlim, following the supplied project files. Confirm that all contributors and the institution permit the intended public release. An MIT licence allows commercial as well as non-commercial reuse; choose a different licence before publication if that is not the intended permission.
