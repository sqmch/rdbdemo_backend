"""grab data from praw and store it periodically using schedule"""

import os
import time
import praw
import schedule
import db
from textblob import TextBlob


reddit = praw.Reddit(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    password=os.environ.get("PASSWORD"),
    user_agent="rdb heroku demo",
    username=os.environ.get("USERNAME"),
)


def get_submission_titles(subname="all", sortmode="hot"):
    """[Return 100 submissions from a specified subreddit + sort mode.]

    Keyword Arguments:
        subname {str} -- [subreddit name] (default: {'all})
        sortmode {str} -- [sorting option (top, hot, new, rising, 
                            controversial)] (default: {'top'})
    """
    if sortmode == "top":
        subreddit = reddit.subreddit(subname).top("all")
    elif sortmode == "hot":
        subreddit = reddit.subreddit(subname).hot(limit=50)
    elif sortmode == "new":
        subreddit = reddit.subreddit(subname).new()
    elif sortmode == "rising":
        subreddit = reddit.subreddit(subname).rising()
    elif sortmode == "controversial":
        subreddit = reddit.subreddit(subname).controversial()
    else:
        return []

    data = []
    for submission in subreddit:
        title = submission.title
        data.append(title)

    return data


def job():
    """[Periodically get average polarity and subjectivity data of submission titles
    """
    polarity_values = []
    subjectivity_values = []
    submission_titles = get_submission_titles()
    for i in submission_titles:
        titlepolarity = TextBlob(i).sentiment.polarity
        polarity_values.append(titlepolarity)
        titlesubjectivity = TextBlob(i).sentiment.subjectivity
        subjectivity_values.append(titlesubjectivity)

    date = time.strftime("%d/%m/%y %H:%M")
    avg_polarity = sum(polarity_values) / len(polarity_values)
    avg_subjectivity = sum(subjectivity_values) / len(subjectivity_values)

    db.create_table()
    db.insert(date, avg_polarity, avg_subjectivity)


if __name__ == "__main__":
    job()
