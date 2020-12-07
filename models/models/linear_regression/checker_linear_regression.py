import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn import metrics, tree, neighbors, ensemble, svm
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_predict
import time
from sklearn.tree import ExtraTreeRegressor

start = time.time()

data = pd.read_csv("../../dataset/checkerDatasetv2.csv")
print(data.head())  # default: read first 5 lines
print(data.shape)

x = data[["r1_service_a", "r1_service_b", "r2_service_b", "r1_service_c",
        "r2_service_d"]]  
print(x.head())

y = data[["throughput"]]
print(y.head())

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
print("Train Data x Shape %s, y Shape %s" % (x_train.shape, y_train.shape))
print("Test Data x Shape %s, y Shape %s" % (x_test.shape, y_test.shape))

model = LinearRegression()
# model = tree.DecisionTreeRegressor()
# model = neighbors.KNeighborsRegressor()
# model = ensemble.AdaBoostRegressor(n_estimators=50)
# model = ExtraTreeRegressor()
model.fit(x_train, y_train)
# display intercept_ and coef_
print(model.intercept_)  
print(model.coef_)  

# 模型拟合测试集
y_pred = model.predict(x_test)
# calculate MSE (Mean Squared Error)
print("MSE:", metrics.mean_squared_error(y_test, y_pred))
# calculate RMSE (Root Mean Squared Error)
print("RMSE", np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

# train time
end = time.time()
print("time cost: ", (end - start) * 1000, "ms")

predicted = cross_val_predict(model, x, y, cv=10)
plt.scatter(y, predicted)
# display plt result
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
plt.xlabel("Measured")
plt.ylabel("Predicted")
plt.show()
