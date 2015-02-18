# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 20:07:24 2015

@author: james
"""

import pandas
import sqlite3
import numpy

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

holdout_num = round(len(df.index) * CROSS_VALIDATION_AMOUNT)

testing_indices  = numpy.random.choice(df.index, len(df.index) * 0.2, replace = False)
training_indices = df.index[~df.index.isin(testing_indices)]

#delineate cause from effect—response from explanation
response_variables    = df.is_inducted
explanation_variables = df[["Runs", "Games_started", "Strikeouts_Thrown"]]

#create the response's (whether inducted or not) testing and training series
response_testing  = response_variables.ix[testing_indices]
response_training = response_variables.ix[training_indices]

#create explanation's (what is causing the effect: number of runs, games started, and strikouets thrown) training and testing series
explanation_testing = explanation_variables.ix[testing_indices]
explanation_training = explanation_variables.ix[training_indices]
