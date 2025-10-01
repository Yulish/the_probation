import requests

url = 'http://127.0.0.1:8000/api/submitData/'
data = {
    "beautyTitle": "пер. ",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "",
    "add_time": "2021-09-22 13:18:13",
    "user": {
        "email": "qwerty@mail.ru",
        "fam": "Пупкин",
        "name": "Василий",
        "otc": "Иванович",
        "phone": "+7 555 55 55"
    },
    "coord": {
        "latitude": 45.3842,
        "longitude": 7.1525,
        "height": 1200
    },
    "level": {
        "winter": "",
        "summer": "1А",
        "autumn": "1А",
        "spring": ""
    },
    "images": [
        {
            "title": "Седловина",
            "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        }
    ]
}

response = requests.post(url, json=data)
print('Статус код:', response.status_code)
print('Ответ:', response.text)
