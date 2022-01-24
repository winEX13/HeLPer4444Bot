# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 20:36:56 2021

@author: winEX
"""

import sqlite3
from xlsxwriter.workbook import Workbook
import csv

# workbook = Workbook('export.xlsx')
# worksheet = workbook.add_worksheet()

# conn = sqlite3.connect(':memory:')
# conn = sqlite3.connect('database.db')
# cur = conn.cursor()
    
def exelConnect(name):
    global workbook
    global worksheet
    
    workbook = Workbook(name + '.xlsx')
    worksheet = workbook.add_worksheet()

def sqlConnect(name):
    global conn
    global cur

# conn = sqlite3.connect(':memory:')
    conn = sqlite3.connect(str(name) + '.db', check_same_thread=False)
    cur = conn.cursor()

def sqlCreate(name, items):
    table_name = 'CREATE TABLE IF NOT EXISTS ' + name + '(id INT PRIMARY KEY, ' + ', '.join(items) + ')'
    cur.execute(table_name)
    conn.commit()
    table_name = 'SELECT * FROM ' + name
    cur.execute(table_name)
    # print(cur.fetchall())

def sqlAdd(name, item, count):
    count_items = []
    for i in range(count - 1):
        count_items.append('?')
    table_name = 'INSERT INTO ' + name + ' VALUES(' + ', '.join(count_items) + ', ?)'
    # cur.execute(table_name, item)
    try:
        cur.execute(table_name, item)
    except:
        sqlDel(name, 'id = ' + str(item[0]))
        cur.execute(table_name, item)
        
    conn.commit()
    table_name = 'SELECT * FROM ' + name
    cur.execute(table_name)
    # print(len(cur.fetchall()))
    # print(cur.fetchall()[int(item[0]) - 1])
    # print(cur.fetchall()[1])
    # print(cur.fetchall()[len(cur.fetchall()) - 1])

def sqlFind(name, param1, param2):
    table_name = 'SELECT ' + param1 + ' FROM ' + name + ' WHERE ' + param2
    # print(table_name)
    cur.execute(table_name)
    # print(cur.fetchall())
    return(cur.fetchall())
    # conn.commit()

def sqlUpd(name, param1, param2):
    table_name = 'UPDATE ' + name + ' SET ' + param1 + ' WHERE ' + param2
    # print(table_name)
    cur.execute(table_name)
    conn.commit()
    
def sqlDel(name, param):
    table = 'DELETE FROM ' + name + ' WHERE ' + param
    cur.execute(table)
    conn.commit()
    table_name = 'SELECT * FROM ' + name
    cur.execute(table_name)
    # print(cur.fetchall())
    
def sqlShow(name):
    table_name = 'SELECT * FROM ' + name
    cur.execute(table_name)
    # print(cur.fetchall())
    return(cur.fetchall())
    
def sqlSortA(name, param):
    table_name = 'SELECT * FROM ' + name + ' ORDER BY ' + param + ' ASC'
    cur.execute(table_name)
    conn.commit()
    
def sqlSortZ(name, param):
    table_name = 'SELECT * FROM ' + name + ' ORDER BY ' + param + ' DESC'
    cur.execute(table_name)
    conn.commit()
    
def sqlToExel(name):
    table = 'SELECT * FROM ' + name
    for y, row in enumerate(cur.execute(table)):
        for x, value in enumerate(row):
            worksheet.write(y, x, value)
    # workbook.close()
    # workbook = Workbook('export.xlsx')
    # worksheet = workbook.add_worksheet()
    
def sqlDisconnect():
    cur.close()
    
def exelDisconnect():
    workbook.close()

# l = ['fname TEXT', 'lname TEXT', 'city TEXT']
# sqlConnect('users')
# sqlCreate('users', l)
# with open('users.csv', newline='') as File:  
#     reader = csv.reader(File)
#     for row in reader:
        # user = [row[0], row[1], row[2], row[4]]
        # sqlAdd('users', user, 4)
        # exelConnect('export_u')
        # sqlToExel('users')
        # exelDisconnect()
        # print(row)

# user = ['00007', 'Lois', 'Lane', 'Female']
# l = ['fname TEXT', 'lname TEXT', 'gender TEXT']
# sqlConnect('bot_db')
# print(sqlShow('dict'))
# sqlDel('users', 'lname = "GivenName"')
# sqlFind('users', 'fname, city', 'lname = "GivenName"')
# print(sqlShow('users')[0][1])
# sqlCreate('users', l)
# sqlAdd('users', user, 4)
# sqlSortA('users', 'id')
# sqlToExel('users')
# sqlShow('users')

# one_result = cur.fetchone()
# three_results = cur.fetchmany(3)
# all_results = cur.fetchall()

