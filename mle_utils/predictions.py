import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def pred_and_score_model(model, X, y, label: str=None):


    preds = model.predict(X)
    RMSE = np.sqrt(mean_squared_error(y, preds))
    MAPE = mean_absolute_error(y, preds)
    R2 = r2_score(y, preds)
    if label != None:
        print(pd.DataFrame(data={"RMSE":[RMSE], "MAPE": [MAPE], "R2": [R2]}, index=[label]))
    return preds, RMSE, MAPE, R2

def plot_predictions(y, p, time_index):
    # TODO xlabels in time series data must be uniformly distributed

    import matplotlib.gridspec as gridspec
    import matplotlib.dates as mdates
    sns.set_style("whitegrid")

    e = y - p

    fig = plt.figure(figsize=(16, 22))
    plt.suptitle("Forecasting and residual analysis", y=0.9)
    gspec = gridspec.GridSpec(3, 2)

    top_ts = plt.subplot(gspec[0, 0:2])
    #fig.autofmt_xdate()
    up_le = plt.subplot(gspec[1, 0])
    up_ri = plt.subplot(gspec[1, 1])
    down_le = plt.subplot(gspec[2, 0])
    down_ri = plt.subplot(gspec[2, 1])
    #top time series: actual and forecasted
    top_ts.plot(time_index, y, label="Actual values")
    top_ts.scatter(time_index, p, color="red", alpha=0.25, label="Forecasted values")
    top_ts.legend()
    plt.setp(top_ts.get_xticklabels(), rotation=30, ha='right')

    up_le.scatter(p, y)
    up_le.plot(y, y, alpha=0.75)
    up_le.set_ylabel("Actual values")
    up_le.set_xlabel("Forecasted values")

    up_ri.hist(e)
    up_ri.set_xlabel("Residuals")

    down_le.scatter(y, e)
    down_le.set_ylabel("Residuals")
    down_le.set_xlabel("Actual values")

    down_ri.scatter(np.arange(1, len(time_index)+1), e)
    down_ri.axhline(y=0, alpha=0.75)
    down_ri.set_xlabel("idx")

    plt.show()