from flask import Flask
from flask_ask import Ask, statement


app = Flask(__name__)
ask = Ask(app, '/bot')

@ask.intent('GetRules')
def rules():
    return statement("Yo")

if __name__ == "__main__":
    app.run(port=4990, debug=True)