import datetime

import bcrypt
import re
from flask import Flask, request, jsonify
import jwt
import os
from ping import send
from countriesDB import make_country_table
from get_countries import get_countries, get_country_by_alpha
from userDB import make_user_table
from registration import registration
from login import login
from encs import oss

app = Flask(__name__)


@app.route('/api/ping', methods=['GET'])
def _send():
    return send()


@app.route('/api/countries', methods=['GET'])
def _get_countries():
    return get_countries(request.args.getlist('region'))


@app.route('/api/countries/<alpha2>', methods=['GET'])
def _get_country_by_alpha(alpha2):
    return get_country_by_alpha(alpha2)

@app.route('/api/auth/register', methods=['POST'])
def _registration():
    return registration(request.get_json())


@app.route('/api/auth/sign-in', methods=['POST'])
def _login():
    return login(request.get_json())

if __name__ == "__main__":
    make_country_table()
    make_user_table()
    # oss()
    app.run(port=8080)
