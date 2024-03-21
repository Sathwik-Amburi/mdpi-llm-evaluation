import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/sample_req")
def sample_req():
    target = request.args["target"]
    resp = requests.get("https://" + target + ".example.com/data/")