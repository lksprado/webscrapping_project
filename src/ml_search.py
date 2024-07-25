import requests 
from bs4 import BeautifulSoup
import pandas as pd 


keyword = "sabonete"

url = f"https://lista.mercadolivre.com.br/{keyword}"

response = requests.get(url)

if response.status_code ==200:
    print(response.json())
else:
    print("error")

