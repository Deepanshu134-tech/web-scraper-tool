import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_url(self, url):
        try:
            # Validate URL
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                return None, "Invalid URL format"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract common data points
            data = {
                'title': self._get_title(soup),
                'meta_description': self._get_meta_description(soup),
                'headings': self._get_headings(soup),
                'links': self._get_links(soup),
                'images': self._get_images(soup),
                'paragraphs': self._get_paragraphs(soup)
            }
            
            return data, None
        
        except Exception as e:
            return None, str(e)
    
    def _get_title(self, soup):
        title = soup.find('title')
        return title.text if title else ''
    
    def _get_meta_description(self, soup):
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta['content'] if meta else ''
    
    def _get_headings(self, soup):
        headings = {}
        for level in range(1, 7):
            tags = soup.find_all(f'h{level}')
            headings[f'h{level}'] = [h.text.strip() for h in tags]
        return headings
    
    def _get_links(self, soup):
        links = []
        for link in soup.find_all('a', href=True):
            links.append({
                'text': link.text.strip(),
                'href': link['href']
            })
        return links
    
    def _get_images(self, soup):
        images = []
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        return images
    
    def _get_paragraphs(self, soup):
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.text.strip()
            if text:
                paragraphs.append(text)
        return paragraphs
    
    def create_csv(self, data, filename):
        try:
            # Flatten the data structure for CSV
            csv_data = {
                'Title': [data['title']],
                'Meta Description': [data['meta_description']],
                'Headings (H1)': ['\n'.join(data['headings']['h1'])],
                'Headings (H2)': ['\n'.join(data['headings']['h2'])],
                'Paragraphs': ['\n'.join(data['paragraphs'])]
            }
            
            # Links and Images need separate handling
            links_df = pd.DataFrame(data['links'])
            images_df = pd.DataFrame(data['images'])
            
            # Save to CSV
            main_df = pd.DataFrame(csv_data)
            
            # Write to different sheets in Excel would be better, but for CSV we'll combine
            with open(filename, 'w', encoding='utf-8') as f:
                main_df.to_csv(f, index=False)
                f.write("\n\n--- LINKS ---\n")
                links_df.to_csv(f, index=False)
                f.write("\n\n--- IMAGES ---\n")
                images_df.to_csv(f, index=False)
            
            return True, None
        except Exception as e:
            return False, str(e)