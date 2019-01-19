# Backend for the rdb app demo

### Demo: https://rdb.netlify.com/

Authing to praw does not work through praw.ini here. Instead the credentials are stored in Heroku environment variables.

Example of setting a heroku environment variable:
```
heroku config:set CLIENT_ID=asd1a2sd3asda4sd5asd
```

Example of using the Heroku environment variable:
```
import os

self.reddit = praw.Reddit(
            client_id=os.environ.get("CLIENT_ID"),
            client_secret=os.environ.get("CLIENT_SECRET"),
            password=os.environ.get("PASSWORD"),
            user_agent="rdb heroku demo",
            username=os.environ.get("USERNAME"))
```

The 'STATS' tab of the site uses Heroku Scheduler (can add it to your Heroku app through Resources) to call 'python datagrabber.py' periodically. The datagrabber.py file calls the reddit API and stores data using db.py. The db.py file uses Heroku Postgres (postgresql via psycopg2) as the database backend. If you set up a Heroku Postgres resource, you get an additional environment variable called DATABASE_URL which you will need to use instead of your usual connection string with host/username/pw etc. To connect to Heroku Postgres, db.py is modified as follows:

```
import os

DATABASE_URL = os.environ["DATABASE_URL"]

def example():
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    cur = conn.cursor()
    ...

```
