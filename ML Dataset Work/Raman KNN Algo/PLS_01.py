import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_decomposition import PLSRegression
# from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_squared_error, r2_score
# from sklearn import svm
# from sklearn.tree import DecisionTreeRegressor

y_train = pd.read_excel(r"MinMax_TransformedData.xlsx",
                        sheet_name="y_train", index_col=0)
y_test = pd.read_excel(r"MinMax_TransformedData.xlsx",
                       sheet_name="y_test", index_col=0)
minmax_train = pd.read_excel(r"MinMax_TransformedData.xlsx",
                        sheet_name="x_train", index_col=0)
minmax_test = pd.read_excel(r"MinMax_TransformedData.xlsx",
                       sheet_name="x_test", index_col=0)
logged_train = pd.read_excel(r"Logged_TransformedData.xlsx",
                        sheet_name="x_train", index_col=0)
logged_test = pd.read_excel(r"Logged_TransformedData.xlsx",
                       sheet_name="x_test", index_col=0)
raw_train = pd.read_excel(r"NON_TransformedData.xlsx",
                       sheet_name="x_train", index_col=0)
raw_test = pd.read_excel(r"NON_TransformedData.xlsx",
                       sheet_name="x_test", index_col=0)

scoring = pd.DataFrame(index=y_test.index)
scoring["Actual"] = y_test["Glucose"]


def predict_values(model, data):
    predictions = []
    for i in data.index:
        predictions.append(model.predict(data.loc[i].to_numpy().reshape(1, -1)))
    predictions = [float(x[0]) for x in predictions]
    return predictions


pls6 = PLSRegression(n_components=6, scale="False")
pls9 = PLSRegression(n_components=9, scale="False")
pls15 = PLSRegression(n_components=15, scale="False")
pls25_s = PLSRegression(n_components=25, scale="True")
pls25 = PLSRegression(n_components=25, scale="False")


models = [pls6, pls9]
train_set = [minmax_train, logged_train]
test_set = [minmax_test, logged_test]


def fit_and_predict(model, train, test):
    model.fit(train, y_train["Glucose"])
    predictions = []
    for i in test.index:
        predictions.append(model.predict(test.loc[i].to_numpy().reshape(1, -1)))
    predictions = [float(x[0]) for x in predictions]
    return predictions


# for y in models:
#     for x in range(len(train_set)):
#         values = fit_and_predict(y, train_set[x], test_set[x])

mean_squared_error(scoring["Actual"], values4)
scoring.to_excel(r"Predicted Values.xlsx")
