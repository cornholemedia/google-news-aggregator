from flask import Flask, render_template
from newsapi import NewsApiClient
import traceback

app = Flask(__name__)

# Replace with your NewsAPI key (double-check for no spaces/quotes)
NEWSAPI_KEY = 'bc5b63dfdb9f40dba73c40f160bf8dce'
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

def fetch_midwest_news(count=10):
    try:
        # Super simple query to test NewsAPI
        query = 'Midwest local OR business OR fun'
        print(f"API Key starts with: {NEWSAPI_KEY[:8]}...")  # Debug: check key
        print(f"Fetching news with query: {query}")
        articles = newsapi.get_everything(
            q=query,
            language='en',
            page_size=count,
            sort_by='relevancy'
        )
        print(f"Got {len(articles['articles'])} articles")
        return [{'title': article['title'], 'description': article['description'] or 'No description', 'url': article['url'], 'published': article['publishedAt'], 'source': article['source']['name']} for article in articles['articles']]
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        print(traceback.format_exc())
        return []

@app.route('/')
def home():
    print("Handling request to /")
    news = fetch_midwest_news()
    print(f"Rendering {len(news)} articles")
    return render_template('index.html', news=news)

if __name__ == '__main__':
    app.run()
