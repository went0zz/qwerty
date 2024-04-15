from database import c


def make_user_table():
    cur = c.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        login VARCHAR(30) UNIQUE NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(256) NOT NULL,
        countryCode CHAR(2) NOT NULL,
        isPublic BOOLEAN NOT NULL,
        phone VARCHAR(20),
        image VARCHAR(200)
    );''')
    c.commit()
    cur.close()
