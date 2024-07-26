# THIS SCRIPT READS EXCEL FILE THAT CONTAINS THE PRODUCTS THAT WILL BE SEARCHED IN THE SCRAPPER SCRIPT

import json
import pandas as pd
import unicodedata
import logging
from datetime import datetime

logging.basicConfig(
    filename='./logs/product_reader.log',  # Log file name
    level=logging.INFO,             # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class ProductReader:
    def __init__(self, config_file_path: str = './.git/config.json'):
        self.config_file_path = config_file_path
        self.config_data = None
        self.product_df = None
        self.sku_df = None 
        logging.info("Initialized ProductReader with config file: %s", config_file_path)

    def read_config(self):
        try:
            with open(self.config_file_path, 'r') as file:
                self.config_data = json.load(file)
            logging.info("Config file read successfully")
        except Exception as e:
            logging.error("Failed to read config file: %s", e)
            raise

    def read_product(self, sheet_name: str = 'Sheet1'):
        try:
            product_file = self.config_data['product_path']
            self.product_df = pd.read_excel(product_file, sheet_name=sheet_name)
            logging.info("Product file read successfully with %d entries", len(self.product_df))
        except Exception as e:
            logging.error("Failed to read product file: %s", e)
            raise
        
    def read_sku(self, sheet_name: str = 'Sheet2'):
        try:
            product_file = self.config_data['product_path']
            self.sku_df = pd.read_excel(product_file, sheet_name=sheet_name)
            logging.info("SKU file read successfully with %d entries", len(self.sku_df))
        except Exception as e:
            logging.error("Failed to read SKU file: %s", e)
            raise

    def _remove_special_characters(self, text):
        '''REMOVES ACCENTS AND SPECIAL CHARACTERS FROM TEXT, IF TEXT IS STRING'''
        if isinstance(text, str):
            text = unicodedata.normalize('NFKD', text)
            text = ''.join([c for c in text if not unicodedata.combining(c)])
        return text

    def standardize_product(self):
        '''MAKES DATA LOWER CASE, FILTERING, SELECT PRODUCT COLUMN ONLY, REMOVES SPECIAL CHARACTERS'''
        # CONVERTS TO LOWER CASE
        self.product_df['SEARCH_LIST'] = self.product_df['SEARCH_LIST'].apply(lambda x: x.lower() if isinstance(x, str) else x)
        
        # REMOVE SPECIAL CHARACTERS FROM 'SEARCH LIST' 
        self.product_df['SEARCH_LIST'] = self.product_df['SEARCH_LIST'].apply(self._remove_special_characters)
        
        # REMOVE DUPLICATES IF ANY ON 'SEARCH_LIST' 
        self.product_df.drop_duplicates(subset=['SEARCH_LIST'], inplace=True)
        
        search_list = self.product_df['SEARCH_LIST'].tolist()
        
        logging.info("Standardized SEARCH_LIST with %d unique items", len(search_list))
        # RETURN THE LIST OF UNIQUE ITEMS
        return search_list
    
    def standardize_sku(self):
        '''DROPS DUPLICATE SKU IF ANY'''
        self.sku_df.drop_duplicates(subset=['SKU'], inplace=True)
        sku_list = self.sku_df['SKU'].tolist()
        logging.info("Standardized SKU list with %d unique SKUs", len(sku_list))
        return sku_list
