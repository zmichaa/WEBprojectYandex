import sqlite3


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS account (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(50) NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        email VARCHAR(100) NOT NULL,
                        organisation VARCHAR(100) NOT NULL,
                        address VARCHAR(100) NOT NULL,
                        city VARCHAR(100) NOT NULL,
                        region VARCHAR(100) NOT NULL,
                        country VARCHAR(100) NOT NULL,
                        postalcode VARCHAR(100) NOT NULL
                    )''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
