import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import csv
import re
import string

class WebScraper:
    def __init__(self, url):
        self.url = url
        
    def scrape(self):
        retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[ 500, 502, 503, 504 ])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        
        response = http.get(self.url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()
        return content
        
class DataCleaner:
    def __init__(self, content):
        self.content = content
    
    def remove_punctuation(self, text):
        return text.translate(str.maketrans('', '', string.punctuation))
    
    def remove_stopwords(self, text):
        stopwords = ["a", "an", "the", "and", "or", "but", "if", "then", "else", "while", "for", "in", "of", "at", "on", "by", "to", "from", "with"]
        text = ' '.join([word for word in text.split() if word.upper() not in stopwords])
        return text
    
    def clean_data(self):
        # Remove punctuation
        self.content = self.remove_punctuation(self.content)
        # Convert to lower case
        self.content = self.content.lower()
        # Remove stop words
        self.content = self.remove_stopwords(self.content)
        return self.content

if __name__ == '__main__':
    with open('E:\\test\\tender.txt', 'r') as f:
        urls = f.read().splitlines()

    with open('output_4.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['URL', 'Content', 'Cleaned Content']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for i, url in enumerate(urls):
            try:
                scraper = WebScraper(url)
                content = scraper.scrape()
                cleaner = DataCleaner(content)
                cleaned_content = cleaner.clean_data()
                writer.writerow({'URL': url, 'Content': content, 'Cleaned Content': cleaned_content})

                print("Content of page {}: {}".format(i+1, url))
                print("Raw Content: ", content)
                print("Cleaned Content: ", cleaned_content)
            except requests.exceptions.RequestException as e:
                print("Error while processing page {}: {}".format(i+1, url))
                print("Exception: ", e)
                continue
