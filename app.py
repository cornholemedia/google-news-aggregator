from flask import Flask, render_template
import feedparser
from datetime import datetime

app = Flask(__name__)

# Expanded list of local RSS feeds (3-5 per state, small/local focus)
RSS_FEEDS = [
    # Illinois
    "https://theclintonjournal.com/feed/",
    "https://rochellenews-leader.com/feed/",
    "https://thegreenvilleadvocate.com/feed/",
    "https://amboynews.com/feed/",
    # Indiana
    "https://waynedalenews.com/feed/",
    "https://westernwaynenews.com/feed/",
    "https://indianapolisrecorder.com/feed/",
    "https://youarecurrent.com/feed/",
    # Iowa
    "https://www.thehawkeye.com/rss/",
    "https://iowastatedaily.com/feed/",
    "https://southeastiowaunion.com/feed/",
    "https://hometowncurrent.com/feed/",
    # Kansas
    "https://hdnews.net/feed/",
    "https://mcphersonsentinel.com/feed/",
    "https://ctnewsonline.com/feed/",
    # Michigan
    "https://manisteenews.com/news/feed/",
    "https://thelakeshoreguardian.com/feed/",
    "https://alconacountyherald.com/feed/",
    # Minnesota
    "https://hometownsource.com/abc_newspapers/feed/",
    "https://www.sctimes.com/rss/",
    "https://communityreporter.org/feed/",
    "https://pipestonestar.com/feed/",
    # Missouri
    "https://hannibal.net/rss/",
    "https://www.columbiamissourian.com/feed/",
    "https://leadercourier-times.com/feed/",
    "https://madisondailyleader.com/feed/",
    # Nebraska
    "https://yorknewstimes.com/feed/",
    "https://columbustelegram.com/feed/",
    "https://fremonttribune.com/feed/",
    # North Dakota
    "https://minotdailynews.com/feed/",
    "https://willistonherald.com/feed/",
    "https://newtownnews.com/feed/",
    # Ohio
    "https://morningjournal.com/feed/",
    "https://limaohio.com/feed/",
    "https://columbusmessenger.com/feed/",
    "https://lcnewspapers.com/feed/",
    # South Dakota
    "https://bhpioneer.com/feed/",
    "https://capitaljournal.com/feed/",
    "https://madisondailyleader.com/feed/",
    # Wisconsin
    "https://beloitdailynews.com/feed/",
    "https://dailycardinal.com/feed/",
    "https://isthmus.com/rss/",
    "https://southwestjournal.com/feed/"
]

def fetch_rss_articles():
    articles = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:  # 3 per paper for balance
                published = entry.get('published', 'Unknown')[:10]
                description = (entry.summary or '').split('<')[0][:150] + '...' if len(entry.summary or '') > 150 else entry.summary or 'No description'
                articles.append({
                    'title': entry.title,
                    'description': description,
                    'url': entry.link,
                    'published': published,
                    'source': feed.feed.get('title', 'Local Paper')
                })
        except Exception:
            continue  # Skip dead feeds
    # Sort by date (newest first), limit to 20
    articles.sort(key=lambda x: x['published'], reverse=True)
    return articles[:20]

@app.route('/')
def home():
    news = fetch_rss_articles()
    return render_template('index.html', news=news)

if __name__ == '__main__':
    app.run()
