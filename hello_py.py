import scrapy
import pipeline
from scrapy import FormRequest, Request, Selector
from scrapy.crawler import Crawler
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst
from scrapy import log, signals, Spider, Item, Field
from scrapy.settings import Settings
from twisted.internet import reactor

class LyricsSearchItem(scrapy.Item):
    lyrics = scrapy.Field()

 
#artist_name_search = "Bob Marley"

class MySpider(Spider):
    name = 'lyrics_search'
    allowed_domains = ['www.songteksten.nl']
    start_urls = ['http://www.songteksten.nl/']

    def parse(self, response):
        yield FormRequest.from_response(response,
            formname='naam',
            formdata={"naam": artist_name_search},
            callback=self.parse1)

    def parse1(self, response):
        hxs = Selector(response)
        link_to_artist = hxs.xpath("(//tr/td/a/@href)[1]").extract()
        yield Request(
            url=''.join(('http://www.songteksten.nl', link_to_artist[0])),
            callback=self.parse_artist
            )

    def parse_artist(self, response):
        hxs = Selector(response)
        link_to_lyrics = hxs.xpath("//*[contains(@itemprop, 'track')]//@href").extract()
        for link in link_to_lyrics:
            yield Request(
                url=''.join(('http://www.songteksten.nl', link)),
                callback=self.parse_lyrics
            )

    def parse_lyrics(self, response):
        hxs = Selector(response)
        item = LyricsSearchItem()
        item['lyrics'] = hxs.xpath("//*[contains(@itemprop, 'description')]/text()").extract()
        return item
 
def callback(spider, reason):
    stats = spider.crawler.stats.get_stats()
    reactor.stop()
 
settings = Settings()
settings.set('ITEM_PIPELINES', {
    'pipeline.LyricsSearchPipeline': 100
})

 
def crawl():
    crawler = Crawler(settings)
    spider = MySpider()
    crawler.signals.connect(callback, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    reactor.run()
    