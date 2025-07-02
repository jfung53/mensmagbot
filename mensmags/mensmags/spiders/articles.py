import scrapy

class gq_spider(scrapy.Spider):
    name = "gq"
    start_urls = [
        "https://www.gq.com/wellness",
        "https://www.gq.com/style",
        "https://www.gq.com/gq-recommends",
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
            'topic': response.css('a.RubricLink-gRWSOU span::text').get(),
            'title': response.css('h1::text').get(),
            'author': response.css('span.BylineName-kwmrLn a::text').get(),
            'date': response.css('time::text').get(),
            'datetime': response.css('time::attr(datetime)').get(),
            'bodytext': response.css(a_sel.css('article.article p::text').getall()),
            'h2text': response.css(('article.article strong::text').getall()),
        }

