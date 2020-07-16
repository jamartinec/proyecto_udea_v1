# coding: utf8

from pytest import raises

from src.combopt.graph import Grafo, Node, LinkedNode


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


