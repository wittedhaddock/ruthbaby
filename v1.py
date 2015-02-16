# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 20:07:24 2015

@author: james
"""

import pandas
import sqlite3

connection = sqlite3.connect("./lahman2013.sqlite")

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