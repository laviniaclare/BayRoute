##What is it?

BayRoute is an interactive map that allows users to select and view routes from various transit systems in the Bay Area.  When a transit line is selected, the entire route is displayed on the map, helping users visualize what destinations are accessible to them via public transportation.  Includes route data for all buses, shuttles, ferries and commuter trains in the 511.org data base.  Growing up in the Bay Area I was frequently frustrated with the lack of a unified transit map.  This project was my solution to that frustration. 

##Tech Stack
BayRoute is built using Python with a Flask framework and a Postgresql database.  All data was acquired from 511.org. The front end was built with the Mapbox API, including the mapbox.js library.  Bootstrap multi select was used to construct the user interface. Also used: JQuery, AJAX, Jinja, HTML, and CSS.

##Running the Code at Home
First off, I don't recommend trying to run this on your own computer because the database is too big to put on Github.  Which means that in order to run BayRoute from your computer you will first have to get all the data from 511.org, and then put it into a PostgreSQL database.  Which is a pain in the ass.  However, if you *really* want to play BayRoute yourself and see what it does follow the instructions below.

####Step one: Getting the Data.
1. Go download the [Static Transit Data Feed Agreement](http://511.org/developer-resources_transit-data-feed.asp) from 511.org.
2. Print the form an fill it out
3. Mail the form back to 511.org (the address and instructions should be on the form and on the 511.org website as well)
4. Wait for 511.org to email you.  It took less than a week for me, but ymmv.
5. Once 511.org approves you for access to the data they will send you a bunch of CSV files.  For this project you want to use the ones in [General Transit Feed Specifications](https://developers.google.com/transit/gtfs/) format.  They will be in the GTFSdata file.  

Now you have the data, it's time to put it into a usable format.  We're going to use PostgreSQL.

####Step two: Putting the data into a database.

I used a modified version of a handy piece of code called [gtfs_SQL_importer](https://github.com/cbick/gtfs_SQL_importer) written by [cbick](https://github.com/cbick).  The code makes a database for each agency in the 511.org data set.  I wanted one database with all the agencies, so I had make a few modifactions to make that happen, and to avoind primary key conflicts.  The modified verson that I used is included in this repo. 

