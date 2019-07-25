from flask import Flask, render_template
from itertools import groupby
import processing

years = []

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html", years=years)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/precision-ag-farm/<year>")
def mechFarm(year):
    index = getYearIndex(year)
    mech = years[index][1]
    mechFarm = templateInfo(mech)
    # Uncomment to test render_template output for errors and unexpected results
    #output = render_template("mechFarm.html", fields=mechFarm)
    #with open("test.html", "w") as f:
    #    f.write(output)
    return render_template("mechFarm.html", year=year, fields=mechFarm)

@app.route("/rice-farm/<year>")
def riceFarm(year):
    index = getYearIndex(year)
    rice = years[index][2]
    riceFarm = templateInfo(rice)
    return render_template("riceFarm.html", year=year, fields=riceFarm)

@app.route("/weed-farm/<year>")
def schoolFarm(year):
    index = getYearIndex(year)
    school = years[index][3]
    schoolFarm = templateInfo(school)
    return render_template("schoolFarm.html", year=year, fields=schoolFarm)

@app.route("/entire-area/<year>")
def entireFarm(year):
    index = getYearIndex(year)
    entire = years[index][4]
    entireFarm = templateInfo(entire)
    return render_template("entireFarm.html", year=year, fields=entireFarm)

@app.route("/irrigation-area/<year>")
def suiFarm(year):
    index = getYearIndex(year)
    sui = years[index][4]
    suiFarm = templateInfo(sui)
    return render_template("suiFarm.html", year=year, fields=suiFarm)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/precision-ag-farm/<year>/<index>")
def showMechField(year, index):
    i = getYearIndex(year)
    mech = years[i][1]
    mechIndex = int(index.split('-')[1])
    return render_template("fieldTemplate.html", fieldInfo=mech[mechIndex])

@app.route("/rice-farm/<year>/<index>")
def showRiceField(year, index):
    i = getYearIndex(year)
    rice = years[i][2]
    riceIndex = int(index.split('-')[1])
    return render_template("fieldTemplate.html", fieldInfo=rice[riceIndex])

@app.route("/weed-farm/<year>/<index>")
def showSchoolField(year, index):
    i = getYearIndex(year)
    school = years[i][3]
    schoolIndex = int(index.split('-')[1])
    return render_template("fieldTemplate.html", fieldInfo=school[schoolIndex])

@app.route("/entire-area/<year>/<index>")
def showEntireField(year, index):
    i = getYearIndex(year)
    entire = years[i][4]
    entireIndex = int(index.split('-')[1])
    return render_template("fieldTemplate.html", fieldInfo=entire[entireIndex])

@app.route("/irrigation-area/<year>/<index>")
def showSuiField(year, index):
    i = getYearIndex(year)
    sui = years[i][5]
    suiIndex = int(index.split('-')[1])
    return render_template("fieldTemplate.html", fieldInfo=sui[suiIndex])

@app.before_first_request
def generateData():
    data = processing.main()
    for year in data:
        mech = []
        rice = []
        school = []
        entire = []
        sui = []
        for field in year[1]:
            if "Mech Farm" in field:
                mech.append(field)
            if "Rice Farm" in field:
                rice.append(field)
            if "School Farm" in field:
                school.append(field)
            if "Entire Farm" in field:
                entire.append(field)
            if "Sui Farm" in field:
                sui.append(field)
        years.append((year[0], mech, rice, school, entire, sui))

def templateInfo(farm):
    results = []

    namesAndDates = set()
    for item in farm:
        namesAndDates.add((item[2], item[5]))

    for item in namesAndDates:
        lst = []
        for index, field in enumerate(farm):
            if item[0] == field[2] and item[1] == field[5]:
                lst.append((field[6], index))
        if lst:
            results.append((item[0], item[1], lst))

    results = sorted(results)

    group_list = []
    for key, group in groupby(results, lambda x: x[0]):
        group_list.append(list(group))

    info = [(x[0][0], [(y[1], y[2]) for y in x]) for x in group_list]
    return info

def getYearIndex(year):
    for index, y in enumerate(years):
        for item in y:
            if year == item:
                return index

if __name__ == "__main__":
    app.run(debug=True)
