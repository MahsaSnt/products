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
        for product in tree.xpath("//ul[@class='c-listing__items']/li"):
            link = 'https://www.digistyle.com' + product.xpath("normalize-space(.//div[@class='c-product-item__image-container']/a/@href)")
            photo = product.xpath("normalize-space(.//div[@class='c-product-item__image-container']/a/img/@src)")
            brand = product.xpath('.//span[@class="c-product-item__brand"]/text()')[0]
            name = product.xpath('.//span[@class="c-product-item__name"]/text()')[0]
            price = product.xpath('.//span[@class="c-product-item__price-value"]/text()')[0]
            original_price = product.xpath('normalize-space(.//span[@class="c-product-item__discount"]/text())')
            discount = product.xpath('normalize-space(.//span[@class="c-product-item__option c-product-item__option--primary"]/text())')
            tak_size = product.xpath('normalize-space(.//a[@class="c-product-item__option c-product-item__option--secondary"]/text())')
            list_size = product.xpath('.//div[@class="c-product-item__info-row c-product-item__info-row--size-container"]/a/text()')
            sizes=[]
            for size in list_size:
                s = size.replace(' ','')
                s = s.replace("\n", "")
                sizes.append(s)
            products.append({'name': name, 'price': price, 'link':link, 'img':photo, 'brand':brand, 'size': sizes,
                             'discount': discount, 'last_price': original_price, 'tak_size': tak_size,})
        return products

async def fetch_with_sem_all(sem, session, url, page):
    async with sem:
        return await fetch_all(url, session, page)

async def main_all(total,subject):
    set_arsenic_log_level()
    tasks = []
    sem = asyncio.Semaphore(10)
    async with ClientSession(headers=headers) as session:
        for i in range(1, int(total)+1):
            url = 'https://www.digistyle.com/search/?q='+subject+'&pageno='+str(i)+'&sortby=22'
            tasks.append(
                asyncio.create_task(
                    fetch_with_sem_all(sem, session, url, i)
                )
            )
        pages_content = await asyncio.gather(*tasks) 
        return pages_content


def all_digistyle(total_pages,subject):
    results = asyncio.run(main_all(total_pages,subject))
    products=[]

    for result in results:
        products = products + result
    print(len(products))
    return(products)






async def fetch_special(url, session):
    async with session.get(url) as response:
        html_body = await response.text()
        tree=lxml.html.fromstring(html_body)
        products=[]
        for product in tree.xpath("//ul[@class='c-listing__items']/li"):
            link = 'https://www.digistyle.com' + product.xpath("normalize-space(.//div[@class='c-product-item__image-container']/a/@href)")
            photo = product.xpath("normalize-space(.//div[@class='c-product-item__image-container']/a/img/@src)")
            brand = product.xpath('.//span[@class="c-product-item__brand"]/text()')[0]
            name = product.xpath('.//span[@class="c-product-item__name"]/text()')[0]
            price = product.xpath('.//span[@class="c-product-item__price-value"]/text()')[0]
            original_price = product.xpath('normalize-space(.//span[@class="c-product-item__discount"]/text())')
            discount = product.xpath('normalize-space(.//span[@class="c-product-item__option c-product-item__option--primary"]/text())')
            tak_size = product.xpath('normalize-space(.//a[@class="c-product-item__option c-product-item__option--secondary"]/text())')
            list_size = product.xpath('.//div[@class="c-product-item__info-row c-product-item__info-row--size-container"]/a/text()')
            sizes=[]
            for size in list_size:
                s = size.replace(' ','')
                s = s.replace("\n", "")
                sizes.append(s)
            products.append({'name': name, 'price': price, 'link':link, 'img':photo, 'brand':brand, 'size': sizes,
                             'discount': discount, 'last_price': original_price, 'tak_size': tak_size,})
        return products

async def fetch_with_sem_special(sem, session, url):
    async with sem:
        return await fetch_special(url, session)

async def main_special(total):
    set_arsenic_log_level()
    tasks = []
    sem = asyncio.Semaphore(10)
    async with ClientSession(headers=headers) as session:
        for i in range(1, int(total)+1):
            men = 'https://www.digistyle.com/sales/mens-apparel/?pageno=' + str(i) + '&sortby=26'
            women = 'https://www.digistyle.com/sales/womens-apparel/?pageno=' + str(i) + '&sortby=26'
            beauty = 'https://www.digistyle.com/sales/personal-appliance/?pageno=' + str(i) + '&sortby=26'
            
            tasks.append(asyncio.create_task(fetch_with_sem_special(sem, session, men)))
            tasks.append(asyncio.create_task(fetch_with_sem_special(sem, session, women)))  
            tasks.append(asyncio.create_task(fetch_with_sem_special(sem, session, beauty)))
            
        pages_content = await asyncio.gather(*tasks) 
        return pages_content


def special_digistyle(total_pages):
    results = asyncio.run(main_special(total_pages))
    products=[]

    for result in results:
        products = products + result
    print(len(products))
    return(products)