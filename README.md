# Instagram Hashtag Sentiment Analyzer

## Overview

The **Instagram Hashtag Sentiment Analyzer** is a project that:

1. **Scrapes Instagram Posts and Comments**:
   - Scrapes Instagram posts and comments based on a specific hashtag using Selenium.
   - Supports two modes:
     - `light` mode: Scrapes 5 posts and 5 comments per post.
     - `deep` mode: Scrapes 10 posts and 10 comments per post.

2. **Performs Sentiment Analysis**:
   - Analyzes the sentiment of post captions and comments using a pre-trained model (`Hate-speech-CNERG/indic-abusive-allInOne-MuRIL`) from Hugging Face.
   - Classifies text as either:
     - **Positive**
     - **Negative**

3. **Displays Results in a Web Interface**:
   - Shows the scraped posts, comments, and sentiment analysis results in a structured format.
   - Embeds the actual Instagram posts (or profiles) alongside the analysis.

---

## Features

- Scrape Instagram posts and comments for any hashtag.
- Perform sentiment analysis on captions and comments.
- Display results with embedded Instagram posts in a user-friendly web interface.

---

## Prerequisites

Before running this project, ensure you have the following installed:
1. **Python** (>= 3.8)
2. **pip** (Python package manager)
3. **Google Chrome** (latest version)
4. **ChromeDriver** (compatible with your Chrome version)
5. Required Python packages:
   - `selenium`
   - `transformers`
   - `torch`
   - `flask`
   - `flask_cors`

---


---

## Installation Guide

Follow these steps to set up and run the project:

### Step 1: Clone the Repository

    git clone https://github.com/yourusername/InstagramHashtagSentimentAnalyzer.git 
    cd InstagramHashtagSentimentAnalyzer


### Step 2: Install Dependencies

Install all required Python packages:

    pip install selenium transformers torch flask flask_cors


### Step 3: Set Up ChromeDriver

1. Download ChromeDriver from [here](https://chromedriver.chromium.org/downloads).
2. Place the ChromeDriver executable in your system's PATH or in the project directory.

### Step 4: Configure Instagram Credentials

Update the login credentials in `hashtag_scraper.py`:



---
---

## How to Run the Project

### Step 1: Start the Backend Server

Run the Flask server:

    python server.py


The server will start at `http://localhost:5000`.

### Step 2: Access the Web Interface

Open your browser and navigate to `http://localhost:5000`. You’ll see a form where you can:

1. Enter the hashtag you want to scrape (e.g., `crimepatrol`).
2. Select the analysis type (`light` or `deep`).
3. Click the "Analyze Hashtag" button.

### Step 3: Scraping and Analysis

Once you submit the form:

1. The backend triggers **hashtag_scraper.py** to scrape Instagram posts and comments based on your input.
2. The scraped data is saved temporarily in `instagram_hashtag_posts.json`.
3. The backend performs sentiment analysis on captions and comments using the model defined in **model.py**.
4. The results are displayed on the webpage, including:
   - Post captions with sentiment labels and confidence scores.
   - Comments with sentiment labels and confidence scores.

---
---

## License

This project is licensed under the MIT License.
