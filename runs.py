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

SELECT SO as strikeouts, H as hits FROM Batting

"""
df = pandas.read_sql(query, connection)

connection.close()
