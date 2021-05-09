import asyncio
from aiohttp import ClientSession
import nest_asyncio
import lxml.html
import logging
import structlog

# nest_asyncio.apply()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }

def set_arsenic_log_level(level = logging.WARNING):
    logger = logging.getLogger('arsenic')

    def logger_factory():
        return logger

    structlog.configure(logger_factory=logger_factory)
    logger.setLevel(level)

async def fetch_all(url, session, page):
    async with session.get(url) as response:
        html_body = await response.text()
        tree=lxml.html.fromstring(html_body)
        products=[]
        for product in tree.xpath("//ul[@class='c-listing__items js-plp-products-list']/li"):
            fa_name = product.xpath("normalize-space(.//div/@data-title-fa)")
            en_name = product.xpath("normalize-space(.//div/@data-title-en)")
            price= product.xpath(".//div/@data-price")[0]
            link = 'https://www.digikala.com'+product.xpath(".//a/@href")[0]
            pic = product.xpath(".//a/img/@src")[0]
            rate = product.xpath("normalize-space(.//div[@class='c-product-box__engagement-rating']/text())")
            num_vote = product.xpath("normalize-space(.//div[@class='c-product-box__engagement-rating']/span/text())")
            special = product.xpath("normalize-space(.//div[@class='c-promotion__badge c-promotion__badge--special-sale ']/text())")
            incredible_deadline = product.xpath("normalize-space(.//div[@class='c-promotion__special-deal-timer ']/div/@data-countdown)")
            if len(incredible_deadline) > 0 :
                incredible = 'پیشنهاد شگفت انگیز'
            else:
                incredible = ''
            discount = product.xpath("normalize-space(.//div[@class='c-price__discount-oval']/span/text())")
            original_price = product.xpath("normalize-space(.//div[@class='c-price__value c-price__value--plp']/del/text())")
            few = product.xpath("normalize-space(.//div[@class='c-product-box__status c-product-box__status--few']/text())")
            bonous = product.xpath("normalize-space(.//span[@class='c-product-box__digiplus-data c-digiplus-sign--before']/text())")
            
            products.append({'fa_name':fa_name, 'price':price, 'link':link, 'photo':pic,
                             'rate':rate, 'num_vote':num_vote, 'special':special, 'incredible': incredible,
                             'incredible_daedline': incredible_deadline,
                             'discount':discount, 'last_price':original_price, 'few': few,
                             'bonous': bonous})
        return products

async def fetch_with_sem1(sem, session, url, page):
    async with sem:
        return await fetch_all(url, session, page)

async def main_all(total,subject):
    set_arsenic_log_level()
    tasks = []
    sem = asyncio.Semaphore(10)
    async with ClientSession(headers=headers) as session:
        for i in range(1, int(total)+1):
            url = 'https://www.digikala.com/search/?has_selling_stock=1&q='+subject+'&pageno='+str(i)+'&sortby=22'
            tasks.append(
                asyncio.create_task(
                    fetch_with_sem1(sem, session, url, i)
                )
            )
        pages_content = await asyncio.gather(*tasks) 
        return pages_content

def all_digikala(total_pages,subject):
    results = asyncio.run(main_all(total_pages,subject))
    products=[]

    for result in results:
        products = products + result
    print(len(products))
    return(products)





async def fetch_incredible(url, session, page):
    async with session.get(url) as response:
        html_body = await response.text()
        tree=lxml.html.fromstring(html_body)
        products=[]
        for product in tree.xpath("//div[@class='c-product-list__item js-product-list-content']"):
            name = product.xpath("normalize-space(.//div[@class = 'c-product-box__title  js-ab-not-app-incredible-product']/text())")
            price = product.xpath("normalize-space(.//div[@class='c-price__value-wrapper']/text())")
            link = 'https://www.digikala.com'+product.xpath(".//a/@href")[0]
            img = product.xpath(".//img/@src")[0]
            bonous = product.xpath("normalize-space(.//span[@class='c-product-box__digiplus-data c-digiplus-sign--before']/text())")
            saled = product.xpath("normalize-space(.//span[@class='c-product-box__remained-value']/text())")
            try:
                deadline = product.xpath(".//div[@class='c-product-box__timer   js-counter']/@data-countdown")[0]
                last_price = product.xpath(".//div[@class='c-price__value c-price__value--plp js-price-complete-details']/del/text()")[0]
                discount = product.xpath("normalize-space(.//div[@class='c-price__discount-oval']/span/text())")
            except:
                deadline = ''
                last_price = ''
                discount = ''
           
            products.append({'name': name, 'price':price, 'link':link, 'img':img,
                              'discount':discount, 'last_price':last_price, 'deadline': deadline,
                              'bonous': bonous, 'saled': saled,})

        return products
 
async def fetch_with_sem2(sem, session, url, page):
    async with sem:
        return await fetch_incredible(url, session, page)    

async def main_incredible():
    set_arsenic_log_level()
    tasks = []
    sem = asyncio.Semaphore(10)
    async with ClientSession(headers=headers) as session:
        for i in range(1, 5):
            url = 'https://www.digikala.com/incredible-offers/?sortby=7&pageno=' + str(i)
            tasks.append(
                asyncio.create_task(
                    fetch_with_sem2(sem, session, url, i)
                )
            )
        pages_content = await asyncio.gather(*tasks) 
        return pages_content
    
def incredible_digikala():
    results = asyncio.run(main_incredible())
    products=[]

    for result in results:
        products = products + result
    print(len(products))
    return(products)




async def fetch_special(url, session, page):
    async with session.get(url) as response:
        html_body = await response.text()
        tree=lxml.html.fromstring(html_body)
        products=[]
        for product in tree.xpath("//ul[@class='c-listing__items js-plp-products-list']/li"):
            name = product.xpath("normalize-space(.//div/@data-title-fa)")
            price= product.xpath(".//div/@data-price")[0]
            link = 'https://www.digikala.com'+product.xpath(".//a/@href")[0]
            pic = product.xpath(".//a/img/@src")[0]
            rate = product.xpath("normalize-space(.//div[@class='c-product-box__engagement-rating']/text())")
            num_vote = product.xpath("normalize-space(.//div[@class='c-product-box__engagement-rating']/span/text())")
            special = product.xpath("normalize-space(.//div[@class='c-promotion__badge c-promotion__badge--special-sale ']/text())")
            
            discount = product.xpath("normalize-space(.//div[@class='c-price__discount-oval']/span/text())")
            original_price = product.xpath("normalize-space(.//div[@class='c-price__value c-price__value--plp']/del/text())")
            few = product.xpath("normalize-space(.//div[@class='c-product-box__status c-product-box__status--few']/text())")
            bonous = product.xpath("normalize-space(.//span[@class='c-product-box__digiplus-data c-digiplus-sign--before']/text())")
            
            products.append({'name':name, 'price':price, 'link':link, 'photo':pic,
                             'rate':rate, 'num_vote':num_vote, 'special':special,
                             'discount':discount, 'last_price':original_price, 'few': few,
                             'bonous': bonous})
        return products

async def fetch_with_sem3(sem, session, url, page):
    async with sem:
        return await fetch_special(url, session, page)

async def main_special(total):
    set_arsenic_log_level()
    tasks = []
    sem = asyncio.Semaphore(10)
    async with ClientSession(headers=headers) as session:
        for i in range(1, int(total)+1):
            url = 'https://www.digikala.com/landing-page/?pageno=' + str(i) + '&sortby=4'
            tasks.append(
                asyncio.create_task(
                    fetch_with_sem3(sem, session, url, i)
                )
            )
        pages_content = await asyncio.gather(*tasks) 
        return pages_content

def special_digikala(total_pages):
    results = asyncio.run(main_special(total_pages))
    products=[]

    for result in results:
        products = products + result
    print(len(products))
    return(products)

