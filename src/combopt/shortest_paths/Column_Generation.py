# coding: utf8
import gurobipy as gp
from gurobipy import GRB, Column

from src.combopt.graph import Grafo

from src.combopt.shortest_paths.desrochers_soumis_1988 import slave_function
from src.combopt.shortest_paths.Master_problemCG import \
    initial_covering_model,\
    compute_dual_variables,\
    update_covering_model

def update_edge_costs(costos, dual_var):
    # siguiendo la convención que el nodo 0 es el depot y que uno ingresa el grafo
    # completo con el depot duplicado. Si hay n clientes entonces 0 es el depot, 1,.. n
    # son clientes y n+1 es el depot duplicado.
    for (u, v) in costos:
        costos[(u, v)] = costos[(u, v)] - dual_var[u]
        #print(costos[(u, v)])
    return costos

def column_generation(G,depot_init, depot_end, costos, tiempo, ventanas,fleet):
    # Estamos usando la convención de que el depot es el nodo 0 y el nodo n+1, donde n es el número de clientes
    #print('ENTRAMOS A CG')
    customers = G.vertices[1:-1]
    #print('customers', customers)
    modelo = initial_covering_model(customers, fleet)
    dual_variables = compute_dual_variables(modelo)

    costos = update_edge_costs(costos, dual_variables)
    print('costs actualizados',costos)
    Dictio_Paths_Inner, Dictio_Paths, Dictio_Paths_set = slave_function(G,depot_init,depot_end,tiempo,costos,ventanas)
    print('Rutas',Dictio_Paths_Inner)


    num_columns = 0
    while len(Dictio_Paths_Inner)>0:
        modelo, num_columns = update_covering_model(modelo,Dictio_Paths_Inner,num_columns)

        dual_variables = compute_dual_variables(modelo)

        costos = update_edge_costs(costos, dual_variables)

        Dictio_Paths_Inner, Dictio_Paths, Dictio_Paths_set = slave_function(G, depot_init, depot_end, tiempo, costos,ventanas)
        print('paths inner',Dictio_Paths_Inner)
        #input('presione tecla')


    var_all = modelo.getAttr('X', modelo.getVars())
    return modelo.objVal, var_all


## Hacer una función que reconstruya la solución, es decir, encuentre las variables no nulas y retorne
# el camino al cual corresponde.
# 



