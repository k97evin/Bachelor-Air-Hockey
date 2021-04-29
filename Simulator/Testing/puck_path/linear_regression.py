import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from pathlib import Path

path =  Path(__file__).parent


Angles_df = pd.read_csv(path/'Angles.csv')

X = Angles_df.iloc[:, 0].values.reshape(-1, 1)  # values converts it into a numpy array
Y = Angles_df.iloc[:, 1].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)  # make predictions



plt.scatter(X, Y)
plt.plot(X, Y_pred, color='red')
#plt.show()

a =linear_regressor.predict([[10]])
print(type(a))
print(a[0][0])


print(Path.cwd())

from joblib import dump
dump(linear_regressor, path/'model.joblib', compress=3)

