import requests
import json

resp = requests.get("http://45-56-95-50.ip.linodeusercontent.com/x/json", stream=True, headers={"Authorization": "Bearer tk_632ejha524dlfcgx7dnqnxb5in4sx"})
for line in resp.iter_lines():
  if line:
    print(line)
x = 1
