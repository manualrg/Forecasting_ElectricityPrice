import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def time_series_CV(model, cv_splits, min_train_len, X, y, plot=False):
    # Loop over each time split
    kfold_train_scores = []
    kfold_val_scores = []
    #Set train and validation subets
    for train_index, val_index in cv_splits.split(X):
        if (type(X) == pd.core.frame.DataFrame):
            _X_train_ = X.iloc[train_index].copy()
            _X_val_ = X.iloc[val_index].copy()
        elif (type(X) == np.ndarray):
            _X_train_ = X[train_index, :].copy()
            _X_val_ = X[val_index, :].copy()
        else:
            raise Exception('Incorrect X type: {}'.format(type(X)))
        if len(_X_train_)>=min_train_len:
            _y_train_ = y[train_index]
            _y_val_ = y[val_index]
            # fit model and predict over train and validation
            model.fit(_X_train_, _y_train_)
            p_train = model.predict(_X_train_)
            p_val = model.predict(_X_val_)
            # Compute current iteration scores in train and validation
            score_train = np.sqrt(mean_squared_error(_y_train_, p_train))
            score_val = np.sqrt(mean_squared_error(_y_val_, p_val))
            # Append scores
            kfold_train_scores.append(score_train)
            kfold_val_scores.append(score_val)
    # compute average over k-folds score
    cv_mean_train_score = np.mean(kfold_train_scores)
    cv_mean_val_score = np.mean(kfold_val_scores)
    if plot:
        k_fold_scores = kfold_train_scores + kfold_val_scores
        x = ["train"] * len(kfold_train_scores) + ["val"] * len(kfold_val_scores)
        plt.figure(figsize=(8, 6))
        plt.scatter(x, k_fold_scores)
        plt.plot(["train", "val"], [cv_mean_train_score, cv_mean_val_score], color="red")
        plt.ylabel("RMSE")

    return cv_mean_train_score, cv_mean_val_score, kfold_train_scores, kfold_val_scores


def time_series_CV_grid_search(model, param_grid, cv_splits, min_train_len, X, y, refit=True, dev=False):
    i = 0
    train_scores = []
    val_scores = []
    models = []
    # Loop through the parameter grid
    for g in param_grid:

        model.set_params(**g)
        # Loop over each time split and for each model configuration
        cv_mean_train_score, cv_mean_val_score, kfold_train_scores, kfold_val_scores = time_series_CV(model, cv_splits, min_train_len, X, y, False)

        # For each iteration, store the fitted model and mean cv scores (train and val)
        models.append(model)
        train_scores.append(cv_mean_train_score)
        val_scores.append(cv_mean_val_score)

        i += 1
        if dev:
            print("======> CV iteration: {}".format(i))
            print("Model: {}".format(model))
            print("Model Train RMSE: k-fold {} and mean score: {}".format(kfold_train_scores, cv_mean_val_score))
            print("Model Val RMSE: k-fold {} and mean score: {}".format(kfold_val_scores, cv_mean_val_score))

    best_idx = np.argmin(val_scores)
    if refit:
        model.set_params(**param_grid[best_idx]).fit(X, y)

    print("\n======> CV algorithm finished after {} hyperparameter configurations evaluated".format(i))
    print("Best model HyperParams: ", param_grid[best_idx])
    print("Best model Train CV mean RMSE: {} ".format(train_scores[best_idx]))
    print("Best model Val CV mean RMSE: {}".format(val_scores[best_idx]))

    l = list(param_grid)
    for i, dict in enumerate(l):
        dict["Train CV score"] = train_scores[i]
        dict["Val CV score"] = val_scores[i]
    CV_report = pd.DataFrame(l)

    return model, best_idx, train_scores, val_scores, CV_report