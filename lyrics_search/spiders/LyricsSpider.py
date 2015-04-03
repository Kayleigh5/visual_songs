import scrapy
from scrapy.spider import Spider
from scrapy.selector import Selector
from lyrics_search.items import LyricsSearchItem
from scrapy.http import FormRequest, Request
import csv

artist_name_search = "John Legend"

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
        item['artist_name'] = hxs.xpath("//*[contains(@itemprop, 'byArtist')]/text()").extract()
        item['song_name'] = hxs.xpath("//*[contains(@itemprop, 'name')]/text()").extract()
        item['lyrics'] = hxs.xpath("//*[contains(@itemprop, 'description')]/text()").extract()
        return item