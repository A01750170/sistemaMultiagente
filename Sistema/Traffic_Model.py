from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from random import randint

class CarAgent(Agent):
    def __init__(self, unique_id, model, direccion):
        super().__init__(unique_id, model)
        random.seed()
        self.estado = 2 #Detenido 0, Disminuyendo 1, Avanzando 2
        self.cruzando = 0 #Fuera del cruce 0, En el cruce 1, Cruzado 3
        self.pos = [0, 0, 0]
        self.direccion = direccion #x 0, -x 1, z 2, -z 3
        vuelta = randint(0,40)
        if vuelta <= 40:
            self.vuelta = 1
        else:
            self.vuelta = 0

    def darVuelta(self):
        self.pos = [0, 0, 0]
        if self.direccion == 0:
            self.direccion = 3

        elif self.direccion == 1:
            self.direccion = 2

        elif self.direccion == 2:
            self.direccion = 0

        elif self.direccion == 3:
            self.direccion = 1

    def step(self):
        """
        Medir distancia entre carro y carro
        Si carro cerca:
            Detenerse
        Si carro lejos:
            Seguir avanzando
        Medir distancia entre semáforo y carro
        Si semáforo cerca:
            Obtener color
            Si color rojo:
                Detener
            Si color amarillo:
                Disminuir
            Si color verde:
                Avanzar
        Si estamos en cruce:
            Informar
        Si cruzamos cruce:
            Informar
        """
        # Dependiendo del estado se cambia su velocidad en la dirección del carro
        #velocidad = random.uniform(0.1,1.52)
        velocidad = 1
        self.pos = [0, 0, 0]
        if self.direccion == 0:
            self.pos[0] = self.estado * velocidad
        elif self.direccion == 1:
            self.pos[0] = -self.estado * velocidad
        elif self.direccion == 2:
            self.pos[1] = self.estado * velocidad
        elif self.direccion == 3:
            self.pos[1] = -self.estado * velocidad


class Light(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        random.seed()
        self.estado = "amarillo"  # 0 = rojo | 1 = amarillo | 2 = verde
        self.cruzando = 0  # Numero de autos cruzando

    def step(self):
        """
        Revisa cuantos
        """
        # Si autos cruzando, se cambia el color del semáforo
        #if self.cruzando == 0:
            #self.estado = 1
        #elif self.cruzando > 0:
            #self.estado = 2

class TrafficModel(Model):
    def __init__(self, cars, lights):
        self.cars = cars
        self.schedule = RandomActivation(self)
        self.running = True
        self.positions = []
        directions = [1, 3, 0, 0, 1, 2]
        for i in range(self.cars):
            car = CarAgent("Carro " + str(i), self, directions[i])
            self.schedule.add(car)
            self.positions.append(car.pos)
        for i in range(lights):
            light = Light("Semaforo " + str(i), self)
            self.schedule.add(light)

    
    def step(self):
        self.schedule.step()
        for i in range(self.cars):
            self.positions[i] = self.schedule.agents[i].pos