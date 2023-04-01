import requests
from config import app_id, app_key

food_item = 'coke'

# API endpoint for Edamam Food Database
url = f'https://api.edamam.com/api/food-database/v2/parser?ingr={food_item}&app_id={app_id}&app_key={app_key}'

# send GET request to API endpoint
response = requests.get(url)

# parse JSON response
data = response.json()

# retrieve calorie information from response
calories = data['hints'][0]['food']['nutrients']['ENERC_KCAL']
quantity = data['hints'][0]['measures'][0]['label']

# print calorie information
print(f'{quantity} of {food_item} has {calories} calories.')



	