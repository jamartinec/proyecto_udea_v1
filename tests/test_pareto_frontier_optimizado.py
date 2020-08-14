# coding: utf8

from pytest import raises
from sortedcontainers import SortedList
import numpy as np

from src.combopt.shortest_paths import ParetoFrontier
vertex = 0
lista = [(4,2),(5,0.5),(1,5),(3,3),(2,4),(2,2.8),(2.5,5),(2.5,2.7),(0.5,2.7),(6,0.4),(6,5),(0.5,6)]


def test_ParetoFrontier_add():
    # test inicialización sin lista de inicio y adición progresiva de etiquetas
    Descartados = set()
    pareto = ParetoFrontier()
    for etiqueta in lista:
        pareto, indicador, descartados = pareto.add(etiqueta, pure_pareto=True)
        Descartados = Descartados.union(descartados)
    assert pareto.show_pareto() == {0:np.inf, 0.5:2.7, 2.5:2.7, 4:2, 5:0.5, 6:0.4}
    assert Descartados == {(1,5), (3,3), (2,2.8)}
    print('conjunto de descartados', Descartados)

def test_ParetoFrontier_init():
    # test para inicialización con lista no vacía
    pareto = ParetoFrontier(lista)
    pareto_mapa, sucesores_mapa, predecesores_mapa = pareto.show_pareto2()
    print('mapa', pareto_mapa)
    print('sucesores', sucesores_mapa)
    print('predecesores', predecesores_mapa)
    #assert pareto.show_pareto() == {0:np.inf, 0.5:2.7, 2.5:2.7, 4:2, 5:0.5, 6:0.4}

def test_ParetoFrontier_delete():
    pareto = ParetoFrontier(lista)
    pareto = pareto.Delete_label((2.5, 2.7))
    pareto_mapa, sucesores_mapa, predecesores_mapa = pareto.show_pareto2()
    print('mapa', pareto_mapa)
    print('sucesores', sucesores_mapa)
    print('predecesores', predecesores_mapa)
    A = pareto.list_frontlabels()
    print(A)






