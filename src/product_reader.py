# THIS SCRIPT READS EXCEL FILE THAT CONTAINS THE PRODUCTS THAT WILL BE SEARCHED IN THE SCRAPPER SCRIPT

import json
import pandas as pd
import unicodedata

class ProductReader:
    def __init__(self, config_file_path: str = './.git/config.json'):
        self.config_file_path = config_file_path
        self.config_data = None
        self.product_df = None

    def read_config(self):
        with open(self.config_file_path, 'r') as file:
            self.config_data = json.load(file)

    def read_product(self, sheet_name: str = 'Sheet1'):
        product_file = self.config_data['product_path']
        self.product_df = pd.read_excel(product_file, sheet_name=sheet_name)
        
    def read_sku(self,sheet_name: str = 'Sheet2'):
        product_file = self.config_data['product_path']
        self.sku_df = pd.read_excel(product_file, sheet_name=sheet_name)

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
        
        # RETURN THE LIST OF UNIQUE ITEMS
        return self.product_df['SEARCH_LIST'].tolist()
    
    def standardize_sku(self):
        '''DROPS DUPLICATE SKU IF ANY'''
        self.sku_df.drop_duplicates(subset=['SKU'], inplace=True)
        return self.sku_df['SKU'].tolist()

