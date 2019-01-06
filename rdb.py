# get reddit data through praw and serve it as json

import os
import json
import praw
from textblob import TextBlob


class Rdb:
    """pulls data from praw (100 submissions from specified subreddit/sort mode) and serves to vue
    """

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.environ.get("CLIENT_ID"),
            client_secret=os.environ.get("CLIENT_SECRET"),
            password=os.environ.get("PASSWORD"),
            user_agent="rdb heroku demo",
            username=os.environ.get("USERNAME"),
        )

    def get_submissions(self, subname="all", sortmode="hot"):
        """[Return 100 submissions from a specified subreddit + sort mode.]

        Keyword Arguments:
            subname {str} -- [subreddit name] (default: {'programming'})
            sortmode {str} -- [sorting option (top, hot, new, rising, 
                              controversial)] (default: {'top'})
        """
        if sortmode == "top":
            subreddit = self.reddit.subreddit(subname).top("all")
        elif sortmode == "hot":
            subreddit = self.reddit.subreddit(subname).hot(limit=50)
        elif sortmode == "new":
            subreddit = self.reddit.subreddit(subname).new()
        elif sortmode == "rising":
            subreddit = self.reddit.subreddit(subname).rising()
        elif sortmode == "controversial":
            subreddit = self.reddit.subreddit(subname).controversial()
        else:
            return {}

        onepacket = {}
        data = []
        for submission in subreddit:
            onepacket = {"id": submission.id, "title": submission.title}
            data.append(onepacket)

        json_sub_data = json.dumps(data)

        return json_sub_data

    def scan_submissions(self, selected_submissions):
        """[call reddit api through praw and return comment data]
            selected_submissions -- list of subreddit id-s
        """
        data = []
        for i in selected_submissions:
            submission = self.reddit.submission(id=i)

            # fill an object with data and add it to data array
            titlepolarity = TextBlob(submission.title).sentiment.polarity
            titlesubjectivity = TextBlob(submission.title).sentiment.subjectivity
            onepacket = {
                "id": i,
                "title": submission.title,
                "title_polarity": titlepolarity,
                "title_subjectivity": titlesubjectivity,
                "cmnt_amt": str(len(submission.comments.list())),
                "score": str(submission.score),
            }
            data.append(onepacket)

        json_submission_data = json.dumps(data)
        return json_submission_data

