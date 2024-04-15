from flask import jsonify

from database import c

import bcrypt
def login(data):
    try:
        cur = c.cursor()
        cur.execute("SELECT * from users WHERE login = %s", (data['login'],))
        user = cur.fetchone()
        cur.close()
        print(user)
        if not user[0]:
            return jsonify('invalid login'), 401
        password = user[3]
        if bcrypt.checkpw(password, data['password'].encode('utf-8')):
            return jsonify('access granted'), 200
        else:
            return jsonify('wrong password'), 401
    except Exception as e:
        return jsonify('access denied'), 401
