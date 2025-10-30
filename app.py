from flask import Flask, render_template
import feedparser
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Reduced to 12 FAST, RELIABLE local papers (1 per state)
RSS_FEEDS = [
    "https://theclintonjournal.com/feed/",           # IL
    "https://waynedalenews.com/feed/",               # IN
    "https://southeastiowaunion.com/feed/",          # IA
    "https://mcphersonsentinel.com/feed/",           # KS
    "https://manisteenews.com/news/feed/",           # MI
    "https://pipestonestar.com/feed/",               # MN
    "https://hannibal.net/rss/",                     # MO
    "https://yorknewstimes.com/feed/",               # NE
    "https://minotdailynews.com/feed/",              # ND
    "https://limaohio.com/feed/",                    # OH
    "https://bhpioneer.com/feed/",                   # SD
    "https://beloitdailynews.com/feed/"              # WI
]

# Global cache
cached_articles = []
cache_time = 0
CACHE_DURATION = 300  # 5 minutes

def fetch_rss_articles():
    global cached_articles, cache_time
    # Return cache if fresh
    if time.time() - cache_time < CACHE_DURATION and cached_articles:
        return cached_articles[:20]

    articles = []
    for url in RSS_FEEDS:
        try:
            # 5-second timeout per feed
            feed = feedparser.parse(url, request_headers={'User-Agent': 'MidwestNewsBot/1.0'}, 
                                  handlers=[], modified=None, etag=None)
            for entry in feed.entries[:2]:  # Only 2 per paper
                published = entry.get('published', '')[:10] or 'Recent'
                summary = (entry.get('summary', '') or '').split('<')[0][:200]
                articles.append({
                    'title': entry.title,
                    'description': summary + '...' if len(summary) > 197 else summary,
                    'url': entry.link,
                    'published': published,
                    'source': feed.feed.get('title', 'Local Paper').split(' - ')[0]
                })
        except Exception as e:
            print(f"Feed failed: {url} -> {e}")
            continue

    articles.sort(key=lambda x: x['published'], reverse=True)
    cached_articles = articles
    cache_time = time.time()
    return articles[:20]

@app.route('/')
def home():
    sort = request.args.get('sort', 'recent')  # HN-style ?sort=new
    news = fetch_rss_articles()  # Your existing function
    if sort == 'new':
        news = sorted(news, key=lambda x: x['published'], reverse=True)  # Already recent, but for demo
    return render_template('index.html', news=news)
