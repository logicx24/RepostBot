from configuration import ConfiguredObjectsFactory
from datetime import date, datetime, timedelta
from threading import Timer
import random
import multiprocessing

class Main(object):

    def __init__(self):
        self.configured_obj_factory = ConfiguredObjectsFactory()

        self.praw_interface = self.configured_obj_factory.get_praw_interface()
        self.reddit_store = self.configured_obj_factory.get_submission_storage_instance()
        self.monitored_subs = self.configured_obj_factory.get_monitored_subreddits()

    def cache_subreddit_posts(self):
        print("Caching current hot posts.")
        for subreddit in self.monitored_subs:
            top_link_subs = self.praw_interface.get_top_link_submissions(subreddit)
            for submission in top_link_subs:
                self.reddit_store.save_submission(submission)

    def get_subreddit_posts(self, subreddit):
        return list(self.reddit_store.get_subreddit_submissions_before_date(
            datetime.combine(date.today() - timedelta(days=5), datetime.min.time()),
            subreddit
        ))


    def make_post(self):
        print("Making post if hot posts exist.")
        possible_posts = []
        for subreddit in self.monitored_subs:
            possible_posts.extend(self.get_subreddit_posts(subreddit))

        if len(possible_posts) > 0:
            self.praw_interface.make_submission(
                random.choice(possible_posts)
            )


if __name__ == "__main__":
    main = Main()
    main.cache_subreddit_posts()
    main.make_post()
