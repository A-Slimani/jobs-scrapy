# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

class ProcessJobsPipeline:

    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.environ.get('hostname'), 
            database=os.environ.get('database'), 
            user=os.environ.get('username'), 
            password=os.environ.get('password')
        )

        self.cursor = self.connection.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            title TEXT,
            company TEXT,
            salary VARCHAR(100),
            location TEXT,
            link TEXT,
            close_date DATE,
            website TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

    def process_item(self, item, spider):
        self.cursor.execute("SELECT * FROM jobs WHERE title=%s AND company=%s", (item['title'], item['company'],))
        result = self.cursor.fetchone()

        if result:
            spider.logger.warn(f"Job item already exists: {item['title']}")
        else:
            try:
                self.cursor.execute("INSERT INTO jobs (title, company, close_date, salary, location, link, website) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                ,(
                    item['title'],
                    item['company'],
                    item['close_date'],
                    item['salary'],
                    item['location'],
                    item['link'],
                    item['website']
                ))
                self.connection.commit()
            except Exception as e:
                spider.logger.error(f"Error inserting job item: {e}")
                spider.crawler.engine.close_spider(spider, 'Closing spider due to database insertion error')
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()