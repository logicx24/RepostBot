import praw
import datetime


class PrawInterface(object):

    def __init__(self, authed_reddit_object, posts_to_cache, qualifying_score_for_posting):
        self.authed_reddit_object = authed_reddit_object
        self.posts_to_cache = posts_to_cache
        self.qualifying_score_for_posting = qualifying_score_for_posting

    def get_subreddit(self, subreddit_name):
        return self.authed_reddit_object.subreddit(subreddit_name)

    def get_post_metadata_with_filter(self, subreddit_name, filter_function):
        found_posts = []
        subreddit = self.get_subreddit(subreddit_name)
        for submission in subreddit.hot(limit=self.posts_to_cache):
            if filter_function(submission):
                found_posts.append(submission)
        return found_posts

    def get_top_link_submissions(self, subreddit_name):
        found_posts = []

        for submission in self.get_post_metadata_with_filter(subreddit_name, lambda submission: not submission.is_self and not submission.stickied):
            submission_dict = {
                "link": submission.url,
                "subreddit": submission.subreddit.display_name.lower(),
                "title": submission.title,
                "score": submission.score,
                "created_at": datetime.datetime.utcfromtimestamp(submission.created),
                "unique_key": submission.permalink,
                "id": submission.id
            }

            if submission.author:
                submission_dict["username"] = submission.author.name

            found_posts.append(submission_dict)

        return [found_post for found_post in found_posts if found_post["score"] >= self.qualifying_score_for_posting]

    def get_top_askreddit_posts(self):
        return self.get_post_metadata_with_filter(
                "askreddit",
                lambda submission: submission.is_self
            )

    def get_top_comments(self, submission):
        top_comments = []

        submission.comments.replace_more(limit=self.posts_to_cache)
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

    def make_submission(self, submission_object, subreddit):
        subreddit = self.get_subreddit(subreddit)
        return subreddit.submit(
            title=submission_object['title'],
            url=submission_object['link'],
            resubmit=True,
            send_replies=True
        )

    def get_submission(self, submission_id):
        return praw.models.Submission(reddit=self.authed_reddit_object, id=submission_id)

    def upvote_submission(self, praw_submission_object):
        praw_submission_object.upvote()
