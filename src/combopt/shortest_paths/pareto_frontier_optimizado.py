# coding: utf8

from sortedcontainers import SortedList
import numpy as np


class ParetoFrontier():

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





class Label_feillet2004():
    '''
    clase para representar etiquetas en el algoritmo de feillet2004
    '''
    def __init__(self, nodo_rel: object, name_recursos: list, nodos: list):
        # supongamos que pasamos una lista name_recursos con los nombres de
        # los recursos.

        # lista de nodos con la cual se inicializa la etiqueta (debería ser la lista de nodos del grafo G)
        self.nodos = nodos

        # es necessario la siguiente línea?
        self.lista_recursos = name_recursos

        self.label_recursos= {nombre: 0 for nombre in name_recursos}
        for nombre in name_recursos:
            self.label_recursos[nombre] +=


        self.label_visitas = {nodo: 0 for nodo in self.nodos}
        # el nodo relacionado con la etiqueta debe estar marcado como visitado
        self.label_visitas[nodo_rel]=1

        self.conteo = 0

        self.costo_acumulado = 0

        #self.label = self.label_recursos.update(self.label_visitas)
        self.label = {**self.label_recursos, **self.label_visitas}

        # nodo relacionado
        self.nodo_rel = nodo_rel

        self.longitud = len(self.label) + 2



    # considerar un método que permita imprimir las etiquetas en
    # determinado orden.
    def visited_nodes(self):
        visited = {x for x in self.label_visitas.keys() if self.label_visitas[x] == 1}
        return visited

    def is_visited_node(self,nodo):
        try:
            return self.label_visitas[nodo]
        except:
            print('no es un nodo en la lista de inicialización de la etiqueta')

    def update_nodo_rel(self, nodo):
        self.nodo_rel=nodo

    def update_label_recursos(self, valores_recursos:dict):
        # Deberíamos garantizar que el recurso que intento actualizar sea en
        # efecto un recurso de los especificados en la creación de la etiqueta (self.lista_recursos)?

        for (recurso, valor) in valores_recursos.items():
            self.label_recursos[recurso] = valor
            self.label[recurso] = valor

    def update_label_visitas(self, nodos_list:list):
        for nodo in nodos_list:
            self.label_visitas[nodo] = 1
            self.label[nodo] = 1
            self.conteo += 1


    def update_recursos_sucesores(self,dict_sucesores:dict):
        # pilas, no todos los sucesores del nodo de referencia (para la etiqueta) que aparecen en la
        # estructura de G deben venir en dict_sucesores, pues allí sólo vienen los que se verificó que pueden
        # ser extendidos.
        self.dict_sucesores = dict_sucesores

    def update_cost(self,costo_arco):
        self.costo_acumulado += costo_arco







