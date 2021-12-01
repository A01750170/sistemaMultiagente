'''
Programa que ejecuta el servidor del proyecto,
contiene referencias a TrafficModel.py para modificar el
estado del modelo dependiendo de las peticiones que se le 
hagan al servidor

Autores:
David Rodríguez Fragoso  A01748760
Erick Hernández Silva    A01750170
Israel Sánchez Miranda   A01378705
Renata de Luna Flores    A1750484
Roberto Valdez Jasso A01746863

01/12/2021
'''

#Librerías a usar
import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from typing import Tuple

#Modelo del sistema multiagentes
from Traffic_Model import *

def positionsToJSON(ps):
    """
    Función que convierte un set de posiciones (coordenadas en x, y, z)
    a JSON

    Parámetros:
    ps = lista con las coordenadas ordenadas de la siguiente manera [[x, z, y], [x, z, y], ...]

    Retornos: 
    Retorna las coordenadas convertidas a formato JSON
    """
    posDICT = []  #Lista a la que se le unirán las coordenadas en JSON
    for p in ps:
        #Por cada posición en la lista de coordenadas
        pos = {
            #Se les da formato de diccionario a las coordenadas
            "x" : p[0],
            "z" : p[1],
            "y" : p[2]
        }
        posDICT.append(pos)  #Se unen las coordenadas a la lista de coordenadas en JSON
    return json.dumps(posDICT) #Se regresa la lista convertida a JSON

def semaforosToJSON(ps):
    """
    Función que convierte un set de atributos de los sempaforos a JSON

    Parámetros:
    ps = lista con los atributos de los semmáforos de la siguiente manera: [[no. de semáforo, estado, cruzando]]

    Retornos: 
    Retorna los atributos de los semáforos convertidos a formato JSON
    """
    posDICT = []  #Lista a la que se le unirán los atributos del semáforo en JSON 
    semaforo = 0  #Número de semáforo
    for i in range(6,10):
        #Se recorren los semáforos
        try:
            pos = {
                #Se le da formato de diccionario a los atributos del semáforo
                "semaforo": semaforo,
                "estado" : ps[i].estado,
                "cruzando" : ps[i].cruzando
            }
            semaforo += 1
        except:
            pass
        posDICT.append(pos)  #Se unen los atributos a la lista de atributos en JSON
    return json.dumps(posDICT)  #Se regresa la lista convertida a JSON

def vueltasToJSON(ps):
    """
    Función que convierte a JSON un set de valores que inidica si el automóvil da vuelta o no

    Parámetros:
    ps = lista que indica qué automóviles dan vuelta

    Retornos: 
    Retorna la lista de vueltas en formato JSON
    """
    posDICT = []  #Lista a la que se le unirán las vueltas en JSON
    for i in range(0,6):
        #Por cada automóvil en la simulación
        try:
            pos = {
                #Se da formato de diccionario a las vueltas de los automóviles
                "vuelta": ps[i].vuelta,
            }
        except:
            pass
        posDICT.append(pos)  #Se unen las vueltas a la lista de vueltas en JSON
    return json.dumps(posDICT)  #Se regresa la lista convertida a JSON

class Server(BaseHTTPRequestHandler):
    """
    Clase Server que funge de servidor, manejando las peticiones que se le hacen al mismo,
    es un enlace entre el modelo del sistema multiagentes y el ambiente gráfico de Unity
    """
    #Atributos de clase
    model = TrafficModel(6,4)  #Modelo del sistema multiagentes
    cars = [[0, 4], [1], [2, 3], [5]]  #Lista de carros y semáforo al que pertenecen

    #Métodos
    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        """
        Init de la clase, inicializa la clase Server
        """
        super().__init__(request, client_address, server)

    def _set_response(self):
        """
        Función que prepara las respuestas del servidor
        """
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """
        Función que maneja las peticiones de tipo GET que el servidor recibe
        """
        try:
            #Se revisan los semaforos y se actualizan los estados
            for i in range(6,10):
                #Por cada semáforo
                semaforo = self.model.schedule.agents[i]
                if semaforo.estado == "verde":
                    #Si el estado del semáforo actual es verde
                    for iCarro in self.cars[i-6]:
                        #Se recorren los automóviles
                        if self.model.schedule.agents[iCarro].forzar_alto == 0:
                            #Si el automóvil no está detenido este avanza
                            self.model.schedule.agents[iCarro].estado = 1
                        else:
                            #De lo contrario este para
                            self.model.schedule.agents[iCarro].estado = 0
                elif semaforo.estado == "amarillo":
                    #Si el semáforo está en amarillo
                    for iCarro in self.cars[i-6]:
                        if self.model.schedule.agents[iCarro].forzar_alto == 0:
                            #Si el automóvil no está detenido este avanza
                            self.model.schedule.agents[iCarro].estado = 1
                        else:
                            #De lo contrario este para
                            self.model.schedule.agents[iCarro].estado = 0
                elif semaforo.estado == "rojo":
                    #Si el semáforo está en rojo
                    for iCarro in self.cars[i-6]:
                        if self.model.schedule.agents[iCarro].vuelta == 0:
                            #Se paran los automóvles asignados al semáforo
                            self.model.schedule.agents[iCarro].estado = 0

            #Paths del servidor
            if self.path.endswith("/carro"):
                #Si el path es /carro
                self.model.step()  #Se avanza un paso en el modelo
                self._set_response()
                resp = "{\"positions\":" + positionsToJSON(self.model.positions) + "}"  #Respuesta del servidor (incrementos de posiciones en formato JSON)
                self.wfile.write(resp.encode('utf-8'))  #Se manda la respuesta del servidor

            elif self.path.endswith("/carroVuelta"):
                #Si el path es /carroVuelta
                self.model.step()
                self._set_response()
                resp = "{\"configVueltas\":" + vueltasToJSON(self.model.schedule.agents) + "}"  #Respuesta del servidor (configuración de las vueltas en formato JSON)
                self.wfile.write(resp.encode('utf-8'))  #Se manda la respuesta del servidor

            elif self.path.endswith("/semaforo"):
                #Si el path es /semaforo
                self.model.step()
                self._set_response()
                resp = "{\"semaforos\":" + semaforosToJSON(self.model.schedule.agents) + "}"  #Respuesta del servidor (atributos de los semáforos en formato JSON)
                self.wfile.write(resp.encode('utf-8'))  #Se manda la respuesta del servidor

            elif self.path.endswith("/reset"):
                #Si el path es /reset
                Server.model.reset()  #Se resetea el modelo
                self._set_response()
                resp = "Reset"
                self.wfile.write(resp.encode('utf-8'))  #Se notifica que el modelo se reseteó
        except IOError:
            #Si el método GET falla se envía un código de error
            self.send_error(404, "Error")

    def do_POST(self):
        """
        Función que maneja las peticiones de tipo POST que el servidor recibe
        """
        try:
            #Paths del servidor
            if self.path.endswith("/carro"):
                #Si el path es /carro
                content_length = int(self.headers['Content-Length'])
                post_data = json.loads(self.rfile.read(content_length))  #Se recuperan los datos recibidos
                self._set_response()
                resp = "Done"
                print(post_data)
                if post_data["estado"] == 0:
                    #Si el estado del carro es 0
                    self.model.schedule.agents[post_data["carro"]].forzar_alto = 1  #Se forza el alto del automóvil
                    self.model.schedule.agents[post_data["carro"]].estado = post_data["estado"]  #Se actualiza el estado del automóvil
                elif  post_data["estado"] == 1:
                    #Si el estado del carro es 0
                    self.model.schedule.agents[post_data["carro"]].forzar_alto = 0  #El automóvil continúa avanzando
                    self.model.schedule.agents[post_data["carro"]].estado = post_data["estado"]  #Se actualiza el estado del automóvil
                else:
                    self.model.schedule.agents[post_data["carro"]].estado = post_data["estado"]  #En cualquiera de los casos se actualizará el estado del automóvil
                self.wfile.write(resp.encode('utf-8')) #Se envía la respuesta del servidor

            elif self.path.endswith("/semaforoEntrada"):
                #Si el path es /semaforoEntrada
                content_length = int(self.headers['Content-Length'])
                post_data = json.loads(self.rfile.read(content_length))  #Se recuperan los datos recibidos
                self._set_response()
                semaforoActual = post_data["semaforo"]  #Se obtiene el semáforo actual
                cochesCruzando = post_data["cruza"]  #Se obtiene el número de automóviles cruzando el semáforo
                resp = "Done"
                puedePasar = True

                if self.model.schedule.agents[post_data["carro"]].vuelta == 0:
                    #Si el automóvil no va a dar vuelta se le suma al número de automóviles cruzando
                    self.model.schedule.agents[semaforoActual + 6].cruzando += cochesCruzando

                #Se revisa si hay algun otro semaforo en verde
                for i in range(6,10):
                    #Se recorren los semáforos
                    semaforoAdyacente = i - 6
                    if semaforoActual % 2 == 0 and semaforoAdyacente % 2 != 0 and self.model.schedule.agents[i].estado == "verde":
                        #Si lo hay, se guarda la información en una variable auxiliar
                        puedePasar = False
                    if semaforoActual % 2 != 0 and semaforoAdyacente % 2 == 0 and self.model.schedule.agents[i].estado == "verde":
                        puedePasar = False

                if puedePasar:
                    #Si no hay ningún semáforo en verde, se cambia el estado del semáforo actual a verde
                    self.model.schedule.agents[post_data["semaforo"] + 6].estado = "verde"
                elif not puedePasar:
                    #Si hay un semaforo en verde, se cambia el estado a rojo
                    self.model.schedule.agents[post_data["semaforo"] + 6].estado = "rojo"
                self.wfile.write(resp.encode('utf-8'))  #Se envía la respuesta del servidor

            elif self.path.endswith("/semaforoSalida"):
                #Si el path es /semaforoSalida
                content_length = int(self.headers['Content-Length'])
                post_data = json.loads(self.rfile.read(content_length))  #Se recuperan los datos recibidos
                self._set_response()
                semaforoActual = post_data["semaforo"] #Semáforo que termino su cruce
                cochesCruzando = post_data["cruza"]  #Automóviles que están terminando su cruce
                resp = "Done"
                print(post_data)
                tieneCochesCruzando = False

                if self.model.schedule.agents[post_data["carro"]].vuelta == 0:
                    #Si el carro no está dando vuelta se resta de los automóviles cruzando
                    self.model.schedule.agents[semaforoActual + 6].cruzando -= cochesCruzando

                #Se revisa si el semÁforo adyacente tiene coches cruzando
                for i in range(6, 10):
                    #Se recorren los semáforos
                    semaforoAdyacente = i - 6
                    if semaforoActual % 2 == 0:
                        if semaforoActual % 2 == 0 and semaforoAdyacente % 2 == 0 and self.model.schedule.agents[i].cruzando > 0:
                                #Si lo hay, se guarda en una variable auxiliar
                                tieneCochesCruzando = True
                        elif semaforoActual % 2 == 0 and semaforoAdyacente % 2 == 0 and self.model.schedule.agents[i].cruzando > 0:
                                tieneCochesCruzando = True
                    else:
                        if semaforoActual % 2 == 1 and semaforoAdyacente % 2 == 1 and self.model.schedule.agents[i].cruzando > 0:
                                tieneCochesCruzando = True
                        elif semaforoActual % 2 == 1 and semaforoAdyacente % 2 ==  1 and self.model.schedule.agents[i].cruzando > 0:
                                tieneCochesCruzando = True

                semaforosRojos = []  #Lista de semáforos en rojo
                semaforosVerdes = []  #Lista de semáforos en verde
                for i in range(6,10):
                    #Se recorren los semáforos
                    if self.model.schedule.agents[i].estado == "rojo":
                        #Si el semáforo está en rojo se agrega a la lista de semáforos rojos
                        semaforosRojos.append(i)
                    elif (self.model.schedule.agents[i].estado == "amarillo" or self.model.schedule.agents[i].estado == "verde") and self.model.schedule.agents[i].cruzando == 0:
                        #Si el semáforo está en verde o amarillo y ya no tiene automóviles cruzando se agrega a la lista de semáforos verdes
                        semaforosVerdes.append(i)
                if len(semaforosVerdes) == 3:
                    #Si hay más de 3 semáforos verdes
                    for i in semaforosVerdes:
                        #Se recorre la lista y se cambia su estado a amarillo
                        self.model.schedule.agents[i].estado == "amarillo"
                    #Se cambia el estado del primer semáforo de la lista de semáforos rojos a verde
                    self.model.schedule.agents[semaforosRojos[0]].estado == "verde"

                if tieneCochesCruzando:
                    #Si tiene carros cruzando, ambos semáforos se quedan en verde porque son paralelos
                    self.model.schedule.agents[semaforoActual + 6].estado = "verde"

                elif not tieneCochesCruzando:
                    #Si ya hay un semaforo en verde, se cambia el estado a amarillo
                    self.model.schedule.agents[semaforoActual + 6].estado = "amarillo"
                    if semaforoActual == 0 or semaforoActual == 1:
                        #Se cambia el semáforo paralelo al mismo estado
                        self.model.schedule.agents[semaforoActual + 6].estado = "amarillo"
                    elif semaforoActual == 2 or semaforoActual == 3:
                        #Se cambia el semáforo paralelo al mismo estado
                        self.model.schedule.agents[semaforoActual + 6].estado = "amarillo"

                    #Se revisa si hay un semáforo no adyacente con vehículos esperando para cambiar su estado
                    for i in range(6, 10):
                        #Se recorren los semáforos
                        if self.model.schedule.agents[i].cruzando > 0:
                            #Si el semáforo tiene más de un carro cruzando este se queda en verde
                            self.model.schedule.agents[i].estado = "verde"

                    #Si ningun semáforo tiene autos esperando, todos cambian a amarillo
                    hayCochesCruzandoOEsperando = False
                    for i in range(6, 10):
                        #Se recorren los semáforos
                        if self.model.schedule.agents[i].cruzando > 0:
                            #Si hay un automóvil cruzando se guarda en una variable auxiliar
                            hayCochesCruzandoOEsperando = True
                    if not hayCochesCruzandoOEsperando:
                        #Si no hay auyomóviles esperando o cruzando
                        for i in range(6, 10):
                            #Se recorren los semáforos y se cambia su estado a amarillo
                            self.model.schedule.agents[i].estado = "amarillo"
                    self.wfile.write(resp.encode('utf-8'))  #Se envía la respuesta del servidor

            elif self.path.endswith("/darVuelta"):
                #Si el path es /darVuelta
                content_length = int(self.headers['Content-Length'])
                post_data = json.loads(self.rfile.read(content_length))  #Se recuperan los datos recibidos
                self._set_response()
                resp = "Done"
                self.model.schedule.agents[post_data["carro"]].darVuelta()  #Se ejecuta la función dar vuelta del automóvil
                self.wfile.write(resp.encode('utf-8'))  #Se envía la respuesta del servidor

        except IOError:
            #Si el método POST falla se envía un código de error
            self.send_error(404, "Error")

def run(server_class=HTTPServer, handler_class=Server, port=config.PUERTO):
    """
    Función que corre el servidor

    Parámetros:
    server_class = clase del servidor
    handler_class = clase que maneja las peticiones del servidor
    port = puerto en el que se ejecutará el servidor

    Retornos: 
    No retorna nada, sin embargo ejecuta el servidor con los parámetros especificaods
    """
    logging.basicConfig(level=logging.INFO)  #Se configura el servidor
    server_address = ('', port)  #Se le asigna una dirección y un puerto
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n") #Se imprime en consola que el servidor ha iniciado
    try:
        httpd.serve_forever()  #Se queda corriendo el servidor de manera infinita
    except KeyboardInterrupt:   #El servidor se para con CTRL+C
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")  #Se notifica que el servidor ha terminado de ejecutarse

if __name__ == '__main__':
    #Si se ejecuta el archivo main entonces se corre el servidor
    run()