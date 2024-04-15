import bcrypt
import re
from flask import jsonify
from database import c
import bcrypt


def check_password(password):
    if not re.search(r'[a-z]', password) or not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

def hash_password(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def registration(data):
    cur = c.cursor()
    if not data.get('login'):
        return jsonify('login is empty'), 400
    if not data.get('email'):
        return jsonify('email is empty'), 400
    if not data.get('password'):
        return jsonify('password is empty'), 400
    if not data.get('countryCode'):
        return jsonify('countryCode is empty'), 400
    if not data.get('isPublic'):
        return jsonify('isPublic is empty'), 400
    if not re.match('[a-zA-Z0-9]+', data['login']):
        return jsonify('login is invalid'), 400
    if not check_password(data['password']):
        return jsonify('password is invalid'), 400
    if len(data['email']) > 50:
        return jsonify('email is too long'), 400
    if len(data['login']) > 30:
        return jsonify('login is too long'), 400
    if len(data['password']) > 100:
        return jsonify('password is too long'), 400
    if len(data['password']) < 6:
        return jsonify('password is too short'), 400
    if data.get('phone') is not None:
        if not re.match('\+[\d]+', data['phone']):
            return jsonify('invalid number'), 400
    if data.get('image') is not None:
        if len(data['image']) > 200:
            return jsonify('image is too long'), 400
    if not re.match('[a-zA-Z]{2}', data['countryCode']):
        return jsonify('countryCode is invalid')
    cur.execute("SELECT COUNT(*) FROM countries WHERE alpha2 = %s", (data['countryCode'], ))
    if cur.fetchone()[0] == 0:
        return jsonify('invalid countryCode'), 400
    cur.close()
    cur = c.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE login = %s;", (data['login'],))
    count = cur.fetchone()[0]
    if count != 0:
        return jsonify('Login already exists'), 409

    cur.execute("SELECT COUNT(*) FROM users WHERE email = %s;", (data['email'],))
    count = cur.fetchone()[0]
    if count != 0:
        return jsonify('Email already exists'), 409
    # user = User(login=data['login'], email=data['email'], password_hash=hashed_password,
    #             countryCode=data['countryCode'], isPublic=data['isPublic'],
    #             phone=data.get('phone', None), image=data.get('image', None))
    try:
        cur = c.cursor()
        cur.execute('''
                INSERT INTO users (login, email, password_hash, countryCode, isPublic, phone, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (
            data['login'], data['email'], hash_password(data['password']).decode('utf-8'), data['countryCode'], data['isPublic'], data.get('phone'),
            data.get('image')))
        c.commit()
        cur.close()
        return jsonify('user registered'), 201
    except Exception as e:
        cur.close()
        return jsonify('registration failed'), 409
