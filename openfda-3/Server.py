import http.server
import socketserver
import http.client
import json

# -- Puerto donde lanzar el servidor
PORT = 8000


# Clase con nuestro manejador. Es una clase derivada de BaseHTTPRequestHandler
# Esto significa que "hereda" todos los metodos de esta clase. Y los que
# nosotros consideremos los podemos reemplazar por los nuestros
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET. Este metodo se invoca automaticamente cada vez que hay una
    # peticion GET por HTTP. El recurso que nos solicitan se encuentra
    # en self.path
    def do_GET(self):

        # La primera linea del mensaje de respuesta es el
        # status. Indicamos que OK
        self.send_response(200)

        # En las siguientes lineas de la respuesta colocamos las
        # cabeceras necesarias para que el cliente entienda el
        # contenido que le enviamos (que sera HTML)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Este es el mensaje que enviamos al cliente: un texto y
        # el recurso solicitado
        headers = {'User-Agent': 'http-client'}

        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json?limit=11", None, headers)

        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()

        info = json.loads(drugs_raw)
        data = []  # Creamos una lista vacía que vaya agregando cada medicamento

        for i in info['results']:  # Iteramos sobre las variables que tiene la página
            if i['openfda']:
                nombre = i['openfda']['brand_name'][0]
                data.append(nombre)  # Cuando la iteración detecte un 'brand_name', ese brand_name se incorpora a la lista data

        with open('medicamentos.html','w') as f:
            mensaje = """<html><head>Nombres de medicamentos:</head><body>"""
            mensaje += "<p>{}</p>".format(data)
            mensaje += "</body></html>"  # Escribimos el mensaje que queremos que nos envíe la html

            f.write(mensaje)
            f.close()

        if self.path == "/" or self.path == "/medicamentos":
            with open("medicamentos.html", "r") as f:
                message = f.read()
        else:
            message = "Error"  # Con esto comprobamos que la URL es la correcta

        # Enviar el mensaje completo
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return



# ----------------------------------
# El servidor comienza a aqui
# ----------------------------------
# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

# -- Configurar el socket del servidor, para esperar conexiones de clientes
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Sirviendo al puerto", PORT)

    # Entrar en el bucle principal
    # Las peticiones se atienden desde nuestro manejador
    # Cada vez que se ocurra un "GET" se invoca al metodo do_GET de
    # nuestro manejador
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Interrumpido por el usuario")

print("")
print("Servidor parado")