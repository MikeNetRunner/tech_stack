import requests

url = 'https://tickets.pionier.gov.pl/public/'

response = requests.get(url)

# Print the status code and response text
print(f'Status Code: {response.status_code}')
print(response.text)
