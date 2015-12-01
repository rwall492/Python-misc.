import scrapy
from tutorial.items import ReviewItem
import csv

#writer = csv.writer(open('reviews_1984.txt','wb'))
writer = csv.writer(open('reviews_rebecca.txt','wb'))

def fill(path1, path2, path3, array):
    item = ReviewItem()
    item['review'] = path1.xpath("string()").extract()#string instead of text to ignore paragraph breaks!!
    item['stars'] = path2.xpath("text()").extract()
    item['date'] = path3.xpath("text()").extract()
    array.append(item)

class ReviewSpider(scrapy.Spider):
    #scrapy crawl text to execute
    name = "amazon"
    allowed_domains = ["amazon.com/"]
    
    def start_requests(self):
        for x in range(1,124):
            yield self.make_requests_from_url("http://www.amazon.com/Rebecca-Daphne-Du-Maurier/product-reviews/0380730405/ref=cm_cr_pr_btm_link_3?ie=UTF8&showViewpoints=1&sortBy=bySubmissionDateDescending&reviewerType=all_reviews&formatType=all_formats&pageNumber=%d" % x)
#        for x in range(1,390):
#            yield self.make_requests_from_url("http://www.amazon.com/1984-Signet-Classics-George-Orwell/product-reviews/0451524934/ref=cm_cr_pr_btm_link_4?ie=UTF8&showViewpoints=1&sortBy=bySubmissionDateDescending&reviewerType=all_reviews&formatType=all_formats&pageNumber=%d" % x)
    
    def parse(self, response):
        sel = scrapy.Selector(response)
        path1 = sel.xpath("//span[@class='a-size-base review-text']")
        path2 = sel.xpath("//span[@class='a-icon-alt']")
        path3 = sel.xpath("//span[@class='a-size-base a-color-secondary review-date']")
        entries = []

        fill(path1, path2, path3, entries)

        del entries[0]['stars'][0:3]#remove average score, most helpful positive score & most helpful negative score
        del entries[0]['date'][0:2]#remove most helpful positive date & most helpful negative date

        for x in range(0,len(entries[0]['review'])):
            writer.writerow([entries[0]['review'][x].encode('utf-8')])
