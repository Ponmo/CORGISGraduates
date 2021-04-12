from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/Data-For-Majors")
def render_page1():
    return render_template('Data-For-Majors.html', firstfact = "", secondfact = "", thirdfact = "", majorsdata = get_major_options(), graphdata = "", graph = "")

@app.route("/response")
def return_data():
    major_selected = request.args['major']
    return render_template('Data-For-Majors.html', major = major_selected, firstfact = salaries(major_selected), secondfact = demographics(major_selected), thirdfact = education_type(major_selected), majorsdata = get_major_options(), graphdata = get_graph_data(major_selected), graph = Markup('<div id="chartContainer" style="height: 370px; width: 100%;"></div><script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>'))

def salaries(selected_major):
    with open('graduates.json') as demographics_data:
        majors = json.load(demographics_data)
    mean_salary = 0.0
    median_salary = 0.0
    standard_deviation = 0.0
    for major in majors:
        if major["Year"] == 2015 and major["Education"]["Major"] == selected_major:
            mean_salary = str(major["Salaries"]["Mean"])
            median_salary = str(major["Salaries"]["Median"])
            standard_deviation = str(major["Salaries"]["Standard Deviation"])
    return "Salary: The mean salary for people with degrees in " + selected_major + " is $" + mean_salary + ". " + "The median salary is $" + median_salary + ". The standard deviation of the salaries data is $" + standard_deviation + "."

def demographics(selected_major):
    with open('graduates.json') as demographics_data:
        majors = json.load(demographics_data)
    asians = 0.0
    whites = 0.0
    minorities = 0.0
    females = 0.0
    males = 0.0
    for major in majors:
        if major["Year"] == 2015 and major["Education"]["Major"] == selected_major:
            asians = str(major["Demographics"]["Ethnicity"]["Asians"])
            whites = str(major["Demographics"]["Ethnicity"]["Whites"])
            minorities = str(major["Demographics"]["Ethnicity"]["Minorities"])
            females = str(major["Demographics"]["Gender"]["Females"])
            males = str(major["Demographics"]["Gender"]["Males"])
    return "Diversity: In 2015, there were " + whites + " whites with a degree in this major, " + asians + " Asians, and " + minorities + " other minorities. There were " + females + " females and " + males + " males."

def education_type(selected_major):
    with open('graduates.json') as demographics_data:
        majors = json.load(demographics_data)
    total = 0.0
    bachelors = 0.0
    doctorates = 0.0
    masters = 0.0
    professionals = 0.0
    for major in majors:
        if major["Year"] == 2015 and major["Education"]["Major"] == selected_major:
            total = str(major["Demographics"]["Total"])
            bachelors = str(major["Education"]["Degrees"]["Bachelors"])
            doctorates = str(major["Education"]["Degrees"]["Doctorates"])
            masters = str(major["Education"]["Degrees"]["Masters"])
            professionals = str(major["Education"]["Degrees"]["Professionals"])
    return "Education: There were a total of " + total + " people with a degree in this major in 2015 (see FAQ). There were " + professionals + " people with professional degrees, " + bachelors + " people with a bachelor's degree, " + masters + " people with a master's degree, and " + doctorates + " people with a doctoral degree."     
    
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

