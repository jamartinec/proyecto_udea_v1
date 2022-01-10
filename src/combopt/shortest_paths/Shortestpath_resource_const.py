# coding: utf8
import heapq
from src.combopt.graph import Grafo,Grafo_consumos
#from src.combopt.shortest_paths.pareto_frontier_structure import Pareto_Frontier
from src.combopt.shortest_paths.pareto_frontier_optimizado import ParetoFrontier, Label_feillet2004
from sortedcontainers import SortedList
from collections import deque
from copy import deepcopy


# def spptw_desrochers1988_imp_fullpareto(G,s,time,costo,ventana):
#     """First algorithm in Desrochers et al. 1988. (modified)
#
#     We guarantee at all times that the Pareto Front will be preserved. For this purpose we make use of a
#     class for the Front, so that upgrade operations are efficient. In order to
#     analogous to Dijkstra's algorithm we distinguish two types of labels:
#
#     1) The labels that have not been treated or extended. They are stored in:
#         A minheap under the lexicographic order to which the new labels generated are added.
#         From the minheap the smallest label is extracted in Lex order among all the Untreated labels of all
#         the vertices. When this label (let's call it a minlabel) is extracted, the following conditions are checked:
#
#           a)  If the minlabel is part of the DISCARDED label set in a previous iteration, then it is NOT extended.
#               We do this check first because it is cheap O(1). See below to understand when a label is added to
#               DISCARDS.
#           b)  We look at the vertex to which this minlabel corresponds and we go to the instance of the Pareto Front
#               class of the TREATED labels of that vertex. If any in TREATEDs dominates the new label then it is added to
#               DISCARDED and NOT extended. Otherwise the Pareto front of the TREATED labels is updated and the extension
#               is done. Note that any extension to a dominated label will be dominated by a label that was already
#               included in the minheap.
#
#      2) A new label resulting from the extension of the minlabel (NOT dominated by someone in the TREATED and NOT
#         previously DISCARDED) is entered into the minheap if it satisfies the following:
#           a) It has not been previously DISCARDED.
#           b) It is not dominated by any label in the Pareto class instance containing the UNTREATED ones of the vertex
#           over which it is defined.
#
#           Note that the criteria for entering heap and the criteria for being extended after leaving heap are the same.
#           Both TREATED and UNTREATED structures are Pareto structures.
#           * A label is discarded when it has been eliminated or a candidate that does not enter the Pareto front of the apex to which it corresponds
#           (and never re-enters)  in which case we know it is inefficient.
#
#
#
#
#     Args:
#         G: A directed instance of Graph class.
#         s: Integer or string denoting the source vertex.
#         time: A dictionary defining a time function on the arcs.
#         costo: A dictionary defining a cost function on the arcs.
#         ventana: A dictionary defining time windows for each vertex.
#
#
#     Returns:
#         A dictionary which for each vertex show the  list of efficient labels from source vertex s.
#
#     """
#
#
#     # Paso 1: inicialización
#     # Crear un diccionario TRATADAS, donde cada clave es el entero que representa un vértice del grafo y donde el valor
#     # es una lista que contiene las etiquetas ya extendidas. Crear un diccionario NO TRATADAS similar,
#     # donde las listas contienen las etiquetas que aun no han sido extendidas.
#     Discard_sets= dict({vertice: set() for vertice in G.vertices})
#     Treated_labels = dict({vertice: Pareto_Frontier(vertice,[]) for vertice in G.vertices})
#     Non_treated_labels = dict({vertice: Pareto_Frontier(vertice,[(float("inf"), float("inf"))]) for vertice in G.vertices})
#     Non_treated_labels[s] = Pareto_Frontier(s,[(0, 0)])
#     label_heap = [((0,0),s)]
#
#     # Paso 2: Extender efe_q, preservar el frente de Pareto de TRATADOS y NO TRATADOS.
#
#     while label_heap:
#         # Se extrae la menor etiqueta en orden lexicográfico de cualquiera de los nodos.
#         (efe_q, actual) = heapq.heappop(label_heap)
#         # la etiqueta efe_q sale de NO TRATADAS[actual]
#         Non_treated_labels[actual] = Non_treated_labels[actual].Delete_label(efe_q)
#
#
#         # verificamos si efe_q ya está en el conjunto de etiquetas que fueron excluidas. De estarlo nos devolvemos y
#         # extraemos (pop) una nueva etiqueta del minheap.
#         if efe_q in Discard_sets[actual]:
#             continue
#         else:
#             # Verificamos si la etiqueta extraida: efe_q del nodo actual, es dominada por alguna etiqueta en
#             # Treated_labels[actual]
#
#             updated_front, check, discarded_after_update = Treated_labels[actual].preserve_pareto(efe_q)
#             # si check es false es porque new_label es dominado y no se inserta en el frente de pareto. En tal caso se
#             # agrega a las etiquetas descartadas.
#             if check == False:
#                 Discard_sets[actual].add(efe_q)
#                 continue
#             else:
#                 # si la etiqueta fue insertada en el frente de pareto, actualizamos éste, y también las posibles
#                 # etiquetas descartadas tras la actualización del frente.
#                 Treated_labels[actual] = updated_front
#                 Discard_sets[actual].union(discarded_after_update)
#                 # Extender la etiqueta efe_q desde actual. Una extensión es factible si se cumple ventanas de tiempo.
#                 for vecino in G.succesors(actual):
#                     if efe_q[0] + time[(actual, vecino)] <= ventana[vecino][1]:
#                         label_time = max(ventana[vecino][0], efe_q[0] + time[(actual, vecino)])
#                         label_cost = efe_q[1] + costo[(actual, vecino)]
#                         new_label = (label_time, label_cost)
#
#                         # Antes de actualizar el frente de Pareto de etiquetas NO TRATADAS de vecino, verificamos si
#                         # new_label está en DESCARTADAS o está dominada por alguna etiqueta en TRATADAS[vecino], en cuyo
#                         # caso no se ingresa a NO TRATADAS , pues a partir de ella se generarán más etiquetas dominadas.
#
#                         if new_label in Discard_sets[vecino]:
#                             continue
#                         else:
#                             ## ACÁ SOLO VERIFICAR si new label es dominado por alguien en TRATADOS (sin agregar)
#                             check = Treated_labels[vecino].check_dominance(new_label)
#                             if check == True:
#                                 Discard_sets[vecino].add(new_label)
#                                 continue
#                             else:
#                                 Non_treated_labels[vecino], insertado, U = Non_treated_labels[vecino].preserve_pareto(new_label)
#                                 if insertado == True:
#                                     heapq.heappush(label_heap, (new_label, vecino))
#                                 else:
#                                     pass
#
#
#     P = dict({vertice: Treated_labels[vertice].to_list() for vertice in G.vertices})
#     print('mire pa que vea', P)
#     return P

def spptw_desrochers1988_imp_fullpareto(G,s,time,costo,ventana,output_type=True):
    """First algorithm in Desrochers et al. 1988. (modified)

    We guarantee at all times that the Pareto Front will be preserved. For this purpose we make use of a
    class for the Front, so that upgrade operations are efficient. In order to
    analogous to Dijkstra's algorithm we distinguish two types of labels:

    1) The labels that have not been treated or extended. They are stored in:
        A minheap under the lexicographic order to which the new labels generated are added.
        From the minheap the smallest label is extracted in Lex order among all the Untreated labels of all
        the vertices. When this label (let's call it a minlabel) is extracted, the following conditions are checked:

          a)  If the minlabel is part of the DISCARDED label set in a previous iteration, then it is NOT extended.
              We do this check first because it is cheap O(1). See below to understand when a label is added to
              DISCARDS.
          b)  We look at the vertex to which this minlabel corresponds and we go to the instance of the Pareto Front
              class of the TREATED labels of that vertex. If any in TREATEDs dominates the new label then it is added to
              DISCARDED and NOT extended. Otherwise the Pareto front of the TREATED labels is updated and the extension
              is done. Note that any extension to a dominated label will be dominated by a label that was already
              included in the minheap.

     2) A new label resulting from the extension of the minlabel (NOT dominated by someone in the TREATED and NOT
        previously DISCARDED) is entered into the minheap if it satisfies the following:
          a) It has not been previously DISCARDED.
          b) It is not dominated by any label in the Pareto class instance containing the UNTREATED ones of the vertex
          over which it is defined.

          Note that the criteria for entering heap and the criteria for being extended after leaving heap are the same.
          Both TREATED and UNTREATED structures are Pareto structures.
          * A label is discarded when it has been eliminated or a candidate that does not enter the Pareto front of the apex to which it corresponds
          (and never re-enters)  in which case we know it is inefficient.




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
    label_heap = [( (0,0), s, (None, None) )]
    # efe_q  es lo mismo que minlabel (corregir)
    # Paso 2: Extender efe_q, preservar el frente de Pareto de TRATADOS y NO TRATADOS.

    while label_heap:
        print('labelheap',label_heap)
        # Se extrae la menor etiqueta en orden lexicográfico de cualquiera de los nodos.
        (minlabel, actual, trazador) = heapq.heappop(label_heap)
        print('minlabel!!', minlabel)
        print('actual!',actual)
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
            print('treated_label después de agreagar minlabel',updated_front.list_frontlabels())
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

def retrieve_path(label,vertex,Treated_labels):

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

def retrieve_paths_inpareto(vertex, Treated_labels):
    # Vamos a guardar en diccionario porque, debido a la estructura de Pareto Set, no es posible
    # que existan dos etiquetas iguales en el frente de Pareto. Garantiza que la clave sea única.
    dict_paths = dict()
    dict_paths_set = dict()
    dict_paths_inner = dict()
    for label in Treated_labels[vertex].list_frontlabels():
        partial_path_inner, partial_path, partial_path_set = retrieve_path(label,vertex,Treated_labels)
        dict_paths[label] = partial_path
        dict_paths_inner[label] = partial_path_inner
        dict_paths_set[label] = partial_path_set
    return dict_paths_inner, dict_paths, dict_paths_set

### pilas, necesitamos Treated_labels[vertex].ALGUNAFUNCION()
#Donde ALGUNAFUNCION es un método de la instancia pareto frontier que retorna un iterable con las etiquetas de ese frente

def slave_function(G,source,sink,time,costo,ventana):

    Frentes_Pareto = spptw_desrochers1988_imp_fullpareto(G,source,time,costo,ventana, output_type=False)
    Dictio_Paths_Inner, Dictio_Paths, Dictio_Paths_set = retrieve_paths_inpareto(sink, Frentes_Pareto)

    return Dictio_Paths_Inner, Dictio_Paths, Dictio_Paths_set

def verificar_recursos(actual, sucesor):

    arco = (actual, sucesor)
    indicador = True
    nuevos_valores = dict()
    for recurso in etiqueta.label_recursos.keys():
        cantidad = etiqueta.label_recursos[recurso] + G.nodo_recursos()[sucesor][recurso] + \
                   G.arco_recursos()[arco][recurso]
        nuevos_valores[recurso] = cantidad
        if cantidad > G.nodo_ventanas()[sucesor][recurso][1]:
            indicador=False
            break
    return indicador, nuevos_valores


def Extend_function_feillet2004(etiqueta,nodo):
    # esta función primero debe verificar si es posible extender la etiqueta al nodo dado, para
    #formar una nueva etiqueta
    nodo_partida = etiqueta.nodo_rel
    # Yo creo que esto no es necesario, porque si no se cumpliera el nodo estaría marcado como inalcanzable
    # desde el principio.
    indicador, nuevos_valores = verificar_recursos(nodo_partida,nodo)
    if indicador == False:
        etiqueta.update_label_visitas([nodo])
        return indicador, etiqueta

    else:
        # si se satisfacen las restricciones de capacidad, lo que sigue es crear una nueva etiqueta
        # cuyo nodo de referencia sea "nodo". Para ello copiamos la etiqueta actual.
        new_etiqueta = deepcopy(etiqueta)
        new_etiqueta.update_nodo_rel(nodo)
        new_etiqueta.update_label_visitas([nodo])
        new_etiqueta.update_label_recursos(nuevos_valores)
        # Es necesario explorar los vecinos de "nodo" para determinar si alguno de ellos es
        # inalcanzable. Esto quiere decir que inspecciono para cada uno de ellos, si

        # para cada nodo que se examine se debería guardar los nuevos valores. Es decir, si estoy
        # considerando una etiqueta que corresponde a cierto nodo y voy a evaluar su extensión a otro nodo
        # de entrada si no es posible tal nodo aparece marcado como inalcanzable. Si es alcanzable ya
        # debería tener guardado los valores de todos los recursos para la etiqueta extendida.
        # vamos a guardar esta información como un diccionario de diccionarios.

        recursos_sucesores =dict()
        for sucesor in G.succesors(new_etiqueta.nodo_rel):
            indicador, nuevos_valores = verificar_recursos(new_etiqueta.nodo_rel,sucesor)
            if indicador == False:
                new_etiqueta.update_label_visitas([sucesor])
            else:
                recursos_sucesores[sucesor]=nuevos_valores

        new_etiqueta.update_recursos_sucesores(recursos_sucesores)
        return new_etiqueta


def comparacion_etiqueta_par(etiquetaA,etiquetaB):
    # Comparar etiquetaA con etiquetaB.
    # Número de entradas de una etiqueta, contando indicadores, recursos, costo y número de visitas:


    try:
        assert etiquetaA.longitud ==etiquetaB.longitud
    except:
        raise ValueError

    num_entradas = etiquetaA.longitud

    A_domina = list()
    B_domina = list()

    for recurso in etiquetaA.label_recursos.keys():
        if etiquetaA.label_recursos[recurso] < etiquetaB.label_recursos[recurso]:
            A_domina.append(recurso)
        elif etiquetaB.label_recursos[recurso] < etiquetaA.label_recursos[recurso]:
            B_domina.append(recurso)

    if etiquetaA.conteo < etiquetaB.conteo:
        # A ha visitado menos nodos que B por tanto B no puede dominar a A. Nos preguntamos si entonces
        # A domina a B:
        





def EFF_function_feillet2004(A):



def espptw_feillet2004(G:Grafo_consumos,s,recursos:list, ventana:list ,costo,output_type=True):
    # a partir del grafo dado y los recursos necesito crear una estructura
    # para las etiquetas. De pronto conviene crear una clase, porque las etiquetas
    # guardan información pero no están cambiando de dimensiones.

    # pensemos que pasamos los diccionarios de recursos en una lista
    # y las correspondientes restricciones o ventanas en otra, relacionadas por la posición

    nombres_recursos = G.nombres_recursos()
    vertices =G.vertices

    # crear un diccionario cuyas llaves sean los vértices y cuyos valores sean listas.
    Delta = dict({vertice: set() for vertice in vertices})
    # ¿cuál es el método para encontrar el conjunto de sucesores de un nodo? G.succesors(nodo)

    Delta[s].add(Label_feillet2004(nodo_rel=s,name_recursos=nombres_recursos,nodos=vertices))

    # pilas! esta sí es la forma adecuada de manejar las etiquetas que se extienden?
    F=dict()

    # Conjunto de nodos esperando a ser tratados. No se especifica cuál es la estructura adecuada,
    # podríamos tratarlo como un cola FIFO siguiendo la mejora de moore para el algoritmo de Bellman Ford.
    # muy importante: if maxlen is not specified, deques may grow up to an arbitrary length.

    E=deque([s])

    while E:
        actual = E.pop()
        for sucesor in G.succesors(actual):
            F[(actual,sucesor)] =set()
            for etiqueta in Delta[actual]:
                if etiqueta.label_visitas[sucesor]==0: # si el nodo sucesor no es un nodo 'inalcanzable'
                    F[(actual, sucesor)].add(Extend_function_feillet2004(etiqueta,sucesor))
            A=Delta[sucesor].union(F[(actual, sucesor)])
            eff,indicador_change = EFF_function_feillet2004(A)
            if indicador_change ==1:
                E.appendleft(sucesor)
        E.remove(actual)





    # para el vertice i la lista dictio[i] contiene las etiquetas ??
    # debemos recordar cómo está definida una etiqueta en este caso.
    

