from flask import Flask, render_template             

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
	
@app.route("/mech-farm")
def mechFarm():
    return render_template("mechFarm.html")
	
@app.route("/rice-farm")
def riceFarm():
    return render_template("riceFarm.html")
	
@app.route("/16Rows-20180806-20m-RGB")
def sixteenRows2018080620mRGB():
    return render_template("16Rows-20180806-20m-RGB.html")

@app.route("/16Rows-20180806-20m-NIR")
def sixteenRows2018080620mNIR():
    return render_template("16Rows-20180806-20m-NIR.html")
	
@app.route("/16Rows-20180806-20m-Red")
def sixteenRows2018080620mRed():
    return render_template("16Rows-20180806-20m-Red.html")
	
@app.route("/16Rows-20180806-20m-Green")
def sixteenRows2018080620mGreen():
    return render_template("16Rows-20180806-20m-Green.html")
	
@app.route("/16Rows-20180806-20m-Blue")
def sixteenRows2018080620mBlue():
    return render_template("16Rows-20180806-20m-Blue.html")

@app.route("/Rice-20180806-90m-RGB")
def Rice2018080690mRGB():
    return render_template("Rice-20180806-90m-RGB.html")
	
@app.route("/Rice-20180806-90m-NIR")
def Rice2018080690mNIR():
    return render_template("Rice-20180806-90m-NIR.html")
	
@app.route("/Rice-20180806-90m-Red")
def Rice2018080690mRed():
    return render_template("Rice-20180806-90m-Red.html")
	
@app.route("/Rice-20180806-90m-Green")
def Rice2018080690mGreen():
    return render_template("Rice-20180806-90m-Green.html")
	
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
