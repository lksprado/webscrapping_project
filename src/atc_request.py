import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import pandas as pd
import datetime
import logging


# Configure logging
logging.basicConfig(
    filename='./logs/atacadao_scrapper.log',  # Log file name
    level=logging.INFO,                # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AtacadaoScrapper:
    def __init__(self):
        self.origin = "https://www.atacadao.com.br/api/graphql?operationName=ProductsQuery&variables="
        self.results_quantity = 100
        self.keyword = ''
        self.http = self._configure_session()
        logging.info("Initialized AtacadaoScrapper")
    

    def _configure_session(self):
        retry_strategy = Retry(
            total=3, # HOW MANY RETRIES
            status_forcelist=[403,429,500, 502, 503, 504] # FOR THESE STATUS CODE FAILURE
        )
        adapter = HTTPAdapter(max_retries=retry_strategy) # CONTROLS THE REQUEST CALLS
        session = requests.Session() # TO PERSIST SESSION VARIABLES FOR THE FOLLOWING REQUESTS
        session.mount("https://",adapter)
        session.mount("http://",adapter)
        
        logging.info("HTTP session configured with retries")
        return session
    

    def search_products(self, keyword):
        url = f'{self.origin}{{%22first%22:{self.results_quantity},%22after%22:%220%22,%22sort%22:%22score_desc%22,%22term%22:%22{keyword}%22,%22selectedFacets%22:[{{%22key%22:%22region-id%22,%22value%22:%22U1cjYXRhY2FkYW9icjM0MA==%22}},{{%22key%22:%22channel%22,%22value%22:%22{{\\%22salesChannel\\%22:\\%221\\%22,\\%22seller\\%22:\\%22atacadaobr340\\%22,\\%22regionId\\%22:\\%22U1cjYXRhY2FkYW9icjM0MA==\\%22}}%22}},{{%22key%22:%22locale%22,%22value%22:%22pt-BR%22}}]}}'
        
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
        }
        try:
            response = self.http.get(url, headers=headers) # USES THE CONFIGURED SESSION
            if response.status_code == 200:
                return response.json()
            else:
                logging.warning("Failed to fetch products. Status code: %d", response.status_code)
                return None
        except Exception as e:
            logging.error("Error occurred while fetching products: %s", e)
            return None
    
    def extract_data(self, data):
        products = []
        for edge in data.get('data', {}).get('search', {}).get('products', {}).get('edges', []): # gets into edges dictionary
            node = edge.get('node') #gets into node dictionary
            breadcrumb_list = node.get('breadcrumbList').get('itemListElement') #gets into itmemListElement 
            category = breadcrumb_list[0]['name']  # gets into first element of list and fetch the name
            sub_category = breadcrumb_list[1]['name'] # gets into second element of list and fetch the name
            seller = node.get('sellers')[0] # gets into first element of seller
            tax = seller.get('commertialOffer').get('Tax') #gets into commertialOffer and fetch tax 
                        
            product = {
                'sku': node.get('sku'),
                'category': category,
                'sub_category': sub_category,
                'product_name': node.get('name'),
                'brand_name': node.get('brand').get('brandName'),
                'high_price': node.get('offers').get('highPrice'),
                'low_price': node.get('offers').get('lowPrice'),
                'tax':tax
            }
            products.append(product)
            
        logging.info("Extracted %d products from data", len(products))
        return products
    

    def start(self, keyword):
        '''STARTS THE SCRAPING PROCESS'''
        data = self.search_products(keyword)
        if data: # checks if data is not empty so it can start the extraction, if not, returns empty
            return self.extract_data(data)
        logging.warning("No data found for keyword: %s", keyword)
        return []   

    def sku_filtering(self, products, skus):
        '''FILTERS THE PRODUCTS BASED ON SKU LIST'''
        filtered_products = [product for product in products if product['sku'] in skus]
        logging.info("Filtered products down to %d items based on SKU list", len(filtered_products))
        return filtered_products

    def save_to_csv(self, products, file_path):
        '''SAVES THE PRODUCTS DATA TO AN EXCEL FILE'''
        df = pd.DataFrame(products)
        
        # Ensure correct data types
        df['high_price'] = pd.to_numeric(df['high_price'], errors='coerce')
        df['low_price'] = pd.to_numeric(df['low_price'], errors='coerce')
        df['tax'] = pd.to_numeric(df['tax'], errors='coerce')
        
        # ADD CURRENT DATE
        df['date_scrapped'] = datetime.datetime.now().strftime('%Y-%m-%d')
        df.to_csv(file_path, index=False)
        
        logging.info("Saved data to %s with %d products", file_path, len(df))