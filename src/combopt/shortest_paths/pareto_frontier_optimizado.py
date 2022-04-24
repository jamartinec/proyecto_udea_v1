# coding: utf8

from sortedcontainers import SortedList
from copy import copy, deepcopy
import numpy as np
import pickle as pkl
import os


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



    def __init__(self, nodo_rel: object, G: object, nombre_label: str):

        #self.ruta_absoluta = r'C:\Users\Usuario\PycharmProjects\proyecto_maestria_v1\experiments\solomon\estados_pd'

        self.ruta_absoluta = r'D:\UdeA\estados_pd'

        self._grafo_consumo_referencia = G

        # nodo relacionado
        self.nodo_rel = nodo_rel

        self.nombre_label = nombre_label

        # lista de nodos con la cual se inicializa la etiqueta
        # (debería ser la lista de nodos del grafo G)

        self.nodos = G.vertices

        self.lista_recursos = G.recursos
        self.label_recursos= {recurso: 0 for recurso in self.lista_recursos}

        # Cuando se genera una etiqueta el valor de consumo de recursos acumulados debe sumar los
        # correspondientes al nodo relacionado con la etiqueta (en el cual se inicia)


        for recurso  in self.lista_recursos:
            self.label_recursos[recurso] += G.recurso_nodo(self.nodo_rel)[recurso]

        self.label_visitas = {nodo: 0 for nodo in self.nodos}
        # el nodo relacionado con la etiqueta debe estar marcado como visitado
        self.label_visitas[self.nodo_rel] = 1

        self.recursos_sucesores = dict()
        self.find_unreachable_successors()

        # Nodos visitados, no tiene en cuenta los marcados como 1 por inalcanzables
        self.conteo = 1
        self.costo_acumulado = 0

        self.label = {**self.label_recursos, **self.label_visitas}
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
        self.nodo_rel = nodo

    def update_label_name(self, new_name):
        self.nombre_label = new_name

    def update_label_recursos(self, valores_recursos:dict):
        # Deberíamos garantizar que el recurso que intento actualizar sea en
        # efecto un recurso de los especificados en la creación de la etiqueta (self.lista_recursos)?

        for (recurso, valor) in valores_recursos.items():
            self.label_recursos[recurso] = valor
            self.label[recurso] = valor

    def update_label_visitas(self, nodos_list: list):
        for nodo in nodos_list:
            if nodo not in self.visited_nodes():
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

    def verificar_recursos(self, sucesor):
        arco = (self.nodo_rel, sucesor)
        nodo_recursos = self._grafo_consumo_referencia.nodo_recursos()
        arco_recursos = self._grafo_consumo_referencia.arco_recursos()
        nodo_ventanas = self._grafo_consumo_referencia.nodo_ventanas()

        indicador = True
        nuevos_valores = dict()
        for recurso in self.label_recursos.keys():
            cantidad = self.label_recursos[recurso] + nodo_recursos[sucesor][recurso] + arco_recursos[arco][recurso]
            nuevos_valores[recurso] = cantidad

            # Pilas, qué pasa si la cantidad es menor que la ventana izquierda

            if cantidad > nodo_ventanas[sucesor][recurso][1]:
                indicador = False
                break

            if cantidad < nodo_ventanas[sucesor][recurso][0]:
                nuevos_valores[recurso] = nodo_ventanas[sucesor][recurso][0]

        return indicador, nuevos_valores

    def extend_label(self, nodo, nuevos_valores, new_name):

        #new_etiqueta = deepcopy(self)
        #new_etiqueta = copy(self)

        lista_estados_guardados = os.listdir(self.ruta_absoluta)
        #lista_estados_guardados = [f.name for f in os.scandir(self.ruta_absoluta) if f.is_file()]
        #print(lista_estados_guardados)

        ruta = self.ruta_absoluta + '/' + self.nombre_label
        if self.nombre_label not in lista_estados_guardados:
            with open(ruta, 'wb') as file_obj:
                pkl.dump(self, file_obj)

        with open(ruta, 'rb') as read_file:
            new_etiqueta = pkl.load(read_file)

        new_etiqueta.update_label_name(new_name)
        new_etiqueta.update_nodo_rel(nodo)
        new_etiqueta.update_label_visitas([nodo])

        new_etiqueta.update_label_recursos(nuevos_valores)
        # update label ????
        new_etiqueta.update_cost(self._grafo_consumo_referencia.costos_arcos((self.nodo_rel, nodo)))

        # Recien se ha extendido una etiqueta, es necesario explorar los vecinos, tomar aquellos
        # que previamente no han sido visitados en el camino parcial, o que no han sido marcados
        # como inalcanzables, verificar si desde el nuevo nodo_rel son inalcanzables, y si no,
        # actualizar el diccionario de valores.

        new_etiqueta.find_unreachable_successors()

        return new_etiqueta

    def find_unreachable_successors(self):
        for sucesor in self._grafo_consumo_referencia.succesors(self.nodo_rel):
            # Cuando la presente etiqueta se ha obtenido mediante la extensión de una etiqueta
            # ya existente, es posible que algún sucesor del nodo_rel actual ya hubiese sido visitado
            # o marcado como inalcanzable para la etiqueta predecesora
            # (y el camino parcial correspondiente) por tanto se quiere evitar volver a corroborarlo.

            # Notar que no debemos preocuparnos por actualizar el diccionario de recursos_sucesores
            # para sucesores del nodo_rel que ya han sido previamente marcados como inalcanzables.
            if self.label_visitas[sucesor] == 1:
                pass
            else:
                indicador, nuevos_valores = self.verificar_recursos(sucesor=sucesor)
                if indicador == False:
                    self.update_label_visitas([sucesor])
                else:
                    self.recursos_sucesores[sucesor] = nuevos_valores

    def extend_function_feillet(self, nodo, new_name):
        if nodo not in self._grafo_consumo_referencia.vertices:
            raise ValueError(f"extended function method expected a node in " \
                             f"reference graph, got{nodo}")

        if self.label_visitas[nodo] == 1:
            raise ValueError('El nodo al cual se desea extender no puede haber sido visitado o'
                             'marcado como inalcanzable')

        nuevos_valores = self.recursos_sucesores[nodo]
        new_etiqueta = self.extend_label(nodo, nuevos_valores, new_name)
        return new_etiqueta
