from flask import Flask
from flask_ask import Ask, statement
from src.static.rules import rules
from datetime import datetime

app = Flask(__name__)
ask = Ask(app, '/bot')

@ask.intent('GetRules')
def tellrules():
    return statement(rules)

@ask.intent('GetTrashMan', mapping={'date' : 'Date'})
def trashquery(date):
    if date == None:
        day = datetime.now().day
    else:
        day = datetime(date).day
    if 1 <= day <= 10:
        trash_man = 'Perret'
    elif 11 <= day <= 19:
        trash_man= "Woo"
    else:
        trash_man = "Zhang"
    return statement(trash_man)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)