# -- Ejemplo de cliente web que se conecta al servidor
import http.client

PORT = 8000
headers=('Content-type', 'text/html')

# Nos conectamos al servidor
conn = http.client.HTTPConnection('localhost', PORT)

# Se envía un mensaje de solicitud (Verbo: GET), Recurso: Raiz
conn.request("GET", "/")

# Lee el mensaje de respuesta recibido del servidor
r1 = conn.getresponse()

# Imprimir la linea de estado de la respuesta
print(r1.status, r1.reason)

# Leer el contenido de la respuesta y convetirlo a una cadena
info = r1.read().decode("utf-8")

# Imprimir el fichero html recibido
print(info)
