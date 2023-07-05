import requests

# POST
data = requests.post('http://127.0.0.1:5000/advert/', json={'title': '23', 'username': '232', 'content': '232'})
print(data.status_code)
print(data.text)

# GET

# data = requests.get('http://127.0.0.1:5000/advert/5/')
# print(data.status_code)
# print(data.text)

# PATCH

# data = requests.patch('http://127.0.0.1:5000/advert/1/', json={'title': 'patched1'})
# print(data.status_code)
# print(data.text)

# DELETE

# data = requests.delete('http://127.0.0.1:5000/advert/9/')
# print(data.status_code)
# print(data.text)






