# Donut Finder

#### Video Demo: <URL HERE>
#### Description

I developed Donut_Finder as my final project for CS50.

Donut_Finder is a web-based application that employs data from the Yelp Fusion API to locate donut shops by city and state.  

The Donut_Finder repository is structured as a single-package monorepo configured with PNPM as the package manager, ASDF, and Changesets. The app-centric packages folder contains the buildable and deployable applications for the project including the Python code for the Flask web server. 

When a user navigates to Donut_Finder, the page displays all of the donut shops stored in the SQLite database on index.html. From there, a user can input a city and select a state from a pre-populated drop-down list to filter donut shops by location. If filtering inputs are submitted, an SQLite query is executed to get the matching donut shops. Flask then renders the matching donut shops on index.html. If a submitted query return no results, Flask notifies the user by rendering an apology. 

In the background of the app, APScheduler is employed to concurrently fetch data from the Yelp Fusion API. BackgroundScheduler uses a separate thread inside the app by initiating a scheduler. The scheduler adds jobs to a queu and then each job executes according to its assigned interval and task. Each job retrieves donut shop data on a per state basis from the API. With every retrieval, data is upserted into the database.

Embed link to video walk through here

# Installation

Instructions for installing

Once you have cloned the repository, navigate to the root project directory and run 

pnpm install

This will install all dependencies.

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


