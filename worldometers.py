import scrapy


class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        countries = response.xpath('//td/a')

        for country in countries:
            country_name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()

            if link:
                yield response.follow(url=link, callback=self.parse_country, meta={'country': country_name})

    def parse_country(self, response):
        rows = response.xpath("(//table[contains(@class, 'table')])[1]/tbody/tr")
        for row in rows:
            country = response.meta.get('country')
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/text()").get()

            yield {
                'country': country,
                'year': year,
                'population': population,
            }
