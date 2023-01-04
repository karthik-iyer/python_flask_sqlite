from flask import Flask, render_template, request
import sqlite3
import os

currentdirectory = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)


@app.route("/")
def main():
    return render_template("phonebook.html")

@app.route("/", methods = ["POST"])
def phonebook():
    name = "TestName1"
    phonenumber = "444444444"
    connection = sqlite3.connect(currentdirectory + "\phonebook.db")
    cursor = connection.cursor()
    query1 = "INSERT INTO PhoneBook VALUES({n},{pnm})".format(n = name, pnm = phonenumber)
    cursor.execute(query1)
    connection.commit()




if __name__ == "__main__":
    app.run()
