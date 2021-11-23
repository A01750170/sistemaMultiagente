from mesa import Agent, Model
from mesa.time import RandomActivation
import random

class CarAgent(Agent):
    def __init__(self, unique_id, model, direccion):
        super().__init__(unique_id, model)
        random.seed()
        self.estado = 0 #Detenido 0, Disminuyendo 1, Avanzando 2
        self.cruzando = 0 #Fuera del cruce 0, En el cruce 1, Cruzado 3
        self.pos = [0, 0, 0]
        self.direccion = direccion #x 0, -x 1, z 2, -< 3
        #self.sentido = 3 

    
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
        self.pos[0] = 1

class TrafficModel(Model):
    def __init__(self, cars):
        self.cars = cars
        self.schedule = RandomActivation(self)
        self.running = True
        self.positions = []

        for i in range(self.cars):
            car = CarAgent("Carro " + str(i), self)
            self.schedule.add(car)
            self.positions.append(car.pos)

    
    def step(self):
        self.schedule.step()
        for i in range(self.cars):
            self.positions[i] = self.schedule.agents[i].pos