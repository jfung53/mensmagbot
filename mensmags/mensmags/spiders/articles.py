import scrapy

class gq_spider(scrapy.Spider):
    name = "gq"
    start_urls = [
        "https://www.gq.com/wellness",
        "https://www.gq.com/style",
        "https://www.gq.com/gq-recommends", #shopping
        "https://www.gq.com/culture",
        "https://www.gq.com/grooming",
    ]

    def parse(self, response):
        article_page_links = response.css("div.SummaryItemAssetContainer-gwhFFH a::attr('href')")
        yield from response.follow_all(article_page_links, self.parse_article)

        next_page = response.css("div.fMoTog a::attr('href')").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        yield {
            'date': response.css('time::text').get(),
            'topic': response.css('a.RubricLink-gRWSOU span::text').get(),
            'author': response.css('span.BylineName-kwmrLn a::text').get(),
            'title': response.css('h1::text').get(),
            'bodytext': response.css('article.article p::text').getall(),
            'h2text': response.css('article.article strong::text').getall(),
        }

""" class menshealth_spider(scrapy.Spider):
    name = "menshealth"
    start_urls = [
        "https://www.menshealth.com/health/",
        "https://www.menshealth.com/mental-health/", #1pg
        "https://www.menshealth.com/style/",
        "https://www.menshealth.com/technology-gear/",
        "https://www.menshealth.com/entertainment/", #1pg
        "https://www.menshealth.com/trending-news/",
        "https://www.menshealth.com/grooming/",
        "https://www.menshealth.com/cool-dad-hq/", #1pg
    ]

    def parse(self, response):
        article_page_links = response.css
        yield from response.follow_all(article_page_links, self.parse_article)

        next_page = response.css
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        yield {
            'date': 
            'topic': 
            'author': 
            'title': 
            'bodytext': 
            'h2text': 
        }

 """