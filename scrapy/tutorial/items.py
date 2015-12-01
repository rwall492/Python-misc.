# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ReviewItem(scrapy.Item):
    review = scrapy.Field()
    stars = scrapy.Field()
    date = scrapy.Field()

class TextItem(scrapy.Item):
    owner = scrapy.Field()
    stuff = scrapy.Field()
    player = scrapy.Field()
    date = scrapy.Field()

class GameItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    final = scrapy.Field()

class StatItem(scrapy.Item):
    # define the fields for your item here like:
    yards = scrapy.Field()
    tos = scrapy.Field()
    top = scrapy.Field()

class PlayerItem(scrapy.Item):
    stats1 = scrapy.Field()
    stats2 = scrapy.Field()
    opponent = scrapy.Field()
    result = scrapy.Field()
#    att_rush = scrapy.Field()
#    yrd_rush = scrapy.Field()
#    lng_rush = scrapy.Field()
#    tds_rush = scrapy.Field()
#    rec_rec = scrapy.Field()
#    yrd_rec = scrapy.Field()
#    lng_rec = scrapy.Field()
#    tds_rec = scrapy.Field()
#    fumbles = scrapy.Field()
#    fumbles_lost = scrapy.Field()
