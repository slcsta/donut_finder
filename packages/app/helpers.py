from flask import redirect, render_template
from functools import wraps

# From CS50 Example

def apology(message, code=400):
    return render_template("apology.html", message=message, code=code), code