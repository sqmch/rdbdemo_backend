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
