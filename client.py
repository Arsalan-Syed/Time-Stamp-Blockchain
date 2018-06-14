import requests
import filemanager as fm

file_name="test.jpg"
headers = {'content-type': 'application/json'}
url="http://127.0.0.1:5000/add"
payload={"file_name":file_name,"file_hash":fm.get_file_hash(file_name)}
resp = requests.post(url, json=payload)
print(resp.text)
print("Client done")
