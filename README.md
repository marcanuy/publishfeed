Publish Feed
============

A publisher of articles from websites RSS feeds to Twitter.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Publish Feed](#publish-feed)
- [Overview](#overview)

<!-- markdown-toc end -->


# Overview

This app currently perform two tasks:

- download RSS content from several sources listed in `feeds.yml`
- publish its titles and links to Twitter

This is an easy way to get your [blog posts automatically tweeted](https://simpleit.rocks/automatically-tweet-new-blog-posts-based-in-rss/).

# Installation

## Install dependencies

Install Pip dependencies: <kbd>make install</kbd>

## Get Twitter credentials

Create a Twitter app at <https://apps.twitter.com/> and generate keys
with **read and write permissions**.

## Set up credentials and feeds

Customize `feeds.yml.skel` and save it as `feeds.yml`:
	
	cd publishfeed
	cp feeds.yml.skel feeds.yml
	
For example, defining feeds for two different Twitter accounts,
<twitter.com/simpleitrocks> and <twitter.com/reddit>, would
look like:

	simpleitrocks: #twitter handler
	  twitter:
		consumer_key: 'XXXXXX'
		consumer_secret: 'XXXXXXX'
		access_key: 'XXXXXX'
		access_secret: 'XXXXXX'
	  urls:
		- https://simpleit.rocks/feed
	  hashtags: '#TechTutorials'
    reddit:
	  twitter:
		consumer_key: 'XXXXXX'
		consumer_secret: 'XXXXXXX'
		access_key: 'XXXXXX'
		access_secret: 'XXXXXX'
	  urls:
        - http://www.reddit.com/.rss
        - http://www.reddit.com/r/news/.rss
        - http://www.reddit.com/user/marcanuy/.rss
	  hashtags: '#RedditFrontPage'

# Running

There are two commands available:

~~~ bash
$ python main.py

usage: main.py [-h] [-g | -t] feed

Process and publish RSS Feeds articles

positional arguments:
  feed            Index from feeds.yml

optional arguments:
  -h, --help      show this help message and exit
  -g, --getfeeds  Download and save new articles from the list of feeds
  -t, --tweet     Tweet unpublished articles from this list of feeds
~~~

- `python main.py <TwitterHandler> --getfeeds`
  
  Download all the pages from the URLs defined in `urls` and save the
   new ones. E.g.: <kbd>python main.py reddit --getfeeds</kbd>
  
- `python main.py <TwitterHandler> --tweet`

  Tweet the oldest unpublished page (previously downloaded with
  `--getfeeds`). E.g.: <kbd>python main.py reddit --tweet</kbd>

## Cronjobs

Set up two cronjobs to publish new feed content automatically:

~~~ bash
crontab -e
~~~

~~~ cronjob
# hourly download new pages 
0 * * * * workon publishfeed; cd publishfeed; python main.py reddit --getfeeds

# tweet every 15 minutes if there are unpublished pages
*/15 * * * * workon publishfeed; cd publishfeed; python main.py reddit --tweet
~~~

**Make sure you configure the tweeter cronjob with at least 2 minutes
between each job so your credentials won't be suspended**

# Design

`feeds.yml` populates the **FeedSet** model, then for each url, new
content is created as **RSSContent** instances (using SQLAlchemy) and saved in
`/databases/rss_<twitterhandler>.db` *SQLite* databases.

To tweet a new post, we get the oldest unpublished page from
**RSSContent**, publish it and change its status.

# Questions

Do you think there is something missing or that can be improved? Feel
free to open issues and/or contributing!

# License

MIT Licensed.
