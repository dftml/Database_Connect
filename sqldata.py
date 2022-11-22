import mysql.connector as conn
import pandas as pd

connect = conn.connect(host="localhost", user="root", password="dftML@1998")
cursor = connect.cursor()

def Source_Database():
    # checking database
    cursor.execute("show databases")
    l1 = [i[0] for i in cursor.fetchall()]
    if "stanie" in l1:
        cursor.execute("drop database stanie")                        # existing database raise error

    cursor.execute("create database stanie")

    df1 = pd.read_csv("https://raw.githubusercontent.com/dftml/Database-Connect/main/bank-full.csv", sep=",")
    schema = ",".join([ f"{i} int(5)" if df1[i].dtypes != "O" else f"{i} varchar(20)"for i in df1.columns ])
    schema = schema.replace("default", "defaults")                    # default column is built_in functions
    cursor.execute(f"create table stanie.bank ({schema})")

    for i in range(len(df1)):
        cursor.execute(f"insert into stanie.bank values {tuple(df1.iloc[i].values)}")

    cursor.execute("select * from stanie.bank")
    data = cursor.fetchall()

    return data


from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/datagain", methods=["POST"])
def getdata():
    data1 = Source_Database()
    if request.method == "POST":
        return jsonify(data1)

if __name__=="__main__":
    app.run()