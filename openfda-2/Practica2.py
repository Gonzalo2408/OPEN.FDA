import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=active_ingredient:acetylsalicylic&limit=10", None, headers)
#Cambiamos la URL para que busque el principio activo de la aspirina
r1 = conn.getresponse()

print(r1.status, r1.reason)

drugs_raw = r1.read().decode("utf-8")
conn.close()

info = json.loads(drugs_raw)['results']

for aspirin in info:
    if aspirin['openfda']:
        manufacturer = aspirin['openfda']['manufacturer_name'][0]
        print("La aspirina con ID", aspirin['id'], " es fabricada por: ",manufacturer,"\n")
    else:
        print("El fabricante de la aspirina con ID", aspirin['id']," no está disponible\n")
