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

async def scraper(url):
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
        box = soup.find("ul", {"class":"category_styles_product_card_list__1Xocv"})
        li = box.findAll("li")
        for l in li:
            try:
                link = 'https://timcheh.com' + l.find ('a', href=True)['href']
                img = l.find('img')['src']
                name = l.find('h3').getText()
                price = l.find('div', {'class':'styles_price__cldWW'}).getText()
            except:
                link = ''
                img = ''
                name = ''
                price = ''
            try:
                discount = l.find('div', {'class':'styles_discount_number__39goM'}).find('span').getText()
                old_price = l.find('div', {'class':'styles_old_price__35bDJ'}).getText()
            except:
                discount = ''
                old_price = ''
            try:
                bonous = l.find('span', {'class':'styles_caption__3SE4x'}).getText()
            except:
                bonous = ''
            
            products.append({'link':link, 'img':img, 'name':name, 'discount':discount, 'last_price':old_price,
                             'price':price, 'bonous':bonous})
        return products


async def run(urls):
    set_arsenic_log_level()
    result = []
    for url in urls:
        result.append(
            asyncio.create_task(scraper(url))
        )
    results = await asyncio.gather(*result)
    products = []
    for r in results:
        products = products + r
    return products

def all_timcheh(total_pages,subject):
    urls = ['https://timcheh.com/search?q='+subject +'&has_selling_stock=1&page='+str(i) for i in range(1,int(total_pages)+1)]
    products = asyncio.run(run(urls))
    print(len(products))
    return(products)   

def special_timcheh(total_pages,subject):
    urls = ['https://timcheh.com/search?q='+subject+'&sortBy=promotion&has_selling_stock=1&page='+str(i) for i in range(1,int(total_pages)+1)]
    products = asyncio.run(run(urls))
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
        box = soup.findAll("div", {"style":"width: 215px; margin-left: 16px;"})
        for l in box:
            try:
                link = 'https://timcheh.com' + l.find ('a', href=True)['href']
                img = l.find('img')['src']
                name = l.find('h3').getText()
                price = l.find('div', {'class':'styles_price__cldWW'}).getText()
            except:
                link = ''
                img = ''
                name = ''
                price = ''
            try:
                discount = l.find('div', {'class':'styles_discount_number__39goM'}).find('span').getText()
                old_price = l.find('div', {'class':'styles_old_price__35bDJ'}).getText()
            except:
                discount = ''
                old_price = ''
            try:
                bonous = l.find('span', {'class':'styles_caption__3SE4x'}).getText()
            except:
                bonous = ''
            
            products.append({'link':link, 'img':img, 'name':name, 'discount':discount, 'last_price':old_price,
                             'price':price, 'bonous':bonous})
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

def incredible_timcheh():
    urls = ['https://timcheh.com/']
    products = asyncio.run(run_incredible(urls))
    print(len(products))
    return(products)   