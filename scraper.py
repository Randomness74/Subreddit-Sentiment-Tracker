import praw, praw_config, time, json
from praw.models import MoreComments

login_information = praw_config.data

reddit_api = praw.Reddit(
    client_id = login_information["client_id"],
    client_secret = login_information["secret"],
    password = login_information["password"],
    user_agent = login_information["user_agent"],
    username = login_information["username"],
)

def return_all_comments(parent):
	comments = []
	parent.comments.replace_more(limit=None)
	for comment in parent.comments.list():
		comments.append([comment.id, comment.body, comment.score])
	return comments

def write_data(subreddit, number):
	submissions = []
	for submission in reddit_api.subreddit(subreddit).hot(limit=number):
		print("Submission Title: " + submission.title)
		every_comment = return_all_comments(submission)
		submissions.append([submission, every_comment])
	data = {}
	for post in submissions:
		data[post[0].id] = {"title": post[0].title, "score": post[0].score, "comments": post[1]}
	with open(subreddit + '-results.json', 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
	try:
		print("Reddit Username: " + str(reddit_api.user.me()))
	except Exception:
		print("Something's wrong with the config file!")

	# example code
	write_data("news", 10)
	write_data("worldnews", 10)
	write_data("politics", 10)
	write_data("polandball", 10)
	write_data("conservative", 10)
	write_data("memes", 10)


	