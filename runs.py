# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 18:03:27 2015

@author: james
"""

from __future__ import division

import numpy
import sqlite3
import pandas
from sklearn.neighbors import KNeighborsClassifier

connection = sqlite3.connect("./lahman2013.sqlite")

query = """

SELECT SO as strikeouts, SB as stolen_bases, H as hits, IBB,  R as runs, HR as homeruns, G as games, AB as at_bats, G_batting as games_as_batter FROM Batting

"""
df = pandas.read_sql(query, connection)
connection.close()


df["hits_per_game_as_batter"] = df.hits / df.games_as_batter
df.dropna(inplace = True)
response_series = df.runs




explanatory_series = df[["hits_per_game_as_batter",  "homeruns"]]

CV_AMOUNT = 0.2

holdout_number = round(len(df) * CV_AMOUNT,0)

test_indices = numpy.random.choice(df.index, holdout_number, replace = False)
train_indices = df.index[~df.index.isin(test_indices)]

response_train = response_series.ix[train_indices,]
explanatory_train = explanatory_series.ix[train_indices,]

response_test = response_series.ix[test_indices,]
explanatory_test = explanatory_series.ix[test_indices,]


KNN_Classifier = KNeighborsClassifier(n_neighbors = 27, p = 2)
KNN_Classifier.fit(explanatory_train, response_train)

response_prediction = KNN_Classifier.predict(explanatory_test)

num_correct = len(response_test[response_test == response_prediction])
total_number = len(response_test)
percent_correct = num_correct / total_number
print "model has an accuracy of " + str(percent_correct) + "%" #30% accuracy

import sklearn.grid_search as gs
knn = KNeighborsClassifier(p = 2)
k_range = range(1, 30, 2)
param_grid = dict(n_neighbors = k_range)
grid = gs.GridSearchCV(knn, param_grid, cv = 5, scoring= "accuracy")
grid.fit(explanatory_series, response_series)

print grid.best_estimator_

