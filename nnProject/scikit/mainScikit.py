# -*- coding: utf-8 -*-
# __author__ = 'Baoting Zhang'
import numpy as np
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

iris = datasets.load_iris()
iris_X = iris.data
iris_y = iris.target

# print(iris_X)
# print(iris_y)

# X_train, X_test, y_train, y_test = train_test_split(iris_X, iris_y, test_size=0.3)

# print(y_train)

knn = KNeighborsClassifier(n_neighbors=6)
model = SVC()
# knn.fit(X_train, y_train)
# print(knn.predict(X_test))
# print(y_test)
scores = cross_val_score(model, iris_X, iris_y, cv=10, scoring='accuracy')
print(scores)
print(scores.mean())