import datetime
import sqlite3

from flask import Flask, render_template,request
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)


def cents_to_dollars(cents):
    return cents / 100


def iso_str_to_date_str(iso_string):
    datetime_ = datetime.datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S.%f")
    return str(datetime_.date())


@app.route('/')
def expenses():
    conn = sqlite3.connect('./interview-app.db')
    expenses_list = conn.execute(
        'SELECT created_datetime, serviced_datetime, amount, status FROM expenses').fetchall()

    expenses_list_formatted = []
    for expense in expenses_list:
        expenses_list_formatted.append([
            iso_str_to_date_str(expense[0]),
            expense[1],
            '${0:.2f}'.format(cents_to_dollars(expense[2])),
            expense[3]
        ])
    return render_template('expenses.html', expenses=expenses_list_formatted)


@app.route('/members')
def members():
    conn = sqlite3.connect('./interview-app.db')
    members_list = conn.execute(
        'SELECT EmployeeId,FirstName,LastName,EmailAddress FROM members').fetchall()

    members_list_formatted = []
   
    for member in members_list:
        members_list_formatted.append([
           member[0],
            member[1],
            member[2],
            member[3],
             "/ExpensesPerEmployee?EmployeeId={0}".format(member[0])
        ])
        
    
    print(members_list_formatted)

    return render_template('members.html', members=members_list_formatted)

@app.route('/ExpensesPerEmployee')
def ExpensesPerEmployee():
    conn = sqlite3.connect('./interview-app.db')
    expense_list_by_member = conn.execute(
        'SELECT a.EmployeeId,FirstName,LastName,EmailAddress,created_datetime, serviced_datetime, amount, status FROM expenses a , members b where a.EmployeeId = b.EmployeeId and a.EmployeeId = {0}'.format(request.args["EmployeeId"]) ).fetchall()

    expense_member_list_formatted = []
   
    for expense_list_per_member in expense_list_by_member:
        expense_member_list_formatted.append([
            expense_list_per_member[0],
             expense_list_per_member[1],
              expense_list_per_member[2],
               expense_list_per_member[3],
           iso_str_to_date_str(expense_list_per_member[4]),
            expense_list_per_member[5],
            '${0:.2f}'.format(cents_to_dollars(expense_list_per_member[6])),
            expense_list_per_member[7]
        ])

    return render_template('expenselistbymember.html', expensebymembers=expense_member_list_formatted)

if __name__ == '__main__':
    app.run(port=5001,debug=True)
