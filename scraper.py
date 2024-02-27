import requests
import pandas as pd
from io import StringIO

# set up the request parameters
params = {
    'api_key': '13E1803DDB10422A95DC3A5631D4B11F',
    'search_term': 'fresh food',
    'type': 'search',
    'category_id': '976759',
    'customer_zipcode': '98007',
    'output': 'csv',
    'page': '21',
    'max_page': '25'
}

# make the http GET request to BlueCart API
api_result = requests.get('https://api.bluecartapi.com/request', params)


# Check if the request was successful
if api_result.status_code == 200:
    # Parse the CSV content
    csv_content = api_result.content.decode('utf-8')

    # Create a DataFrame from the CSV content
    df = pd.read_csv(StringIO(csv_content))

    # Extract the required columns
    selected_columns = ['search_results.product.title',
                        'search_results.product.link',
                        'search_results.product.main_image',
                        'search_results.offers.primary.price',
                        'search_results.offers.primary.list_price']
    extracted_data = df[selected_columns]

    extracted_data = extracted_data.rename(columns={
        'search_results.product.title': 'Product Name',
        'search_results.product.link': 'Product Link',
        'search_results.product.main_image': 'Product Image',
        'search_results.offers.primary.price': 'Current Price',
        'search_results.offers.primary.list_price': 'Original Price'
    })

    # Save the extracted data to a CSV file
    file_path = 'data/products.csv'
    extracted_data.to_csv(file_path, index=False)

    print(f"Extracted data successfully saved to {file_path}")
else:
    print(f"Failed to fetch data: Status code {api_result.status_code}")
