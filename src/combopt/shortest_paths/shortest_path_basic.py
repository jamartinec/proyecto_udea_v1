# coding: utf8

"""

Una función de longitud l: A ---> R  es una función de las aristas de un grafo a los reales

Una representación posible de una función de longitud es un diccionario que tiene como claves
las aristas del grafo y como valor correspondiente la longitud de la arista

"""

import heapq
import bisect

from pqdict import pqdict
#from blist import sortedset

from src.combopt.graph import Grafo
#from src.combopt.shortest_paths.pareto_frontier_structure import Label
# también se puede from ..graph import Grafo

#from ..graph import Grafo
#from ..minpath import minimum_directed_path
#from ..utils import inv
#from ..caminos import DFS
#from ..caminos import caminos_simples_st_prioritize_minlenFIFO



def is_nonnegative_length(G, l):
    """ Checks whether a length function, defined on the arcs, satisfies the non-negative condition.

    Args:
        G: An instance of Graph class.
        l: A dictionary that defines a length function on the edge set.

    Returns:
        A boolean, True if the length function satisfies the non-negativity condition, False in other case.

    """

    assert G.directed

    # Condición de no negatividad
    for e in G.aristas:
        if l[e] < 0:
            return False

    return True

def Dijkstra(G,l,s):
    """ Executes Dijkstra's algorithm on digraph G and length function l.

    This algorithm returns for each vertex v in G, the length of the s-v
    shorter path and also returns a tree of shorter paths.
    The fundamental data structure in Dijsktra is the priority queue.
    In this implementation the pqdict module is used.


    Args:
        G: A directed instance of Graph class.
        l: A dictionary that defines a length function on arc set.
        s: Integer or string denoting the source vertex.

    Returns:
        A dictionary with keys the vertices and values the corresponding shortes path distance from
        source vertex s.

    """

    # Esta implementación es muy costosa en espacio:
    # Usamos un conjunto S para guardar los nodos cuya etiqueta es definitiva
    # es decir, aquellos que en determinada iteración tuvieron la menor etiqueta
    # Usamos un pqdict (implementación externa no nativa de python) como cola de
    # prioridad, el cual va disminuyendo su extensión conforme se hace pop del elemento
    # mínimo. En el diccionario label guardamos la distancia definitiva.

    S = set()
    pred = dict()
    n = G.num_vertices
    d = pqdict({vertice: float('inf') for vertice in G.vertices})
    label = {vertice: float('inf') for vertice in G.vertices}
    d[s] = 0
    label[s] = 0
    pred[s] = None
    while len(S)< n:


        (u2add, dist_min) = d.popitem()
        label[u2add] = dist_min
        #u2add = min(d.keys() - S, key=lambda _: d[_]) #Esto no está implementado como Priority queue
        # returns the key in d.keys()-S such that is value is the minimum one.
        # retorna el vertice u2add tal que su etiqueta es mínima en \bar{S} = V-S
        S.add(u2add)
        for uvec in G.succesors(u2add):
            #print('uvec es',uvec)

            if uvec not in S: # si uvec no ha salido

                if  d[uvec] > dist_min + l[(u2add,uvec)]:
                    d[uvec] = dist_min + l[(u2add,uvec)]
                    pred[uvec] = u2add


    return label

def Reverse_Dijkstra(G,l,t):
    """ Executes the reverse Dijsktra's algorithm

    Executes the reverse Dijsktra's algorithm on
    digraph G with length function l and sink vertex t.

    Args:
        G: A directed instance of Graph class.
        l: A dictionary that defines a length function on arc set.
        t: Integer or string denoting the sink vertex.

    Returns:
        A dictionary with keys the vertices and values the corresponding shortes path distance from vertex
        to sink vertex t.
    """
    # Esta implementación es muy costosa en espacio:
    # Usamos un conjunto S para guardar los nodos cuya etiqueta es definitiva
    # es decir, aquellos que en determinada iteración tuvieron la menor etiqueta
    # Usamos un pqdict (implementación externa no nativa de python) como cola de
    # prioridad, el cual va disminuyendo su extensión conforme se hace pop del elemento
    # mínimo. En el diccionario label guardamos la distancia definitiva.

    S = set()
    succ = dict()
    n = G.num_vertices
    d = pqdict({vertice: float('inf') for vertice in G.vertices})
    label = {vertice: float('inf') for vertice in G.vertices}
    d[t] = 0
    label[t] = 0
    succ[t] = None
    while len(S)< n:


        (u2add, dist_min) = d.popitem()
        label[u2add] = dist_min
        #u2add = min(d.keys() - S, key=lambda _: d[_]) #Esto no está implementado como Priority queue
        # returns the key in d.keys()-S such that is value is the minimum one.
        # retorna el vertice u2add tal que su etiqueta es mínima en \bar{S} = V-S
        S.add(u2add)
        for uvec in G.predecessors(u2add):
            #print('uvec es',uvec)

            if uvec not in S: # si uvec no ha salido

                if  d[uvec] > dist_min + l[(uvec,u2add)]:
                    d[uvec] = dist_min + l[(uvec,u2add)]
                    succ[uvec] = u2add

    #print(label)
    return label

def Bidirectional_Dijkstra(G,l,s,t):
    """ Executes Dijkstra's Bidirectional algorithm.

    Executes Dijkstra's Bidirectional algorithm on a G-digraph with length l, which takes non-negative integer values.
    The fundamental data structure in Dijsktra is the priority queue. In this implementation the pqdict module
    is used.
    Args:
        G: A directed instance of Graph class.
        l: A dictionary that defines a length function on arc set.
        s: Integer or string denoting the source vertex.
        t: Integer or string denoting the sink vertex.

    Returns:
        The shortest path and its distance, between the vertices source s and sink t.

    """


    # Esta implementación es muy costosa en espacio:
    # Usamos un conjunto S para guardar los nodos cuya etiqueta es definitiva en el
    # Dijkstra hacia adelante. Usamos S_prima para guardar los nodos cuya etiqueta es
    # definitiva en el Dijkstra hacia atrás.
    # Usamos dos pqdict (implementación externa no nativa de python) como cola de
    # prioridad para la búsqueda hacia adelante y la búsqueda hacia atrás,
    # los cuales van disminuyendo su extensión conforme se hace pop del elemento
    # mínimo. En los  diccionarios label guardamos la distancia definitiva hacia
    # adelante y hacia atrás.

    S = set()
    S_prima = set()
    d = pqdict({vertice: float('inf') for vertice in G.vertices})
    d_prima = pqdict({vertice: float('inf') for vertice in G.vertices})
    label = {vertice: float('inf') for vertice in G.vertices}
    label_prima = {vertice: float('inf') for vertice in G.vertices}
    d[s] = 0
    label[s] = 0
    d_prima[t]  = 0
    label_prima[t] = 0

    pred = dict()
    succ = dict()
    pred[s]= None
    succ[t] = None

    while len(S & S_prima) == 0 :

        (u2add1, dist_min1) = d.popitem()
        label[u2add1] = dist_min1
        S.add(u2add1)
        for uvec in G.succesors(u2add1):

            if uvec not in S:  # si uvec no ha salido

                if d[uvec] > dist_min1 + l[(u2add1, uvec)]:
                    d[uvec] = dist_min1 + l[(u2add1, uvec)]
                    pred[uvec] = u2add1



        (u2add2, dist_min2) = d_prima.popitem()
        label_prima[u2add2] = dist_min2
        S_prima.add(u2add2)
        for uvec in G.predecessors(u2add2):


            if uvec not in S_prima: # si uvec no ha salido

                if  d_prima[uvec] > dist_min2 + l[(uvec,u2add2)]:
                    d_prima[uvec] = dist_min2 + l[(uvec,u2add2)]
                    succ[uvec] = u2add2


    label_total = dict()
    for vertice in G.vertices:
        label_total[vertice] = label[vertice] + label_prima[vertice]

    joint = min(label_total.keys(), key=lambda _: label_total[_])

    inicio , final = [], []

    inicio.append(joint)
    actual = joint
    while pred[actual] != None:
        inicio.append(pred[actual])
        actual = pred[actual]
    inicio.reverse()

    actual = joint
    while succ[actual] != None:
        final.append(succ[actual])
        actual = succ[actual]

    path = inicio + final

    return (path, label_total[joint])