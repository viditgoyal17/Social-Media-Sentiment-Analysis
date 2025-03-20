from flask import Flask, request, jsonify, send_from_directory
import json
from transformers import pipeline
import subprocess

app = Flask(__name__)

# Load sentiment analysis model at startup
sentiment_model = pipeline("text-classification", model="Hate-speech-CNERG/indic-abusive-allInOne-MuRIL")

def analyze_sentiment(text):
    if not text or text == "Unknown":
        return {
            "label": "Unknown",
            "confidence": 0
        }
    result = sentiment_model(text)[0]
    return {
        "label": result['label'],
        "confidence": round(result['score'], 4)
    }

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    hashtag = data.get('hashtag')
    mode = data.get('analysisType')
    
    try:
        subprocess.run([
            'python', '-c', 
            f'''
import sys
sys.path.append('.')
from hashtag_scraper import HashTagScrapper
scraper = HashTagScrapper()
scraper.login_to_instagram("panfrying40", "panfryinginbits")
scraper.scrape_hashtag("{hashtag}", "{mode}")
scraper.close_session()
            '''
        ], check=True)
        
        return jsonify({"message": f"Successfully scraped hashtag #{hashtag}"}), 200
    
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Scraping failed: {str(e)}"}), 500

@app.route('/analyze', methods=['GET'])
def analyze():
    try:
        with open('instagram_hashtag_posts.json', 'r', encoding='utf-8') as f:
            instagram_data = json.load(f)

        analyzed_posts = []
        for post in instagram_data.get('posts', []):
            caption = post.get('caption', '')
            caption_sentiment = analyze_sentiment(caption)
            
            analyzed_comments = []
            for comment in post.get('comments', []):
                comment_text = comment.get('comment', '')
                comment_sentiment = analyze_sentiment(comment_text)
                
                analyzed_comment = {
                    "username": comment.get('username'),
                    "profile_link": comment.get('profile_link'),
                    "comment": comment_text,
                    "sentiment_analysis": comment_sentiment
                }
                analyzed_comments.append(analyzed_comment)
            
            analyzed_post = {
                "post": post.get('post'),
                "username": post.get('username'),
                "profile_link": post.get('profile_link'),
                "caption": caption,
                "caption_sentiment_analysis": caption_sentiment,
                "comments": analyzed_comments
            }
            analyzed_posts.append(analyzed_post)

        return jsonify({
            "message": "Sentiment analysis completed successfully for captions and comments.",
            "hashtag": instagram_data.get("hashtag"),
            "results": analyzed_posts
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
