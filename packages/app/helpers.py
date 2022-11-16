from flask import redirect, render_template
from functools import wraps

# From CS50 Example

def apology(message, states, code=400):
    return render_template("apology.html", message=message, states=states, code=code)