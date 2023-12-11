from os import unlink
from subprocess import check_output, DEVNULL

from flask import Flask, request, render_template


def challenge(input_code: str):
    with open("/tmp/tmp.py", "w", encoding="utf-8") as w:
        w.write(input_code)
    cmd = ["timeout", "-s", "KILL", "2", "python", "/tmp/tmp.py"]
    try:
        res = check_output(cmd, stderr=DEVNULL).decode().strip()
        return res
    except Exception as e:
        return str(e)


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
