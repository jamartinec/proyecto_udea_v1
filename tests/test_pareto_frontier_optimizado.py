# coding: utf8

from pytest import raises
from sortedcontainers import SortedList
import numpy as np

from src.combopt.shortest_paths import ParetoFrontier,Label_feillet2004
from src.combopt.graph import Grafo, Node, LinkedNode, Grafo_consumos
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

def test_Label_feillet2004():
    vertices = [0, 1, 2, 3, 4]
    arcos = [(0,1), (0,2), (1, 2), (1, 3), (2, 3), (3, 2), (2, 4), (3, 4)]
    tiempo_nodos = {v: 0 for v in vertices}  # no hay tiempo de espera en los nodos
    demanda_nodos = {v: 1 for v in vertices}  # supongamos demanda unitaria
    tiempo_arcos = {(0, 1): 1, (0, 2): 2, (1, 2): 2, (1, 3): 2, (2, 3): 1, (3, 2): 1, (2, 4): 2, (3, 4): 2}
    demanda_arcos = {a: 0 for a in arcos}  # no hay demanda en los arcos, sólo en los nodos
    ventanas_tiempo = {0: [0, 10], 1: [0, 10], 2: [0, 10], 3: [0, 10], 4: [0, 10], }
    ventanas_demanda = {v: 5 for v in vertices}
    # costos_arcos = {arco: 1 for arco in arcos}

    # será qué se puede incluir en las etiquetas de las aristas¡? mirar networkx
    costos_arcos = {(0, 1): 2, (0, 2): 2, (1, 2): 2, (1, 3): 2, (2, 3): 1, (3, 2): 1, (2, 4): 2, (3, 4): 2}

    recursos_nodos = {'tiempo': tiempo_nodos, 'demanda': demanda_nodos}
    recursos_arcos = {'tiempo': tiempo_arcos, 'demanda': demanda_arcos}
    restricciones_nodos = {'tiempo': ventanas_tiempo, 'demanda': ventanas_demanda}

    mi_grafo_consumos = Grafo_consumos(vertices,
                                       arcos,
                                       directed=True,
                                       recursos_nodos=recursos_nodos,
                                       recursos_arcos=recursos_arcos,
                                       restricciones_nodos=restricciones_nodos,
                                       costos_arcos=costos_arcos)

    etiqueta = Label_feillet2004(nodo_rel=0, G=mi_grafo_consumos)

    assert etiqueta.label_recursos == {'tiempo' : 0, 'demanda': 1}

    assert etiqueta.label_visitas == {0: 1, 1: 0, 2: 0, 3: 0, 4: 0}

    assert etiqueta.label == {'tiempo': 0, 'demanda': 1, 0: 1, 1: 0, 2: 0, 3: 0, 4: 0}

    assert etiqueta.nodo_rel == 0

    assert etiqueta.longitud == 9

    etiqueta.update_nodo_rel(2)
    assert etiqueta.nodo_rel == 2

    etiqueta.update_label_recursos({'demanda': 1, 'tiempo': 2})
    assert etiqueta.label_recursos['demanda'] == 1
    assert etiqueta.label_recursos['tiempo'] == 2
    assert etiqueta.label['tiempo'] == 2

    etiqueta.update_label_visitas([1,2])
    assert etiqueta.label_visitas[2] ==1
    assert etiqueta.label[1] == 1
    assert etiqueta.conteo == 3






