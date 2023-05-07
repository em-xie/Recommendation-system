import csv

import scrapy

BASE_URL = 'https://myanimelist.net/anime'

class AnimeSpider(scrapy.Spider):
    name = "anime"
    def start_requests(self):
     with open('E://PyCode/Recommendation-system/dataset/anime.csv',encoding='gb18030', errors='ignore') as csv_file:
        reader = csv.DictReader(csv_file)
        anime_ids = [row["anime_id"] for row in reader]
        with open('output.csv') as output_file:
            output_reader = csv.DictReader(output_file)
            existing_anime_ids = [row['anime_id'] for row in output_reader]
            anime_ids = [id for id in anime_ids if id not in existing_anime_ids]
            for id in anime_ids:
                yield scrapy.Request(url=f'{BASE_URL}/{id}', callback=self.parse, meta={'anime_id': id})

    def parse(self, response):
        anime_id = response.meta.get("anime_id")
        japanese_titles = response.xpath("//span[contains(text(), 'Japanese')]/../text()").getall()
        japanese_titles = [text.strip() for text in japanese_titles]
        japanese_titles = [text for text in japanese_titles if len(text) > 0][0]
        aired = response.xpath("//span[contains(text(), 'Aired')]/../text()").getall()
        aired = [text.strip() for text in aired]
        aired = [text for text in aired if len(text) > 0][0]
        image_url = response.xpath("//a[contains(@href, 'pics')]/img/@data-src").getall()[0]
        print(f"{japanese_titles} {aired}")
        1
        yield {
            'anime_id': anime_id,
            'japanese_title': japanese_titles,
            'aired': aired,
            'image_url': image_url
        }
