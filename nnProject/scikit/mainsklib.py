# -*- coding: utf-8 -*-
# __author__ = 'Baoting Zhang'
import numpy as np
from sklearn import datasets
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.externals import joblib

# loaded_data = datasets.load_boston()
# data_X = loaded_data.data
# data_y = loaded_data.target
#
# # print(data_X)
# model = LinearRegression()
# model.fit(data_X, data_y)
#
# # X, y = datasets.make_regression(n_samples=100,n_features=1,n_informative=1)
# # plt.scatter(X,y)
# print('====================/n======================')
# print(model.coef_)
# print(model.intercept_)
# print(model.score(data_X, data_y))
#
# joblib.dump(model, 'home/myHouse/MyHouse/save/clf.pkl')
# data =np.zeros([2,1])
# print(data)
# print(data.size)
img = np.zeros([500,600,3], np.uint8)
img[100,200] = 6
print(img)