# -*- coding: utf-8 -*-
# __author__ = 'Baoting Zhang'
from sklearn import preprocessing
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.datasets.samples_generator import make_classification
from sklearn import datasets
import matplotlib.pyplot as plt
from sklearn.cross_validation import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVC
from sklearn.learning_curve import v

iris = datasets.load_iris()
iris_X = iris.data
iris_y = iris.target
# iris_X =preprocessing(iris_X)

ucKrange = range(1, 31)
ucKscore = []

for k in ucKrange:
    knn = KNeighborsRegressor(n_neighbors=k)
    loss = -cross_val_score(knn, iris_X, iris_y, cv=10, scoring='mean_squared_error')
    # scores =cross_val_score(knn, iris_X, iris_y, cv=10, scoring="accuracy")
    ucKscore.append(loss.mean())

plt.plot(ucKrange, ucKscore)
plt.xlabel('Value of k for knn')
plt.ylabel('Cross-Validated Accuracy')
plt.show()
