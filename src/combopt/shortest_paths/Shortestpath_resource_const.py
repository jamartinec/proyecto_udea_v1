# coding: utf8
import heapq
from src.combopt.graph import Grafo
from src.combopt.shortest_paths.pareto_frontier_structure import Pareto_Frontier
from sortedcontainers import SortedList


def spptw_desrochers1988_imp_fullpareto(G,s,time,costo,ventana):
    """First algorithm in Desrochers et al. 1988. (modified)

    Garantizamos en todo momento que se preserve el Frente de Pareto. Para ello hacemos uso de una
    clase para el Frente, de modo que las operaciones de actualización sean eficientes. De forma
    análoga al algoritmo de Dijkstra distinguimos dos tipos de etiquetas:
    1) Las etiquetas  que no han sido tratadas o extendidas. Se almacenan en:
          Un minheap bajo el orden lexicográfico al cual se van añadiendo las nuevas etiquetas generadas.
          Del minheap se extrae la menor etiqueta en orden Lex entre todas las etiquetas NO TRATADAS de todos
          los vértices. Cuando esta etiqueta (llamémosla efe_q o minlabel) se extrae se verifican las siguientes
          condiciones:

          a)  Si la etiqueta efe_q (ó minlabel)  hace parte del conjunto de etiquetas DESCARTADAS en una iteración previa,
              entonces NO se extiende. Primero hacemos esta comprobación porque es barata O(1). Ver más abajo para
              entender cuándo una etiqueta se agrega a DESCARTADAS.
          b)  Miramos el vértice al cual corresponde esta etiqueta efe_q y vamos a la instancia de la clase Frente
              de Pareto de las etiquetas TRATADAS de ese vértice. Si alguna en TRATADAS domina a la nueva etiqueta
              entonces esta se agrega a DESCARTADAS y NO se extiende. De lo contrario se actualiza el frente de pareto en
              de las etiquetas TRATADAS y se procede con la extensión. Note que cualquier extensión de una etiqueta
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
    # Crear un diccionario TRATADAS, donde cada clave es el entero que representa un vértice del grafo y donde el valor
    # es una lista que contiene las etiquetas ya extendidas. Crear un diccionario NO TRATADAS similar,
    # donde las listas contienen las etiquetas que aun no han sido extendidas.
    Discard_sets= dict({vertice: set() for vertice in G.vertices})
    Treated_labels = dict({vertice: Pareto_Frontier(vertice,[]) for vertice in G.vertices})
    Non_treated_labels = dict({vertice: Pareto_Frontier(vertice,[(float("inf"), float("inf"))]) for vertice in G.vertices})
    Non_treated_labels[s] = Pareto_Frontier(s,[(0, 0)])
    label_heap = [((0,0),s)]

    # Paso 2: Extender efe_q, preservar el frente de Pareto de TRATADOS y NO TRATADOS.

    while label_heap:
        # Se extrae la menor etiqueta en orden lexicográfico de cualquiera de los nodos.
        (efe_q, actual) = heapq.heappop(label_heap)
        # la etiqueta efe_q sale de NO TRATADAS[actual]
        Non_treated_labels[actual] = Non_treated_labels[actual].Delete_label(efe_q)


        # verificamos si efe_q ya está en el conjunto de etiquetas que fueron excluidas. De estarlo nos devolvemos y
        # extraemos (pop) una nueva etiqueta del minheap.
        if efe_q in Discard_sets[actual]:
            continue
        else:
            # Verificamos si la etiqueta extraida: efe_q del nodo actual, es dominada por alguna etiqueta en
            # Treated_labels[actual]

            updated_front, check, discarded_after_update = Treated_labels[actual].preserve_pareto(efe_q)
            # si check es false es porque new_label es dominado y no se inserta en el frente de pareto. En tal caso se
            # agrega a las etiquetas descartadas.
            if check == False:
                Discard_sets[actual].add(efe_q)
                continue
            else:
                # si la etiqueta fue insertada en el frente de pareto, actualizamos éste, y también las posibles
                # etiquetas descartadas tras la actualización del frente.
                Treated_labels[actual] = updated_front
                Discard_sets[actual].union(discarded_after_update)
                # Extender la etiqueta efe_q desde actual. Una extensión es factible si se cumple ventanas de tiempo.
                for vecino in G.succesors(actual):
                    if efe_q[0] + time[(actual, vecino)] <= ventana[vecino][1]:
                        label_time = max(ventana[vecino][0], efe_q[0] + time[(actual, vecino)])
                        label_cost = efe_q[1] + costo[(actual, vecino)]
                        new_label = (label_time, label_cost)

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
                                Non_treated_labels[vecino], insertado, U = Non_treated_labels[vecino].preserve_pareto(new_label)
                                if insertado == True:
                                    heapq.heappush(label_heap, (new_label, vecino))
                                else:
                                    pass


    P = dict({vertice: Treated_labels[vertice].to_list() for vertice in G.vertices})
    print('mire pa que vea', P)


    return P
