# coding: utf8
import heapq
import bisect
import numpy as np
from blist import sortedset
from src.combopt.shortest_paths.desrochers_soumis_1988.estructuras_fijacion import \
    ParetoFrontier

###########################################################################################
def pareto_set(A):
    # originalmente en shortest_path_basic
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
    # originalmente en shortest_path_basic
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
    # originalmente en shortest_path_basic.py
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
    Q_set = dict({vertice:{ (float("inf"),float("inf")) }  for vertice in G.vertices} )
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
    # originalmente en shortes_path_basic.py
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
    # originalmente en shortes_path_basic.py
    """ Checks if a new label is efficient, an update the original list.

    Given an ordered list (under lexicographical order) of n efficient (time, cost) labels, and a new new_label
    checks if it is efficient and should be included in A preserving order Lex, and removes from A those labels that are
    now dominated by new_label.


    Args:
        A: A list of pairs (u,v), in ascending Lex order.
        new_label: A new label/pair (u,v).

    Returns:
        A list containing the resulting Paretro frontier.

    """

    # Este algoritmo tiene complejidad O(n), donde n es la longitud de A.
    index = list()
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
    # originalmente en shortest_path_basic.py
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
    # originalmente en shortes_path_basic.py
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



def spptw_desrochers1988_imp1(G,s,time,costo,ventana):
    # originalmente en shortes_path_basic.py
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


###########################################################################################

def spptw_desrochers1988_imp_fullpareto(G,s,time,costo,ventana,output_type=True):
    """
    First algorithm in Desrochers et al. 1988. (modified)

    We guarantee at all times that the Pareto Front will be preserved. For this purpose we make
    use of a class for the Front, so that upgrade operations are efficient. Analogous to Dijkstra's
    algorithm we distinguish two types of labels:

    1) The labels that have not been treated or extended. They are stored in:
        A minheap under the lexicographic order to which the new labels generated are added.
        From the minheap the smallest label is extracted in Lex order among all the Untreated
        labels of all the vertices. When this label (let's call it a minlabel) is extracted,
        the following conditions are checked:

    a)  If the minlabel is part of the DISCARDED label set in a previous iteration,
        then it is NOT extended. We do this check first because it is cheap O(1).
        See below to understand when a label is added to DISCARDS.

    b)  We look at the vertex to which this minlabel corresponds and we go to the instance of
        the Pareto Front class of the TREATED labels of that vertex. If any in TREATEDs dominates
        the new label then it is added to DISCARDED and NOT extended. Otherwise the Pareto front of the
        TREATED labels is updated and the extension is done. Note that any extension to a dominated label
        will be dominated by a label that was already included in the minheap.

    2) A new label resulting from the extension of the minlabel (NOT dominated by someone in the
        TREATED and NOT previously DISCARDED) is entered into the minheap if it satisfies the
        following:

    a)  It has not been previously DISCARDED.
    b)  It is not dominated by any label in the Pareto class instance containing the UNTREATED
        ones of the vertex over which it is defined.

    Note that the criteria for entering heap and the criteria for being extended after leaving heap
    are the same. Both TREATED and UNTREATED structures are Pareto structures.
    * A label is discarded when it has been eliminated or a candidate that does not enter the
    Pareto front of the apex to which it corresponds (and never re-enters)  in which case we know
    it is inefficient.




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
    # Crear un diccionario TRATADAS, donde cada clave es el entero que representa un vértice del grafo y donde el valor
    # es una lista que contiene las etiquetas ya extendidas. Crear un diccionario NO TRATADAS similar,
    # donde las listas contienen las etiquetas que aun no han sido extendidas.
    Discard_sets= dict({vertice: set() for vertice in G.vertices})
    Treated_labels = dict({vertice: ParetoFrontier(vertice) for vertice in G.vertices})
    Non_treated_labels = dict({vertice: ParetoFrontier(vertice, [(float("inf"), float("inf"))]) for vertice in G.vertices})
    Non_treated_labels[s] = ParetoFrontier(s,[(0, 0)]) # pilas, no estamos usando trazador!!!
    label_heap = [((0, 0), s, (None, None))]
    # efe_q  es lo mismo que minlabel (corregir)
    # Paso 2: Extender efe_q, preservar el frente de Pareto de TRATADOS y NO TRATADOS.

    while label_heap:
        print('labelheap', label_heap)
        # Se extrae la menor etiqueta en orden lexicográfico de cualquiera de los nodos.
        (minlabel, actual, trazador) = heapq.heappop(label_heap)
        print('minlabel!!', minlabel)
        print('actual!', actual)
        # la etiqueta efe_q sale de NO TRATADAS[actual]
        print('Non_treatedlabelsANTES de borrar minlabel', Non_treated_labels[actual].list_frontlabels())
        #¿hay algún problema con que la función retorne la misma instancia de la clase?
        Non_treated_labels[actual] = Non_treated_labels[actual].Delete_label(minlabel)
        print('Non_treatedlabelsDespues de borrar minlabel', Non_treated_labels[actual].list_frontlabels())

        # verificamos si efe_q ya está en el conjunto de etiquetas que fueron excluidas. De estarlo nos devolvemos y
        # extraemos (pop) una nueva etiqueta del minheap.
        if minlabel in Discard_sets[actual]:
            continue
        else:
            # Verificamos si la etiqueta extraida: efe_q del nodo actual, es dominada por alguna etiqueta en
            # Treated_labels[actual]

            updated_front, check, discarded_after_update = Treated_labels[actual].add(minlabel,trazador)
            print('treated_label después de agreagar minlabel', updated_front.list_frontlabels())
            # si check es false es porque new_label es dominado y no se inserta en el frente de pareto. En tal caso se
            # agrega a las etiquetas descartadas.
            if check == False:
                Discard_sets[actual].add(minlabel)
                print('No se agregó minlabel y se agregó a DISCARDSETS')
                continue
            else:
                # si la etiqueta fue insertada en el frente de pareto, actualizamos éste, y también las posibles
                # etiquetas descartadas tras la actualización del frente.
                print('MINLABEL SI SE AGREGÓ A TREATED LABELS')
                Treated_labels[actual] = updated_front
                Discard_sets[actual].union(discarded_after_update)

                # Extender la etiqueta efe_q desde actual. Una extensión es factible si se cumple ventanas de tiempo.
                for vecino in G.succesors(actual):
                    if minlabel[0] + time[(actual, vecino)] <= ventana[vecino][1]:
                        label_time = max(ventana[vecino][0], minlabel[0] + time[(actual, vecino)])
                        label_cost = minlabel[1] + costo[(actual, vecino)]
                        new_label = (label_time, label_cost)
                        new_trazador= (actual,minlabel)
                        print('newlabel es',new_label, 'esta en nodo:', vecino, 'y su trazador(act, minlabel) es', new_trazador)

                        # Antes de actualizar el frente de Pareto de etiquetas NO TRATADAS de vecino, verificamos si
                        # new_label está en DESCARTADAS o está dominada por alguna etiqueta en TRATADAS[vecino], en cuyo
                        # caso no se ingresa a NO TRATADAS , pues a partir de ella se generarán más etiquetas dominadas.

                        if new_label in Discard_sets[vecino]:
                            continue
                        else:
                            ## ACÁ SOLO VERIFICAR si new label es dominado por alguien en TRATADOS (sin agregar)
                            check = Treated_labels[vecino].check_dominance(new_label)
                            if check == True:
                                Discard_sets[vecino].add(new_label)
                                continue
                            else:
                                Non_treated_labels[vecino], insertado, U = Non_treated_labels[vecino].add(new_label, new_trazador)
                                if insertado == True:
                                    heapq.heappush(label_heap, (new_label, vecino,new_trazador))
                                else:
                                    pass
    if output_type== True:
        P = dict({vertice: Treated_labels[vertice].list_frontlabels() for vertice in G.vertices})
        #print('mire pa que vea', P)
        return P
    else:
        return Treated_labels

# PILAS, NO ES BUENA IDEA GUARDAR CAMINOS EN DICCIONARIOS CON KEYS ETIQUETAS: pueden haber dos etiquetas
# exactamente iguales producidas mediante caminos distintos. Posibilidad: Guardar como listas de tripletas
# donde la primera entrada es la etiqueta, la segunda entrada es el camino como lista y la tercera entrada
# sea el conjunto de vértices incluidos en dicho camino.

def retrieve_path(label,vertex: object,Treated_labels: dict):

    frontier = Treated_labels[vertex]
    partial_path = [vertex]
    partial_path_set = {vertex}
    (vert_prev, etiq_prev) = frontier.label_track(label[0])
    #print('Esto es lo que retorna label track que es infolabel',(vert_prev,etiq_prev))

    while vert_prev != None:
        partial_path.append(vert_prev)
        partial_path_set.add(vert_prev)
        #print('este es el partialpath', partial_path)
        frontier = Treated_labels[vert_prev]
        (vert_prev, etiq_prev) = frontier.label_track(etiq_prev[0])
    partial_path.reverse()
    partial_path_inner = partial_path[1:-1]
    return partial_path_inner,  partial_path, partial_path_set

def retrieve_paths_inpareto(vertex, Treated_labels: dict):
    # Vamos a guardar en diccionario porque, debido a la estructura de Pareto Set, no es posible
    # que existan dos etiquetas iguales en el frente de Pareto. Garantiza que la clave sea única.
    dict_paths = dict()
    dict_paths_set = dict()
    dict_paths_inner = dict()
    for label in Treated_labels[vertex].list_frontlabels():
        partial_path_inner, partial_path, partial_path_set = retrieve_path(label, vertex, Treated_labels)
        dict_paths[label] = partial_path
        dict_paths_inner[label] = partial_path_inner
        dict_paths_set[label] = partial_path_set
    return dict_paths_inner, dict_paths, dict_paths_set

### pilas, necesitamos Treated_labels[vertex].ALGUNAFUNCION()
#Donde ALGUNAFUNCION es un método de la instancia pareto frontier que retorna un iterable con las etiquetas de ese frente

def slave_function(G,source,sink,time,costo,ventana):

    Frentes_Pareto = spptw_desrochers1988_imp_fullpareto(G, source, time, costo, ventana, output_type=False)
    Dictio_Paths_Inner, Dictio_Paths, Dictio_Paths_set = retrieve_paths_inpareto(sink, Frentes_Pareto)

    return Dictio_Paths_Inner, Dictio_Paths, Dictio_Paths_set


def build_generalized_bucket(ventana_dict:dict, width:float):
    minimo, maximo = np.inf, -np.inf
    minimo_set, maximo_set = set(), set()
    sorted_windows_left = sorted(ventana_dict.items(), key=lambda kv: kv[1][0])


    for vertex in ventana_dict:
        if ventana_dict[vertex][0] < minimo:
            minimo = ventana_dict[vertex][0]
            minimo_set.add(vertex)
        if ventana_dict[vertex][1] > maximo:
            maximo = ventana_dict[vertex][1]
            maximo_set.add(vertex)
    bucket_limits = list()
    limit = minimo
    while limit <= maximo:
        bucket_limits.append(limit)
        limit += width

    sub_intervalos = list()
    for limit, nextlimit in zip(bucket_limits, bucket_limits[1:]):
        for x in sorted_windows_left:
            a, b = x[1][0], x[1][1]

            if a < limit < b <= nextlimit:
                sub_intervalos.append([limit, b])

            elif limit <= a < b <= nextlimit: ## unir con el sgt
                sub_intervalos.append([a, b])

            elif a < limit < nextlimit < b:
                sub_intervalos.append([limit, nextlimit])

            elif limit <= a < nextlimit < b:
                sub_intervalos.append([a, nextlimit])
    limit = bucket_limits[-1]
    for x in sorted_windows_left:
        a, b = x[1][0], x[1][1]
        if limit < b:
            sub_intervalos.append([limit, b])
    return sub_intervalos