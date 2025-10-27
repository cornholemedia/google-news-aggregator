from flask import Flask, render_template
from newsapi import NewsApiClient
import traceback  # For better error logging

app = Flask(__name__)

# Replace with your NewsAPI key (keep this as-is)
NEWSAPI_KEY = 'bc5b63dfdb9f40dba73c40f160bf8dce'
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

def fetch_midwest_news(query, count=5):
    try:
        # Simplified: Focus on Midwest states + topics for local/obscure/fun/business/cultural/family hits
        # Filters out unwanted; NewsAPI pulls from local papers automatically
        articles = newsapi.get_everything(
            q=f"{query} (Illinois OR Indiana OR Iowa OR Kansas OR Michigan OR Minnesota OR Missouri OR Nebraska OR 'North Dakota' OR Ohio OR 'South Dakota' OR Wisconsin)",
            language='en',
            page_size=count,
            sort_by='relevancy'
        )
        return [{'title': article['title'], 'description': article['description'], 'url': article['url'], 'published': article['publishedAt'], 'source': article['source']['name']} for article in articles['articles']]
    except Exception as e:
        print(f"Error fetching news: {str(e)}")  # Logs the real issue to Render
        print(traceback.format_exc())  # Full stack trace for debugging
        return []

@app.route('/')
def home():
    # Call 1: Main stories (obscure/fun/local/business/cultural/family)
    main_news = fetch_midwest_news("Midwest local OR obscure OR fun OR business OR traditional culture OR family values")
    
    # Call 2: People-focused (Midwest locals/heroes)
    people_news = fetch_midwest_news("notable people OR hometown hero OR local innovator OR farmer success", count=5)
    
    # Combine
    all_news = main_news + people_news
    return render_template('index.html', news=all_news)

if __name__ == '__main__':
    app.run()
