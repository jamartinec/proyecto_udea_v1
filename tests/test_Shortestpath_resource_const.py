# coding: utf8

from pytest import raises
from sortedcontainers import SortedList

from src.combopt.shortest_paths import Pareto_Frontier
from src.combopt.graph import Grafo
from src.combopt.shortest_paths import spptw_desrochers1988_imp_fullpareto, \
    retrieve_path, retrieve_paths_inpareto, slave_function


my_graph2 = Grafo([0,1,2,3,4],[(0,1),(0,2),(0,3),(1,4),(2,4),(3,4)],directed=True)
time = {(0,1):8,(0,2):5,(0,3):12,(1,4):4,(2,4):2,(3,4):4}
cost  = {(0,1):3,(0,2):5,(0,3):2,(1,4):7,(2,4):6,(3,4):3}
window = {0:[0,0],1:[6,14],2:[9,12],3:[8,12],4:[9,15]}
demanda ={0:1,1:1,2:1,3:1,4:1}


def test_spptw_desrochers1988_imp_fullpareto():
    assert spptw_desrochers1988_imp_fullpareto(my_graph2, 0, time, cost, window) == \
           {0: [(0, 0)], 1: [(8, 3)], 2: [(9, 5)], 3: [(12, 2)], 4: [(11, 11), (12, 10)]}

def test_retrieve_path():
    Frentes = \
        spptw_desrochers1988_imp_fullpareto(my_graph2, 0, time, cost, window,False)

    camino_inner, camino, camino_set = retrieve_path((11,11),4,Frentes)
    assert camino_inner == [2] and camino== [0,2,4] and camino_set == {0,2,4}
    camino_inner, camino, camino_set = retrieve_path((12,10),4,Frentes)
    assert camino_inner == [1] and camino == [0,1,4] and camino_set == {0,1,4}

def test_retrieve_paths_inpareto():
    Frentes = \
        spptw_desrochers1988_imp_fullpareto(my_graph2, 0, time, cost, window, False)
    Dictio_inner, Dictio, Dictio_sets = retrieve_paths_inpareto(4,Frentes)
    assert Dictio_inner== {(12,10):[1], (11,11):[2]} and Dictio == {(12,10):[0,1,4], (11,11):[0,2,4]} and \
           Dictio_sets == {(12,10):{0,1,4}, (11,11):{0,2,4}}

def test_slave_functions():
    Dictio_inner, Dictio_Paths, Dictio_Paths_set = slave_function(my_graph2,0,4,time, cost, window)
    assert Dictio_Paths == {(12,10):[0,1,4], (11,11):[0,2,4] } and \
           Dictio_Paths_set == {(12,10): {0,1,4}, (11,11):{0,2,4}} and \
           Dictio_inner =={(12,10):[1], (11,11):[2]}

