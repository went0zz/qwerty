from database import c
from flask import request, jsonify


def get_countries(regions):
    try:
        cur = c.cursor()
        countries = []
        if regions:
            for region in regions:
                cur.execute("SELECT name, alpha2, alpha3, region FROM countries WHERE region = %s", (region,))
                countries += cur.fetchall()
        else:
            cur.execute("SELECT name, alpha2, alpha3, region FROM countries")
            countries = cur.fetchall()
            cur.close()
        return jsonify(countries), 200
    except Exception as e:
        return jsonify('invalid region'), 400


def get_country_by_alpha(alpha_code):
    try:
        cur = c.cursor()
        cur.execute("SELECT * FROM countries WHERE alpha2 = %s", (alpha_code, ))
        country = cur.fetchone()
        cur.close()
        if not country:
            return jsonify('invalid alpha'), 404
        return jsonify(country), 200
    except Exception as e:
        return jsonify('invalid alpha'), 404
