# Donut Finder

#### Video Demo: <URL HERE>
#### Description

I developed Donut_Finder as my final project for CS50.

Donut_Finder is a web-based application that employs data from the Yelp Fusion API to search and locate donut shops by city and state.  

The Donut_Finder repository is structured as a single-package monorepo configured with PNPM, ASDF, and Changesets. The app-centric packages folder contains the buildable and deployable applications for the project including the Python code for the Flask web server. 

When a user navigates to Donut_Finder, the landing page defaults to displaying all of the donut shops stored in the SQLite database. From there, a user can filter donut shops by location. The landing page has a search form requiring an inputted city and a selected state from a pre-populated drop-down list. When submitted, the form retrieves the filtered set of data from the database and then renders the filtered list of donut shops according to the search.

Donut_Finder also makes use of APScheduler to carry out Yelp Fusion API calls. The scheduler runs in the background inside of the Flask app and schedules a job queu that executes Yelp API calls to fetch donut shops by state. API calls by state are paginated, making several calls to retrieve more records. With every data retrieval job, data is upserted into the database.

Embed link to video walk through here

# Installation

Instructions for installing
Examples


# Links

#### A list of links to relevant documentation for this design:

[Python Documentation](https://docs.python.org/3/)
[Flask Documentation](https://flask.palletsprojects.com/en/2.2.x/)
[Jinja Documentation](https://jinja.palletsprojects.com/en/3.1.x/)
[SQLite Documentation](https://www.sqlite.org/docs.html)
[Yelp Fusion API](https://docs.developer.yelp.com/docs/fusion-intro)
[APScheduler Documentation](https://apscheduler.readthedocs.io/en/latest/modules/schedulers/background.html)
[CS50 Final Project Guidelines](https://cs50.harvard.edu/x/2022/project/)

# Contributing

# Assumptions

# Questions

If you have any questions about the project, you can reach me here:
Email: sarahlchavez@gmail.com


