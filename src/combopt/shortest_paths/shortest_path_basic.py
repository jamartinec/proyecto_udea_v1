# coding: utf8

"""

Una función de longitud l: A ---> R  es una función de las aristas de un grafo a los reales

Una representación posible de una función de longitud es un diccionario que tiene como claves
las aristas del grafo y como valor correspondiente la longitud de la arista

"""

import heapq
import bisect

from pqdict import pqdict
from blist import sortedset

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

### implementaciones ineficientes###
def pareto_set(A):
    """ Find the Pareto set.

    Given a list of n pairs, find the Pareto Front (for a minimization problem) in O(n log(n)) time, using Timsort first
    to sort the pairs in ascending order with respect the first coordinates (regardelss of the second one) and then look
    for the efficient pairs by comparing the second coordinate, running along the Pareto front as if descending a
    staircase.

    Args:
        A: A list of pairs, not necessarily in a Lex order.

    Returns:
        A list pareto containing the pareto set from the original list A.

    """
    # El Timsort inicial cuesta O(nlog(n)) y la búsqueda
    #posterior cuesta O(n). La complejidad es  O(n log(n)) + O(n)
    # o sea O(nlog(n)).

    A.sort(key=lambda x:x[0])
    pareto = list()
    (u,v) = A[0]
    pareto.append((u,v))
    actual = v

    for j in range(1,len(A)):
        if A[j][1] <= actual:
            pareto.append(A[j])
            actual = A[j][1]
        else:
            pass
    return pareto

def SPPTW_basic(G,s,time,costo,ventana):
    """ Inefficient implementation of the SPPTW algorithm.

    First attempt of the implementation of Desrochers et al. 1988.
    The data structures used here are not those suggested in the paper to guarantee the indicated complexity.

    Args:
        G: A directed instance of Graph class.
        s: Integer or string denoting the source vertex.
        time: A dictionary defining a time function on the arcs.
        costo: A dictionary defining a cost function on the arcs.
        ventana: A dictionary defining time windows for each vertex.

    Returns:
        A dictionary which for each vertex show the  list of efficient labels from source vertex s.

    """
    #P: crear un diccionario, donde cada clave es el entero que representa
    #un vértice del grafo y donde el valor es una lista que contiene
    #las etiquetas ya extendidas.

    # Q es un diccionario similar a P, donde las listas contienen las
    # etiquetas que aun no han sido extendidas.

    P = dict({vertice: [] for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"),float("inf"))] for vertice in G.vertices})
    P[s] = [(0, 0)]
    Q[s] = []
    actual = s
    efe_q = (0,0)
    QQ = [efe_q]

    while len(QQ)>0:

        # Definir una función que tome actual y efe_q y devuelva los nodos
        # a los cuales se puede extender efe_q desde actual.
        for vecino in G.succesors(actual):
            if efe_q[0] + time[(actual,vecino)] <= ventana[vecino][1]:
                label_time = max(ventana[vecino][0], efe_q[0] + time[(actual,vecino)])
                label_cost = efe_q[1] + costo[(actual,vecino)]
                #agregar la etiqueta (label_time, label_cost) a Q[vecino]
                #luego actualizar el frente de pareto de Q[vecino] usando Pareto_set.
                Q[vecino].append((label_time, label_cost))
                Q[vecino] = pareto_set(Q[vecino])
                # QQ es la unión de todos las listas que están como valores
                # del diccionario Q. Estas listas pueden cambiar mucho cuando se añade
                # una nueva etiqueta y se actualiza el frente de Pareto, QQ también puede
                # cambiar mucho.  Aqui optamos por crear un nuevo heap en cada iteración.

        QQ = list()
        for clave in Q.keys():
            for par in Q[clave]:
                QQ.append((par,clave)) # ((tiempo,costo),clave).

        # Sacamos el mínimo del heap QQ
        root = heapq.heappop(QQ)
        efe_q, actual = root[0], root[1]
        # root[0] nos es la etiquete mínima en el orden lexicográfico
        # root[1] nos dice el nodo al cual hay que actualizar Q[nodo] y P[nodo]
        P[actual].append(efe_q)
        Q[actual].remove(efe_q)

    return P

def SPPTW_basic_B(G,s,time,costo,ventana):
    """ Inefficient implementation of the SPPTW algorithm.

        Second attempt of the implementation of Desrochers et al. 1988.
        The data structures used here are not those suggested in the paper to guarantee the indicated complexity.

        Args:
            G: A directed instance of Graph class.
            s: Integer or string denoting the source vertex.
            time: A dictionary defining a time function on the arcs.
            costo: A dictionary defining a cost function on the arcs.
            ventana: A dictionary defining time windows for each vertex.

        Returns:
            A dictionary which for each vertex show the  list of efficient labels from source vertex s.

        """
    #P: crear un diccionario, donde cada clave es el entero que representa
    #un vértice del grafo y donde el valor es una lista que contiene
    #las etiquetas ya extendidas.

    # Q es un diccionario similar a P, donde las listas contienen las
    # etiquetas que aun no han sido extendidas.

    P = dict({vertice: [] for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"),float("inf"))] for vertice in G.vertices})
    Q_set = dict({vertice:{ (float("inf"),float("inf")) }    for vertice in G.vertices} )
    P[s] = [(0, 0)]
    Q[s] = []
    Q_set[s] = set()
    actual = s
    efe_q = (0,0)
    QQ = list()
    for clave in Q.keys():
        for par in Q[clave]:
            QQ.append((par,clave))
    QQ_set = set(QQ)


    while len(QQ)>0:

        # Definir una función que tome actual y efe_q y devuelva los nodos
        # a los cuales se puede extender efe_q desde actual.
        for vecino in G.succesors(actual):
            if efe_q[0] + time[(actual,vecino)] <= ventana[vecino][1]:
                label_time = max(ventana[vecino][0], efe_q[0] + time[(actual,vecino)])
                label_cost = efe_q[1] + costo[(actual,vecino)]
                #agregar la etiqueta (label_time, label_cost) a Q[vecino]
                #luego actualizar el frente de pareto de Q[vecino] usando Pareto_set.
                Q_vecino2 = Q[vecino].copy()
                Q_vecino2.append((label_time, label_cost))
                Q_vecino2 = pareto_set(Q_vecino2)
                Q_vecino2_set = set(Q_vecino2)
                # contiene el frente de Pareto en el nodo vecino2
                print('Q_VECINO',Q[vecino])
                print('Q_VECINO2',Q_vecino2)
                for par in Q[vecino]:
                    print(par)
                    if par not in Q_vecino2_set:
                        QQ.remove((par,vecino))
                        QQ_set.remove((par,vecino))

                for par in Q_vecino2:
                    if par not in Q_set[vecino]:
                        heapq.heappush(QQ,(par,vecino))
                        QQ_set.add((par,vecino))
                Q[vecino] = Q_vecino2
                Q_set[vecino] = Q_vecino2_set

                # QQ es la unión de todos las listas que están como valores
                # del diccionario Q. Estas listas pueden cambiar mucho cuando se añade
                # una nueva etiqueta y se actualiza el frente de Pareto, QQ también puede
                # cambiar mucho. Aqui optamos por crear un heap al inicio y actualizar en cada
                # iteración.
                # Para verificar si un elemento está en el heap mantenemos un conjunto con
                # sus elementos.

        # Sacamos el mínimo del heap QQ
        root = heapq.heappop(QQ)
        print(root)
        QQ_set.remove(root)
        efe_q, actual = root[0], root[1]
        # root[0] nos es la etiquete mínima en el orden lexicográfico
        # root[1] nos dice el nodo al cual hay que actualizar Q[nodo] y P[nodo]
        P[actual].append(efe_q)
        Q[actual].remove(efe_q)
        Q_set[actual].remove(efe_q)

    return P

##################################################


### implementaciones siguiendo desrochers 1988 #######

def reduce_to_pareto_frontier(A):
    """ Find the Pareto frontier of an lex ordered list of pairs.

    Given an ordered (Lex) list of n pairs, find the Pareto front (for a minimization problem) in O(n).
    Search for efficient pairs by comparing the second coordinate, goint through the Pareto front as if
    descending a staircase.

    Args:
        A: A list of n pairs (u,v) sorted in ascending Lex order.

    Returns:
        A list containing the Pareto front from the original list A.

    """
    # La búsqueda cuesta O(n).
    pareto = list()
    (u, v) = A[0]
    pareto.append((u, v))
    actual = v

    for j in range(1, len(A)):
        if A[j][1] <= actual:
            pareto.append(A[j])
            actual = A[j][1]
        else:
            pass
    return pareto

def preserve_pareto_frontier(A, new_label):
    """ Checks if a new label is efficient, an update the original list.

    Given an ordered list (under lexicographical order) of n efficient (time, cost) labels, and a new new_label
    checks if it is efficient and should be included in A preserving order Lex, and removes from A those labels that are
    now dominated by new_label.


    Args:
        A: A list of pairs (u,v), in ascending Lex order.
        new_label: A new label/pair (u,v).

    Returns:
        A list wit

    """

    # Este algoritmo tiene complejidad O(n), donde n es la longitud de A.
    index=list()
    contador, comparacion = 0, True
    for i in range(len(A)):

        # si la nueva etiqueta es dominada por alguna etiqueta en A
        # entonces (por el orden Lex) nueva_etiqueta no puede dominar
        # a ninguna  y salimos del ciclo.
        if (A[i][0] < new_label[0] and A[i][1] < new_label[1] ):
            comparacion = False
            break

        # si la nueva etiqueta (new) domina a cierta etiqueta (b) en A, entonces
        # en caso de ser la primera que encontramos, reemplazamos b por new en A
        # manteniendo el orden Lex, si no es la primera eliminamos b de A.
        elif (new_label[0] < A[i][0] and new_label[1] < A[i][1]):
            contador += 1
            if contador == 1:
                A[i] = new_label
            else:
                index.append(i)
            comparacion = False

        # no(b < nueva_etiqueta) and no(nueva_etiqueta<b)
        elif ((new_label[0] <= A[i][0]  or new_label[1] <= A[i][1] )
              and (A[i][0] <= new_label[0]  or A[i][1] <= new_label[1] )):
            pass
    for j in sorted(index, reverse=True):
        del A[j]

    if comparacion == True:
        # si la nueva etiqueta no domina y no es dominada por
        # ninguna etiqueta de A, entonces insertamos esta
        # nueva etiqueta manteniendo el orden Lex. bisect tiene
        # complejidad O(n).
        bisect.insort(A, new_label)

    return A

def check_dominance(A,new_label,B):
    """ Checks if any label in the list A dominates the new_label.

    Args:
        A: List of labels/pairs
        new_label: A new label/pair
        B: A set with discarded labels

    Returns:
        indicador: A boolean that is True if some label in A dominates new_label
        B: the set of discarded labels, possibly updated.
    """

    indicador = False
    for i in range(len(A)):
        if A[i][0] < new_label[0] and A[i][1] < new_label[1]:
            indicador = True
            B.add(new_label)
            break
    return  indicador, B

def contain_pareto_frontier(A,new_label,B):
    """ Find a list that contains the Pareto frontier after adding a new label.

    Given a minheap A (under lexicographical order) of n efficient (time, cost) labels, and a new new_label
    checks if it dominates A[0], in which case A[0] = new_label (the root of the heap). A still has all the efficient
    labels and potentially some inefficient labels.

    Args:
        A: A minheap of pairs/labels.
        new_label: A new label pair (time, cost).
        B: A set of pairs/labels that were discarded

    Returns:
        A: the resulting list according if the label was inserted or not.
        insertado: A boolean that is True if the new label was added to A.
        B: The set of discarded pairs possible updated.
    """

    insertado = False
    # si new_label domina a la primera etiqueta de A
    if (new_label[0] < A[0][0] and new_label[1] < A[0][1]):
        B.add(A[0])
        A[0] = new_label
        insertado = True
    # si las etiquetas no son comparables
    elif ((new_label[0] <= A[0][0]  or new_label[1] <= A[0][1])
              and (A[0][0] <= new_label[0]  or A[0][1] <= new_label[1])):
        heapq.heappush(A, new_label)
        #bisect.insort(A, new_label)
        insertado = True

    else:
        B.add(new_label)

    return (A, insertado,B)

def spptw_desrochers1988_imp_MEJORADA(G,s,time,costo,ventana):
    """Third algorithm in Desrochers et al. 1988.

    Garantizamos en todo momento que se preserve el Frente de Pareto. Para ello hacemos uso de una
    clase para el Frente, de modo que las operaciones de actualización sean eficientes. De forma
    análoga al algoritmo de Dijkstra distinguimos dos tipos de etiquetas:
    1) Las etiquetas  que no han sido tratadas o extendidas. Se almacenan en:
          Un minheap bajo el oden lexicográfico al cual se van añadiendo las nuevas etiquetas generadas.
          Del minheap se extrae la menor etiqueta en orden Lex entre todas las etiquetas NO TRATADAS de todos
          los vértices. Cuando esta etiqueta (llamémosla efe_q o minlabel) se extrae se verifican las siguientes
          condiciones:

          a)  Si la etiqueta efe_q (ó minlabel)  hace parte del conjunto de etiquetas DESCARTADAS en una iteración previa,
              entonces NO se extiende. Primero hacemos esta comprobación porque es barata O(1). Ver más abajo para
              entender cuándo una etiqueta se agrega a DESCARTADAS.
          b)  Miramos el vértice al cual corresponde esta etiqueta efe_q y vamos a la instancia de la clase Frente
              de Pareto de las etiquetas TRATADAS de ese vértice. Si alguna en TRATADAS domina a la nueva etiqueta
              entonces esta se agrega a DESCARTADAS y NO se extiende. Note que cualquier extensión de una etiqueta
              dominada estará dominada por alguna etiqueta que ya fue incluida en el minheap.

     2) Una nueva etique (new_label) resultante de la extensión de la etiqueta efe_q (NO dominada por alguien en
            TRATADAS y NO previamente DESCARTADA) se ingresa al minheap si satisface lo siguiente:

          a) No ha sido previamente DESCARTADA.
          b) No es dominada por alguna etiqueta en la instancia de la clase Pareto que contiene las NOTRATADAS
             del vértice sobre el cual está definida.

          Note que el criterio para entrar al heap y el criterio para ser extendida tras salir del heap es el mismo
          Tanto TRATADAS como NO TRATADAS son estructuras Pareto.

             * Una etiqueta es descartada cuando ha sido:
               -- Eliminada o candidata que no entra al frente de pareto del vértice al que corresponde
               (y nunca vuelve a entrar) en cuyo caso sabemos que es ineficiente.




    Args:
        G: A directed instance of Graph class.
        s: Integer or string denoting the source vertex.
        time: A dictionary defining a time function on the arcs.
        costo: A dictionary defining a cost function on the arcs.
        ventana: A dictionary defining time windows for each vertex.


    Returns:
        A dictionary which for each vertex show the  list of efficient labels from source vertex s.

    """


    # Paso 1: inicialización
    # Crear un diccionario P, donde cada clave es el entero que representa
    # un vértice del grafo y donde el valor es una lista que contiene
    # las etiquetas ya extendidas. Crear un diccionario Q similar a P,
    # donde las listas contienen las etiquetas que aun no han sido extendidas.
    S = dict({vertice: set() for vertice in G.vertices})
    P = dict({vertice: sortedset([]) for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"), float("inf"))] for vertice in G.vertices})
    Q[s] = [(0, 0)]
    label_heap = [((0,0),s)]

    # Paso 2: Extender efe_q, contener el frente de Pareto
    # en cada lista Q[j].

    while label_heap:

        (efe_q, actual) = heapq.heappop(label_heap)

        # Verificamos si la etiqueta extraida: efe_q del nodo actual, es dominada por alguna
        # etiqueta en P[actual]
        check, S[actual] =  check_dominance(P[actual], efe_q, S[actual])
        # si alguien en P[actual] domina a efe_q, continuamos con la iteración del while
        if check == True:
            pass
        else:
            # verificamos si efe_q ya está en el conjunto de etiquetas que fueron excluidas
            if efe_q in S[actual]:
                pass
            else:
                # Extender la etiqueta efe_q desde nodo actual. Una extensión
                # es factible si se respetan ventanas de tiempo.

                for vecino in G.succesors(actual):
                    if efe_q[0] + time[(actual, vecino)] <= ventana[vecino][1]:
                        label_time = max(ventana[vecino][0], efe_q[0] + time[(actual, vecino)])
                        label_cost = efe_q[1] + costo[(actual, vecino)]
                        new_label = (label_time, label_cost)
                        print('new label', new_label)
                        # Antes de actualizar el frente de Pareto verificamos si new_label está dominada por
                        # alguna etiqueta en P[vecino], en cuyo caso no tiene sentido ingresar a las
                        # posibles etiquetas, pues de ella se generarán más etiquetas dominadas.
                        check_int, S[vecino] = check_dominance(P[vecino], new_label, S[vecino])
                        if  check_int == False:
                            # Actualizar el frente de Pareto (potencialmente hay etiquetas no eficientes)
                            Q[vecino], insertado, S[vecino] = contain_pareto_frontier(Q[vecino], new_label, S[vecino])
                            if insertado == True:
                                heapq.heappush(label_heap, (new_label, vecino))
                        else:
                            pass
                # Como la etiqueta efe_q perteneciente al nodo "actual" ya fue extendida
                # (es decir, tratada) actualizamos las listas P[actual] y Q[actual]

                P[actual].add(efe_q)
                heapq.heappop(Q[actual])


    # Paso 4: Como para cada nodo j, la lista  P_j puede tener etiquetas no
    # eficientes, reducimos la lista hasta quedar sólo con el frente de Pareto.
    # como las listas ya están ordenadas en orden Lex, el costo es O(D), donde D
    # es el número de posibles etiquetas. NO ENTIENDO POR QUÉ EL ARTÍCULO DICE
    # QUE ES O(d) con d la máxima amplitud de una ventana de tiempo.

    for vertice in G.vertices:
        P[vertice] = reduce_to_pareto_frontier(P[vertice])

    print('Este es P',P)
    return P

def spptw_desrochers1988_imp1(G,s,time,costo,ventana):
    """ First algorithm in Desrochers et al. 1988.

    In the first implementation each Q_j is an ordered list (Lex order) and after creating a new label in the j node,
    it is appended if it is efficient and all labels in Q_j that are no longer efficient are removed.

    Args:
        G: A directed instance of Graph class.
        s: Integer or string denoting the source vertex.
        time: A dictionary defining a time function on the arcs.
        costo: A dictionary defining a cost function on the arcs.
        ventana: A dictionary defining time windows for each vertex.


    Returns:
        A dictionary which for each vertex show the  list of efficient labels from source vertex s.

    """

    # Paso 1: inicialización
    # Crear un diccionario P, donde cada clave es el entero que representa
    # un vértice del grafo y donde el valor es una lista que contiene
    # las etiquetas ya extendidas. Crear un diccionario Q similar a P,
    # donde las listas contienen las etiquetas que aun no han sido extendidas.

    P = dict({vertice: [] for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"),float("inf"))] for vertice in G.vertices})
    Q[s] = [(0, 0)]
    actual, efe_q, detener = s, (0,0), 0

    # Paso 2: Extender efe_q, mantener estrictamente el frente de Pareto
    # en cada lista Q[j].

    while detener == 0:

        # Extender la etiqueta efe_q desde nodo actual. Una extensión
        # es factible si se respetan ventanas de tiempo.

        for vecino in G.succesors(actual):
            if efe_q[0] + time[(actual,vecino)] <= ventana[vecino][1]:
                label_time = max(ventana[vecino][0], efe_q[0] + time[(actual,vecino)])
                label_cost = efe_q[1] + costo[(actual,vecino)]
                new_label = (label_time, label_cost)
                print('new label',new_label)
                # Actualizar el frente de Pareto (sólo se dejan etiquetas eficientes)
                Q[vecino] = preserve_pareto_frontier(Q[vecino],new_label)

        # Como la etiqueta efe_q perteneciente al nodo "actual" ya fue extendida
        # (es decir, tratada) actualizamos las listas P[actual] y Q[actual]

        P[actual].append(efe_q)
        Q[actual].remove(efe_q)


        # Encontrar efe_q como el mínimo entre los primeros elementos
        # (o sea los mínimos en orden Lex) de cada Q[j].

        # el testigo detener es idéntico a 1 si todos los Q[j] son vacios,
        # en cuyo caso el algoritmo se detiene. Notar que no es necesario
        # crear una nueva lista con el mínimo de cada Q[j].

        efe_q  = (float("inf"),float("inf"))
        detener = 1
        for vertice in G.vertices:

            if len(Q[vertice])>0 :
                detener *= 0
                if Q[vertice][0] < efe_q:
                    efe_q = Q[vertice][0]
                    actual = vertice
            else:
                detener *= 1

    return P

def spptw_desrochers1988_imp2(G,s,time,costo,ventana):
    """ Second algorithm in Desrochers et al. 1988.

    In implementation 2 each Q_j is an ordered list (Lex order) and after creating a new label in the j node,
    it is appended after comparing only with the first element of the Q_j list, so that it always contains efficient
    labels and potentially some non-efficient labels.

    Args:
        G: A directed instance of Graph class.
        s: Integer or string denoting the source vertex.
        time: A dictionary defining a time function on the arcs.
        costo: A dictionary defining a cost function on the arcs.
        ventana: A dictionary defining time windows for each vertex.


    Returns:
        A dictionary which for each vertex show the  list of efficient labels from source vertex s.

    """


    # Paso 1: inicialización
    # Crear un diccionario P, donde cada clave es el entero que representa
    # un vértice del grafo y donde el valor es una lista que contiene
    # las etiquetas ya extendidas. Crear un diccionario Q similar a P,
    # donde las listas contienen las etiquetas que aun no han sido extendidas.

    P = dict({vertice: [] for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"),float("inf"))] for vertice in G.vertices})
    Q[s] = [(0, 0)]
    actual, efe_q, detener = s, (0,0), 0

    # Paso 2: Extender efe_q, contener el frente de Pareto
    # en cada lista Q[j].

    while detener == 0:

        # Extender la etiqueta efe_q desde nodo actual. Una extensión
        # es factible si se respetan ventanas de tiempo.

        for vecino in G.succesors(actual):
            if efe_q[0] + time[(actual,vecino)] <= ventana[vecino][1]:
                label_time = max(ventana[vecino][0], efe_q[0] + time[(actual,vecino)])
                label_cost = efe_q[1] + costo[(actual,vecino)]
                new_label = (label_time, label_cost)
                print('new label',new_label)
                # Actualizar el frente de Pareto (potencialmente hay etiquetas no eficientes)
                Q[vecino], insertado = contain_pareto_frontier(Q[vecino],new_label)


        # Como la etiqueta efe_q perteneciente al nodo "actual" ya fue extendida
        # (es decir, tratada) actualizamos las listas P[actual] y Q[actual]

        P[actual].append(efe_q)
        Q[actual].remove(efe_q)


        # Encontrar efe_q como el mínimo entre los primeros elementos
        # (o sea los mínimos en orden Lex) de cada Q[j].

        # el testigo detener es idéntico a 1 si todos los Q[j] son vacios,
        # en cuyo caso el algoritmo se detiene. Notar que no es necesario
        # crear una nueva lista con el mínimo de cada Q[j].

        efe_q  = (float("inf"),float("inf"))
        detener = 1
        for vertice in G.vertices:

            if len(Q[vertice])>0 :
                detener *= 0
                if Q[vertice][0] < efe_q:
                    efe_q = Q[vertice][0]
                    actual = vertice
            else:
                detener *= 1
    # Paso 4: Como para cada nodo j, la lista  P_j puede tener etiquetas no
    # eficientes, reducimos la lista hasta quedar sólo con el frente de Pareto.
    # como las listas ya están ordenadas en orden Lex, el costo es O(D), donde D
    # es el número de posibles etiquetas. NO ENTIENDO POR QUÉ EL ARTÍCULO DICE
    # QUE ES O(d) con d la máxima amplitud de una ventana de tiempo.

    for vertice in G.vertices:
        P[vertice] = reduce_to_pareto_frontier(P[vertice])

    return P

def spptw_desrochers1988_imp3(G,s,time,costo,ventana):
    """Third algorithm in Desrochers et al. 1988.

    In implementation #3 each Q_j is an ordered list (Lex order) and after creating a new label in the j node, it is
    attached after comparing only with the first element in the Q_j list, so that it always contains efficient labels
    and potentially some non-efficient labels. The new label is also added in a heap, from which the minimum is
    extracted (efe_q) (and we don't worry about the inefficient labels because they are the last ones to be extracted
    from the heap).



    Args:
        G: A directed instance of Graph class.
        s: Integer or string denoting the source vertex.
        time: A dictionary defining a time function on the arcs.
        costo: A dictionary defining a cost function on the arcs.
        ventana: A dictionary defining time windows for each vertex.


    Returns:
        A dictionary which for each vertex show the  list of efficient labels from source vertex s.

    """


    # Paso 1: inicialización
    # Crear un diccionario P, donde cada clave es el entero que representa
    # un vértice del grafo y donde el valor es una lista que contiene
    # las etiquetas ya extendidas. Crear un diccionario Q similar a P,
    # donde las listas contienen las etiquetas que aun no han sido extendidas.
    S = dict({vertice: set() for vertice in G.vertices})
    P = dict({vertice: sortedset([]) for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"), float("inf"))] for vertice in G.vertices})
    Q[s] = [(0, 0)]
    label_heap = [((0,0),s)]

    # Paso 2: Extender efe_q, contener el frente de Pareto
    # en cada lista Q[j].

    while label_heap:

        (efe_q, actual) = heapq.heappop(label_heap)

        # Verificamos si la etiqueta extraida: efe_q del nodo actual, es dominada por alguna
        # etiqueta en P[actual]
        check, S[actual] =  check_dominance(P[actual], efe_q, S[actual])
        # si alguien en P[actual] domina a efe_q, continuamos con la iteración del while
        if check == True:
            pass
        else:
            # verificamos si efe_q ya está en el conjunto de etiquetas que fueron excluidas
            if efe_q in S[actual]:
                pass
            else:
                # Extender la etiqueta efe_q desde nodo actual. Una extensión
                # es factible si se respetan ventanas de tiempo.

                for vecino in G.succesors(actual):
                    if efe_q[0] + time[(actual, vecino)] <= ventana[vecino][1]:
                        label_time = max(ventana[vecino][0], efe_q[0] + time[(actual, vecino)])
                        label_cost = efe_q[1] + costo[(actual, vecino)]
                        new_label = (label_time, label_cost)
                        print('new label', new_label)
                        # Antes de actualizar el frente de Pareto verificamos si new_label está dominada por
                        # alguna etiqueta en P[vecino], en cuyo caso no tiene sentido ingresar a las
                        # posibles etiquetas, pues de ella se generarán más etiquetas dominadas.
                        check_int, S[vecino] = check_dominance(P[vecino], new_label, S[vecino])
                        if  check_int == False:
                            # Actualizar el frente de Pareto (potencialmente hay etiquetas no eficientes)
                            Q[vecino], insertado, S[vecino] = contain_pareto_frontier(Q[vecino], new_label, S[vecino])
                            if insertado == True:
                                heapq.heappush(label_heap, (new_label, vecino))
                        else:
                            pass
                # Como la etiqueta efe_q perteneciente al nodo "actual" ya fue extendida
                # (es decir, tratada) actualizamos las listas P[actual] y Q[actual]

                P[actual].add(efe_q)
                heapq.heappop(Q[actual])


    # Paso 4: Como para cada nodo j, la lista  P_j puede tener etiquetas no
    # eficientes, reducimos la lista hasta quedar sólo con el frente de Pareto.
    # como las listas ya están ordenadas en orden Lex, el costo es O(D), donde D
    # es el número de posibles etiquetas. NO ENTIENDO POR QUÉ EL ARTÍCULO DICE
    # QUE ES O(d) con d la máxima amplitud de una ventana de tiempo.

    for vertice in G.vertices:
        P[vertice] = reduce_to_pareto_frontier(P[vertice])

    print('Este es P',P)
    return P



def min_time_cost(G,tiempo,costo):
    """ Find the lexicographical minimum among all labels.

    Find the pair (m_d,m_c) defined as the lexicographical minimum among all the pairs (time, cost) on the arcs of
    network G.

    Args:
        G: A directed instance of Graph class.
        tiempo: A dictionary with keys the arcs (u,v) in the graph and values their distances
        costo: A dictionary with keys the arcs (u,v) in the graph and values their costs

    Returns:
        A pair (m_d,m_c) corresponding to the Lex minimum.

    """


    time_cost = list()
    for arista in G.aristas:
        time_cost.append((tiempo[arista],costo[arista]))
    (mt,mc) = min(time_cost)

    return (mt,mc)

def spptw_desrochers1988_imp3_bucket(G,s,time,costo,ventana):
    """Third algorithm, using buckets,  in Desrochers et al. 1988.

     In implementation 3 each Q_j is an ordered list (Lex order) and after creating a new label on the j node,
     it is attached after comparing only with the first element in the Q_j list, so that the list always contains
     efficient labels and potentially some inefficient labels. The new label is also added in a heap, from which it goes
     extracting the minimum (efe_q) (and we don't worry about the inefficient labels because they are the last to be
     removed from the heap). All tags contained in a generalized BUCKET are extended before finding F(Q) (efe_q) the
     new minimum label in Q.


    Args:
        G: A directed instance of Graph class.
        s: Integer or string denoting the source vertex.
        time: A dictionary defining a time function on the arcs.
        costo: A dictionary defining a cost function on the arcs.
        ventana: A dictionary defining time windows for each vertex.


    Returns:
        A dictionary which for each vertex show the  list of efficient labels from source vertex s.


    """


    # Paso 1: inicialización
    # Calcular la dupla (mt,mc) que es el mínimo entre las parejas (tiempo, costo)
    # definidas sobre las aristas del grafo G.
    # Crear un diccionario P, donde cada clave es el entero que representa
    # un vértice del grafo y donde el valor es una lista que contiene
    # las etiquetas ya extendidas. Crear un diccionario Q similar a P,
    # donde las listas contienen las etiquetas que aun no han sido extendidas.

    (mt,mc) = min_time_cost(G,time,costo)
    P = dict({vertice: [] for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"), float("inf"))] for vertice in G.vertices})
    Q[s] = [(0, 0)]
    label_heap = [((0, 0), s)]



    while label_heap:

        # Paso 2: Definir y encontrar las etiquetas pertenecientes al bucket actual

        (efe_q,actual) = heapq.heappop(label_heap)
        upper_bound = efe_q + (mt, mc)
        bucket = list()
        for vertice in G.vertices:
            for label in Q[vertice]:
                if label < upper_bound:
                    bucket.append((label,vertice))


        # Paso 3: Extraer una a una las etiquetas de bucket.

        while bucket:
            (current_label, current_node) = bucket.pop()
            # Paso 4: Extender la etiqueta extraida.Una extensión es factible
            # si se respetan ventanas de tiempo.
            for vecino in G.succesors(current_node):
                if current_label[0] + time[(current_node, vecino)] <= ventana[vecino][1]:
                    label_time = max(ventana[vecino][0], current_label[0] + time[(current_node, vecino)])
                    label_cost = current_label[1] + costo[(current_node, vecino)]
                    new_label = (label_time, label_cost)
                    print('new label', new_label)
                    # Actualizar el frente de Pareto (potencialmente hay etiquetas no eficientes)
                    Q[vecino], insertado = contain_pareto_frontier(Q[vecino], new_label)
                    if insertado == True:
                        heapq.heappush(label_heap, (new_label,vecino))

            # Como la etiqueta current_label perteneciente al nodo current_node ya
            # fue extendida (es decir, tratada) actualizamos las listas
            # P[current_node] y Q[current_node]

            P[current_node].append(current_label)
            Q[current_node].remove(current_label)


    # Paso 5: Como para cada nodo j, la lista  P_j puede tener etiquetas no
    # eficientes, reducimos la lista hasta quedar sólo con el frente de Pareto.
    # como las listas ya están ordenadas en orden Lex, el costo es O(D), donde D
    # es el número de posibles etiquetas. NO ENTIENDO POR QUÉ EL ARTÍCULO DICE
    # QUE ES O(d) con d la máxima amplitud de una ventana de tiempo.

    for vertice in G.vertices:
        P[vertice] = reduce_to_pareto_frontier(P[vertice])

    return P

###################################################################
def spptw_desrochers1988_imp3V2(G,s,time,costo,ventana):
    """Third algorithm in Desrochers et al. 1988.

    In implementation #3 each Q_j is an ordered list (Lex order) and after creating a new label in the j node, it is
    attached after comparing only with the first element in the Q_j list, so that it always contains efficient labels
    and potentially some non-efficient labels. The new label is also added in a heap, from which the minimum is
    extracted (efe_q) (and we don't worry about the inefficient labels because they are the last ones to be extracted
    from the heap). In version 2 we use the class Label.



    Args:
        G: A directed instance of Graph class.
        s: Integer or string denoting the source vertex.
        time: A dictionary defining a time function on the arcs.
        costo: A dictionary defining a cost function on the arcs.
        ventana: A dictionary defining time windows for each vertex.


    Returns:
        A dictionary which for each vertex show the  list of efficient labels from source vertex s.

    """


    # Paso 1: inicialización
    # Crear un diccionario P, donde cada clave es el entero que representa
    # un vértice del grafo y donde el valor es una lista que contiene
    # las etiquetas ya extendidas. Crear un diccionario Q similar a P,
    # donde las listas contienen las etiquetas que aun no han sido extendidas.
    S = dict({vertice: set() for vertice in G.vertices})
    P = dict({vertice: [] for vertice in G.vertices})
    Q = dict({vertice: [(float("inf"), float("inf"))] for vertice in G.vertices})
    #Q = dict({vertice: [Label(vertice, None, float("inf"), float("inf")) ] for vertice in G.vertices})
    Q[s] = [(0, 0)]
    label_heap = [((0,0),s)]

    # Paso 2: Extender efe_q, contener el frente de Pareto
    # en cada lista Q[j].

    while label_heap:

        (efe_q, actual) = heapq.heappop(label_heap)

        # Verificamos si la etiqueta extraida: efe_q del nodo actual, es dominada por alguna
        # etiqueta en P[actual]
        check, S[actual] =  check_dominance(P[actual], efe_q, S[actual])
        # si alguien en P[actual] domina a efe_q, continuamos con la iteración del while
        if check == True:
            pass
        else:
            # verificamos si efe_q ya está en el conjunto de etiquetas que fueron excluidas
            if efe_q in S[actual]:
                pass
            else:
                # Extender la etiqueta efe_q desde nodo actual. Una extensión
                # es factible si se respetan ventanas de tiempo.

                for vecino in G.succesors(actual):
                    if efe_q[0] + time[(actual, vecino)] <= ventana[vecino][1]:
                        label_time = max(ventana[vecino][0], efe_q[0] + time[(actual, vecino)])
                        label_cost = efe_q[1] + costo[(actual, vecino)]
                        new_label = (label_time, label_cost)
                        print('new label', new_label)
                        # Antes de actualizar el frente de Pareto verificamos si new_label está dominada por
                        # alguna etiqueta en P[vecino], en cuyo caso no tiene sentido ingresar a las
                        # posibles etiquetas, pues de ella se generarán más etiquetas dominadas.
                        check_int, S[vecino] = check_dominance(P[vecino], new_label, S[vecino])
                        if  check_int == False:
                            # Actualizar el frente de Pareto (potencialmente hay etiquetas no eficientes)
                            Q[vecino], insertado, S[vecino] = contain_pareto_frontier(Q[vecino], new_label, S[vecino])
                            if insertado == True:
                                heapq.heappush(label_heap, (new_label, vecino))
                        else:
                            pass
                # Como la etiqueta efe_q perteneciente al nodo "actual" ya fue extendida
                # (es decir, tratada) actualizamos las listas P[actual] y Q[actual]

                P[actual].append(efe_q)
                heapq.heappop(Q[actual])


    # Paso 4: Como para cada nodo j, la lista  P_j puede tener etiquetas no
    # eficientes, reducimos la lista hasta quedar sólo con el frente de Pareto.
    # como las listas ya están ordenadas en orden Lex, el costo es O(D), donde D
    # es el número de posibles etiquetas. NO ENTIENDO POR QUÉ EL ARTÍCULO DICE
    # QUE ES O(d) con d la máxima amplitud de una ventana de tiempo.

    for vertice in G.vertices:
        P[vertice] = reduce_to_pareto_frontier(P[vertice])

    return P

###################################################################
#def espptw_feillet2004(G,s,time, costo,ventana):
