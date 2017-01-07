#!/usr/bin/python
# coding=utf-8
# ^^ because https://www.python.org/dev/peps/pep-0263/


def parse_text(title, author, dates, url):
    #parses html from given url, identifying book book name, chapter, verse and passage
    #each paragraph is considered to be a verse
    #title, book, author, date, chapter, verse, passage, and link are all defined in the project 1, phase 1 description

    from bs4 import BeautifulSoup
    import urllib2
    
    language = 'latin'#entire text is in latin
    verse = 1

    schema_list = [] #store all tuples in schema_list
    
    content = urllib2.urlopen(url)#retreive html from website
    content = content.read().decode('utf-8','replace')
    content = content.replace(',&#151;',' --')#emdash is incorrectly encoded in cp-1252 on website
    
    soup = BeautifulSoup(content)#use BeautifulSoup to parse html

    book = soup.p.text.strip()#the first paragraph is the book title
    
    for p in soup.body.find_all('p')[2:-2]: #parse contents of body to get the passages
        if p.find('b'):#locate new chapters
            chapter = p.find('b').text.strip() 
            verse = 1
            p.find('b').replaceWith('')#do not want to include chapter in in passages as it is its own entry
               
        
        passage = p.text.strip()
        schema = (title, book, language, author, dates, chapter, verse, passage, url)#store all required info in tuple

        schema_list.append(schema)#add tuple to schema_list
            
        verse += 1#increment verse
                    
    return schema_list
        

def sqlCreateTable(dbname, tablename):
    #creates a table tablename in in database dbname
    #dbname is a string that is the name of the database and has a .db extension
    #tablename is a string that is the name of the table to create
    import sqlite3
    conn = sqlite3.connect(dbname)#connects to dbname
    #creates table tablename
    conn.execute('CREATE TABLE ' + tablename + '''(
                 title TEXT NOT NULL,
                 book TEXT,
                 language TEXT,
                 author TEXT,
                 date TEXT,
                 chapter TEXT,
                 verse TEXT,
                 passage TEXT,
                 link TEXT NOT NULL);''')
    conn.close()#close connection

def sqlPopulateTable(schema):
    #populates database
    import sqlite3
    conn = sqlite3.connect('LatinText.db')#connect to LatinText.db
    cursor = conn.cursor()#create cursor
    for s in schema:#insert tuples from list into database
        try:
            cursor.execute('INSERT INTO LatinText VALUES(?,?,?,?,?,?,?,?,?)',
                           (s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8]))
            
        except sqlite3.Error as er:
            print ('er:', er.message)
            conn.rollback()
            print('error')
    conn.commit()#commit changes
    conn.close()#close database
        
def sqlEmptyTable(dbname, tablename):
    #empties tablename from, dbname of all data 
    import sqlite3
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    conn.execute('DELETE FROM ' + tablename)
    conn.commit()
    conn.close()

def dbSize(tablename):
    #returns size of database
    import sqlite3
    conn = sqlite3.connect('LatinText.db')
    cursor = conn.cursor()
    result = cursor.execute('SELECT COUNT(*) FROM ' + tablename)
    data = cursor.fetchall()
    return data[0][0]

def tableExist():
    #determines if LatinText exists
    import sqlite3
    conn = sqlite3.connect('LatinText.db')
    cur = conn.cursor()
    try:
        cur.execute('SELECT COUNT(*) FROM LatinText')
        return True
    except:
        return False



def create_ftsTable():
    #creates full text search table over LatinText
    import sqlite3

    conn = sqlite3.connect('LatinText.db')
    cur = conn.cursor()
    try:
        conn.execute("CREATE VIRTUAL TABLE LatinText_fts USING fts4(title, book, language, author, date, chapter, verse, passage, link)")
        conn.execute("INSERT INTO LatinText_fts SELECT * FROM LatinText")
        conn.commit()
    except sqlite3.Error as er:
                print ('er:', er.message)
                conn.rollback()
                print('error')    
    conn.close()

def ftsExist():
    #determines if fts table exists
    import sqlite3
    conn = sqlite3.connect('LatinText.db')
    cur = conn.cursor()
    try:
        cur.execute('SELECT COUNT(*) FROM LatinText_fts')
        return True
    except:
        return False
    
def drop_ftsTable():
    #drops fts table
    import sqlite3
    
    conn = sqlite3.connect('LatinText.db')
    cur = conn.cursor()
    try:
        conn.execute("DROP TABLE LatinText_fts")
    except sqlite3.Error as er:
                print ('er:', er.message)
                conn.rollback()
                print('error')   
    conn.close()

import urllib2
from bs4 import BeautifulSoup

if tableExist() == False:
    sqlCreateTable('LatinText.db','LatinText')

content = urllib2.urlopen('http://thelatinlibrary.com/curtius.html')#opens connection to curtius in the Latin Library
soup = BeautifulSoup(content.read().decode('utf-8','replace'))#use BeautifulSoup to parse html
title = soup.h1.text.strip()#title of document
date = soup.h2.text.strip('(').strip(')')#date written
author = 'UNKNOWN'#author is not given on The Latin Library

href = soup.find_all('a',href=True)#get hrefs from html
url_links = []#create list of book links
for a in href[:-2]:
    link = 'http://thelatinlibrary.com/' + a['href']#get links to the books
    url_links.append(link)#add link to list of books

tot_schema_list = []#used for combining the lists of tuples returned by parse_text

for link in url_links:#run parse_text on each link
    schema_list = parse_text(title, author, date, link)
    for s in schema_list:
        tot_schema_list.append(s)

if dbSize('LatinText') == 0:#populate database if it is empty
    sqlPopulateTable(tot_schema_list)

if ftsExist() == False:#create fts table if it does not already exist
    create_ftsTable()


       
        
