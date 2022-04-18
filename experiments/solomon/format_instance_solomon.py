import os
import pickle as pkl
import pandas as pd
import numpy as np


def give_format_instance(route_instance: str, tipo_instance: str):
    with open(route_instance, 'r') as f:
        lines = f.readlines()
        instance_name = str(lines[0]).strip() + tipo_instance
        info_instance = new_line = [int(x) for x in lines[4].split()]
        num_vehicles = info_instance[0]
        capacity = info_instance[1]

    df = pd.read_csv(route_instance, skiprows=8, nrows=26, dtype='int64', delimiter=r"\s+", header=None)

    df.rename(columns={0: 'customer', 1: 'coord_x', 2: 'coord_y', 3: 'demanda', 4: 'ready_time',
                       5: 'due_date', 6: 'service_time'}, inplace=True)

    df.set_index(['customer'], inplace=True)

    test = df.to_dict(orient='index')

    test[26] = test[0]

    distancia = dict()
    for p in test.keys():
        for q in test.keys():
            if p != q and not ((p == 0 and q == 26) or (p == 26 and q == 0)):
                distancia[(p, q)] = np.round(((test[p]['coord_y'] - test[q]['coord_y']) ** 2 +
                                              (test[p]['coord_x'] - test[q]['coord_x']) ** 2) ** (1 / 2), 1)

    costo = dict()
    for p in test.keys():
        for q in test.keys():
            if p != q and not ((p == 0 and q == 26) or (p == 26 and q == 0)):
                costo[(p, q)] = np.round(distancia[(p, q)] - np.random.randint(0, 21), 1)

    tiempo = dict()
    for p in test.keys():
        for q in test.keys():
            if p != q and not ((p == 0 and q == 26) or (p == 26 and q == 0)):
                tiempo[(p, q)] = np.round(distancia[(p, q)] + test[p]['service_time'], 1)

    consumo = dict()
    for p in test.keys():
        for q in test.keys():
            if p != q and not ((p == 0 and q == 26) or (p == 26 and q == 0)):
                consumo[(p, q)] = test[q]['demanda']

    vertices = list(test.keys())
    arcos = list(distancia.keys())

    tiempo_nodos = {v: 0 for v in vertices}
    demanda_nodos = {v: 0 for v in vertices}
    ventanas_tiempo = dict()
    for p in test.keys():
        ventanas_tiempo[p] = [test[p]['ready_time'], test[p]['due_date']]

    ventanas_demanda = dict()
    for p in test.keys():
        ventanas_demanda[p] = [0, capacity]
    recursos_nodos = {'tiempo': tiempo_nodos, 'demanda': demanda_nodos}
    recursos_arcos = {'tiempo': tiempo, 'demanda': consumo}
    restricciones_nodos = {'tiempo': ventanas_tiempo, 'demanda': ventanas_demanda}

    return instance_name, [vertices, arcos, recursos_nodos, recursos_arcos, restricciones_nodos, costo]