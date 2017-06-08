Publish Feed
============

A publisher of articles from RSS feeds to other platforms, currently
to Twitter only.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Publish Feed](#publish-feed)
- [Overview](#overview)

<!-- markdown-toc end -->


# Overview

This app currently perform two tasks:

- download RSS content from several sources listed in `feeds.yml`
- publish its titles and links to Twitter

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
   new ones. E.g.: `python main.py reddit --getfeeds`
  
- `python main.py <TwitterHandler> --tweet`

  Tweet the oldest unpublished page (previously downloaded with
  `--getfeeds`). E.g.: `python main.py reddit --tweet`

## Cronjobs

Set up two cronjobs to publish new feed content automatically:

~~~ bash
crontab -e
~~~

~~~ cronjob
# hourly download new pages 
0 * * * * workon publishfeed; cd publishfeed; python main.py reddit -g

# tweet every 15 minutes if there are unpublished pages
*/15 * * * * workon publishfeed; cd publishfeed; python main.py reddit -g
~~~

**Make sure you configure the tweeter cronjob with at least 2 minutes
between each job so your credentials won't be suspended**

# Questions

Do you think there is something missing or that can be improved? Feel
free to open issues and/or contributing!

# License

MIT Licensed.
