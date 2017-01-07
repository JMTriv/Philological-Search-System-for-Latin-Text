
import pytest
import project1a_trivisonno_joseph as p1a



def test_connection():
    #test to ensure connection to the latin library is available
    #failure could indicate lack of internet connection or issue with the latin library
    import urllib2
    urllist = p1a.url_links
    urllist.append('http://thelatinlibrary.com/curtius.html')
    for l in urllist:
        response = urllib2.urlopen(l).getcode()#ensure correct response is received from website
        assert response == 200

def test_TableNotEmpty():
    #test to ensure database not empty
    assert p1a.dbSize('LatinText') > 0
    assert p1a.dbSize('LatinText_fts') > 0

def test_DBLength():
    #test to ensure the database is the correct size
    assert p1a.dbSize('LatinText') == len(p1a.tot_schema_list)
    assert p1a.dbSize('LatinText_fts') == len(p1a.tot_schema_list)

def test_numColumns():
    #test to ensure correct number of columns in the database
    import sqlite3
    conn = sqlite3.connect('LatinText.db')
    cur = conn.cursor()
    data = cur.execute('SELECT * FROM LatinText').fetchall()
    assert len(data[0]) == 9
    datafts = cur.execute('SELECT * FROM LatinText_fts').fetchall()
    assert len(datafts[0]) == 9
    
def test_numBooks():
    #test to ensure correct number of books in the database
    import sqlite3
    conn = sqlite3.connect('LatinText.db')
    cur = conn.cursor()
    numBooks = cur.execute('SELECT COUNT(DISTINCT book) FROM LatinText').fetchall()
    assert numBooks[0][0] == 8
    numBooksfts = cur.execute('SELECT COUNT(DISTINCT book) FROM LatinText_fts').fetchall()
    assert numBooksfts[0][0] == 8



 
        
