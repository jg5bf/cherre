#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 09:46:31 2019

@author: JWG
"""

import sqlite3
conn = sqlite3.connect('/Users/JWG/Downloads/ProgrammerTest/testdb.db') #replace with your db directory
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%'")
table_list = c.fetchall()
people = c.execute("SELECT * FROM people")
col_people = list(map(lambda x: x[0], people.description))

sites = c.execute("SELECT * FROM sites")
col_sites = list(map(lambda x: x[0], sites.description))

visits = c.execute("SELECT * FROM visits")
col_visits = list(map(lambda x: x[0], visits.description))
group_v = c.execute("SELECT personId, COUNT(personId) FROM visits GROUP BY personId").fetchall()

frequent_browsers = c.execute("SELECT * FROM frequent_browsers")
col_frequent_browsers = list(map(lambda x: x[0], frequent_browsers.description))

top10= c.execute("SELECT v.personId, \
                   COUNT(DISTINCT v.siteId) AS maxdiffsites \
                   FROM visits AS v \
                   LEFT JOIN sites AS s \
                   ON s.id = v.siteId \
                   GROUP BY v.personId\
                   ORDER BY maxdiffsites DESC LIMIT 10").fetchall()

c.executemany('INSERT INTO frequent_browsers VALUES (?,?)', top10)

top10name = c.execute("SELECT first_name || ' ' || last_name FROM people AS p\
                      INNER JOIN frequent_browsers as f\
                      ON p.id = f.person_id").fetchall()
conn.close()