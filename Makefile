#virtualenv:
#	mkvirtualenv -p /usr/bin/python3.6 twitter_feeder
install:
	pip install -r requirements.txt
freeze:
	pip freeze > requirements.txt
tests:
	cd publishfeed; python -m unittest discover
