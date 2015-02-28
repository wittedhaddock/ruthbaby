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

SELECT SO as strikeouts, H as hits, R as runs FROM Batting

"""
df = pandas.read_sql(query, connection)
connection.close()

df.dropna(inplace = True)
response_series = df.runs
explanatory_series = df[["strikeouts", "hits"]]

CV_AMOUNT = 0.2

holdout_number = round(len(df) * CV_AMOUNT,0)

test_indices = numpy.random.choice(df.index, holdout_number, replace = False)
train_indices = df.index[~df.index.isin(test_indices)]

response_train = response_series.ix[train_indices,]
explanatory_train = explanatory_series.ix[train_indices,]

response_test = response_series.ix[test_indices,]
explanatory_test = explanatory_series.ix[test_indices,]


KNN_Classifier = KNeighborsClassifier(n_neighbors = 3, p = 2)
KNN_Classifier.fit(explanatory_train, response_train)

response_prediction = KNN_Classifier.predict(explanatory_test)

num_correct = len(response_test[response_test == response_prediction])
total_number = len(response_test)
percent_correct = num_correct / total_number
print "model has an accuracy of " + str(percent_correct) + "%"
#30% accuracy