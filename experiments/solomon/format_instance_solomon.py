import os
import pickle as pkl
import pandas as pd
import numpy as np
from src.combopt.shortest_paths import Dijkstra, Reverse_Dijkstra, Bidirectional_Dijkstra
from src.combopt.graph import Grafo

def give_format_instance(route_instance: str, tipo_instance: int):
    [instance_name, num_vehicles, capacity, vertices, arcos, distancia, costo, tiempo, consumo,
     tiempo_nodos, demanda_nodos, ventanas_tiempo, ventanas_demanda] =\
        read_instance_solomon(route_instance, tipo_instance)

    temp_inf_nodes, consumo_inf_nodes, temp_inf_arcs, demand_inf_arcs = \
        detect_infeasible_nodes_arcs(vertices, arcos, tiempo, consumo, ventanas_tiempo, ventanas_demanda)

    nodos_infeasible = temp_inf_nodes.union(consumo_inf_nodes)
    arcos_infeasible = temp_inf_arcs.union(demand_inf_arcs)


    for (a, b) in arcos:
        if a in nodos_infeasible or b in nodos_infeasible:
            arcos_infeasible.add((a, b))

    while arcos_infeasible:
        arco = arcos_infeasible.pop()
        arcos.remove(arco)
        del distancia[arco]
        del costo[arco]
        del tiempo[arco]
        del consumo[arco]

    while nodos_infeasible:
        nodo = nodos_infeasible.pop()
        vertices.remove(nodo)
        del tiempo_nodos[nodo]
        del demanda_nodos[nodo]
        del ventanas_tiempo[nodo]
        del ventanas_demanda[nodo]

    recursos_nodos = {'tiempo': tiempo_nodos, 'demanda': demanda_nodos}
    recursos_arcos = {'tiempo': tiempo, 'demanda': consumo}
    restricciones_nodos = {'tiempo': ventanas_tiempo, 'demanda': ventanas_demanda}

    return instance_name, [vertices, arcos, recursos_nodos, recursos_arcos, restricciones_nodos, costo]

def read_instance_solomon(route_instance: str, tipo_instance: int):
    with open(route_instance, 'r') as f:
        lines = f.readlines()
        instance_name = str(lines[0]).strip() + '_' + str(tipo_instance)
        info_instance = new_line = [int(x) for x in lines[4].split()]
        num_vehicles = info_instance[0]
        capacity = info_instance[1]
        fin = tipo_instance + 1

    df = pd.read_csv(route_instance, skiprows=8, nrows=fin, dtype='int64', delimiter=r"\s+", header=None)

    df.rename(columns={0: 'customer', 1: 'coord_x', 2: 'coord_y', 3: 'demanda', 4: 'ready_time',
                       5: 'due_date', 6: 'service_time'}, inplace=True)

    df.set_index(['customer'], inplace=True)

    test = df.to_dict(orient='index')

    test[fin] = test[0]

    distancia = dict()
    for p in test.keys():
        for q in test.keys():
            if p != q and not( (p==0 and q==fin) or (p==fin and q==0)) and (q!=0) and (p!=fin):
                distancia[(p, q)] = np.round(((test[p]['coord_y'] - test[q]['coord_y']) ** 2 +
                                              (test[p]['coord_x'] - test[q]['coord_x']) ** 2) ** (1 / 2), 1)

    costo = dict()
    for p in test.keys():
        for q in test.keys():
            if p != q and not( (p==0 and q==fin) or (p==fin and q==0)) and (q!=0) and (p!=fin):
                costo[(p, q)] = np.round(distancia[(p, q)] - np.random.randint(0, 21), 1)

    tiempo = dict()
    for p in test.keys():
        for q in test.keys():
            if p != q and not( (p==0 and q==fin) or (p==fin and q==0)) and (q!=0) and (p!=fin):
                tiempo[(p, q)] = np.round(distancia[(p, q)] + test[p]['service_time'], 1)

    consumo = dict()
    for p in test.keys():
        for q in test.keys():
            if p != q and not( (p==0 and q==fin) or (p==fin and q==0)) and (q!=0) and (p!=fin):
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

    return [instance_name, num_vehicles, capacity,  vertices, arcos,  distancia, costo, tiempo,
            consumo, tiempo_nodos, demanda_nodos, ventanas_tiempo, ventanas_demanda]


def detect_infeasible_nodes_arcs(vertices: list, arcos: list, tiempo: dict,
                                 consumo: dict, ventanas_tiempo: dict, ventanas_demanda: dict):

    grafo_temporal = Grafo(vertices, arcos, directed = True)

    min_temp_path = Dijkstra(grafo_temporal, tiempo, 0)

    #print(min_temp_path)

    temp_inf_nodes = set()
    for nodo in vertices:
        if ventanas_tiempo[nodo][1] < min_temp_path[nodo]:
            temp_inf_nodes.add(nodo)



    min_consumo_path = Dijkstra(grafo_temporal, consumo, 0)

    #print(min_consumo_path)
    consumo_inf_nodes = set()
    for nodo in vertices:
        if ventanas_demanda[nodo][1] < min_consumo_path[nodo]:
            consumo_inf_nodes.add(nodo)

    temp_inf_arcs = set()
    demand_inf_arcs = set()
    for arco in arcos:
        if tiempo[arco] > ventanas_tiempo[arco[1]][1]:
            temp_inf_arcs.add(arco)
        if consumo[arco] > ventanas_demanda[arco[1]][1]:
            demand_inf_arcs.add(arco)

    return temp_inf_nodes, consumo_inf_nodes, temp_inf_arcs, demand_inf_arcs

def save_instances(folder_name, name, lista_grafo):
    file_name = folder_name + '_diccionarios/' + name + '.pkl'
    with open(file_name, 'wb') as a_file:
        pkl.dump(lista_grafo, a_file)

def generar_guardar_instancias(folder_name='solomon_25', tipo_instance=25):
    instancias = os.listdir(folder_name)
    for inst in instancias:
        route_instance = r'./' + folder_name + '/' + inst
        name, lista_grafo = give_format_instance(route_instance, tipo_instance)
        save_instances(folder_name, name, lista_grafo)
    return


if __name__ == '__main__':
    generar_guardar_instancias('solomon_10', 10)



