import pandas as pd
from flask import Flask, jsonify, render_template, request, redirect, abort, make_response
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import scrape_nasa

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/nasa_app")


@app.route("/")
def index():
    input_data = mongo.db.nasa.find_one()
    
  #  landing_page = '''<h1>Deep Space Network API</h1>
   # <p> Available links<p>
    #<p> /api/v1/all </p>
   # <p> /api/v1/active</p>'''

    return render_template("index.html", input_data=input_data)  

@app.route("/scrape")
def scrape():
    nasa_data = scrape_nasa.scrape_info()

    mongo.db.nasa.update({}, nasa_data, upsert=True)

    return redirect("/")

@app.route("/api/v1/all")
def all():

    full = mongo.db.nasa.find_one({})

    return jsonify(list(full['Mission_titles']['Mission']))
   # return render_template("index.html", input_data=full_data)  

if __name__ == "__main__":
    app.run(debug=True)

