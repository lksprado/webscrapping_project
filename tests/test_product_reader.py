import pandas as pd 
import pytest 
from unittest.mock import patch, mock_open, MagicMock
from src.product_reader import ProductReader


# MOCKING FILES AND THEIR DATA
mock_config =  '{"product_path": "test_products.xlsx"}'
mock_df = pd.DataFrame({'SEARCH_LIST': ['Café', 'café', 'Água', 'Cachaça']})
mock_sku_df = pd.DataFrame({'SKU': ['1234', '578', '896']})

# THE PATCH DECORATOR IS USED TO REPLACE A SPECIFIED OBJECT WITH A MOCK FOR THE TEST. IT ALLOWS CONTROLLING
# AND INSPECT THE BEHAVIOR OF THE OBJECT BEING REPLACED, WITHOUT EXECUTING THE ACTUAL CODE.

# THE builtins.open SPECIFIES THE TARGET OPTION AND MIMICS THE BUILT IN PYTHON FUNCTION 'OPEN' WITHOUT THE NEED TO ACCESS THE FILE SYSTEM
# THE NEW_CALLABLE PARAMETER CALLS THE FUNCTION THAT WILL BE USED TO TO MOCK THE OBJECT THA REPLACES THE TARGET ONE
# READ_DATA PARAMETER IS AN ARGUMENT FOR THE MOCK_OPEN
# THIS TEST ENSURES THE FUNCTION CORRECTLY READS THE JSON FILE AND THE PATH FOR THE PRODUCTS FILE 
@patch('builtins.open', new_callable=mock_open, read_data=mock_config)
def test_read_config(mock_file):
    reader = ProductReader(config_file_path='test_config.json')
    reader.read_config()
    assert reader.config_data['product_path'] == 'test_products.xlsx'

# REPLACES THE PANDAS.READ_EXCEL FUNCTION WITH A MOCK OBJETCT FOR THE DURATION OF THE TEST    
@patch('pandas.read_excel')
def test_read_product(mock_read_excel):
    mock_read_excel.return_value = mock_df
    
    reader = ProductReader()
    reader.config_data = {'product_path': 'test_products.xlsx'}
    reader.read_product(sheet_name='Sheet1')
    
    pd.testing.assert_frame_equal(reader.product_df, mock_df)

@patch('pandas.read_excel')
def test_read_sku(mock_read_excel):
    mock_read_excel.return_value = mock_sku_df
    
    reader = ProductReader()
    reader.config_data = {'product_path': 'test_products.xlsx'}
    reader.read_sku(sheet_name='Sheet2')
    pd.testing.assert_frame_equal(reader.sku_df, mock_sku_df)
                        
    
# THIS DECORATOR DEFINES MULTIPLE SETS OF INPUT DATA AND EXPECTED OUTPUT FOR THE TESTING
@pytest.mark.parametrize("input_text, expected_output", [
    ("Café com açúcar", "Cafe com acucar"),
    ("Cachaça", "Cachaca"),
    ("FEIJÃO", "FEIJAO"),
    ("arroz", "arroz"),
    ("", ""),
    (None, None)
])
def test_remove_special_characters(input_text, expected_output):
    reader = ProductReader()
    result = reader._remove_special_characters(input_text)
    assert result == expected_output

# REPLACES THE PANDAS.READ_EXCEL FUNCTION WITH A MOCK OBJECT FOR THE DURATION OF THE TEST  
# USES THE MOCKED DATAFRAME 
@patch('pandas.read_excel')    
def test_standardize_product(mock_read_excel):
    mock_read_excel.return_value = mock_df  # makes pandas.read_excel return the mocks whenever its called
    
    reader = ProductReader()
    reader.config_data = {'product_path': 'test_products.xlsx'}
    reader.read_product(sheet_name='Sheet1')
    product_list = reader.standardize_product()
    
    expected_product_list = ['cafe', 'agua', 'cachaca']
    assert product_list == expected_product_list
    
@patch('pandas.read_excel')    
def test_standardize_sku(mock_read_excel):
    mock_read_excel.return_value = mock_sku_df  # makes pandas.read_excel return the mocks whenever its called
    
    reader = ProductReader()
    reader.config_data = {'product_path': 'test_products.xlsx'}
    reader.read_sku(sheet_name='Sheet2')
    sku_list = reader.standardize_sku()
    
    expected_sku_list = ['1234', '578', '896']
    assert sku_list == expected_sku_list