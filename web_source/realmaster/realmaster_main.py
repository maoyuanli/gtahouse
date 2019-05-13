from scrapy.cmdline import execute
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    os.remove('listing.json')
finally:
    execute(["scrapy", "crawl", "realmaster", "-o", "listing.json"])