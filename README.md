# Social Media Sentiment Analyzer

A unified platform for real-time sentiment analysis of Instagram hashtags and Reddit subreddits, featuring both transformer-based and generative AI (GPT) models. The project includes interactive web interfaces for scraping, analysis, and result visualization.

---

## 🚀 Features

- **Instagram Sentiment Analysis**
  - Scrapes hashtags, captions, and comments using Selenium.
  - Two implementations:  
    - **Transformer Model**: Classifies content as abusive/non-abusive.
    - **GenAI Model**: Provides detailed, descriptive sentiment using GPT (OpenAI).
  - Interactive web interface for real-time input and result display.

- **Reddit Sentiment Analysis**
  - Scrapes subreddit posts and comments using PRAW (Reddit API).
  - Uses generative AI (GPT) for sentiment summaries.
  - Web interface for subreddit input, mode selection, and result visualization.

---

## 🛠️ Setup Instructions

1. **Clone the repository and navigate to the desired implementation folder.**

2. **Install dependencies:**
*(Each implementation may have its own requirements. Common: Flask, openai, praw, selenium, transformers, etc.)*

3. **Set up API keys:**
- Instagram: Update credentials in `hashtag_scraper.py`.
- Reddit: Add your Reddit API credentials in `reddit_scraper.py`.
- OpenAI: Add your API key in `server.py`.

4. **Run the backend server:**
    `python server.py`

5. **Open the frontend:**
- Navigate to `http://localhost:5000` in your browser.

---

## 🖥️ Usage

- **Instagram:**  
- Go to the appropriate implementation folder (GenAI or Transformer).
- Enter a hashtag and select analysis mode (light/deep).
- View sentiment for each post and comment.

- **Reddit:**  
- Enter a subreddit name and select analysis mode (light/dark).
- View sentiment for each post and comment, plus overall post sentiment.

---

## 📂 File Descriptions

- `hashtag_scraper.py` / `reddit_scraper.py`  
Scrapes Instagram hashtags or Reddit subreddits and saves content to JSON.

- `server.py`  
Flask backend for running scrapers, performing sentiment analysis, and serving the frontend.

- `index.html`, `script.js`  
Frontend files for user interaction and displaying results.

- `instagram_hashtag_posts.json` / `reddit_subreddit_posts.json`  
Intermediate data files storing scraped content.

---

## 📌 Notes

- For Instagram scraping, a dummy account and Selenium WebDriver are required.
- For Reddit, you need to register a Reddit app for API credentials.
- OpenAI GPT-based analysis may incur API usage costs.

---

## 📄 License

This project is for educational and research purposes.

---

