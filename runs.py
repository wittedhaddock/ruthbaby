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

response_series = df.runs
explanatory_series = df[["strikeouts", "hits"]]

CV_AMOUNT = 0.2

holdout_number = round(len(df) * CV_AMOUNT,0)

test_indices = numpy.random.choice(df.index, holdout_number, replace = False)
train_indices = df[~df.index.isin(test_indices)]