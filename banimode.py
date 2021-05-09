import asyncio
from arsenic import get_session, browsers, services
from bs4 import BeautifulSoup
import logging
import structlog


def set_arsenic_log_level(level = logging.WARNING):
    logger = logging.getLogger('arsenic')

    def logger_factory():
        return logger

    structlog.configure(logger_factory=logger_factory)
    logger.setLevel(level)


async def scraper_all(url):
    service = services.Chromedriver()
    browser = browsers.Chrome()
    browser.capabilities = {
        "goog:chromeOptions": {"args": ["--headless", "--disable-gpu"]}
    }
    async with get_session(service, browser) as session:
        await asyncio.wait_for(session.get(url),timeout=100)
        
        body = await session.get_page_source()
        soup = BeautifulSoup(body, 'html.parser')
        products = []
        box = soup.find("div", {"id":"product_list"})
        li = box.findAll("article")
        for l in li:
            try:
                link = 'https://banimode.com' + l.find ('a', href=True)['href']
                img = l.find('img')['src']
                name = l.find('span', {'class':'product-card-name'}).getText()
                price = l.find('span', {'class':'price-disgit'}).getText()
                sizes = [(s.find('a').getText()).replace(' ','').replace('\n','') for s in l.find('ul', {'class':'product-card-size'}).findAll('li')]
                brand = l.find('span', {'class':'product-card-brand'}).getText()
                
            except:
                link = ''
                img = ''
                name = ''
                price = ''
                sizes = []
                brand = ''
            try:
                discount = l.find('span', {'class':'product-card-discount'}).getText()
                last_price = l.find('span', {'class':'product-card-lastprice'}).getText()
            except:
                discount = ''
                last_price = ''
            try:
                bonous = (l.find('span', {'class':'product-card-size-tag'}).getText()).replace('  ','').replace('\n', '')
            except:
                bonous = ''
            
            products.append({'link':link, 'img':img, 'name':name, 'discount':discount, 'last_price':last_price,
                             'price':price, 'bonous':bonous, 'sizes': sizes, 'brand': brand})
        return products


async def run_all(urls):
    set_arsenic_log_level()
    result = []
    for i, url in enumerate(urls):
        result.append(
            asyncio.create_task(scraper_all(url))
        )
    results = await asyncio.gather(*result)
    products = []
    for r in results:
        products = products + r  
    return products


def all_banimode(total_pages,subject):
    urls = ['https://www.banimode.com/search?search_query=' + subject + '&page=' + str(i) for i in range(1,int(total_pages)+1)]
    products = asyncio.run(run_all(urls))
    
    print(len(products))
    return(products) 


def special_banimode(total_pages,subject):
    urls = ['https://www.banimode.com/search?sort|discount=desc&search_query=' + subject + '&page=' + str(i) for i in range(1,int(total_pages)+1)]
    products = asyncio.run(run_all(urls))
    
    print(len(products))
    return(products) 



async def incredible(url):
    service = services.Chromedriver()
    browser = browsers.Chrome()
    browser.capabilities = {
        "goog:chromeOptions": {"args": ["--headless", "--disable-gpu"]}
    }
    async with get_session(service, browser) as session:
        await asyncio.wait_for(session.get(url),timeout=100)
        
        body = await session.get_page_source()
        soup = BeautifulSoup(body, 'html.parser')
        products = []
        box = soup.find("div", {"class":"flash-product-wrapper bani-container"})
        li = box.findAll("a",{'class':'flash-product'})
        for l in li:
            link = l['href']
            img =  l.find('div',{'class':'img-box'}).find('img')['src']
            name = l.find('p', {'class':'f-p-name'}).getText()
            price = l.find('span', {'class':'specific-price price'}).getText()
            brand = l.find('p', {'class':'f-p-logo'}).getText()
            
            try:
                discount = l.find('div', {'class':'discount'}).find('p').getText()
                last_price = l.find('span', {'class':'old-price price'}).getText()
            except:
                discount = ''
                last_price = ''
            
            products.append({'link':link, 'img':img, 'name':name, 'discount':discount, 'last_price':last_price,
                             'price':price, 'brand': brand})
        return products


async def run_incredible(urls):
    set_arsenic_log_level()
    result = []
    for url in urls:
        result.append(
            asyncio.create_task(incredible(url))
        )
    results = await asyncio.gather(*result)
    products = []
    for r in results:
        products = products + r  
    return products


def incredible_banimode():
    urls = ['https://www.banimode.com/flashsales']
    products = asyncio.run(run_incredible(urls))
    
    print(len(products))
    return(products) 

    
