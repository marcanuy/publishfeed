#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import argparse

from helpers import RSSContentHelper, FeedSetHelper
from twitter import Twitter
from models import FeedSet,create_tables
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@contextmanager
def session_scope(account):
    """Provide a transactional scope around a series of operations."""
    session = db_session(account)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def db_session(account):
    """
    Performs database connection using database settings from the 
    account selected in feeds.yml.
    Returns sqlalchemy session instance
    """
    db_path = 'databases/rss_{}.db'.format(account)
    engine = create_engine("sqlite:///{}".format(db_path))
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def getfeeds(account):
    """
    Download and save articles from feeds
    """
    create_tables(account)
    with session_scope(account) as session:
        helper = FeedSetHelper(session, account)
        helper.get_pages_from_feeds()

def tweet(account):
    with session_scope(account) as session:
        helper = RSSContentHelper(session, account)
        rsscontent = helper.get_oldest_unpublished_rsscontent(session)
        if(rsscontent):
            helper.tweet_rsscontent(rsscontent)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process and publish RSS Feeds articles')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-g", "--getfeeds", action='store_true', help="Download and save new articles from the list of feeds")
    group.add_argument("-t", "--tweet", action='store_true', help="Tweet unpublished articles from this list of feeds")
    parser.add_argument("feed", help="Index from feeds.yml")
    args = parser.parse_args()
    
    account = args.feed
    if(args.getfeeds):
        getfeeds(account)
    elif(args.tweet):
        tweet(account)

