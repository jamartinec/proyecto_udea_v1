# coding: utf8
from copy import deepcopy

import bisect
from sortedcontainers import SortedList

class Pareto_Frontier():
    """ It contains the structure of Pareto Frontier of labels.

    It contains the structure of a Pareto Frontier of labels in the context of
    Desrochers et al. (1988) and Feillet et al. (2004) algorithms
    for the Shortest Path Problem with Resource Constraint (SPPRC) and
    the Elementary SPPRC (ESPPRC).

    Attributes:
        vertex:
    Methods:
        corresponding_path:
    """


    ## ¿para qué necesitamos que dependa del vertex?

    def __init__(self, vertex, lista=None):
        """Inits Label class

        Args:
            vertex: Int or str. The vertex to which the labels contained on the Pareto Front belongs.

        """


        self.vertex = vertex
        if lista == None:
            self._pareto_list = SortedList() # Crear una lista ordenada con sorted list tiene complejidad O(n*log(n))
            self._coor_y = SortedList([], key=lambda x: -x)
        else:
            self._original_list = lista
            self._pareto_list = SortedList(lista)
            self._coor_y = SortedList([self._pareto_list[i][1] for i in range(len(self._pareto_list))])
            # Crear una SortedList a partir de una list tiene complejidad O(n*log(n))




    def pareto_list(self):
        """ Returns the list with all label in the pareto frontier.

        Returns:
            A sorted list containing all the labels in the pareto frontier.

        """
        return self._pareto_list


    def preserve_pareto(self, new_label):

        indi_pareto_modified = False
        A = self._pareto_list
        coor_y = self._coor_y
        # bisect tiene runtime complexity O(log(n)).
        index_label = A.bisect_left(new_label)
        index_y = coor_y.bisect_right(new_label[1])
        discard_set = set()

        # Adicionar un elemento al SortedList tiene complejidad O(log(n))
        # Pop del SortedList tiene complejidad O(log(n))
        if index_label == 0:
            # cómo hacer esto más barato?
            for j in reversed(range(len(A)-index_y)):
                u = A.pop(j)
                discard_set.add(u)
            A.add(new_label)
            coor_y.add(new_label[1])
            indi_pareto_modified = True
        elif index_label == len(A):
            if coor_y[len(A)-index_label] >= new_label[1]:
                A.add(new_label)
                coor_y.add(new_label[1])
                indi_pareto_modified = True
        else:
            if coor_y[len(A)-index_label] > new_label[1] > coor_y[len(A)-index_label-1]:
                A.add(new_label)
                coor_y.add(new_label[1])
                indi_pareto_modified = True
            elif new_label[1] < coor_y[len(A)-index_label-1]:
                # cómo hacer esto más barato?
                for j in reversed(range(len(A)-index_label-1, len(A)-index_y)):
                    u = A.pop(j)
                    discard_set.add(u)
                    coor_y.pop(j)
                A.add(new_label)
                coor_y.add(new_label[1])
                indi_pareto_modified = True

        self._pareto_list = A
        self._coor_y = coor_y

        return self, indi_pareto_modified, discard_set

    def check_dominance(self,new_label):
        
        """ Checks if any label in the list A dominates the new_label. (Esta función es para mirar
        dominancia sin actualizar el frente de pareto, a diferencia de preserve pareto que verifica y
        actualiza de ser necesario.

        Args:
            new_label: A new label/pair

        Returns:
            indicador: A boolean that is True if some label in A dominates new_label
        """

        indi_dominance = False
        A = self._pareto_list
        # bisect tiene runtime complexity O(log(n)).
        index_label = A.bisect_left(new_label)
        if index_label == 0:
            pass
        elif A[index_label-1][1] < new_label[1]:
            indi_dominance = True
        return indi_dominance

    def Delete_label(self, old_label):
        # dicard es O(log(n))
        self._pareto_list.discard(old_label)
        self._coor_y.discard(old_label[1])
        return self


    def is_pareto_frontier(self):
        A = self._pareto_list
        coor_Y = [self._pareto_list[i][1] for i in range(len(self._pareto_list))]
        return all(coor_Y[i] >= coor_Y[i+1] for i in range(len(coor_Y) -1))

    def find_pareto_set(self):
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
        # posterior cuesta O(n). La complejidad es  O(n log(n)) + O(n)
        # o sea O(nlog(n)).
        A = self._pareto_list
        #A.sort(key=lambda x: x[0])
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
        self._pareto_list = SortedList(pareto)
        return pareto

    def to_list(self):
        return list(self._pareto_list)

# class Label():
#     """ It contains the structure of a label for SPPRC and ESPPRC algorithms.
#
#     It contains the structure of a label in the context of
#     Desrochers et al. (1988) and Feillet et al. (2004) algorithms
#     for the Shortest Path Problem with Resource Constraint (SPPRC) and
#     the Elementary SPPRC (ESPPRC).
#
#     Attributes:
#         current: Int/str, the vertex to which the label belongs.
#         predecessor: Instance of Label class. The predecessor label.
#         time_label: Time stamp in this label.
#         cost_label: Cost stamp in this label.
#         label: Duple (time_label, cost_label)
#     Methods:
#         corresponding_path: Returns a list with the source-current path that originated the present label.
#     """
#
#     def __init__(self, current_vertex, predecessor_label,time_label, cost_label):
#         """Inits Label class
#
#         Args:
#             current_vertex: Int or str. The vertex to which this label belongs.
#             predecessor_label: An instance of Label class. The label that was extended to form the presented label.
#             time_label: float. The time in the current vertex, i.e. "the first entry of the tuple".
#             cost_label: float. The cost in the current vertex, i.e. "the second entry of the tuple".
#         """
#
#         self.current = current_vertex
#         self.predecessor = predecessor_label
#         self.time_label = time_label
#         self.cost_label = cost_label
#         self.label = (time_label, cost_label)
#
#         self._path = list()
#
#     def corresponding_path(self):
#         self._actual = self
#         self._path.append(self._actual.current)
#         self._prede = self._actual.predecessor
#         # la única etiqueta con predecesor None será la etiqueta (0,0) en el vértice source s.
#         while self._prede != None:
#             self._actual = self._prede
#             self._path.append(self._actual.current)
#             self._prede = self._actual.predecessor
#         return self._path



