import yaml
import praw
import imgurpython

from reddit_store import RedditStore
from praw_interface import PrawInterface

class ConfiguredObjectsFactory(object):

    def __init__(self):
        self.authFilename = "auth_params.yaml"
        self.configFilename = "config.yaml"

    def get_authed_reddit_instance(self):
        with open(self.authFilename) as authFile:
            authDict = yaml.safe_load(authFile)['reddit_auth_secrets']
            return praw.Reddit(
                client_id=authDict['client_id'],
                client_secret=authDict['client_secret'],
                user_agent="TOTALLY REAL REDDIT USER - EXECUTING HUMAN.EXE",
                username=authDict['username'],
                password=authDict['password']
            )

    def get_config_params(self):
        with open(self.configFilename) as configFile:
            return yaml.safe_load(configFile)

    def get_submission_storage_instance(self):
        dbDict = self.get_config_params()['db_options']
        return RedditStore(
            dbDict['db_name'],
            dbDict['submission_collection_name'],
            dbDict['id_property'],
            dbDict['date_property'],
            dbDict['posted_property']
        )

    def get_praw_interface(self):
        authed_reddit_instance = self.get_authed_reddit_instance()
        posts_to_cache = self.get_config_params()['submission_options']['num_posts_to_cache']

        return PrawInterface(
            authed_reddit_instance,
            posts_to_cache
        )

    def get_monitored_subreddits(self):
        return [
            "nsfw",
            "pics",
            "funny",
            "unexpected",
            "art",
            "aww",
            "gaming",
            "todayilearned",
            "food",
            "mildlyinteresting",
            "earthporn",
            "oldschoolcool"
        ]