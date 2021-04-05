from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/Data-For-Majors")
def render_page1():
    return render_template('Data-For-Majors.html', firstfact = "", secondfact = "", thirdfact = "", majorsdata = get_major_options())

def get_major_options():
    with open('graduates.json') as demographics_data:
        majors = json.load(demographics_data)
    listOfMajors = []
    options = ""
    for major in majors:
        if major["Year"] == 2015:
            listOfMajors.append(major["Education"]["Major"])
    for item in listOfMajors:
        options += Markup("<option value=\"" + item + "\">" + item + "</option>")
    return options

if __name__=="__main__":
    app.run(debug=True)
