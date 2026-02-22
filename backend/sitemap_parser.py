import xml.etree.ElementTree as ET
import requests

class SitemapParser:
    def __init__(self, url):
        self.url = url
        self.urls = []

    def fetch_sitemap(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f'Failed to fetch sitemap: {response.status_code}')

    def parse_sitemap(self, xml_content):
        root = ET.fromstring(xml_content)
        for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap-image/}url'):
            loc = url.find('{http://www.sitemaps.org/schemas/sitemap-image/}loc')
            if loc is not None:
                self.urls.append(loc.text)

    def extract_urls(self):
        xml_content = self.fetch_sitemap()
        self.parse_sitemap(xml_content)
        return self.urls

# Example usage:
# sitemap_parser = SitemapParser('https://example.com/sitemap.xml')
# urls = sitemap_parser.extract_urls()  
# print(urls)