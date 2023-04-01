import requests

url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"

querystring = {"ingr":"5 star"}

headers = {
	"X-RapidAPI-Key": "d9aba84d9emshcb2865b2454f504p1c8708jsn67d111f19bad",
	"X-RapidAPI-Host": "edamam-food-and-grocery-database.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.json())