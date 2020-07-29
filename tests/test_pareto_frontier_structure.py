# coding: utf8

from pytest import raises
from sortedcontainers import SortedList

from src.combopt.shortest_paths import Pareto_Frontier
vertex = 0
lista = [(1,5),(2,4),(3,3),(4,2),(5,0.5)]

#def test_pareto_frontier_initialization():
#    pareto = Pareto_Frontier(vertex,lista)
#    assert pareto.pareto_set() == [(1,5),(2,4),(3,3),(4,2),(5,0.5)]

def test_preserve_pareto0():
    pareto = Pareto_Frontier(vertex,lista)
    up, ind = pareto.preserve_pareto((0.5, 0.3))
    assert ind == True
    assert up == SortedList([(0.5, 0.3)])

def test_preserve_pareto3():
    pareto = Pareto_Frontier(vertex, lista)
    up, ind = pareto.preserve_pareto((0.5,6))
    assert ind == True
    assert up == SortedList([(0.5, 6), (1, 5), (2, 4), (3, 3), (4, 2), (5, 0.5)])


def test_preserve_pareto1():
    pareto = Pareto_Frontier(vertex, lista)
    up, ind = pareto.preserve_pareto((6, 0.3))
    assert ind == True
    assert up == SortedList([(1,5),(2,4),(3,3),(4,2),(5,0.5),(6,0.3)])

def test_preserve_pareto2():
    pareto = Pareto_Frontier(vertex, lista)
    up, ind = pareto.preserve_pareto((6, 1))
    assert ind == False
    assert up == SortedList([(1, 5), (2, 4), (3, 3), (4, 2), (5, 0.5)])


def test_preserve_pareto4():
    pareto = Pareto_Frontier(vertex, lista)
    up, ind = pareto.preserve_pareto((2.5, 8))
    assert ind == False
    assert up == SortedList([(1, 5), (2, 4), (3, 3), (4, 2), (5, 0.5)])

def test_preserve_pareto5():
    pareto = Pareto_Frontier(vertex, lista)
    up, ind = pareto.preserve_pareto((2.5, 3.5))
    assert ind == True
    assert up == SortedList([(1, 5), (2, 4),(2.5, 3.5), (3, 3), (4, 2), (5, 0.5)])

def test_preserve_pareto6():
    pareto = Pareto_Frontier(vertex, lista)
    up, ind = pareto.preserve_pareto((3.5, 2.5))
    assert ind == True
    assert up == SortedList([(1, 5), (2, 4), (3, 3), (3.5,2.5), (4, 2), (5, 0.5)])

def test_preserve_pareto7():
    pareto = Pareto_Frontier(vertex, lista)
    up, ind = pareto.preserve_pareto((2.5, 0.6))
    assert ind == True
    assert up == SortedList([(1, 5), (2, 4), (2.5, 0.6), (5, 0.5)])

def test_presrve_pareto8():
    vertex=0
    lista=[]
    pareto = Pareto_Frontier(vertex, lista)
    up, ind = pareto.preserve_pareto((2.5, 0.6))
    assert ind == True
    assert up == SortedList([(2.5, 0.6)])

def test_is_pareto_frontier():
    vertex = 0
    lista = [(1, 5), (2, 4), (3, 3), (4, 2), (5, 0.5)]
    pareto = Pareto_Frontier(vertex, lista)
    assert pareto.is_pareto_frontier() == True

def test_is_pareto_frontier2():
    vertex = 0
    lista = [(1, 5), (2, 4), (7,9), (3, 3), (4, 2), (5, 0.5)]
    pareto = Pareto_Frontier(vertex, lista)
    assert pareto.is_pareto_frontier() == False


def test_find_pareto_set():
    vertex = 0
    lista = [(1, 5), (2, 4), (7, 9), (3, 3), (0.2,7), (4, 2), (5, 0.5)]
    pareto = Pareto_Frontier(vertex, lista)
    assert pareto.find_pareto_set() == SortedList([(0.2, 7), (1, 5), (2, 4),(3, 3),(4, 2), (5, 0.5)])