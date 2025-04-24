import praw
import json
import sys


# --- CONFIGURATION ---
REDDIT_CLIENT_ID = "Gw7IhnZTq3EFhTBWXleRcg"
REDDIT_CLIENT_SECRET = "RXxZU7oW2SJUnebbDd-WYk3z0FVGjA"
REDDIT_USER_AGENT = "myredditapp/0.1 by /u/panfrying"

def scrape_subreddit(subreddit_name, mode):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    if mode == "light":
        num_posts = 5
        num_comments = 5
    else:
        num_posts = 10
        num_comments = 10

    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []
   
    for submission in subreddit.hot(limit=num_posts):
        post_info = {
            "post": submission.title,
            "caption": submission.selftext or "",
            "username": str(submission.author),
            "comments": []
        }
        # Fetch all comments, including nested ones
        submission.comments.replace_more(limit=None)
        all_comments = submission.comments.list()
        for comment in all_comments[:num_comments]:
            if hasattr(comment, "body"):
                post_info["comments"].append({
                    "username": str(comment.author),
                    "comment": comment.body
                })
        posts_data.append(post_info)


    with open("reddit_subreddit_posts.json", "w", encoding="utf-8") as f:
        json.dump({"subreddit": subreddit_name, "posts": posts_data}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    subreddit = sys.argv[1] if len(sys.argv) > 1 else "python"
    mode = sys.argv[2] if len(sys.argv) > 2 else "light"
    scrape_subreddit(subreddit, mode)

