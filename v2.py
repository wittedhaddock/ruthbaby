# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 18:32:13 2015

@author: james
"""
from __future__ import division #without this, division acts real whacky

import pandas
import sqlite3
import numpy
import matplotlib.pyplot as plt

connection = sqlite3.connect("./lahman2013.sqlite")

CROSS_VALIDATION_AMOUNT = 0.2

sql_query = """
SELECT
    Batting.playerID, Batting.yearID, Batting.R as Runs, Fielding.GS as Games_started, Fielding.playerID, Pitching.playerID, Pitching.SO as Strikeouts_Thrown, HallofFame.inducted as is_inducted, HallofFame.playerID
FROM 
    Batting
LEFT JOIN 
    Fielding 
ON 
    Batting.playerID = Fielding.playerID
JOIN Pitching ON Fielding.playerID = Pitching.playerID
JOIN HallofFame ON HallofFame.playerID = Fielding.playerID
WHERE Batting.yearID < 2000
GROUP BY Fielding.playerID"""


df = pandas.read_sql(sql_query, connection)
connection.close()

df.count()
df.dropna(inplace = True)
explanatory_variables = df[["Strikeouts_Thrown", "Games_started", "Runs"]]
response_series = df.is_inducted

response_series.index[~response_series.index.isin(explanatory_variables.index)]
#Assert that above is empty!
#indices map mutually between both series. Good! 

from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import cross_val_score

classifier_naive_bayes = MultinomialNB()

accuracy_scores = cross_val_score(classifier_naive_bayes, explanatory_variables, response_series, cv=10, scoring='accuracy', n_jobs = -1)

print accuracy_scores.mean()