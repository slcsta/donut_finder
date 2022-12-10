# Donut Finder

#### Description

I developed Donut_Finder as my final project for CS50.

Donut_Finder is a web-based application that employs data from the Yelp Fusion API to locate donut shops by city and state.  

The Donut_Finder repository is structured as a single-package monorepo configured with PNPM as the package manager, ASDF, and Changesets. The app-centric packages folder contains the buildable and deployable applications for the project including the Python code for the Flask web server. 

When a user navigates to Donut_Finder, the page displays all of the donut shops stored in the SQLite database on index.html. From there, a user can filter donut shops by location by inputting a city and selecting a state from the pre-populated drop-down list. If filtering inputs are submitted, an SQLite query is executed to get the matching donut shops. Flask then renders the matching donut shops on index.html. If a query returns no results, Flask notifies the user by rendering an apology. 

In the background of the app, APScheduler is used to concurrently fetch data from the Yelp Fusion API. BackgroundScheduler runs a separate thread inside the app by initiating a scheduler to add jobs to a queu. Each job retrieves donut shop data on a per state basis from the Yelp Fusion API. The API returns up to 50 results at a time. The API's request parameters don't explicitly include pagination, however, using a combination of the parameters limit and offset can create a pagination effect. Limit controls the number of results returned, and offset determines from which point the next results will be returned. Currently, the scheduler sets job's limit to 20 and offset to 0, where offset increments by limit's value of 20 in a loop ranging from 0 to 40 for each job. Limit and offset can be manipulated to return different results.

#### Video Demo: 
<https://youtu.be/8hzaBFgAxV0>

# Installation

Once you have cloned the repository, navigate to the root project directory and run: 

`pnpm install`

This will install all dependencies for the project.

You will need your own Yelp Fusion API key. Head to the link below and follow all instructions for setting up your access to the Yelp Fusion API:

[Yelp Fusion API](https://docs.developer.yelp.com/docs/fusion-intro)

Activate the virtual environment from the root folder:

`. venv/bin/activate`

Navigate to the app folder and run the flask app:

`flask --app app run`

# Links

#### A list of links to relevant documentation for this design:

[Python Documentation](https://docs.python.org/3/)
[Flask Documentation](https://flask.palletsprojects.com/en/2.2.x/)
[Jinja Documentation](https://jinja.palletsprojects.com/en/3.1.x/)
[SQLite Documentation](https://www.sqlite.org/docs.html)
[Yelp Fusion API](https://docs.developer.yelp.com/docs/fusion-intro)
[APScheduler Documentation](https://apscheduler.readthedocs.io/en/latest/modules/schedulers/background.html)
[CS50 Final Project Guidelines](https://cs50.harvard.edu/x/2022/project/)

# Contributors


# Questions

If you have any questions about the project, you can reach me here:
sarahlchavez@gmail.com


