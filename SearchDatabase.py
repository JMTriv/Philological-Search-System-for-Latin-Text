#!/usr/bin/python
# coding=utf-8
# ^^ because https://www.python.org/dev/peps/pep-0263/

from __future__ import division


def bookNames():
    #Searches fts table for distinct book names and
    #stores them in a list called books
    import sqlite3
    conn = sqlite3.connect('LatinText.db')
    cur = conn.cursor()
    books = []
    try:
        cur.execute("SELECT DISTINCT book FROM LatinText_fts")
        results = cur.fetchall()
        for r in results:
            books.append(r[0])
    except sqlite3.Error as er:
        print ('er:', er.message)
        conn.rollback()
        print('error')  
    conn.close()
    return books

def keywordSearchLat(lat_keyword):
    #Takes input of a latin word or phrase searches fts table for
    #passages that contain the word or phrase
    #returns all passages with the phrase and creates a bar chart with the
    #number of occurence by book for the phrase
    import matplotlib as plt
    import sqlite3
    conn = sqlite3.connect('LatinText.db')
    cur = conn.cursor()
    data = []#data returned from fts search
    chart_data = []#data necessary to create bar chart
    
    for b in bookNames():
        #sqlite fts query by book for the phrase 
        search = cur.execute("SELECT * FROM LatinText_fts WHERE book = '" + b + "' AND passage MATCH '" + lat_keyword + "'").fetchall()
        for s in search:
            data.append(s)
        num = len(search)#number of results
        result = (b, num)
        if num > 0:#only interested in books that contain the phrase
            chart_data.append(result)

    if len(data)==0:
        #if phrase is not found in the text, return a message and dont perform
        #any more operations in this function
        print(lat_keyword + ' not found in text')
        return
    
    info = data[0]
    title = info[0]
    author = info[3]
    date = info[4]
    #since all passages have the same Title, Author, Date, and Language,
    #only print this info once at the top of the results
    print('\nTitle: ' + title)
    print('\nAuthor: ' + author)
    print('\nDate: ' + date)
    print('\nLanguage: Latin\n')
    
    chartData(chart_data, lat_keyword)#create bar chart of results

    for d in data:#print results
        passage = d[7]
        passage.replace(u'\x97','--')
        print('\nBook: ' + str(d[1]))
        print('\nChapter: ' + str(d[5]))
        print('\nParagraph: ' + str(d[6]))
        print('\nLink: ' + str(d[8]))
        print('\nPassage:\n\t' + passage)

def keywordSearchEng(eng_keyword):
    #Takes input of an english word or phrase and translates it to latin.
    #Then, searches fts table for passages that contain the latin word or phrase
    #returns all passages with the phrase and creates a bar chart with the
    #number of occurence by book for the phrase
    import subprocess
    import json
    import sqlite3

    conn = sqlite3.connect('LatinText.db')
    cur = conn.cursor()
    #Linux Command Line command to utilize the mymemory.translated.net api
    #to translate word or phrase from english to latin
    lin_input = "wget -O - 'http://api.mymemory.translated.net/get?q=" + eng_keyword + "&langpair=en|la' | python -m json.tool"

    p = subprocess.Popen(lin_input, shell = True, stdout = subprocess.PIPE)
    out = p.communicate()[0]#returns the output of the Linux Command Line command
    parsed = json.loads(out)#parse the json data
    responseData = parsed['responseData']#parse for responseData
    translatedText = responseData['translatedText']#parse for the translated word
    print(eng_keyword + ' translates to ' + translatedText + ' in Latin\n')#print latin translation of the english word
    chart_data = []#data necessary to create bar chart
    data = []#data returned from fts search
    for b in bookNames():
        #sqlite fts query by book for the translated phrase
        search = cur.execute("SELECT * FROM LatinText_fts WHERE book = '" + b + "' AND passage MATCH '" + translatedText + "'").fetchall()
        for s in search:
            data.append(s)
        num = len(search)
        if num > 0:#only interested in books where the phrase appears
            result = (b, num)
            chart_data.append(result)
            
        
    if len(data)==0:
        #if translated phrase is not found in the text, return a message and
        #dont perform any more operations in this function
        print(translatedText + ' not found in text')
        return

    #since all passages have the same Title, Author, Date, and Language,
    #only print this info once at the top of the results
    info = data[0]
    title = info[0]
    author = info[3]
    date = info[4]
    print('\nTitle: ' + title)
    print('\nAuthor: ' + author)
    print('\nDate: ' + date)
    print('\nLanguage: Latin\n')
    
    chartData(chart_data, translatedText)#create bar chart of results
    print len(data)
    for d in data: #print results
        passage = d[7]
        passage.replace(u'\x97','--')
        print('\nBook: ' + str(d[1]))
        print('\nChapter: ' + str(d[5]))
        print('\nParagraph: ' + str(d[6]))
        print('\nLink: ' + str(d[8]))
        print('\nPassage:\n\t' + passage)

def chartData(data, keyword):
    #Takes input of the results of the fts search and the phrase that was searched for
    #and creates bar chart of occurences by book for the phrase
    from matplotlib import pyplot as plt
    import numpy as np
    import math
    
    data = sorted(data, key=lambda x: x[1], reverse=True)
    info = []#number of occurences 
    books = []#list of books
    for d in data:
        info.append(d[1])
        b = d[0]
        books.append(b[b.find('LIBER'):])#Use only book number for label since name is the same for all books
    
    #create chart
    plt.close()
    fig = plt.figure()
    width = 0.4
    ind = np.arange(len(books))
    plt.bar(ind, info, width=width)
    plt.xticks(ind + width/2., books)
    plt.yticks(np.arange(0,max(info)*2,math.ceil(max(info)/5)))
    plt.ylabel('Number of Occurences')
    plt.xlabel('Books')
    plt.title('Occurences of "' + keyword + '" by book in Curtius Rufus (Latin)')
    fig.autofmt_xdate()
    plt.show(block=False)#display plot, and continue with program

def part2():
    #Creates UI to perform the required actions for phase 2 of this project

    #Asks user to input language
    language = raw_input('Enter Language (Type E for English or L for Latin): ')
    #Only looks at first character input to determine language, accepts both lower and upper case characters
    if (language[0] == 'E' or language[0] == 'e'):
        #If user chooses to enter an english phrase,
        #Perform the keywordSearchEng function
        print('\nYou have selected English\n')
        word = raw_input('\nEnter the word you would like to search: ')
        keywordSearchEng(word)
        
    elif (language[0] == 'L' or language[0] == 'l'):
        #If user chooses to enter a latin phrase,
        #Perform the keywordSearchLat function
        print('\nYou have selected Latin\n')
        word = raw_input('\nEnter the word you would like to search: ')
        keywordSearchLat(word)
        
    else:
        #If user enters invalid language, print error 
        print('Invalid Language. Please Try Again.')


while True:#Loop part 2 until user decides to end.
    part2()
    cont = raw_input('\nWould you like to continue? Enter Y or Yes or N for No: ')
    if (cont[0] == 'N' or cont == 'n'):
        break
    

        
        
                
        

