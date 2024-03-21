import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/partial_req")
def partial_req():
    user_id = request.args["user_id"]
    resp = requests.get("https://api.example.com/user_info/" + user_id)