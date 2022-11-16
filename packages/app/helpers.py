from flask import redirect, render_template
from functools import wraps

def apology(message, code=400):
    # def escape(s):
    #     for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
    #                      ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
    #         s = s.replace(old, new)
    #     return s
    return render_template("apology.html", message=message, code=code), code