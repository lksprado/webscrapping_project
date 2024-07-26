from src.atc_request import AtacadaoScrapper
from src.product_reader import ProductReader
import datetime

if __name__ == "__main__":
    # Initialize and configure ProductReader
    pr = ProductReader()
    pr.read_config()
    pr.read_product()
    pr.read_sku()
    product_keywords = pr.standardize_product()
    sku_code = pr.standardize_sku()

    sku_code = [str(sku) for sku in sku_code]
    # Initialize scraper and fetch data
    scraper = AtacadaoScrapper()
    
    all_products_data = []
    for keyword in product_keywords:
        products_data = scraper.start(keyword)
        if products_data:
            all_products_data.extend(products_data)
            
    print(all_products_data)
    filtered_products = scraper.sku_filtering(all_products_data, sku_code)
    
    file_date = datetime.datetime.now().strftime('%Y-%m-%d')    
    
    # Save filtered products to an Excel file
    if filtered_products:
        file_path = f'/media/lucas/Files/2.Projetos/0.mylake/bronze/atacadao_products/products_scrapped{file_date}.csv'
        scraper.save_to_csv(filtered_products, file_path)
        print(f"Filtered data saved to {file_path}")
    else:
        print("No data found")
    
    
    # if all_products_data:
    #     file_path = f'/media/lucas/Files/2.Projetos/0.mylake/bronze/atacadao_products/products_scrapped{file_date}.csv'
    #     scraper.save_to_csv(all_products_data, file_path)
    #     print(f"Filtered data saved to {file_path}")
    # else:
    #     print("No data found")