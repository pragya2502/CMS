# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 17:49:51 2020

@author: Pragya Sinha
"""

import sqlite3

conn = sqlite3.connect('complaints.db')
print('database created successfully')

conn.execute("CREATE TABLE complaints_info (first_name text not null, last_name text not null, city text not null, country text not null, Issue text not null, department text)")
print("Table created successfully")

conn.close()