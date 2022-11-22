# Connect to the database

import pymongo

client = pymongo.MongoClient("mongodb+srv://dftML:dftML@stano.mez9zwp.mongodb.net/?retryWrites=true&w=majority")
client.Test
database = client['stanie']
collection = database['Bank-Data']
collection.drop()

# Get the data using URL
import pandas as pd


def Source_Database():
    df1 = pd.read_csv("https://raw.githubusercontent.com/dftml/Database-Connect/main/bank-full.csv", sep=";")
    df1.insert(0, "_id", range(0, len(df1)))

    # Insert into database by converting a dictonary
    for row in range(len(df1)):
        # convert into str & capture the values
        instances = [str(value) for value in list(df1.iloc[row].values)]

        # capture the keys of dictonary
        attributes = list(df1.iloc[row].index)

        # Convert it into dictonary
        data = dict(zip(attributes, instances))
        collection.insert_one(data)

    return list(collection.find())


# Service Provider

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/mongodata", methods=["POST"])
def getdata():
    data = Source_Database()
    if request.method == "POST":
        return jsonify(str(data))


if __name__ == "__main__":
    app.run()
