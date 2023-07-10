import requests

for i in range(len(jobList)):
     url = "https://172.26.88.203/ " + i + "/kill"

payload = ""
headers = {
  'x-apikey': 'accesskey=redact; secretkey=redact;'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
