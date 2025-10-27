from flask import Flask, render_template
from newsapi import NewsApiClient

app = Flask(__name__)

# Replace with your NewsAPI key
NEWSAPI_KEY = 'bc5b63dfdb9f40dba73c40f160bf8dce'
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

def fetch_midwest_news(count=10):
    try:
        # Tailored query for obscure/fun/local Midwest stories on business, culture, family values, and people
        query = '"Midwest local news OR obscure fun stories OR business OR traditional culture OR family values OR notable people" sources:local AND (Illinois OR Indiana OR Iowa OR Kansas OR Michigan OR Minnesota OR Missouri OR Nebraska OR "North Dakota" OR Ohio OR "South Dakota" OR Wisconsin) '
        articles = newsapi.get_everything(q=query, language='en', page_size=count, sort_by='relevancy')
        return [{'title': article['title'], 'description': article['description'], 'url': article['url'], 'published': article['publishedAt'], 'source': article['source']['name']} for article in articles['articles']]
    except:
        return []

@app.route('/')
def home():
    news = fetch_midwest_news()
    return render_template('index.html', news=news)

if __name__ == '__main__':
    app.run()
