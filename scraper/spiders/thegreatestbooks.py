from pathlib import Path
from urllib.parse import urljoin

import scrapy

class TheGreatestBooks(scrapy.Spider):
    name = "thegreatestbooks"

    start_urls = ["https://thegreatestbooks.org"]

    def parse(self, response):
        base = "https://thegreatestbooks.org/"
        count = -1
        for li in response.css("div.list-body .list-unstyled li"):
            if li.css("h4 a::text") == []:
                continue
            title, author = [i.strip() for i in li.css("h4 a::text").getall()]
            book_url, author_url = [urljoin(base, i) for i in li.css("h4 a::attr(href)").getall()]
            summary = li.css(".pb-3 p::text").get().strip().replace("\r", "").replace("\n", "")
            image_url = li.css(".pb-3 a img::attr(src)")[0].get()
            amazon_url = li.css(".pb-3 .pull-left.mr-3 a::attr(href)")[1].get()
            count += 1

            yield {
                "index": count,
                "title": title,
                "book_url": book_url,
                "author": author,
                "author_url": author_url,
                "summary": summary,
                "image_url": image_url,
                "amazon_url": amazon_url,
            }
