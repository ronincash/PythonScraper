import scrapy

#define scraper class and give it the starting url to scrape.
class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016']

    def parse(self,response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            #locates the details of the page that we want to see.
            NAME_SELECTOR = 'h1 ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'

            yield {
                'name' : brickset.css(NAME_SELECTOR).extract_first(),
                'pieces' : brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs' : brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                'image' : brickset.css(IMAGE_SELECTOR).extract_first(),
            }

        #We want to traverse links to other pages.  This section handles that.
        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
