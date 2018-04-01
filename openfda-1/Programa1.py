import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
drugs_raw = r1.read().decode("utf-8")
conn.close()

info = json.loads(drugs_raw)

medicamento = info['results'][0]
print("Id del medicamento: ", medicamento['id'])
print("Uso del medicamento: ", medicamento['purpose'][0])
print("Fabricado por: ", medicamento['openfda']['manufacturer_name'])
