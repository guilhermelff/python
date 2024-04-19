import requests

response = requests.get('https://reqres.in/api/users/2')

print(response.__dict__)