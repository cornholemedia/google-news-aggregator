from flask import Flask, render_template
from newsapi import NewsApiClient
import traceback

app = Flask(__name__)

# ←←← PASTE YOUR REAL NEWSAPI KEY HERE ←←←
NEWSAPI_KEY = 'bc5b63dfdb9f40dba73c40f160bf8dce'  # 

newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

def fetch_midwest_news(count=10):
    try:
        # TEST QUERY — WILL RETURN ARTICLES
        query = 'Iowa OR Illinois OR Indiana OR Wisconsin OR Minnesota OR Iowa OR South Dakota'
        print(f"Fetching with query: {query}")
        
        articles = newsapi.get_everything(
            q=query,
            language='en',
            page_size=count,
            sort_by='publishedAt'  # Most recent first
        )
        
        print(f"Success! Got {len(articles['articles'])} articles")
        return [
            {
                'title': a['title'],
                'description': a['description'] or 'No description',
                'url': a['url'],
                'published': a['publishedAt'][:10],
                'source': a['source']['name']
            }
            for a in articles['articles']
        ]
    except Exception as e:
        print(f"API Error: {str(e)}")
        print(traceback.format_exc())
        return []

@app.route('/')
def home():
    print("Page loaded — fetching news...")
    news = fetch_midwest_news()
    return render_template('index.html', news=news)

if __name__ == '__main__':
    app.run()
