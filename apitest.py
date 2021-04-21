import requests

url = "https://community-open-weather-map.p.rapidapi.com/find"

querystring = {"q":"Aberdeen","cnt":"0","mode":"null","lon":"0","type":"link, accurate","lat":"0","units":"metric"}

headers = {
    'x-rapidapi-key': "1ee9e278d4msh3e637e58cb6150cp1c278fjsncb7f528a56f2",
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
print(q.weathertem)