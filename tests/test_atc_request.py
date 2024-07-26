import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.atc_request import AtacadaoScrapper


# MOCKING FILES AND THEIR DATA
mock_response_json = {
    "data": {
        "search": {
            "products": {
                "pageInfo": {
                    "totalCount": 51
                },
                "edges": [
                    {
                        "node": {
                            "id": "9925",
                            "slug": "feijao-carioca-kicaldo-tipo-1-pacote-com-1kg-11874-9925",
                            "sku": "9925",
                            "measurementUnit": "PCT",
                            "unitMultiplier": 1,
                            "properties": [
                                {
                                    "originalName": "sellerId",
                                    "name": "sellerId",
                                    "values": [
                                        "1"
                                    ]
                                }
                            ],
                            "brand": {
                                "brandName": "Kicaldo",
                                "name": "Kicaldo"
                            },
                            "name": "Feijão Carioca Kicaldo Tipo 1 Pacote com 1kg",
                            "gtin": "11874948",
                            "isVariantOf": {
                                "productGroupID": "9925",
                                "name": "Feijão Carioca Kicaldo Tipo 1 Pacote com 1kg"
                            },
                            "image": [
                                {
                                    "url": "https://atacadaobr.vtexassets.com/arquivos/ids/229327/g.jpg?v=638353718648770000",
                                    "alternateName": ""
                                }
                            ],
                            "offers": {
                                "highPrice": 6.3,
                                "lowPrice": 6.19,
                                "offers": [
                                    {
                                        "availability": "available",
                                        "minQuantity": 1,
                                        "unitPerBox": 10,
                                        "price": 6.3,
                                        "listPrice": 6.3,
                                        "quantity": 1,
                                        "seller": {
                                            "identifier": "atacadaobr340"
                                        }
                                    },
                                    {
                                        "availability": "available",
                                        "minQuantity": 10,
                                        "unitPerBox": 10,
                                        "price": 6.19,
                                        "listPrice": 6.19,
                                        "quantity": 1,
                                        "seller": {
                                            "identifier": "atacadaobr340"
                                        }
                                    }
                                ]
                            },
                            "breadcrumbList": {
                                "itemListElement": [
                                    {
                                        "item": "/mercearia/",
                                        "name": "Mercearia",
                                        "position": 1
                                    },
                                    {
                                        "item": "/mercearia/graos/",
                                        "name": "Grãos",
                                        "position": 2
                                    },
                                    {
                                        "item": "/mercearia/graos/feijao/",
                                        "name": "Feijão",
                                        "position": 3
                                    },
                                    {
                                        "item": "/feijao-carioca-kicaldo-tipo-1-pacote-com-1kg-11874-9925/p",
                                        "name": "Feijão Carioca Kicaldo Tipo 1 Pacote com 1kg",
                                        "position": 4
                                    }
                                ],
                                "numberOfItems": 3
                            },
                            "sellers": [
                                {
                                    "sellerId": "1",
                                    "sellerName": "ATACADAO SA",
                                    "sellerDefault": 'true',
                                    "addToCartLink": "",
                                    "commertialOffer": {
                                        "AvailableQuantity": 10000,
                                        "Price": 6.3,
                                        "ListPrice": 6.3,
                                        "spotPrice": 6.3,
                                        "taxPercentage": 'null',
                                        "Tax": 0.38
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }
}
mock_products = [
    {'sku': '9925','category':'Mercearia', 'sub_category': 'Grãos' ,'product_name': 'Feijão Carioca Kicaldo Tipo 1 Pacote com 1kg', 'brand_name': 'Kicaldo', 'high_price': 6.3, 'low_price': 6.19, 'tax': 0.38}
]

skus_all = ['9925']

# TEST IF SEARCH PRODUCTS METHOD CORRECTLY HANDLES AN HTTP RESPONSE
@patch('src.atc_request.requests.Session.get') # REPLACES requests.Session.get with mock object
def test_search_products(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_response_json
    mock_get.return_value = mock_response
    
    scraper = AtacadaoScrapper()
    result = scraper.search_products('test_keywork')
    
    assert result == mock_response_json

#  THIS TESTS DOESN'T NEED PATCH BECAUSE IT DOES NOT INTERACT WITH EXTERNAL SYSTEMS SUCH AS FILES, FILE SYSTEMS OR NETWORKS
def test_extract_data():
    scraper = AtacadaoScrapper()
    result = scraper.extract_data(mock_response_json)
    
    assert result == mock_products


# TEST START METHOD
# THE DECORATOR REPLACES THE SEARCH_PRODUCT AND EXTRACT_DATA WITH A MOCK OBJECT THAT CAN BE CONFIGURED
# TO RETURN SPECIFIC VALUES
@patch.object(AtacadaoScrapper, 'search_products')
@patch.object(AtacadaoScrapper, 'extract_data')
def test_start(mock_extract_data, mock_search_products):
    mock_search_products.return_value = mock_response_json # ASSIGN MOCK DATA
    mock_extract_data.return_value = mock_products # ASSIGN MOCK DATA
    
    scraper = AtacadaoScrapper()
    result = scraper.start('test_keyword')
    
    mock_search_products.assert_called_once_with('test_keyword')
    mock_extract_data.assert_called_once_with(mock_response_json)
    assert result == mock_products

def test_sku_filtering():
    scraper = AtacadaoScrapper()
    filtered_products = scraper.sku_filtering(mock_products, skus_all)
    assert len(filtered_products) ==len(mock_products)
    assert filtered_products == mock_products
    


