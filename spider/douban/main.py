import sys
from scrapy import cmdline

sys.path.append("../")
# cmdline.execute(["scrapy", "crawl", "douban_spider"])
cmdline.execute(["scrapy", "crawl", "douban_spider", "-o", "mingyan.json"])