from flask import redirect, render_template

def apology(message, code=400):
    return render_template("apology.html", top=code), code