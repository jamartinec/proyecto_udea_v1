# coding: utf8

from sortedcontainers import SortedList
import numpy as np

class Pareto_Frontier():
    # viene de pareto_frontier_structure
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
            self._pareto_list = SortedList()  # Crear una lista ordenada con sorted list tiene complejidad O(n*log(n))
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
            for j in reversed(range(len(A) - index_y)):
                u = A.pop(j)
                discard_set.add(u)
            A.add(new_label)
            coor_y.add(new_label[1])
            indi_pareto_modified = True
        elif index_label == len(A):
            if coor_y[len(A) - index_label] >= new_label[1]:
                A.add(new_label)
                coor_y.add(new_label[1])
                indi_pareto_modified = True
        else:
            if coor_y[len(A) - index_label] > new_label[1] > coor_y[len(A) - index_label - 1]:
                A.add(new_label)
                coor_y.add(new_label[1])
                indi_pareto_modified = True
            elif new_label[1] < coor_y[len(A) - index_label - 1]:
                # cómo hacer esto más barato?
                for j in reversed(range(len(A) - index_label - 1, len(A) - index_y)):
                    u = A.pop(j)
                    discard_set.add(u)
                    coor_y.pop(j)
                A.add(new_label)
                coor_y.add(new_label[1])
                indi_pareto_modified = True

        self._pareto_list = A
        self._coor_y = coor_y

        return self, indi_pareto_modified, discard_set

    def check_dominance(self, new_label):

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
        elif A[index_label - 1][1] < new_label[1]:
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
        return all(coor_Y[i] >= coor_Y[i + 1] for i in range(len(coor_Y) - 1))

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
        # A.sort(key=lambda x: x[0])
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

class ParetoFrontier():
# viene de pareto frontier optimizado
    def __init__(self, vertex, lista=None):
        # El último elemento de sucesores va a tener como sucesor a infinito.

        self.sucesores_map = {0: np.inf}
        self.predecesores_map = {np.inf: 0, 0: None}
        self.contenedor = []
        self.sorted_list = SortedList(self.contenedor)
        self.pareto_map = {0: np.inf}
        ##############################################################################
        self.vertex = vertex  # PILAS, ACABO DE AGREGAR ESTE
        self.info_label = {} # A cada etiqueta apunta a una dupla con vértice previo y x_previo ¿hay que incicializar?
        self.lista_labels = []

        if lista != None:
            for label in lista:
                if label == (0,0):
                    trazador = (None, None)
                else:
                    trazador = None

                self.add(label, trazador)

    def show_pareto(self):
        return self.pareto_map

    def show_pareto2(self):
        return self.pareto_map, self.sucesores_map, self.predecesores_map

    #def to_list(self):
    #   return list(self.sorted_list)

    def list_frontlabels(self):
        ## PILAS, ESTO ES MUY INEFICIENTE Y SÓLO LO TENGO PARA HACER PRINTS, NOTE QUE SIEMPRE RECONSTRUYE
        #LA LISTA DESDE EL PRINCIPIO.
        self.lista_labels = []
        #print('en list_frontlabels sorted_list:', self.sorted_list )
        #print('en list_frontlabels lista labels',self.lista_labels)

        for x in self.sorted_list:
            #print('en list_frontlabels: x en sorted_list',x)
            self.lista_labels.append((x, self.pareto_map[x]))
        print('lista_labels',self.lista_labels)
        return self.lista_labels


    def x_in_pareto(self, x):
        return x in self.pareto_map


    def _xleft(self, x):

        if self.x_in_pareto(x):
            return x
        else:
            i = self.sorted_list.bisect(x)
            if (i == 0):
                return 0
            else:
                return self.sorted_list[i - 1]


    def _yleft(self, x):
        return self.pareto_map[self._xleft(x)]


    def check_dominance(self, label):
        x = label[0]
        y = label[1]
        return self._yleft(x) <= y

     # En la siguiente función está implícito  que las etiquetas se van adicionando a Pareto Frontier
     # una a una.
     #def add(self, label,  pure_pareto=True):
    def add(self, label, trazadorx=None, pure_pareto=True):
        indi_pareto_modified = False
        discard_set = set()
        x = label[0]
        y = label[1]
        x_left = self._xleft(x)

        # SI LABEL ES DOMINADO POR ALGUIEN EN PARETO
        if self.check_dominance(label):
        #if self.pareto_map[x_left] <= y:
            return self, indi_pareto_modified, discard_set


        if x_left != x:

            next_x = self.sucesores_map[x_left]
            self.sucesores_map[x] = next_x
            self.predecesores_map[next_x] = x

            self.sucesores_map[x_left] = x
            self.predecesores_map[x] = x_left

            self.contenedor.append(x)
            self.sorted_list.add(x)
        elif x not in self.sorted_list:
            self.contenedor.append(x)
            self.sorted_list.add(x)

        self.pareto_map[x] = y
        if trazadorx != None:
            self.info_label[x] = trazadorx

        #print('PILAS',(x,y))
        indi_pareto_modified = True

        sucesor = self.sucesores_map[x]
        #print('cuando x es:', x, 'sucesor es:',sucesor)

        if pure_pareto == False:

            while sucesor < np.inf:
                if self.pareto_map[sucesor] > y:
                    self.pareto_map[sucesor] = y
                else:
                    break
                sucesor = self.sucesores_map[sucesor]

        else:
            while sucesor < np.inf:
                #print('ENTRAMOS AL WHILE cuando x es:', x, 'sucesor es:', sucesor)
                # Pilas, cuando una etiqueta se elimina del frente, debemos borrar también la información
                # consignada en info_label
                if self.pareto_map[sucesor] > y:
                    discard_set.add((sucesor, self.pareto_map[sucesor]))
                    del self.pareto_map[sucesor]
                    ########################################
                    del self.info_label[sucesor]
                    ########################################
                    nextt_x = self.sucesores_map[sucesor]
                    self.sucesores_map[x] = nextt_x
                    self.predecesores_map[nextt_x] = x

                    del self.sucesores_map[sucesor]
                    del self.predecesores_map[sucesor]

                    self.contenedor.remove(sucesor)
                    self.sorted_list.remove(sucesor)

                else:
                    break
                sucesor = self.sucesores_map[x]
        return self, indi_pareto_modified, discard_set



    def Delete_label(self, label):
        print('Entramos a Delete_label')
        x = label[0]
        y = label[1]
        if self.x_in_pareto(x):
            print(x, 'está en pareto')
            del self.pareto_map[x]
            print('así queda pareto map después de borrar', x, self.pareto_map)
            ################################################################################
            del self.info_label[x] # puede haber problemas si en info_label no está x PILAS
            print('asi queda info_label después de borrar', x, self.info_label)
            ################################################################################
            predx = self.predecesores_map[x]
            sucx = self.sucesores_map[x]
            self.sucesores_map[predx] = sucx
            self.predecesores_map[sucx] = predx
            del self.sucesores_map[x]
            del self.predecesores_map[x]
            self.contenedor.remove(x)
            self.sorted_list.remove(x)
            print('esta es sorted_list después de borrar',x, self.sorted_list)
            return self
        else:
            #raise ValueError()
            print('No está en Pareto y retorno el mismo ParetoFrontier')

            return self


    def label_track(self, x):
        return self.info_label[x]
