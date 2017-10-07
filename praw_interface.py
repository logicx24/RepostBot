from main import get_authed_reddit_instance
import praw
import datetime

def get_top_link_submissions(authed_reddit_object, subreddit_name, posts_to_cache):
	found_posts = []
	subreddit = authed_reddit_object.subreddit(subreddit_name)

	for submission in subreddit.hot(limit=posts_to_cache):
		if not submission.is_self:
			found_posts.append({
				"link": submission.url,
				"subreddit": subreddit.display_name,
				"title": submission.title,
				"score": submission.score,
				"found_at": datetime.datetime.now(),
				"unique_key": submission.permalink
			})

	return found_posts

