from configuration import ConfiguredObjectsFactory
from datetime import date, datetime, timedelta
from threading import Timer
import random
import multiprocessing

class Main(object):

    def __init__(self):
        self.configured_obj_factory = ConfiguredObjectsFactory()

        self.praw_interface = self.configured_obj_factory.get_praw_interface()
        self.imgur_interface = self.configured_obj_factory.get_imgur_interface()
        self.reddit_store = self.configured_obj_factory.get_submission_storage_instance()
        self.monitored_subs = self.configured_obj_factory.get_monitored_subreddits()
        self.banned_subs = self.configured_obj_factory.get_banned_subreddits()
        self.rehost_subs = self.configured_obj_factory.get_subs_to_rehost()

    def cache_subreddit_posts(self):
        print("Caching current hot posts.")
        for subreddit in self.monitored_subs:
            top_link_subs = self.praw_interface.get_top_link_submissions(subreddit)
            for submission in top_link_subs:
                if submission.get("username", None) != self.configured_obj_factory.get_main_reddit_username():
                    self.reddit_store.save_submission(submission, date=datetime.now())

    def get_subreddit_posts(self, subreddit):
        return list(self.reddit_store.get_subreddit_submissions_before_date(
            datetime.combine(date.today() - timedelta(days=2), datetime.min.time()),
            subreddit
        ))

    def get_all_posts(self):
        return list(self.reddit_store.get_submissions_before_date(
            datetime.combine(date.today() - timedelta(days=2), datetime.min.time())
        ))

    def make_post(self):
        print("Making post if hot posts exist.")
        possible_posts = self.get_all_posts()

        posting_predicate = lambda post: post['subreddit'] not in self.banned_subs and post.get("username", None) != self.configured_obj_factory.get_main_reddit_username()
        possible_posts = [post for post in possible_posts if posting_predicate(post)]

        if len(possible_posts) > 0:
            chosen_submission = random.choice(possible_posts)
            if chosen_submission['subreddit'] in self.rehost_subs:
                rehosted_link = self.imgur_interface.upload_image_from_url(chosen_submission['link'])
                if rehosted_link:
                    chosen_submission['link'] = rehosted_link

            self.praw_interface.make_submission(
                chosen_submission,
                chosen_submission['subreddit']
            )

            chosen_submission['username'] = self.configured_obj_factory.get_main_reddit_username()
            self.reddit_store.mark_posted(chosen_submission)


if __name__ == "__main__":
    main = Main()
    main.cache_subreddit_posts()
    main.make_post()
