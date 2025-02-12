from flask import Flask , render_template

app = Flask(__name__)

#  render_template grabs the html code and renders that as the web page

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/forecast")
def forecast():
    return render_template("forecast.html")

if __name__ == "__main__":
    app.run()