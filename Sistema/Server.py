import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from typing import Tuple

from Traffic_Model import *

def positionsToJSON(ps):
    posDICT = []
    for p in ps:
        pos = {
            "x" : p[0],
            "z" : p[1],
            "y" : p[2]
        }
        posDICT.append(pos)
    return json.dumps(posDICT)
def semaforosToJSON(ps):
    posDICT = []
    semaforo = 0
    for i in range(6,10):
        try:
            pos = {
                "semaforo": semaforo,
                "estado" : ps[i].estado,
                "cruzando" : ps[i].cruzando
            }
            semaforo += 1
        except:
            pass
        posDICT.append(pos)
    return json.dumps(posDICT)

class Server(BaseHTTPRequestHandler):
    model = TrafficModel(6,4)
    cars = [[0, 4], [1], [2, 3], [5]]
    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)


    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        try:
            # Revisamos los semaforos y actualizamos estados
            for i in range(6,10):
                semaforo = self.model.schedule.agents[i]
                if semaforo.estado == "verde":
                    for iCarro in self.cars[i-6]:
                        self.model.schedule.agents[iCarro].estado = 2
                elif semaforo.estado == "amarillo":
                    for iCarro in self.cars[i-6]:
                        self.model.schedule.agents[iCarro].estado = 1
                elif semaforo.estado == "rojo":
                    for iCarro in self.cars[i-6]:
                        self.model.schedule.agents[iCarro].estado = 0


            # Enviamos las posiciones
            if self.path.endswith("/carro"):
                self.model.step()
                self._set_response()
                resp = "{\"positions\":" + positionsToJSON(self.model.positions) + "}"
                self.wfile.write(resp.encode('utf-8'))
            elif self.path.endswith("semaforo"):
                self.model.step()
                self._set_response()
                #resp = "{\"Coches Cruzando\":" + str(self.model.schedule.agents[6].cruzando) + "}"
                resp = "{\"semaforos\":" + semaforosToJSON(self.model.schedule.agents) + "}"
                self.wfile.write(resp.encode('utf-8'))
        except IOError:
            self.send_error(404, "Error")

    def do_POST(self):
        try:
            if self.path.endswith("/carro"):
                content_length = int(self.headers['Content-Length'])
                post_data = json.loads(self.rfile.read(content_length))
                self._set_response()
                resp = "Done"
                print(post_data)
                self.model.schedule.agents[post_data["carro"]].estado = post_data["estado"]
                self.wfile.write(resp.encode('utf-8'))

            # Cuando cruza un carro, al semáforo se le suma la cantidad de coches que están cruzando
            elif self.path.endswith("/semaforoEntrada"):
                content_length = int(self.headers['Content-Length'])
                post_data = json.loads(self.rfile.read(content_length))
                self._set_response()
                semaforoActual = post_data["semaforo"]
                cochesCruzando = post_data["cruza"]
                resp = "Done"
                print(post_data)
                puedePasar = True
                self.model.schedule.agents[semaforoActual + 6].cruzando += cochesCruzando
                # Revisamos si hay algun otro semaforo en verde
                for i in range(6,10):
                    # Si lo hay, lo guardamos en una variable auxiliar
                    semaforoAdyacente = i - 6
                    if semaforoActual % 2 == 0 and semaforoAdyacente % 2 != 0 and self.model.schedule.agents[i].estado == "verde":
                        puedePasar = False
                    if semaforoActual % 2 != 0 and semaforoAdyacente % 2 == 0 and self.model.schedule.agents[i].estado == "verde":
                        puedePasar = False
                # Si no hay ningún semáforo en verde, cambiamos el estado a verde
                if puedePasar:
                    self.model.schedule.agents[post_data["semaforo"] + 6].estado = "verde"
                # Si hay un semaforo en verde, cambiamos el estado a rojo
                elif not puedePasar:
                    self.model.schedule.agents[post_data["semaforo"] + 6].estado = "rojo"
                self.wfile.write(resp.encode('utf-8'))

            # Cuando termina su cruce un carro, el semáforo quita la cantidad de coches que están cruzando
            elif self.path.endswith("/semaforoSalida"):
                content_length = int(self.headers['Content-Length'])
                post_data = json.loads(self.rfile.read(content_length))
                self._set_response()
                semaforoActual = post_data["semaforo"] # Semaforo que termino su cruce
                cochesCruzando = post_data["cruza"] # Coches que estan terminando su cruce
                resp = "Done"
                print(post_data)
                tieneCochesCruzando = False
                self.model.schedule.agents[semaforoActual + 6].cruzando -= cochesCruzando
                # Revisar si el semaforo adyacente tiene coches cruzando
                for i in range(6, 10):
                    # Si lo hay, lo guardamos en una variable auxiliar
                    semaforoAdyacente = i - 6
                    if semaforoActual % 2 == 0:
                        if semaforoActual % 2 == 0 and semaforoAdyacente % 2 == 0 and self.model.schedule.agents[i].cruzando > 0:
                                tieneCochesCruzando = True
                        if semaforoActual % 2 == 0 and semaforoAdyacente % 2 == 0 and self.model.schedule.agents[i].cruzando > 0:
                                tieneCochesCruzando = True
                    else:
                        if semaforoActual % 2 == 1 and semaforoAdyacente % 2 == 1 and self.model.schedule.agents[i].cruzando > 0:
                                tieneCochesCruzando = True
                        if semaforoActual % 2 == 1 and semaforoAdyacente % 2 ==  1 and self.model.schedule.agents[i].cruzando > 0:
                                tieneCochesCruzando = True
                # Si tiene coches cruzando, ambos semaforos se quedan en verde
                if tieneCochesCruzando:
                    self.model.schedule.agents[semaforoActual + 6].estado = "verde"

                # Si hay un semaforo en verde, cambiamos el estado a rojo
                elif not tieneCochesCruzando:
                    self.model.schedule.agents[semaforoActual + 6].estado = "rojo"
                    if semaforoActual == 0 or semaforoActual == 1:
                        self.model.schedule.agents[semaforoActual + 4].estado = "rojo"

                    elif semaforoActual == 2 or semaforoActual == 3:
                        self.model.schedule.agents[semaforoActual + 4].estado = "rojo"
                    # Revisamos si hay un semaforo no adyacente con vehículos esperando para cambiar su estado
                    for i in range(6, 10):
                        if self.model.schedule.agents[i].cruzando > 0:
                            self.model.schedule.agents[i].estado = "verde"

                    # Si ningun coche tiene autos esperando, los ponemos todos en amarillo
                    hayCochesCruzandoOEsperando = False
                    for i in range(6, 10):
                        if self.model.schedule.agents[i].cruzando > 0:
                            hayCochesCruzandoOEsperando = True
                    if not hayCochesCruzandoOEsperando:
                        for i in range(6, 10):
                            self.model.schedule.agents[i].estado = "amarillo"
                    self.wfile.write(resp.encode('utf-8'))


        except IOError:
            self.send_error(404, "Error")

def run(server_class=HTTPServer, handler_class=Server, port=8080): # 8080 para IBM CLoud
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")

if __name__ == '__main__':
    run()