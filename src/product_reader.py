import json
import pandas as pd  

# THIS CODE IS STRAIGHT FORWARD TO COLLECT DESIRED PRODUTS FROM EXCEL FILE

class ProductReader:
    '''INITIALIZES THE PRODUCTREAD WITH A CONFIGURATION FILE FOR ENVIRONMENT VARIABLES'''
    def __init__(self, config_file_path: str = './.git/config.json'):
        self.config_file_path =  config_file_path
        self.config_data = None
        self.product_df = None

    def read_config(self):
        '''READS CONFIGURATION FILE AND STORES IT MEMORY'''
        with open(self.config_file_path, 'r') as file:
            self.config_data = json.load(file)
        
    def read_product(self, sheet_name: str = 'Sheet1'):
        '''READS EXCEL FILE WITH DESIRED PRODUCTS'''
        product_file = self.config_data['product_path']
        self.product_df = pd.read_excel(product_file,sheet_name=sheet_name)
    
    def standardize(self):
        '''STANDARDIZES COLUMNS TO LOWER CASE'''
        self.product_df[['Produto','Marca']] = self.product_df[['Produto','Marca']].apply(lambda x: x.str.lower())        
        return self.product_df

if __name__ == "__main__":
    pr = ProductReader()
    pr.read_config()
    pr.read_product()
    pr.standardize()
