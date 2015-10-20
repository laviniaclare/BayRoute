##What is it?

BayRoute is an interactive map that allows users to select and view routes from various transit systems in the Bay Area.  When a transit line is selected, the entire route is displayed on the map, helping users visualize what destinations are accessible to them via public transportation.  Includes route data for all buses, shuttles, ferries and commuter trains in the 511.org data base.  Growing up in the Bay Area I was frequently frustrated with the lack of a unified transit map.  This project was my solution to that frustration. 

Screen shot showing dropdown selection by word search.
![alt text](https://github.com/laviniaclare/BayRoute/blob/master/Screen-Shots/Screen%20Shot%202014-08-05%20at%204.30.18%20PM.png)
Options can also be filtered by typing a route number in to the text search bar.
![alt text](https://github.com/laviniaclare/BayRoute/blob/master/Screen-Shots/Screen%20Shot%202014-08-05%20at%204.30.58%20PM.png)
Showing selection of all lines in the BART system.
![alt text](https://github.com/laviniaclare/BayRoute/blob/master/Screen-Shots/Screen%20Shot%202014-08-05%20at%205.01.48%20PM.png)

##Tech Stack
BayRoute is built using Python with a Flask framework and a Postgresql database.  All data was acquired from 511.org. The front end was built with the Mapbox API, including the mapbox.js library.  Bootstrap multi select was used to construct the user interface. Also used: JQuery, AJAX, Jinja, HTML, and CSS.

##Running the Code at Home
First off, I don't recommend trying to run this on your own computer because the database is too big to put on Github.  Which means that in order to run BayRoute from your computer you will first have to get all the data from 511.org, and then put it into a PostgreSQL database.  Which is a pain in the ass.  However, if you *really* want to play with BayRoute yourself and see what it does follow the instructions below.

####Step one: Getting the Data.
1. Go download the [Static Transit Data Feed Agreement](http://511.org/developer-resources_transit-data-feed.asp) from 511.org.
2. Print the form and fill it out
3. Mail the form back to 511.org (the address and instructions should be on the form and on the 511.org website as well)
4. Wait for 511.org to email you.  It took less than a week for me, but ymmv.
5. Once 511.org approves you for access to the data they will send you a bunch of CSV files.  For this project you want to use the ones in [General Transit Feed Specifications](https://developers.google.com/transit/gtfs/) format.  They will be in the GTFSdata file.  

Now you have the data, it's time to put it into a usable format.  We're going to use PostgreSQL.

####Step two: Putting the data into a database.

I used a modified version of a handy piece of code called [gtfs_SQL_importer](https://github.com/cbick/gtfs_SQL_importer) written by [cbick](https://github.com/cbick).  The orginal code makes a database for each agency in the 511.org data set.  I wanted one database with all the agencies, so I had make a few modifactions to make that happen, and to avoind primary key conflicts.  The modified verson that I used is included in this repo. 

1. If you haven't already, clone the BayRoute repo onto your local machine, make a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/), activate it, and then run ```pip install -r requirements.txt``` in your terminal (make sure you are in the correct directory first, of course).
2. Make a file in your local version of the BayRoute repo called "useful-docs", and put the GTFSTdata file you got from 511.org into that file.  Also, If you don't already have PostgreSQL on your local machine you should [download](http://www.postgresql.org/download/) it now.  Make sure it's running properly and everything then go on to the next step.
3. In your terminal type ```createdb transit``` to create the empty database where all the 
data will go.
4. In your terminal run parse_511_txt.py.  This function will print out the command you need to run to parse and load the data from 511.org.  Copy this output, past it into your terminal and then hit "enter" to run.
5. Open the "transit" database in PostgreSQL in your terminal (type ```psql transit```).
6. Copy the text from the file called "psql_indexes.sql" into your terminal.  This should create an index in the datatbase that makes some queries faster.

And now you should have a working database with all the correct data.  Yay!

####Step three: Actually running BayRoute on your local machine

This is the easy part. 

1. In your terminal, run "routes.py".  Make sure you're in the correct directory and all that first, of course.
2. Paste the address its running on into your browser.
3. You should see something like the pictures in the "Screen-Shots" folder.

####Step four: jk, there are no more steps.  Just have fun.

You can use the search bar in the menu to search for routes or agencies you are interested in seeing.  If you type in letters you will get mostly agencies.  If you type in numbers you will get all routes containing those digits.  I like to just scroll around and find transit sytems I've never heard of and check a bunch of boxes to see where they are.  If you type "free" in the search bar, you will get some of the free transit options around the Bay Area. 


