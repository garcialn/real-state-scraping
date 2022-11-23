import scrapy
from scrapy_playwright.page import PageMethod

class PwspiderSpider(scrapy.Spider):
    name = 'bh_spider'
    allowed_domains = ['loft.com.br']

    def start_requests(self):
        for i in range(132):
            yield scrapy.Request(
                url=f'https://loft.com.br/venda/imoveis/mg/belo-horizonte?pagina={i}', 
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod('wait_for_selector', 'div.jss265'),
                    ],
                    errback = self.errback
                )   
            )  
        

    async def parse(self, response):
        page = response.meta['playwright_page']
        await page.close()
        for property in response.css('div.jss274'):
            yield {
                'type': property.css('span.jss280::text').get(),
                'address': property.css('div.jss274 h2::text').get().split(', ')[0].replace('R.', 'Rua').replace('Av.', 'Avenida').replace(' ', '_').rstrip('_0123456789'),
                'neighborhood': property.css('div.jss274 h2::text').get().split(', ')[1].replace(' ', '_'),
                'footage': property.css('span.MuiTypography-root.jss121.jss99.jss110.MuiTypography-body1.MuiTypography-noWrap::text').getall()[0],
                'doorms': property.css('span.MuiTypography-root.jss121.jss99.jss110.MuiTypography-body1.MuiTypography-noWrap::text').getall()[2],
                'garages': property.css('span.MuiTypography-root.jss121.jss99.jss110.MuiTypography-body1.MuiTypography-noWrap::text').getall()[3],
                'price': property.css('div.jss278 span::text').get()
            }

    async def errback(self, failture):
            page = failture.request.meta['playwright_page']
            await page.close()