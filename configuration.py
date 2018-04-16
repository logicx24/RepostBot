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

        authDict = self.get_auth_params()['reddit_auth_secrets']
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

    def get_auth_params(self):
        with open(self.authFilename) as authFile:
            return yaml.safe_load(authFile)

    def get_submission_storage_instance(self):
        dbDict = self.get_config_params()['db_options']
        dbAuthDict = self.get_auth_params()['mongodb_host_auth']
        return RedditStore(
            dbAuthDict['uri'],
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
            "girlskissing",
            "pics",
            "funny",
            "unexpected",
            "bustypetite",
            "beamazed",
            "prequelmemes",
            "sequelmemes",
            "meirl",
            "me_irl",
            "aww",
            "arianagrande",
            "celebnsfw",
            "asstastic",
            "realgirls",
            "nsfw_gifs",
            "ass",
            "theratio",
            "gaming",
            "todayilearned",
            "pics",
            "thisismylifenow",
            "gentlemanboners",
            "holdthemoan",
            "anal",
            "burstingout",
            "sexytummies",
            "adorableporn",
            "ifyouhadtopickone",
            "straightgirlsplaying",
            "tgirls",
            "justhotwomen",
            "girlswithglasses",
            "transporn",
            "bimbofetish",
            "socialmediasluts",
            "tightdresses",
            "yanetgarcia",
            "cat_girls",
            "choker",
            "snapchatgw",
            "collared",
            "strugglefucking",
            "legs",
            "nekoirl",
            "shelikesitrough",
            "theangiecompetition",
            "watchitfortheplot",
            "boobbounce",
            "complexionexcellence",
            "cutemodeslutmode",
            "fuckingmachines",
            "nsfw_korea",
            "nsfw_japan",
            "realitydicks",
            "slutsofsnapchat",
            "squirting"
        ]

    def get_banned_subreddits(self):
        return [
            "aww",
            "holdthemoan",
            "cat_girls",
            "pics",
            "ass"
        ]