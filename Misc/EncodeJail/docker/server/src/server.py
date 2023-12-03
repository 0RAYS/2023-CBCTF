from os import unlink

from flask import Flask, request, render_template

from challenge import challenge

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/challenge")
def palindrome_challenge():
    user_code = request.json["code"]
    res = challenge(user_code)
    try:
        unlink("/tmp/calc.py")
    except Exception as e:
        print(e)
    return {"result": res}
