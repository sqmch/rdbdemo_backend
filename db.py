"""store rdb data with postgresql"""

import os
import psycopg2
import psycopg2.extras
import json


DATABASE_URL = os.environ["DATABASE_URL"]


def create_table():
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS rdb (id SERIAL PRIMARY KEY,
                                           fulldate TEXT,
                                           avg_title_polarity TEXT,
                                           avg_title_subjectivity TEXT)"""
    )
    conn.commit()
    conn.close()


def insert(fulldate, avg_title_polarity, avg_title_subjectivity):
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO rdb (fulldate, avg_title_polarity, avg_title_subjectivity) VALUES(%s, %s, %s)",
        (fulldate, avg_title_polarity, avg_title_subjectivity),
    )
    conn.commit()
    conn.close()


def grab_all():
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM rdb")
    data = cur.fetchall()
    json_data = json.dumps([dict(ix) for ix in data])
    return json_data

