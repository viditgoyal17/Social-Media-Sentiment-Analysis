document.addEventListener('DOMContentLoaded', function() {
    const submitBtn = document.getElementById('submitBtn');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');

    submitBtn.addEventListener('click', async function() {
        const hashtag = document.getElementById('hashtag').value.trim();
        const analysisType = document.getElementById('analysisType').value;

        if (!hashtag) {
            alert('Please enter a subreddit');
            return;
        }

        loadingDiv.style.display = 'block';
        resultsDiv.innerHTML = '';

        try {
            const scrapeResponse = await fetch('/scrape', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ hashtag: hashtag, analysisType: analysisType })
            });

            if (!scrapeResponse.ok) {
                throw new Error('Scraping failed');
            }

            const analyzeResponse = await fetch('/analyze');
            if (!analyzeResponse.ok) {
                throw new Error('Analysis failed');
            }

            const data = await analyzeResponse.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        } finally {
            loadingDiv.style.display = 'none';
        }
    });

    function displayResults(data) {
        if (!data.results || data.results.length === 0) {
            resultsDiv.innerHTML = '<div>No results found.</div>';
            return;
        }

        let html = `<h2>Results for r/${data.subreddit}</h2>`;
        data.results.forEach(post => {
            html += `<div class="post">
                        <h3>${post.post}</h3>
                        <p>Caption: ${post.caption}</p>
                        <p>Sentiment Analysis: ${post.caption_sentiment_analysis.description}</p>
                        <h4>Comments:</h4>`;
            
            if (post.comments.length === 0) {
                html += '<p>No comments on this post.</p>';
            } else {
                post.comments.forEach(comment => {
                    let cleanComment = comment.comment.slice(0, 80).replace(/\n/g, ' ');
                    html += `<div class="comment">
                                <p>@${comment.username}: ${cleanComment}...</p>
                                <p>Sentiment Analysis: ${comment.sentiment_analysis.description}</p>
                             </div>`;
                });
            }

            html += '</div>';
        });

        resultsDiv.innerHTML = html;
    }
});
