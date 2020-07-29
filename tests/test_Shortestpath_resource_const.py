# coding: utf8

from pytest import raises
from sortedcontainers import SortedList

from src.combopt.shortest_paths import Pareto_Frontier
from src.combopt.graph import Grafo
from src.combopt.shortest_paths import spptw_desrochers1988_imp_fullpareto

my_graph2 = Grafo([0,1,2,3,4],[(0,1),(0,2),(0,3),(1,4),(2,4),(3,4)],directed=True)
time = {(0,1):8,(0,2):5,(0,3):12,(1,4):4,(2,4):2,(3,4):4}
cost  = {(0,1):3,(0,2):5,(0,3):2,(1,4):7,(2,4):6,(3,4):3}
window = {0:[0,0],1:[6,14],2:[9,12],3:[8,12],4:[9,15]}

def test_spptw_desrochers1988_imp_fullpareto():
    assert spptw_desrochers1988_imp_fullpareto(my_graph2, 0, time, cost, window) == \
           {0: [(0, 0)], 1: [(8, 3)], 2: [(9, 5)], 3: [(12, 2)], 4: [(11, 11), (12, 10)]}