# coding: utf8

from pytest import raises
from src.combopt.graph import Grafo
from src.combopt.shortest_paths import Dijkstra, Reverse_Dijkstra, Bidirectional_Dijkstra



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
cost  = {(0,1):3,(0,2):5,(0,3):2,(1,4):7,(2,4):6,(3,4):3}
window = {0:[0,0],1:[6,14],2:[9,12],3:[8,12],4:[9,15]}
############################################################
B=[(0,5),(1,3),(3,3),(5,7),(8,4),(9,1)]
########################################################
def test_Dijkstra():
    assert Dijkstra(my_graph, L, 1) == {1: 0, 2: 6, 3: 4, 4: 5, 5: 6, 6: 9}

def test_Reverse_Dijkstra():
    assert Reverse_Dijkstra(my_graph, L, 6) == {1: 9, 2: 7, 3: 5, 4: 7, 5: 3, 6: 0}

def test_Bidirectional_Dijkstra():
    assert Bidirectional_Dijkstra(my_graph, L, 1, 6) == ([1, 3, 5, 6], 9)



