# coding: utf8


import pickle as pkl
import os


def visited_nodes(etiqueta_atributos: dict):
    visited = {x for x in etiqueta_atributos['label_visitas'].keys() if etiqueta_atributos['label_visitas'][x] == 1}
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

def update_label_visitas(nodos_list: list, etiqueta_atributos: dict):
    for nodo in nodos_list:
        if nodo not in visited_nodes(etiqueta_atributos):
            etiqueta_atributos['label_visitas'][nodo] = 1
            etiqueta_atributos['label'][nodo] = 1
            etiqueta_atributos['conteo'] += 1
    return etiqueta_atributos

def verificar_recursos(G, sucesor, etiqueta_atributos):
    arco = (etiqueta_atributos['nodo_rel'], sucesor)
    nodo_recursos = G.nodo_recursos()
    arco_recursos = G.arco_recursos()
    nodo_ventanas = G.nodo_ventanas()

    indicador = True
    nuevos_valores = dict()
    for recurso in etiqueta_atributos['label_recursos'].keys():
        cantidad = etiqueta_atributos['label_recursos'][recurso] + nodo_recursos[sucesor][recurso] + arco_recursos[arco][recurso]
        nuevos_valores[recurso] = cantidad

        # Pilas, qué pasa si la cantidad es menor que la ventana izquierda

        if cantidad > nodo_ventanas[sucesor][recurso][1]:
            indicador = False
            break

        if cantidad < nodo_ventanas[sucesor][recurso][0]:
            nuevos_valores[recurso] = nodo_ventanas[sucesor][recurso][0]

    return indicador, nuevos_valores


def find_unreachable_successors(etiqueta_atributos, G):
    for sucesor in G.succesors(etiqueta_atributos['nodo_rel']):
        # Cuando la presente etiqueta se ha obtenido mediante la extensión de una etiqueta
        # ya existente, es posible que algún sucesor del nodo_rel actual ya hubiese sido visitado
        # o marcado como inalcanzable para la etiqueta predecesora
        # (y el camino parcial correspondiente) por tanto se quiere evitar volver a corroborarlo.

        # Notar que no debemos preocuparnos por actualizar el diccionario de recursos_sucesores
        # para sucesores del nodo_rel que ya han sido previamente marcados como inalcanzables.
        if etiqueta_atributos['label_visitas'][sucesor] == 1:
            pass
        else:
            indicador, nuevos_valores = verificar_recursos(sucesor=sucesor)
            if indicador == False:
                update_label_visitas([sucesor])
            else:
                etiqueta_atributos['recursos_sucesores'][sucesor] = nuevos_valores


def inicializar_etiqueta(nodo_rel: object, G: object, nombre_label: str ):

    etiqueta_atributos = {'nodo_rel': nodo_rel,
                          'nombre_label': nombre_label}

    ruta_absoluta = r'D:\UdeA\estados_pd'
    label_recursos = {recurso: 0 for recurso in G.recursos}

    # Cuando se genera una etiqueta el valor de consumo de recursos acumulados debe sumar los
    # correspondientes al nodo relacionado con la etiqueta (en el cual se inicia)

    for recurso in G.recursos:
        label_recursos[recurso] += G.recurso_nodo(nodo_rel)[recurso]

    etiqueta_atributos['label_recursos'] = label_recursos

    label_visitas = {nodo: 0 for nodo in G.vertices}
    # el nodo relacionado con la etiqueta debe estar marcado como visitado
    label_visitas[nodo_rel] = 1

    etiqueta_atributos['label_visitas'] = label_visitas

    #recursos_sucesores = dict()

    etiqueta_atributos['recursos_sucesores'] = dict()
    etiqueta_atributos = find_unreachable_successors(etiqueta_atributos, G)

    # Nodos visitados, no tiene en cuenta los marcados como 1 por inalcanzables
    etiqueta_atributos['conteo'] = 1
    etiqueta_atributos['costo_acumulado'] = 0

    etiqueta_atributos['label'] = {**label_recursos, **label_visitas}
    etiqueta_atributos['longitud'] = len(etiqueta_atributos['label']) + 2


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