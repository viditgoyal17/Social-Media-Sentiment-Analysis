from flask import Flask, request, jsonify, send_from_directory
import subprocess
import json
import openai

app = Flask(__name__)

openai.api_key = "OPENAI_API_KEY"

def analyze_sentiment(text):
    if not text.strip():
        return {"description": "No sentiment detected."}
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides a 1-2 sentence descriptive sentiment analysis of Reddit posts and comments."},
                {"role": "user", "content": f"Analyze the sentiment of the following text: {text}"}
            ],
            max_tokens=60,
            temperature=0.7
        )
        return {"description": response['choices'][0]['message']['content'].strip()}
    except Exception as e:
        return {"description": f"Error: {e}"}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    subreddit = data.get('hashtag')  # frontend uses 'hashtag' for input
    mode = data.get('analysisType', 'light')
    try:
        subprocess.run(
            ['python', 'reddit_scraper.py', subreddit, mode],
            check=True
        )
        return jsonify({"message": f"Successfully scraped r/{subreddit}"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Scraping failed: {str(e)}"}), 500

@app.route('/analyze', methods=['GET'])
def analyze():
    try:
        with open('reddit_subreddit_posts.json', 'r', encoding='utf-8') as f:
            reddit_data = json.load(f)
            analyzed_posts = []
            for post in reddit_data.get('posts', []):
                caption = post.get('caption', '')
                caption_sentiment = analyze_sentiment(caption)
                analyzed_comments = []
                for comment in post.get('comments', []):
                    comment_text = comment.get('comment', '')
                    comment_sentiment = analyze_sentiment(comment_text)
                    analyzed_comments.append({
                        "username": comment.get('username'),
                        "comment": comment_text,
                        "sentiment_analysis": comment_sentiment
                    })
                analyzed_posts.append({
                    "post": post.get('post'),
                    "username": post.get('username'),
                    "caption": caption,
                    "caption_sentiment_analysis": caption_sentiment,
                    "comments": analyzed_comments
                })
            return jsonify({
                "message": "Sentiment analysis completed successfully.",
                "subreddit": reddit_data.get("subreddit"),
                "results": analyzed_posts
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
