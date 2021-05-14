import praw
import string
import random
import configparser
import os

options = configparser.ConfigParser()
script_directory = os.path.dirname(os.path.realpath(__file__))
options.read(f"{script_directory}\\options.ini")
login = options["LOGIN"]
settings = options["SETTINGS"]

reddit_username = login["username"]
reddit_password = login["password"]
reddit_client_id = login["client_id"]
reddit_client_secret = login["client_secret"]
skip_subreddits = settings["skip_subreddits"].split()
min_comment_length = int(settings["min_comment_length"])
max_comment_length = int(settings["max_comment_length"])


reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    password=reddit_password,
    user_agent="My awesome script to manage my Reddit",
    username=reddit_username
)


def get_random_string(min_length, max_length):
    list_of_characters = f"{string.ascii_letters}{string.digits}"
    random_string = ("".join(random.choice(list_of_characters) for _ in range(random.randint(min_length, max_length))))
    return random_string


reddit.validate_on_submit = True

# Replace and delete all comments
comment_found = True
while comment_found:
    comment_found = False
    print("Searching for comments to replace and delete")
    for comment in reddit.user.me().comments.new():
        if comment.subreddit.display_name in skip_subreddits:
            print(f"Skipping comment {comment.id}")
            continue
        comment_found = True
        print(f"Deleting comment {comment.id}")
        random_comment = get_random_string(min_comment_length, max_comment_length)
        comment.edit(random_comment)
        comment.delete()

# Replace and delete all submissions
submission_found = True
while submission_found:
    submission_found = False
    print("Searching for submissions to replace and delete")
    for submission in reddit.user.me().submissions.new():
        if submission.subreddit.display_name in skip_subreddits:
            print(f"Skipping submission {submission.id}")
            continue
        submission_found = True
        print(f"Deleting submission {submission.id}")
        if submission.is_self:
            random_comment = get_random_string(min_comment_length, max_comment_length)
            submission.edit(random_comment)
        submission.delete()

# Remove upvoted content
content_found = True
while content_found:
    content_found = False
    print("Searching for upvoted content to unvote")
    for content in reddit.user.me().upvoted():
        if content.subreddit.display_name in skip_subreddits:
            print(f"Skipping content {content.id}")
            continue
        content_found = True
        print(f"Removing upvote from content {content.id}")
        content.clear_vote()

# Remove downvoted content
content_found = True
while content_found:
    content_found = False
    print("Searching for downvoted content to unvote")
    for content in reddit.user.me().downvoted():
        if content.subreddit.display_name in skip_subreddits:
            print(f"Skipping content {content.id}")
            continue
        content_found = True
        print(f"Removing downvote from content {content.id}")
        content.clear_vote()

# Remove saved content
content_found = True
while content_found:
    content_found = False
    print("Searching for saved content to remove from saved content")
    for content in reddit.user.me().saved():
        if content.subreddit.display_name in skip_subreddits:
            print(f"Skipping content {content.id}")
            continue
        content_found = True
        print(f"Removing content {content.id} from saved content")
        content.unsave()

# Remove hidden content
content_found = True
while content_found:
    content_found = False
    print("Searching for hidden content to remove from hidden content")
    for content in reddit.user.me().hidden():
        if content.subreddit.display_name in skip_subreddits:
            print(f"Skipping content {content.id}")
            continue
        content_found = True
        print(f"Removing content {content.id} from hidden content")
        content.unhide()
