import requests

# POST
# data = requests.post('http://127.0.0.1:5000/advert/', json={'title': '9', 'username': '91', 'content': '19'})
# print(data.status_code)
# print(data.text)

# GET

# data = requests.get('http://127.0.0.1:5000/advert/4/')
# print(data.status_code)
# print(data.text)

# PATCH

data = requests.patch('http://127.0.0.1:5000/advert/4/', json={'title': 'patched1'})
print(data.status_code)
print(data.text)

# DELETE

# data = requests.delete('http://127.0.0.1:5000/advert/1/')
# print(data.status_code)
# print(data.text)






