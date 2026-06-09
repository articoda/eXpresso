#!/usr/bin/env python

import sys
import requests
import time
import feedparser
from datetime import datetime, timedelta

def chunk_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# 1. GENERATE TIME INTERVAL
today = datetime.now().strftime("%Y%m%d") + '0600'
day_of_week = datetime.today().weekday()

if day_of_week == 0 or day_of_week == 1:
    yesterday = (datetime.today() - timedelta(days=4)).strftime("%Y%m%d") + '0001'
else:
    yesterday = (datetime.today() - timedelta(days=2)).strftime("%Y%m%d") + '0001'

time_interval = "submittedDate:[{}+TO+{}]".format(yesterday, today)
categories = "%28cat:hep-th+OR+cat:hep-ph%29"

# 2. READ AUTHORS
inFile = sys.argv[1]
with open(inFile) as file:
    author_list = [line.strip() for line in file if line.strip()]

# 3. PROCESS IN BATCHES
batch_size = 10  # Smaller batches prevent "URL too long" and 429 errors
all_entries = []

for author_chunk in chunk_list(author_list, batch_size):
    # Assemble author string for this batch
    authors_query = "+OR+".join(["au:" + a for a in author_chunk])
    query_url = (
        "http://export.arxiv.org/api/query?search_query="
        "%28" + categories + "+AND+%28" + authors_query + "%29%29"
        "+AND+" + time_interval + "&start=0&max_results=100"
    )

    # print(f"Fetching batch: {author_chunk[0]}... ({len(author_chunk)} authors)")

    response = requests.get(query_url)

    if response.status_code == 200:
        feed = feedparser.parse(response.text)
        all_entries.extend(feed.entries)
    elif response.status_code == 429:
        print("Error 429: Rate limited. Try increasing the sleep timer.")
        break
    else:
        print(f"Error {response.status_code} for batch.")

    # arXiv asks for a 3-second delay between hits
    time.sleep(3)

# 4. REMOVE DUPLICATES (If an article has multiple authors from your list)
unique_entries = {e.id: e for e in all_entries}.values()

# 5. PRINT RESULTS
print("\n" + "="*64)
for i, entry in enumerate(unique_entries, 1):
    article_authors = ', '.join(author.name for author in entry.authors)
    article_tags = ', '.join(tag.term for tag in entry.tags)

    print("{}) {}\nby {}".format(i, entry.title, article_authors))
    print("{}\n{}".format(article_tags, entry.link))
    print("Published at {}".format(entry.published))
    print("-" * 64)
