#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 19:29:44 2019

@author: atta


COMMANDS :
    
    cd $DIR/db_scripts/
    python create_db.py

"""

import sqlite3

conn = sqlite3.connect('../db/face_weights.sqlite')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS face_encodings;""")
cur.execute("""CREATE TABLE face_encodings (
            id INTEGER PRIMARY KEY,user_id VARCHAR ,
            encoding array);""")
conn.commit()

conn.close()