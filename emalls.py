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
    
async def fetch_all(url, session):
    async with session.get(url) as response:
        html_body = await response.text()
        tree=lxml.html.fromstring(html_body)
        products=[]
        for product in tree.xpath("//div[@class='item']"):
            link = 'https://emalls.ir' + product.xpath(".//div[@class = 'item-image']/a/@href")[0]
            name = product.xpath(".//div[@class = 'item-image']/a/@title")[0]
            img = product.xpath(".//div[@class = 'item-image']/a/img/@src")[0]
            price = product.xpath(".//span[@class = 'item-price']/text()")[0]
            discount = product.xpath("normalize-space(.//div[@class = 'item-price-discount-box']/div/text())")
            old_price = product.xpath("normalize-space(.//div[@class = 'item-price-discount-box']/del/text())")
            products.append({'link': link, 'name': name, 'img':img, 'price':price,
                             'discount': discount, 'old_price': old_price})
        return products

async def fetch_with_sem_all(sem, session, url):
    async with sem:
        return await fetch_all(url, session)

async def main_all(total,subject):
    set_arsenic_log_level()
    tasks = []
    sem = asyncio.Semaphore(10)
    async with ClientSession(headers=headers) as session:
        for i in range(1, int(total)+1):
            url = 'https://emalls.ir/محصولات~search~'+subject + '~page~' + str(i)
            tasks.append(
                asyncio.create_task(
                    fetch_with_sem_all(sem, session, url)
                )
            )
        pages_content = await asyncio.gather(*tasks) 
        return pages_content


def all_emalls(total_pages,subject):
    results = asyncio.run(main_all(total_pages,subject))
    products=[]

    for result in results:
        products = products + result
    
    return(products)



async def main_special(total,subject):
    set_arsenic_log_level()
    tasks = []
    sem = asyncio.Semaphore(10)
    async with ClientSession(headers=headers) as session:
        for i in range(1, int(total)+1):
            url = 'https://emalls.ir/محصولات~Search~' + subject +'~o~dd~page~' + str(i)
            tasks.append(
                asyncio.create_task(
                    fetch_with_sem_all(sem, session, url)
                )
            )
        pages_content = await asyncio.gather(*tasks) 
        return pages_content


def special_emalls(total_pages,subject):
    results = asyncio.run(main_special(total_pages,subject))
    products=[]

    for result in results:
        products = products + result
    
    return(products)




    
async def fetch_shoplist(url, session):
    async with session.get(url) as response:
        html_body = await response.text()
        tree=lxml.html.fromstring(html_body)
        shops=[]
        for shop in tree.xpath("//ul[@class='shoplist']/li"):
            link = 'https://emalls.ir' + shop.xpath(".//div[@class = 'shop-logo-wrapper']/a/@href")[0]
            shop_name = shop.xpath(".//div[@class = 'shop-logo-wrapper']/a/@title")[0]
            rate = shop.xpath("normalize-space(.//span[@class = 'ml5 bold']/text())")
            location = shop.xpath(".//a[@class = 'shop-location']/span/text()")[0]
            name = shop.xpath(".//a[@class = 'shop-description m5']/text()")[0]
            direct_link = shop.xpath(".//a[@class = 'shop-description m5']/@href")[0]
            try:
                garantee = shop.xpath(".//span[@class = 'shop-description blue bold']/text()")[0]
            except:
                garantee = ''
            description = shop.xpath("normalize-space(.//span[@class = 'shop-description shop-description-mini']/text())")
            price = shop.xpath("normalize-space(.//a[@class = 'shop-price']/text())")
            time = shop.xpath(".//span[@class = 'block right-align hide700']/text()")[0]
            try:
                discount = shop.xpath("normalize-space(.//div[@class = 'shop-price-discount']/text())")
                last_price = shop.xpath("normalize-space(.//div[@class = 'shop-price-discount-box']/del/text())")
            except:
                discount = ''
                last_price = ''
            #status = shop.xpath("normalize-space(.//span[@style = 'shop-price-discount-box']/text())")
            shops.append({'link': link, 'shop_name': shop_name, 'price':price,
                             'discount': discount, 'last_price': last_price, 'time': time,
                             'rate':rate, 'name': name, 'location': location,
                             'direct_link': direct_link, 'garantee':garantee, 'description':description,
                             })
        return shops

async def fetch_with_sem_shoplist(sem, session, url):
    async with sem:
        return await fetch_shoplist(url, session)

async def main_shoplist(urls):
    set_arsenic_log_level()
    tasks = []
    sem = asyncio.Semaphore(10)
    async with ClientSession(headers=headers) as session:
        for url in urls:
            tasks.append(
                asyncio.create_task(
                    fetch_with_sem_shoplist(sem, session, url)
                )
            )
        pages_content = await asyncio.gather(*tasks) 
        return pages_content


def shoplist_emalls(urls):
    results = asyncio.run(main_shoplist(urls))
    shops=[]

    for result in results:
        shops = shops + result
    print(len(shops))
    return(shops)
