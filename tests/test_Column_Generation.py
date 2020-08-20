# coding: utf8
from pytest import raises
from src.combopt.graph import Grafo
from src.combopt.shortest_paths.Column_Generation import update_edge_costs, column_generation

def test_update_edge_costs():
    cost = {(0, 1): 3, (0, 2): 5, (0, 3): 2, (1, 4): 7, (2, 4): 6, (3, 4): 3}
    dual_variables = [0.0, 2.0, 2.8, 2.0]
    costos = update_edge_costs(cost, dual_variables)
    print(costos)

def test_column_generation():
    grafo = Grafo([0,1,2,3,4],[(0,1),(0,2),(0,3),(1,4),(2,4),(3,4),(1,2),(2,1),(1,3),(3,1),(2,3),(3,2) ], directed=True)
    print(grafo.vertices)

    time = {(0,1):1,(0,2):1.4,(0,3):1,(1,4):1,(2,4):1.4,(3,4):1,(1,2):1,(2,1):1,(1,3):1.4,(3,1):1.4,(2,3):1,(3,2):1}
    cost = {(0,1):1,(0,2):1.4,(0,3):1,(1,4):1,(2,4):1.4,(3,4):1,(1,2):1,(2,1):1,(1,3):1.4,(3,1):1.4,(2,3):1,(3,2):1}
    window = {0: [0, 4], 1: [1,1], 2: [2,2], 3: [3,3], 4: [0,4]}
    fleet = 10

    of_value, var_values = column_generation(grafo,0, 4, cost, time, window, fleet)
    print('of_value',of_value)
    print('variables',var_values)

