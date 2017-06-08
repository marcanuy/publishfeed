from models import RSSContent, FeedSet
from twitter import Twitter
import yaml
import config
import feedparser
from datetime import datetime

class Helper:
    def __init__(self, session, data):
        self.session = session
        if(isinstance(data, dict)):
            self.data = data
        else:
            with open('feeds.yml', 'r') as f:
                self.data = yaml.safe_load(f)[data]

class FeedSetHelper(Helper):

    def get_pages_from_feeds(self):
        feed = FeedSet(self.data)
        for url in feed.urls:
            parsed_feed = feedparser.parse(url)
            for entry in parsed_feed.entries:
                # if feed page not exist, add it as rsscontent
                q = self.session.query(RSSContent).filter_by(url = entry.link)
                exists = self.session.query(q.exists()).scalar()    # returns True or False
                if not exists:
                    item_title = entry.title
                    item_url = entry.link #.encode('utf-8')
                    #RFC 2822  standard: Wed, 7 Jun 2017 16:25:41 +0000
                    item_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S +0000")
                    item = RSSContent(url=item_url, title=item_title, dateAdded = item_date)
                    self.session.add(item)

class RSSContentHelper(Helper):
    
    def get_oldest_unpublished_rsscontent(self, session):
        rsscontent = session.query(RSSContent).filter_by(published = 0).order_by(RSSContent.dateAdded.asc()).first()
        return rsscontent

    def _calculate_tweet_length(self):
        tweet_net_length = config.TWEET_MAX_LENGTH - config.TWEET_URL_LENGTH - config.TWEET_IMG_LENGTH
        hashtag_length = len(self.data['hashtags'])
        body_length = tweet_net_length - hashtag_length
        return body_length
    
    def tweet_rsscontent(self, rsscontent):
        credentials = self.data['twitter']
        twitter = Twitter(**credentials)
        
        body_length = self._calculate_tweet_length()
        tweet_body = rsscontent.title[:body_length]
        tweet_url = rsscontent.url
        tweet_hashtag = self.data['hashtags']
        tweet_text = "{} {} {}".format(tweet_body, tweet_url, tweet_hashtag)
        twitter.update_status(tweet_text)
        rsscontent.published=True
        self.session.flush()
