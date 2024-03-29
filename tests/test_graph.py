# coding: utf8

from pytest import raises

from src.combopt.graph import Grafo, Node, LinkedNode, Grafo_consumos


def test_graph_initialization():
    mi_grafo = Grafo([1, 2, 3], [(1, 2), (1, 3)])

    assert mi_grafo.vecinos(1) == {2, 3}

    mi_grafo.add_info((1, 2), 'valor', 20)

    assert mi_grafo.get_info((1, 2), 'valor') == 20

    assert mi_grafo.get_info((2, 1), 'valor') == 20

    with raises(ValueError):
        mi_grafo.add_info((2, 3), 'valor', 30)

    with raises(KeyError):
        mi_grafo.get_info((1, 3), 'value')

    with raises(ValueError):
        mi_grafo.get_info((2, 3), 'valor')


def test_directed_graph_initialization():

    mi_grafo = Grafo([1, 2, 3], [(1, 2), (1, 3)], directed=True)

    with raises(KeyError):
        mi_grafo.vecinos(1)

    assert mi_grafo.succesors(1) == {2, 3}

    assert mi_grafo.predecessors(1) == set()

    assert mi_grafo.predecessors(2) == {1}

    mi_grafo.add_info((1, 2), 'valor', 20)

    assert mi_grafo.get_info((1, 2), 'valor') == 20

    with raises(ValueError):
        mi_grafo.get_info((2, 1), 'valor')

    with raises(ValueError):
        mi_grafo.get_info((2, 3), 'valor')

    with raises(ValueError):
        mi_grafo.add_info((2, 1), 'valor', 30)

    with raises(KeyError):
        mi_grafo.get_info((1, 3), 'value')

def test_linked_node():
    nodo1 = LinkedNode(1)
    nodo2 = LinkedNode(2)
    nodo3 = LinkedNode(3)
    nodo1.linkto(nodo2)
    nodo2.linkto(nodo3)

    assert nodo1.successor.name == 2
    assert nodo1.successor.successor.name == 3
    assert nodo2.successor.name == 3
    assert nodo2.successor.successor is None
    assert nodo1.tolist() == [1, 2, 3]
    assert nodo2.tolist() == [2, 3]
    assert nodo3.tolist() == [3]
def test_directed_graph_edge_deletion():

    mi_grafo = Grafo([1, 2, 3], [(1, 2), (1, 3)], directed=True)

    mi_grafo.add_info((1, 2), 'valor', 20)

    mi_grafo.remove_edge((1, 2))

    assert mi_grafo.succesors(1) == {3}

    assert mi_grafo.predecessors(2) == set()

    with raises(ValueError):
        mi_grafo.get_info((1, 2), 'valor')

    with raises(ValueError):
        mi_grafo.add_info((1, 2), 'valor', 20)


def test_node_initialization():

    nodo1 = Node(1)
    nodo2 = Node(2)
    nodo1.add_sucessor(nodo1)
    nodo1.add_sucessor(nodo2)

    assert len(nodo1.get_succesors()) == 2
    assert len(nodo2.get_succesors()) == 0


def test_linked_node():
    nodo1 = LinkedNode(1)
    nodo2 = LinkedNode(2)
    nodo3 = LinkedNode(3)
    nodo1.linkto(nodo2)
    nodo2.linkto(nodo3)

    assert nodo1.successor.name == 2
    assert nodo1.successor.successor.name == 3
    assert nodo2.successor.name == 3
    assert nodo2.successor.successor is None

    assert nodo1.tolist() == [1, 2, 3]
    assert nodo2.tolist() == [2, 3]
    assert nodo3.tolist() == [3]


def test_graph_consumos_initialization():

    vertices=[0, 1, 2, 3, 4]
    arcos = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)]
    tiempo_nodos ={v:0 for v in vertices} # no hay tiempo de espera en los nodos
    demanda_nodos={v:1 for v in vertices} # supongamos demanda unitaria
    tiempo_arcos = {(0,1):8,(0,2):5,(0,3):12,(1,4):4,(2,4):2,(3,4):4}
    demanda_arcos ={a:0 for a in arcos} # no hay demanda en los arcos, sólo en los nodos
    ventanas_tiempo = {0:[0,0],1:[6,14],2:[9,12],3:[8,12],4:[9,15]}
    ventanas_demanda ={v:5 for v in vertices}
    costos_arcos = {arco: 1 for arco in arcos}


    # será qué se puede incluir en las etiquetas de las aristas¡? mirar networkx
    cost  = {(0,1):3,(0,2):5,(0,3):2,(1,4):7,(2,4):6,(3,4):3}

    recursos_nodos={'tiempo': tiempo_nodos, 'demanda': demanda_nodos}
    recursos_arcos={'tiempo': tiempo_arcos, 'demanda': demanda_arcos}
    restricciones_nodos ={'tiempo':ventanas_tiempo,'demanda':ventanas_demanda}

    mi_grafo_consumos = Grafo_consumos(vertices,
                                        arcos,
                                        directed=True,
                                        recursos_nodos=recursos_nodos,
                                        recursos_arcos=recursos_arcos,
                                        restricciones_nodos=restricciones_nodos,
                                        costos_arcos=costos_arcos)


    assert mi_grafo_consumos.nodo_recursos() == {0: {'tiempo': 0, 'demanda': 1}, 1: {'tiempo': 0, 'demanda': 1}, \
                                                 2: {'tiempo': 0, 'demanda': 1}, 3: {'tiempo': 0, 'demanda': 1}, \
                                                 4: {'tiempo': 0, 'demanda': 1}}


    assert mi_grafo_consumos.nodo_ventanas() =={0: {'tiempo': [0, 0], 'demanda': 5},  \
                                                1: {'tiempo': [6, 14], 'demanda': 5}, \
                                                2: {'tiempo': [9, 12], 'demanda': 5}, \
                                                3: {'tiempo': [8, 12], 'demanda': 5}, \
                                                4: {'tiempo': [9, 15], 'demanda': 5}}




    assert mi_grafo_consumos.arco_recursos()=={(0, 1): {'tiempo': 8, 'demanda': 0}, (1, 4): {'tiempo': 4, 'demanda': 0},\
                                               (2, 4): {'tiempo': 2, 'demanda': 0}, (0, 3): {'tiempo': 12, 'demanda': 0},\
                                               (3, 4): {'tiempo': 4, 'demanda': 0}, (0, 2): {'tiempo': 5, 'demanda': 0}}



    assert {'tiempo','demanda'} == set(mi_grafo_consumos.nombres_recursos())


    return None

def test_graph_consumos_initialization2():

    vertices=[1, 2, 3, 4]
    arcos = [(1,2),(1,3),(2,3),(3,2),(2,4),(3,4)]
    tiempo_nodos ={v:0 for v in vertices} # no hay tiempo de espera en los nodos
    demanda_nodos={v:1 for v in vertices} # supongamos demanda unitaria
    tiempo_arcos = {(1,2): 2, (1,3):2, (2,3):1, (3,2):1, (2,4):2, (3,4):2}
    demanda_arcos ={a:0 for a in arcos} # no hay demanda en los arcos, sólo en los nodos
    ventanas_tiempo = {1:[0,10],2:[0,10],3:[0,10],4:[0,10],}
    ventanas_demanda ={v:5 for v in vertices}
    #costos_arcos = {arco: 1 for arco in arcos}


    # será qué se puede incluir en las etiquetas de las aristas¡? mirar networkx
    costos_arcos  = {(1,2): 2, (1,3):2, (2,3):1, (3,2):1, (2,4):2, (3,4):2}

    recursos_nodos={'tiempo': tiempo_nodos, 'demanda': demanda_nodos}
    recursos_arcos={'tiempo': tiempo_arcos, 'demanda': demanda_arcos}
    restricciones_nodos ={'tiempo':ventanas_tiempo,'demanda':ventanas_demanda}

    mi_grafo_consumos = Grafo_consumos(vertices,
                                        arcos,
                                        directed=True,
                                        recursos_nodos=recursos_nodos,
                                        recursos_arcos=recursos_arcos,
                                        restricciones_nodos=restricciones_nodos,
                                        costos_arcos=costos_arcos)

    assert mi_grafo_consumos.recurso_arco((1, 2)) == {'tiempo':2, 'demanda': 0}
    assert mi_grafo_consumos.recurso_nodo(2) == {'tiempo': 0, 'demanda': 1}