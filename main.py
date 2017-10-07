import yaml
import praw
import imgurpython

def get_authed_reddit_instance():
    with open('auth_params.yaml') as authFile:
        authDict = yaml.safe_load(authFile)['reddit_auth_secrets']
        return praw.Reddit(
            client_id=authDict['client_id'],
            client_secret=authDict['client_secret'],
            user_agent="TOTALLY REAL REDDIT USER - EXECUTING HUMAN.EXE",
            username=authDict['username'],
            password=authDict['password']
        )

def get_config_params():
    with open('config.yaml') as configFile:
        return yaml.safe_load(configFile)

