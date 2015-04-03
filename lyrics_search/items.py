# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LyricsSearchItem(scrapy.Item):
    artist_name = scrapy.Field()
    song_name = scrapy.Field()
    lyrics = scrapy.Field()