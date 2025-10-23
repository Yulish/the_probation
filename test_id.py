import requests


url = 'http://127.0.0.1:8000/api/submitData/36'

response = requests.get(url)


if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Ошибка: {response.status_code}")
    print(response.text)