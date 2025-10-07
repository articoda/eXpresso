#!/usr/bin/env python


import sys
import requests
from datetime import datetime, timedelta

#HERE GENERATE TIME INTERVAL
today = datetime.now().strftime("%Y%m%d")+'0001'
yesterday = (datetime.today() - timedelta(days=4)).strftime("%Y%m%d")+'0001'
time_interval = "submittedDate:[{}+TO+{}]".format(yesterday,today)

#ASSEMBLE QUERY WITH CATEGORIES, TIME INTERVAL AND AUTHORS
categories = "%28"+"cat:hep-th"+"+OR+"+"cat:hep-ph"+"%29"

##AUTHORS ARE GENERATED FROM LIST GIVEN TO SCRIPT
inFile = sys.argv[1]

with open(inFile) as file:
    counter = 1
    authors = ''
    for line in file:
        if counter != 1:
            authors+=('+OR+'+'au:'+line.rstrip())
        else:
            authors+=('au:'+line.rstrip())
        counter+=1
    authors=('%28'+authors+'%29')

response = requests.get("http://export.arxiv.org/api/query?search_query="+"%28"+categories+'+AND+'+authors+"%29"+"+AND+"+time_interval+'&start=0&max_results=100')

if response.status_code!=200:
    print(response.status_code)

#print(response.text)

#TAKES THE RESPONSE AND CREATES THE OUTPUT

import feedparser

feed = feedparser.parse(response.url)

feed_entries = feed.entries
counter = 1
for entry in feed.entries:

    article_title = entry.title
    article_link = entry.link
    article_published_at = entry.published # Unicode string
    article_published_at_parsed = entry.published_parsed # Time object
    article_authors = '%s' % ', '.join(author.name for author in entry.authors)
    content = entry.summary
    article_tags = '%s' % ', '.join(tag.term for tag in entry.tags)


    print ("{}) {} by {}".format(counter,article_title,article_authors))
    print ("{}\n{}".format(article_tags, article_link))
    print ("Published at {}".format(article_published_at))
    print("-"*64)
    # print("Content {}".format(content))

    counter = counter + 1
