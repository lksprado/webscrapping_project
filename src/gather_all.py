
import json 
import os 
import pandas as pd 

class Gather:
    def __init__(self, config_file_path: str = './.git/config.json'):
        self.config_file_path = config_file_path
        self.config = self.read_config()
        self.scrapped_folder = self.config.get('scrapped_folder')
        self.silver_dir = self.config.get('silver_dir') 
        
    

    # READING CONFIG FILE
    def read_config(self):
        with open(self.config_file_path, 'r') as file:
            config_data = json.load(file)
        return config_data
        
    def gather_files(self):
        li = [] 
        
        for file in os.listdir(self.scrapped_folder):
            if file.endswith('.csv'):
                df = pd.read_csv(os.path.join(self.scrapped_folder, file), index_col=None, header=0)
                li.append(df)
        final_df = pd.concat(li, axis=0, ignore_index=True)
        
        destination = os.path.join(self.silver_dir, 'all_data_products.csv')
        final_df.to_csv(destination, index=False)
        
if __name__ == "__main__":
    gather = Gather()
    gather.gather_files() 
        
        