from configuration import ConfiguredObjectsFactory
from datetime import date, datetime, timedelta
import random
import multiprocessing

class Main(object):

    def __init__(self):
        self.configured_obj_factory = ConfiguredObjectsFactory()

        self.praw_interface = self.configured_obj_factory.get_praw_interface()
        self.reddit_store = self.configured_obj_factory.get_submission_storage_instance()
        self.monitored_subs = self.configured_obj_factory.get_monitored_subreddits()

    def cache_subreddit_posts(self):

        for subreddit in self.monitored_subs:
            top_link_subs = self.praw_interface.get_top_link_submissions(subreddit)
            for submission in top_link_subs:
                self.reddit_store.save_submission(submission)

    def make_subreddit_post(self, subreddit):
        possible_posts = list(self.reddit_store.get_subreddit_submissions_after_date(
            datetime.combine(date.today() - timedelta(days=1), datetime.min.time()),
            subreddit
        ))

        if len(possible_posts) > 0:
            self.praw_interface.make_submission(
                random.choice(possible_posts)
            )

    def make_all_posts(self):
        for subreddit in self.monitored_subs:
            self.make_subreddit_post(subreddit)


if __name__ == "__main__":
    main_class = Main()

    #main_class.cache_subreddit_posts()
    main_class.make_all_posts()

