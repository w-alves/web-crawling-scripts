import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class G1Spider(scrapy.Spider):
    name = 'g1'
    start_urls = ['http://g1.globo.com/index/feed/pagina-1.html']

    rules = (
        Rule(LinkExtractor(allow=('(.+).html$', '(.+).ghtml$'), deny=('(.+)(/blog/)', '(.+)(/previsao-do-tempo/)', '(extra.+)', '(.+)(/globo-news/)')),
             callback='parse', follow=True,),
    )

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'g1newsdata.csv'
    }

    def parse(self, response):
        news_url = response.css("a.feed-post-link::attr(href)").extract()
        for url in news_url:
            yield response.follow(url, self.parse_new)

        next_page = response.css('div.load-more a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_new(self, response):
        if 'playlist' not in str(response.url):
            title=  response.css('h1.content-head__title::text').get()
            date = response.xpath("//time[@itemprop='datePublished']/text()").get()
            topic = response.css('a.header-editoria--link::text').get()

            yield {
                'title': title,
                'date': date,
                'topic': topic,
            }
        else:
            pass







