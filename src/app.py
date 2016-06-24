from flask import Flask
from flask_ask import Ask, statement
from src.static.rules import rules
from datetime import datetime

app = Flask(__name__)
ask = Ask(app, '/bot')

@ask.intent('GetRules')
def tellrules():
    return statement(rules)

@ask.intent('GetTrashMan', convert={'date':'date'})
def trashquery(date):
    if date == None:
        day = datetime.now().day
    else:
        day = date.day
    if 1 <= day <= 10:
        trash_man = 'Perret is the trash man'
    elif 11 <= day <= 19:
        trash_man= 'Woo is the trash man'
    else:
        trash_man = "Zhang is the trash man"
    return statement(trash_man)

@ask.intent('GetRecord')
def record(name, location):
    return statement("Got {} for mess in {}".format(name, location))

@ask.intent('GetTally')
def charge():
    return statement("Got it")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)