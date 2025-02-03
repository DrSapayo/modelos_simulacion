import simpy
import random
import matplotlib.pyplot as plt

TIEMPO_LLEGADA = 5
TIEMPO_SERVICIO = 7
TIEMPO_ABIERTO = 600

#variables para graficas
tiempos = []
vehiculos_en_sistema = []

#variable contadora
vehiculos_esperados = 0

class Estacion:
    def __init__(self, env, num_surtidores,):
        self.env = env
        self.surtidores = simpy.Resource(env, num_surtidores)

    def atencion_vehiculo(self, vehiculo):
        global vehiculos_esperados
        tiempo = random.expovariate(1.0/TIEMPO_SERVICIO)
        yield self.env.timeout(tiempo)
        print(f'El vehiculo {vehiculo} atendido en {self.env.now:.2f}')
        vehiculos_esperados += 1
        registro_vehiculos(env.now, vehiculos_esperados)

        with self.surtidores.request() as req:
            yield req
            print(f'Vehiculo {vehiculo} esta siendo atendido en el minuto {self.env.now:.2f}')
            vehiculos_esperados -= 1
            registro_vehiculos(env.now, vehiculos_esperados)
            yield self.env.timeout(tiempo)
            print(f'Vehiculo {vehiculo} termino su servicio en el minuto {self.env.now:.2f}')


def llegada_vehiculos(env, estacion):
    vehiculo_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / TIEMPO_LLEGADA))
        vehiculo_id += 1
        print(f'Vehiculo {vehiculo_id} llega a la estacion de servicio a los {env.now:.2f}')
        env.process(estacion.atencion_vehiculo(vehiculo_id))

def registro_vehiculos(tiempo, vehiculos):
    tiempos.append(tiempo)
    vehiculos_en_sistema.append(vehiculos)

env = simpy.Environment()
estacion = Estacion(env, num_surtidores=2)

env.process(llegada_vehiculos(env, estacion))
env.run(until=TIEMPO_ABIERTO)

plt.figure(figsize=(10,6))
plt.step(tiempos, vehiculos_en_sistema,where='post', label="Vehiculos en el sistema")
plt.title("Evolucion de vehiculos")
plt.xlabel("Tiempo (Minutos)")
plt.ylabel("Numero de vehiculos")
plt.grid()
plt.legend()
plt.show()