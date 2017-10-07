from main import get_authed_reddit_instance
import praw
import datetime


class PrawWrapper(object):

    def __init__(self, authed_reddit_object):
        self.authed_reddit_object = authed_reddit_object

    def get_subreddit(self, subreddit_name):
        return self.authed_reddit_object.subreddit(subreddit_name)

    def get_post_metadata_with_filter(self, subreddit_name, posts_to_cache, filter_function):
        found_posts = []
        subreddit = self.get_subreddit(subreddit_name)
        for submission in subreddit.hot(limit=posts_to_cache):
            if filter_function(submission):
                found_posts.append(submission)
        return found_posts

    def get_top_link_submissions(self, subreddit_name, posts_to_cache):
        found_posts = []

        for submission in self. get_post_metadata_with_filter(subreddit_name, posts_to_cache, lambda submission: not submission.is_self):
            found_posts.append({
                "link": submission.url,
                "subreddit": subreddit.display_name,
                "title": submission.title,
                "score": submission.score,
                "found_at": datetime.datetime.now(),
                "unique_key": submission.permalink,
                "id": submission.id
            })

        return found_posts

    def get_top_askreddit_posts(self, posts_to_cache):
        return self.get_post_metadata_with_filter(
                "askreddit",
                posts_to_cache,
                lambda submission: submission.is_self
            )

    def get_top_comments(self, submission):
        top_comments = []

        submission.comments.replace_more(limit=15)
        for top_level_commment in submission.comments:
            if isinstance(top_level_comment, praw.models.MoreComments):
                continue
            top_comments.append({
                "link": top_level_commment.url,
                "body": top_level_commment.body,
                "unique_key": top_level_commment.permalink,
                "id": top_level_commment.id,
                "submission_id": submission.id
            })
        return top_comments

