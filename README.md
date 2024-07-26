# PERSONAL CPI INDEX - A WEBSCRAPPING PROJECT

## DESCRIPTION
This project involves building a personal consumer price index based on web scraping from the retailer where I make most of my purchases. I believe that this approach will provide a more realistic view of how price variations affect my consumption patterns at the source.

In developing this project, I've tried to apply a series of best practices, including:

- OOP
- Logging
- Testing
- CI/CD

It is expected that weekly files will be generated, which will be loaded into my local data warehouse and later analyzed with Tableau.

## EXECUTION

1. **product_reader.py**    
This script contains the class that reads and stores the data of search terms and SKUs of the products I usually consume. These were previously scraped on another occasion to form an initial filtering base for the queries in an Excel file.

2. **atc_requests.py**  
This script contains the class that generates requests to the product search API on the site, returning a list of products in JSON format. This list is filtered based on SKUs and saved as a CSV file.

3. **main.py**  
Executes the application.
