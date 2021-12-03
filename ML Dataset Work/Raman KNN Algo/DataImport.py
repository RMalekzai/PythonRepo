import pandas as pd
from sklearn import decomposition
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
# from sklearn.metrics import f1_score, classification_report
from matplotlib import pyplot as plt
from sklearn.preprocessing import PowerTransformer
# from numpy.linalg import norm
# import numpy as np
import math
import time
from sklearn.preprocessing import MinMaxScaler

time1 = time.time()
df = pd.read_excel(r"C:\Users\roman\PythonRepo\ML Dataset Work\Altogether Raw Data - 09feb21.xlsx")
df = df.dropna(subset=["Glucose"])

time2 = time.time()

"""Separate offline data from spectra database"""
OData = df[df.columns[9:28]]
Specs = df.drop(labels=[x for x in df.columns[:28]], axis=1)

"""Remove redundant wave numbers from the data set, based on literature"""
dropped_cols = []
for x in Specs.columns:
    if int(x) < 301:
        dropped_cols.append(x)
    elif 1850 < int(x) < 2900:
        dropped_cols.append(x)
    elif 3200 < int(x) < 3426:
        dropped_cols.append(x)
Specs = Specs.drop(labels=[x for x in dropped_cols], axis=1)

Specs_train, Specs_test, y_train, y_test = train_test_split(Specs, OData, test_size=0.1, random_state=0)

"""Limit to one metabolite/variable"""
y_train = y_train["Glucose"]
y_test = y_test["Glucose"]

"""Output raw datafile"""
with pd.ExcelWriter(r'C:\Users\roman\PythonRepo\ML Dataset Work\Raman KNN Algo\NON_TransformedData.xlsx') as writer:
    Specs_train.to_excel(writer, sheet_name='x_train')
    y_train.to_excel(writer, sheet_name='y_train')
    Specs_test.to_excel(writer, sheet_name='x_test')
    y_test.to_excel(writer, sheet_name='y_test')



"""Min/Max Scaler here"""
scale = MinMaxScaler((0, 1))
minmax_train = pd.DataFrame(scale.fit_transform(Specs_train))
minmax_test = pd.DataFrame(scale.transform(Specs_test))

minmax_train.index = Specs_train.index
minmax_test.index = Specs_test.index

with pd.ExcelWriter(r'C:\Users\roman\PythonRepo\ML Dataset Work\Raman KNN Algo\MinMax_TransformedData.xlsx') as writer:
    minmax_train.to_excel(writer, sheet_name='x_train')
    y_train.to_excel(writer, sheet_name='y_train')
    minmax_test.to_excel(writer, sheet_name='x_test')
    y_test.to_excel(writer, sheet_name='y_test')


"""Log scaling"""
logged_train = pd.DataFrame()
for x in Specs_train.columns:
    logged = []
    for y in Specs_train[x]:
        logged.append(math.log10(y))
    logged_train[str(x)] = logged

logged_test = pd.DataFrame()
for x in Specs_test.columns:
    logged = []
    for y in Specs_test[x]:
        logged.append(math.log10(y))
    logged_test[str(x)] = logged

logged_train.index = Specs_train.index
logged_test.index = Specs_test.index

with pd.ExcelWriter(r'C:\Users\roman\PythonRepo\ML Dataset Work\Raman KNN Algo\Logged_TransformedData.xlsx') as writer:
    logged_train.to_excel(writer, sheet_name='x_train')
    y_train.to_excel(writer, sheet_name='y_train')
    logged_test.to_excel(writer, sheet_name='x_test')
    y_test.to_excel(writer, sheet_name='y_test')

"""Power Transformer here"""
pt = PowerTransformer()
Power_train = pd.DataFrame(pt.fit_transform(Specs_train))
Power_test = pd.DataFrame(pt.transform(Specs_test))

Power_train.index = Specs_train.index
Power_test.index = Specs_test.index

with pd.ExcelWriter(r'C:\Users\roman\PythonRepo\ML Dataset Work\Raman KNN Algo\Power_TransformedData.xlsx') as writer:
    Power_train.to_excel(writer, sheet_name='x_train')
    y_train.to_excel(writer, sheet_name='y_train')
    Power_test.to_excel(writer, sheet_name='x_test')
    y_test.to_excel(writer, sheet_name='y_test')

"""PCA happens here, always comes out to 1 PC for some reason"""
# pca = decomposition.PCA(n_components=100)
# x_train = pca.fit_transform(minmax_train)
# x_test = pca.transform(minmax_test)


# def exp_var(vectors):
#     var = 0
#     for x in range(vectors):
#         var += pca.explained_variance_ratio_[x]
#     return var

time3 = time.time()
print("Time to import = {0} and time to 3 = {1}".format(time2-time1, time3 - time2))


