import requests

# Change made
r = requests.get("https://coreyms.com")
print(r.status_code)
