# Philological-Search-System-for-Latin-Text

I have created a database with the contents of the Latin Book QVINTVS CVRTIVS RVFVS (Quintus Curtius Rufus) broken up into paragraphs. The contents of the book can be found at http://thelatinlibrary.com/curtius.html. The links contained on this page were parsed using the BeautifulSoup package in python, and the contents were added to a SQLite database 'LatinText.db' in a table called 'LatinText', which uses  Schema (title|book|language|author|dates|chapter|verse|passage|link). All information for this schema was parsed from The Latin Library webpage with the exception of verse, which was incremented for each new passage, and reset for each chapter. Once the database was created, a Full Text Search (FTS) system was created across the passage attribute. This system will be used in Part 2 to perform queries for latin phrases input by the user.

An interface was created that allows a user to perform either a latin or english term search of the FTS table. The search will return paragraphs where the search term appears as the original link to where the term appears. The english search will additionally display the latin translation of the search term. Every search will print the Title, Author, Dates, and Language at the top of the page, with the English search also printing the latin translation. These will only be printed once, since they do not change for the entire text. For each instance of the search term, the Book, Chapter, Paragraph Number, Link, and Passage Content will be displayed. In addition to the paragraphs where the term appears, a usage chart will be created for the given search term that displays how often it appears in each book. Only books where the search term appears will be displayed on the usage chart. 

Suffixing a term with a * (eg Alexand*) will search for the term with any suffix (eg Alexander and Alexandri will both be returned).
Placing a phrase in quotations will search for the words in the specific order given. Otherwise, any passage that contains all of the words in any order and not necessarily one after the other will be returned. 

To translate english terms into latin, this project utilizes the mymemory.translated.net API. The Linux wget command is used to get a json string from the API, which is then parsed to determine the translation. It should be noted that this API does not do a good job translating multiple word english phrases into latin, which could affect the results of the search, most likely resulting in the phrase not being found in the text when it should be. This is a limitation with the translated.net API, and not an issue with the database. 
The Usage Chart displays the number of times the term appears on the y-axis with the Book name on the x-axis. Only the book number is displayed across the x-axis, since all of the books have the same title otherwise (QUINTI CURTI RUFI HISTORIAE ALEXANDRI MAGNI). The x-axis of the chart is sorted by height, with the book in which the search term appears in the most paragraphs on the left.


A narrated video displaying this project can be found at https://youtu.be/TwsPDM-TxlQ

In the video, the results for the following terms are shown:

Language	Term
Latin		Alexand*
Latin		Macedon*
English		Phalanx
English		Army
Latin		Tum Quidem
