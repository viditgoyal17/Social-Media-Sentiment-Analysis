document.addEventListener('DOMContentLoaded', function() {
    const submitBtn = document.getElementById('submitBtn');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    
    submitBtn.addEventListener('click', async function() {
        const hashtag = document.getElementById('hashtag').value.trim();
        const analysisType = document.getElementById('analysisType').value;
        
        if (!hashtag) {
            alert('Please enter a hashtag');
            return;
        }
        
        loadingDiv.style.display = 'block';
        resultsDiv.innerHTML = '';
        
        try {
            const scrapeResponse = await fetch('/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    hashtag: hashtag,
                    analysisType: analysisType
                })
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
            resultsDiv.innerHTML = `<p style="color: red">Error: ${error.message}</p>`;
        } finally {
            loadingDiv.style.display = 'none';
        }
    });
    
    function displayResults(data) {
        if (!data.results || data.results.length === 0) {
            resultsDiv.innerHTML = '<p>No results found.</p>';
            return;
        }
        
        let html = `<h2>Results for hashtag: #${data.hashtag}</h2>`;
        
        data.results.forEach((post, index) => {
            let sentimentClass = post.caption_sentiment_analysis.label === 'Non-Abusive' ? 'non-abusive' : 'abusive';
            
            html += `
                <div class="post">
                    <div class="post-header">
                        <h3>${post.post} by <a href="${post.profile_link}" target="_blank">@${post.username}</a></h3>
                    </div>
                    
                    <div class="instagram-embed-container" id="instagram-post-${index}">
                        <blockquote 
                            class="instagram-media" 
                            data-instgrm-permalink="https://www.instagram.com/${post.username}/"
                            data-instgrm-version="14">
                            <div style="padding:16px;">
                                <a href="https://www.instagram.com/${post.username}/" target="_blank">View this post on Instagram</a>
                            </div>
                        </blockquote>
                    </div>
                    
                    <div class="caption">
                        <strong>Caption:</strong> ${post.caption}
                        <span class="sentiment ${sentimentClass}">
                            ${post.caption_sentiment_analysis.label} 
                            (${(post.caption_sentiment_analysis.confidence * 100).toFixed(2)}%)
                        </span>
                    </div>
                    
                    <div class="comments">
                        <h4>Comments (${post.comments.length}):</h4>
            `;
            
            if (post.comments.length === 0) {
                html += '<p>No comments on this post.</p>';
            } else {
                post.comments.forEach(comment => {
                    let commentSentimentClass = comment.sentiment_analysis.label === 'Non-Abusive' ? 'non-abusive' : 'abusive';
                    
                    html += `
                        <div class="comment">
                            <strong><a href="${comment.profile_link}" target="_blank">@${comment.username}</a>:</strong> 
                            ${comment.comment}
                            <span class="sentiment ${commentSentimentClass}">
                                ${comment.sentiment_analysis.label} 
                                (${(comment.sentiment_analysis.confidence * 100).toFixed(2)}%)
                            </span>
                        </div>
                    `;
                });
            }
            
            html += `
                    </div>
                </div>
            `;
        });
        
        resultsDiv.innerHTML = html;
        
        if (window.instgrm) {
            window.instgrm.Embeds.process();
        } else {
            setTimeout(() => window.instgrm.Embeds.process(), 1000);
        }
    }
});
