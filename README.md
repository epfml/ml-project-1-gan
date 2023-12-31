[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/U9FTc9i_)

# CS 433 - Project 1

**Team GAN** - Gabriel Dehame, Andrea Miele, Nicolas Moyne

# Repository organization
-  `helpers.py` is the provided file to load the dataset and create submissions
- `implementations.py` implements the ML methods of Step 2
- `score.py` implements functions to calculate the quality of a model (`f1_score`, `accuracy`)
- `preprocessing.py` implements our preprocessing which removes useless features, computes through an ANOVA (Analysis of Variance)
the most impactful features and thus those to keep in priority. The ANOVA is implemented in `anova_selection.py`. It also performs an oversampling and undersampling to cope with the
unbalanced dataset, these are implemented in `OverUnderSampling.py`.
- `utils.py` implements utilitary methods train models such as `build_poly` computing polynomial extensions, `standardize` standardizing data or `predict` computing the prediction for a given model and given datapoints
It also contains a logistic regression with newton's method, cross-validation, local search and KNN but we ended up not using them because it was too slow and/or lead to strange results so they might be bugged.
- `finetuning.py` implements the tuning of the hyperparameters for the models we compared.
- `run.py` reproduces the training of the best performing model we've trained. For it to work, the dataset must be installed in a folder `dataset/`
- `f_scores_after_strat105_500.csv` is a file containing the precomputed ANOVA scores for the features of the dataset to avoid recomputing it each time as it's slow

# Best submission
The best submission on AICrowd is submission #243500, which is reproduced in `run.py`
We also got a F1 of 0.437 in submission #240074 on AICrowd. Unfortunately, the algorithm was not seeded and is therefore difficult to reproduce.
