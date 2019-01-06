"""store rdb data with postgresql"""

import psycopg2
import psycopg2.extras
import json


def create_table():
    conn_string = "dbname='rdbtest' user='postgres' password='teretere' host='localhost' port='5432'"
    conn = psycopg2.connect(conn_string)
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
    conn_string = "dbname='rdbtest' user='postgres' password='teretere' host='localhost' port='5432'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO rdb (fulldate, avg_title_polarity, avg_title_subjectivity) VALUES(%s, %s, %s)",
        (fulldate, avg_title_polarity, avg_title_subjectivity),
    )
    conn.commit()
    conn.close()


def grab_all():
    conn_string = "dbname='rdbtest' user='postgres' password='teretere' host='localhost' port='5432'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM rdb")
    data = cur.fetchall()
    json_data = json.dumps([dict(ix) for ix in data])
    return json_data

