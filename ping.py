from flask import jsonify


def send():
    return jsonify({"status": "ok"}), 200
