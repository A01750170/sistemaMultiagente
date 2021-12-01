'''
Archivo de configuraciones del sistema, los siguientes parámetros pueden ser
modificados para cambiar el funcionamiento y comportamiento de la simulación.
Estos cambios solo se ven aplicados cuando se ejecuta el servidor de manera local.

Autores:
David Rodríguez Fragoso  A01748760
Erick Hernández Silva    A01750170
Israel Sánchez Miranda   A01378705
Renata de Luna Flores    A1750484
Roberto Valdez Jasso A01746863

01/12/2021
'''
# Probabilidad de que un carro de vuelta del 1 al 100. Usa 0 para desactivar la vuelta.
PROBABILIDAD_DE_DAR_VUELTA = 35

# Si el valor es False, todos los autos tendrán una velocidad constante.
VELOCIDAD_VARIABLE = True

# Velocidad máxima que puede tener un auto. Solo funciona si VELOCIDAD_VARIABLE está activada.
VELOCIDAD_MAX = 40

# Velocidad mínima que puede tener un auto. Solo funciona si VELOCIDAD_VARIABLE está activada.
# Si se elige 0, entonces hay probabilidad de que el auto no avance.
VELOCIDAD_MIN = 35

# Puerto en el que va a correr el servidor web. IBM Cloud usa el puerto 8080.
PUERTO = 8080
