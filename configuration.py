import yaml
import praw
import pyimgur

from reddit_store import RedditStore
from praw_interface import PrawInterface
from imgur_interface import ImgurInterface

class ConfiguredObjectsFactory(object):

    def __init__(self):
        self.authFilename = "auth_params.yaml"
        self.configFilename = "config.yaml"

        self.authFile = None
        self.configFile = None

    def get_config_params(self):
        if not self.configFile:
            self.configFile = yaml.safe_load(open(self.configFilename))
        return self.configFile

    def get_auth_params(self):
        if not self.authFile:
            self.authFile = yaml.safe_load(open(self.authFilename))
        return self.authFile

    def get_authed_reddit_instance(self):
        authDict = self.get_auth_params()['reddit_auth_secrets']
        return praw.Reddit(
            client_id=authDict['client_id'],
            client_secret=authDict['client_secret'],
            user_agent="TOTALLY REAL REDDIT USER - EXECUTING HUMAN.EXE",
            username=authDict['username'],
            password=authDict['password']
        )

    def get_main_reddit_username(self):
        return self.get_auth_params()['reddit_auth_secrets']['username']

    def get_authed_reddit_bot_instances(self):
        instances = []
        authDicts = self.get_auth_params()['reddit_bot_accounts']
        for authDict in authDicts:
            instance = praw.Reddit(
                client_id=authDict['client_id'],
                client_secret=authDict['client_secret'],
                user_agent="TOTALLY REAL REDDIT USER - EXECUTING HUMAN.EXE",
                username=authDict['username'],
                password=authDict['password']
            )
            instances.append(instance)
        return instances

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
            posts_to_cache,
            self.get_qualifying_score_for_posting()
        )

    def get_bot_praw_interfaces(self):
        posts_to_cache = self.get_config_params()['submission_options']['num_posts_to_cache']
        return [PrawInterface(authed_reddit_instance, posts_to_cache, self.get_qualifying_score_for_posting()) 
                for authed_reddit_instance
                in self.get_authed_reddit_bot_instances()
        ]

    def get_qualifying_score_for_posting(self):
        return self.get_config_params()['submission_options']['qualifying_score_for_posting']

    def get_authed_imgur_instance(self):
        authDict = self.get_auth_params()['imgur_auth_secrets']
        return pyimgur.Imgur(authDict['client_id'], authDict['client_secret'])

    def get_imgur_interface(self):
        return ImgurInterface(
            self.get_authed_imgur_instance()
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
            "squirting",
            "cozyplaces",
            "mildlyinteresting",
            "accidentalrenaissance",
            "insanepeoplefacebook",
            "iamverysmart",
            "oldpeoplefacebook",
            "kenm",
            "ihavesex",
            "holdmybeer",
            "holdmycosmo",
            "yesyesyesno",
            "watchpeopledie",
            "facepalm",
            "catsstandingup",
            "cringepics",
            "instant_regret",
            "whatcouldgowrong",
            "memes",
            "gatekeeping",
            "misleadingthumbnails",
            "wellthatsucks",
            "fakehistoryporn",
            "interestingasfuck",
            "nevertellmetheodds",
            "all",
            "popular"
        ]

    def get_banned_subreddits(self):
        return [
            "aww",
            "holdthemoan",
            "cat_girls",
            "pics",
            "ass",
            "gentlemanboners",
            "nsfw",
            "thisismylifenow",
            "girlskissing",
            "transporn",
            "bimbofetish",
            "funny",
            "todayilearned",
            "collared",
            "asstastic",
            "nsfw_gifs"
        ]

    def get_subs_to_rehost(self):
        return [
            "gentlemanboners"
        ]
