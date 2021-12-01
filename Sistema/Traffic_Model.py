'''
Programa que almacena los agentes y el modelo
del sistema multieagentes

Autores:
David Rodríguez Fragoso  A01748760
Erick Hernández Silva    A01750170
Israel Sánchez Miranda   A01378705
Renata de Luna Flores    A1750484
Roberto Valdez Jasso A01746863

01/12/2021
'''

#Librerías a usar
from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from random import randint
import config

class CarAgent(Agent):
    """
    Clase que maneja al agente Automóvil, sus atributos y funciones
    """
    #Métodos
    def __init__(self, unique_id, model, direccion):
        """
        Init de la clase, inicializa a los agentes de tipo Automóvil
        
        Parámetros:
        unique_id = id único del agente
        model = modelo al que pertenece
        direccion = dirección a la que se dirige
        """
        super().__init__(unique_id, model)
        random.seed()
        #Atributos
        self.estado = 2  #Detenido 0, Disminuyendo 1, Avanzando 2
        self.cruzando = 0  #Fuera del cruce 0, En el cruce 1, Cruzado 3
        self.pos = [0, 0, 0]  #incrementos en x z y
        self.direccion = direccion  #x 0, -x 1, z 2, -z 3
        self.forzar_alto = 0  #Variable que forza el alto del automóvil
        vuelta = randint(1,101)  #Variable que determina si el automóvil da vuelta o no
        if vuelta <= config.PROBABILIDAD_DE_DAR_VUELTA:
            #Si vuelta cae dentro de la probabilidad entonces el auto dará vuelta
            self.vuelta = 1
        else:
            #De lo contrario no dará vuelta
            self.vuelta = 0

        if config.VELOCIDAD_VARIABLE:
            #Si la velocidad se configura como variable se establece el multiplicador de velocidad
            self.velocidad = random.uniform(config.VELOCIDAD_MIN, config.VELOCIDAD_MAX)
        else:
            #De lo contrario la velocidad no variará
            self.velocidad = 1

    def darVuelta(self):
        """
        Función que se encarga de cambiar la dirección del automóvil
        cuando da la vuelta
        """
        self.pos = [0, 0, 0]  #Incrementadores de posición en x z y
        if self.direccion == 0:
            #Si el automóvil se dirige a x positiva entonces al dar la vuelta se dirigirá a z negativa
            self.direccion = 3
        elif self.direccion == 1:
            #Si el automóvil se dirige a x negativa entonces al dar la vuelta se dirigirá a z positiva
            self.direccion = 2
        elif self.direccion == 2:
            #Si el automóvil se dirige a z positiva entonces al dar la vuelta se dirigirá a x positiva
            self.direccion = 0
        elif self.direccion == 3:
            #Si el automóvil se dirige a z negativa entonces al dar la vuelta se dirigirá a x negativa
            self.direccion = 1

    def step(self):
        """
        Función que se ejecuta cada que hay un step en el modelo
        """
        self.pos = [0, 0, 0]  #incrementadores de posición en x z y
        if self.direccion == 0:
            #Si la dirección es en x positiva se incrementa la posición en x
            self.pos[0] = self.estado * self.velocidad
        elif self.direccion == 1:
            #Si la dirección es en x negativa se decrementa la posición en x
            self.pos[0] = -self.estado * self.velocidad
        elif self.direccion == 2:
            #Si la dirección es a z positiva se incrementa la posición en z
            self.pos[1] = self.estado * self.velocidad
        elif self.direccion == 3:
            #Si la dirección es a z negativa se decrementa la posición en z
            self.pos[1] = -self.estado * self.velocidad

class Light(Agent):
    """
    Clase que maneja al agente Semáforo, sus atributos y funciones
    """
    #Métodos
    def __init__(self, unique_id, model):
        """
        Init de la clase, inicializa a los agentes de tipo Semáforo

        Parámetros:
        unique_id = id único del agente
        model = modelo al que pertenece
        """
        super().__init__(unique_id, model)
        random.seed()
        #Atributos
        self.estado = "amarillo"  #Estado del semáforo (color de la luz)
        self.cruzando = 0  #Número de autos cruzando

    def step(self):
        """
        Función que se ejecuta cada que hay un step en el modelo
        """
        if self.cruzando == 0:
            #Si no hay autos cruzando entonces se cambia el estado del semáforo a amarillo
            self.estado = "amarillo"

class TrafficModel(Model):
    """
    Clase que maneja el modelo del sistema multiagentes, sus atributos y funciones
    """
    #Métodos
    def __init__(self, cars, lights):
        """
        Init de la clase, inicializa al modelo

        Parámetros:
        cars = número de carros presentes en el cruce
        lights = número de semáforos presentes en el cruce
        """
        #Atributos
        self.cars = cars  #Número de carros 
        self.schedule = RandomActivation(self)  #Schedule que se activa de manera aleatoria
        self.running = True  #Indica si el modelo está corriendo o no
        self.positions = []  #Lista de incrementos en las posiciones x z y de cada auto
        self.lights = lights  #Número de semáforos
        directions = [1, 3, 0, 0, 1, 2]  #Direccion de cada automóvil
        for i in range(self.cars):
            #Se inicializan los agentes Automóvil
            car = CarAgent("Carro " + str(i), self, directions[i])
            self.schedule.add(car)  #Se añade el agente al schedule
            self.positions.append(car.pos)  #Se agregua su posición a la lista de posiciones
        for i in range(lights):
            #Se inicializan los agentes Semáforo
            light = Light("Semaforo " + str(i), self)
            self.schedule.add(light)  #Se agregan al schedule

    
    def step(self):
        """
        Función que se ejecuta cada step del modelo
        """
        self.schedule.step()
        for i in range(self.cars):
            #Se actualizan las posiciones de los automóviles
            self.positions[i] = self.schedule.agents[i].pos

    def __del__(self):
        """
        Función que borra la clase modelo y todos sus atributos e hijos establecidos
        """
        print(self.__class__.__name__, "Morimdo")  #Se indica que se ha borrado la clase

    def reset(self):
        """
        Función que resetea el modelo
        """
        #Se vuelven a definir los parámetros iniciales
        self.schedule = RandomActivation(self)
        self.running = True
        self.positions = []
        lights = self.lights
        directions = [1, 3, 0, 0, 1, 2]
        for i in range(self.cars):
            #Se inicializan nuevos agentes Automóvil
            car = CarAgent("Carro " + str(i), self, directions[i])
            self.schedule.add(car)
            self.positions.append(car.pos)
        for i in range(lights):
            #Se inicializan nuevos agentes Semáforo
            light = Light("Semaforo " + str(i), self)
            self.schedule.add(light)
            