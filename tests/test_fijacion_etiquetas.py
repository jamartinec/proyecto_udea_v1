# coding: utf8

from pytest import raises
from src.combopt.graph import Grafo
from src.combopt.shortest_paths.desrochers_soumis_1988 import  \
    pareto_set, SPPTW_basic, SPPTW_basic_B, \
    reduce_to_pareto_frontier, preserve_pareto_frontier, \
    contain_pareto_frontier, spptw_desrochers1988_imp1, \
    spptw_desrochers1988_imp2, spptw_desrochers1988_imp3, \
    min_time_cost, spptw_desrochers1988_imp3_bucket, \
    spptw_desrochers1988_imp_fullpareto, retrieve_path, \
    retrieve_paths_inpareto, slave_function, \
    build_generalized_bucket

############################################
my_graph = Grafo([1,2,3,4,5,6],[(1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(4,6),(5,4),(5,6)],
                     directed=True)

L = {(1,2):6,(1,3):4,(2,3):2,(2,4):2,(3,4):1,(3,5):2,(4,6):7,(5,6):3,(5,4):1}
##########################################################
A = [(1,3),(0,5),(9,1),(5,7),(8,4),(3,3)]
##########################################################
my_graph2 = Grafo([0,1,2,3,4],[(0,1),(0,2),(0,3),(1,4),(2,4),(3,4)],
                  directed=True)
time = {(0,1):8,(0,2):5,(0,3):12,(1,4):4,(2,4):2,(3,4):4}
cost = {(0,1):3,(0,2):5,(0,3):2,(1,4):7,(2,4):6,(3,4):3}
window = {0:[0,0],1:[6,14],2:[9,12],3:[8,12],4:[9,15]}
############################################################
B=[(0,5),(1,3),(3,3),(5,7),(8,4),(9,1)]
########################################################
demanda ={0:1,1:1,2:1,3:1,4:1}
#############################################################


def test_pareto_set():
    assert pareto_set(A) == [(0, 5), (1, 3), (3, 3), (9, 1)]

def test_SPPTW_basic():
    assert SPPTW_basic(my_graph2, 0, time, cost, window) ==\
           {0: [(0, 0)], 1: [(8, 3)], 2: [(9, 5)], 3: [(12, 2)], 4: [(11, 11), (12, 10)]}

def test_SPPTW_basic_B():
    assert SPPTW_basic_B(my_graph2, 0, time, cost, window) ==\
           {0: [(0, 0)], 1: [(8, 3)], 2: [(9, 5)], 3: [(12, 2)], 4: [(11, 11), (12, 10)]}

def test_reduce_to_pareto_frontier():
    assert reduce_to_pareto_frontier(B) == [(0, 5), (1, 3), (3, 3), (9, 1)]

def test_preserve_pareto_frontier():
    assert preserve_pareto_frontier(B, (2, 2)) == [(0, 5), (1, 3), (2, 2), (9, 1)]

# REVISAR
def test_contain_pareto_frontier():
    assert contain_pareto_frontier(B, (2, 2), {}) == ( [(0, 5), (1, 3), (2, 2), (3, 3), (5, 7), (8, 4), (9, 1)], True, {})

def test_spptw_desrochers1988_imp1():
    assert spptw_desrochers1988_imp1(my_graph2, 0, time, cost, window) == \
           {0: [(0, 0)], 1: [(8, 3)], 2: [(9, 5)], 3: [(12, 2)], 4: [(11, 11), (12, 10)]}

# REVISAR
def test_spptw_desrochers1988_imp2():
    assert spptw_desrochers1988_imp2(my_graph2, 0, time, cost, window) == \
           {0: [(0, 0)], 1: [(8, 3)], 2: [(9, 5)], 3: [(12, 2)], 4: [(11, 11), (12, 10)]}

def test_spptw_desrochers1988_imp3():
    assert spptw_desrochers1988_imp3(my_graph2, 0, time, cost, window) == \
           {0: [(0, 0)], 1: [(8, 3)], 2: [(9, 5)], 3: [(12, 2)], 4: [(11, 11), (12, 10)]}

def test_min_time_cost():
    assert min_time_cost(my_graph2, time, cost) == (2,6)


def test_spptw_desrochers1988_imp3_bucket():
    assert spptw_desrochers1988_imp3(my_graph2, 0, time, cost, window) == \
           {0: [(0, 0)], 1: [(8, 3)], 2: [(9, 5)], 3: [(12, 2)], 4: [(11, 11), (12, 10)]}


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

def test_build_generalized_bucket():
    width = min(time.values())
    print(width)

    sub_intervalos = build_generalized_bucket(window, width)
    assert sub_intervalos == [[6, 8], [8, 10], [8, 10],
                              [9, 10], [9, 10],
                              [10, 12], [10, 12], [10, 12], [10, 12],
                              [12, 14], [12, 14],
                              [14, 15]]