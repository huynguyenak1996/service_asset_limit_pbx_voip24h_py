import requests
import json

url = "http://14.225.251.72:7227/eapi/api/backupservice/restoreServicePbx"

payload = json.dumps({
  "contract_code": "HD100005539",
  "extension": [
    "100",
    "101",
    "102"
  ],
  "did": [
    "842871098000"
  ]
})
headers = {
  'Content-Type': 'application/json',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
