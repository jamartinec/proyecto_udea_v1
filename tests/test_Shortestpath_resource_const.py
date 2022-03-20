# coding: utf8

from pytest import raises
from sortedcontainers import SortedList

from src.combopt.shortest_paths import Pareto_Frontier
from src.combopt.graph import Grafo, Grafo_consumos
from src.combopt.shortest_paths import spptw_desrochers1988_imp_fullpareto, \
    retrieve_path, retrieve_paths_inpareto, slave_function, verificar_recursos, Extend_function_feillet2004, Label_feillet2004


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

def test_verificar_recursos():

    # Verificar recursos recibe grafo G y etiqueta.
    # Crear un grafo de la clase grafo recursos:
    vertices = [1, 2, 3, 4]
    arcos = [(1, 2), (1, 3), (2, 3), (3, 2), (2, 4), (3, 4)]
    tiempo_nodos = {v: 0 for v in vertices}  # no hay tiempo de espera en los nodos
    demanda_nodos = {v: 1 for v in vertices}  # supongamos demanda unitaria
    tiempo_arcos = {(1, 2): 2, (1, 3): 2, (2, 3): 1, (3, 2): 1, (2, 4): 2, (3, 4): 2}
    demanda_arcos = {a: 0 for a in arcos}  # no hay demanda en los arcos, sólo en los nodos
    ventanas_tiempo = {1: [0, 10], 2: [0, 10], 3: [0, 10], 4: [0, 10], }
    ventanas_demanda = {v: [0,5] for v in vertices}
    # costos_arcos = {arco: 1 for arco in arcos}

    # será qué se puede incluir en las etiquetas de las aristas¡? mirar networkx
    costos_arcos = {(1, 2): 2, (1, 3): 2, (2, 3): 1, (3, 2): 1, (2, 4): 2, (3, 4): 2}

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
    # Crear una etiqueta

    nombres_recursos = ['tiempo', 'demanda']
    etiqueta = Label_feillet2004(nodo_rel=1, name_recursos=nombres_recursos, nodos=vertices)

    assert etiqueta.visited_nodes() == {1}
    assert etiqueta.is_visited_node(1) == 1
    assert etiqueta.is_visited_node(2) == 0
    assert etiqueta.costo_acumulado == 0

    indicador, nuevos_valores = verificar_recursos(actual=1, sucesor=2, etiqueta=etiqueta, G=mi_grafo_consumos)

    assert indicador == True
    assert nuevos_valores['tiempo']==2
    assert nuevos_valores['demanda'] ==2


def test_Extended_function_feillet2004():
    # Verificar recursos recibe grafo G y etiqueta.
    # Crear un grafo de la clase grafo recursos:
    vertices = [1, 2, 3, 4]
    arcos = [(1, 2), (1, 3), (2, 3), (3, 2), (2, 4), (3, 4)]
    tiempo_nodos = {v: 0 for v in vertices}  # no hay tiempo de espera en los nodos
    demanda_nodos = {v: 1 for v in vertices}  # supongamos demanda unitaria
    tiempo_arcos = {(1, 2): 2, (1, 3): 2, (2, 3): 1, (3, 2): 1, (2, 4): 2, (3, 4): 2}
    demanda_arcos = {a: 0 for a in arcos}  # no hay demanda en los arcos, sólo en los nodos
    ventanas_tiempo = {1: [0, 10], 2: [0, 10], 3: [0, 10], 4: [0, 10], }
    ventanas_demanda = {v: [0, 5] for v in vertices}
    # costos_arcos = {arco: 1 for arco in arcos}

    # será qué se puede incluir en las etiquetas de las aristas¡? mirar networkx
    costos_arcos = {(1, 2): 2, (1, 3): 2, (2, 3): 1, (3, 2): 1, (2, 4): 2, (3, 4): 2}

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
    # Crear una etiqueta

    nombres_recursos = ['tiempo', 'demanda']
    etiqueta = Label_feillet2004(nodo_rel=1, name_recursos=nombres_recursos, nodos=vertices)

    new_etiqueta = Extend_function_feillet2004(mi_grafo_consumos,etiqueta,2)
    assert new_etiqueta.nodo_rel == 2
    assert new_etiqueta.visited_nodes() == {1,2}
    assert new_etiqueta.costo_acumulado == 2

    new_etiqueta3 = Extend_function_feillet2004(mi_grafo_consumos, etiqueta, 3)
    assert new_etiqueta3.nodo_rel == 3
    assert new_etiqueta3.visited_nodes() == {1, 3}
    assert new_etiqueta3.costo_acumulado == 2
    assert new_etiqueta3.label == {'tiempo':2}
    print('etiqueta new_etiqueta3:')
    print(new_etiqueta3.label)




