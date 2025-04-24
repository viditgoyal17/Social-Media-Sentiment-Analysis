from flask import Flask, request, jsonify, send_from_directory
import json
import subprocess
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "OPENAI_API_KEY"

def analyze_sentiment_individual(text):
    """Analyze individual text (caption or comment) using GPT-4o-mini."""
    if not text or text == "Unknown":
        return {
            "description": "No sentiment detected.",
            "confidence": 0
        }
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides descriptive sentiment analysis for text."},
                {"role": "user", "content": f"Analyze the sentiment of the following text: {text}"}
            ],
            max_tokens=50,
            temperature=0.7
        )
        description = response['choices'][0]['message']['content'].strip()
        return {
            "description": description,
            "confidence": 1  # Generative models don't provide confidence scores; set it to 1 by default
        }
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return {
            "description": "Error analyzing sentiment.",
            "confidence": 0
        }

def analyze_sentiment_combined(caption, comments):
    """Analyze combined text (caption + comments) using GPT-3.5-turbo."""
    combined_text = f"Caption: {caption}\nComments: {' '.join(comments)}"
    if not combined_text.strip():
        return {
            "description": "No overall sentiment detected.",
            "confidence": 0
        }
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides descriptive sentiment analysis for combined text."},
                {"role": "user", "content": f"Analyze the overall sentiment of the following combined text: {combined_text}"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        description = response['choices'][0]['message']['content'].strip()
        return {
            "description": description,
            "confidence": 1  # Generative models don't provide confidence scores; set it to 1 by default
        }
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return {
            "description": "Error analyzing overall sentiment.",
            "confidence": 0
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
scraper.login_to_instagram("USERID", "PASSWORD")
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
                comments_texts = [comment.get('comment', '') for comment in post.get('comments', [])]
                
                # Analyze individual caption
                caption_sentiment = analyze_sentiment_individual(caption)
                
                # Analyze individual comments
                analyzed_comments = []
                for comment in post.get('comments', []):
                    comment_text = comment.get('comment', '')
                    comment_sentiment = analyze_sentiment_individual(comment_text)
                    analyzed_comments.append({
                        "username": comment.get('username'),
                        "profile_link": comment.get('profile_link'),
                        "comment": comment_text,
                        "sentiment_analysis": comment_sentiment
                    })
                
                # Perform overall sentiment analysis on combined caption and comments
                overall_sentiment = analyze_sentiment_combined(caption, comments_texts)
                
                analyzed_post = {
                    "post": post.get('post'),
                    "username": post.get('username'),
                    "profile_link": post.get('profile_link'),
                    "caption": caption,
                    "caption_sentiment_analysis": caption_sentiment,
                    "comments": analyzed_comments,
                    "overall_sentiment_analysis": overall_sentiment
                }
                
                analyzed_posts.append(analyzed_post)
            
            return jsonify({
                "message": "Sentiment analysis completed successfully for posts.",
                "hashtag": instagram_data.get("hashtag"),
                "results": analyzed_posts
            }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
