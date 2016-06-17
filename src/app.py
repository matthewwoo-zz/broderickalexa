from flask import Flask, render_template
from flask_ask import Ask, statement


app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('GetRules')
def rules():
    return statement("Yo")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)