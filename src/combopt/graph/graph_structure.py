# coding: utf8

from copy import deepcopy

class Grafo_consumos():
    """It contains the structure of a graph initialized from its vertices and edges..

    Consult the neighbors of a vertex operates in time O(1). We can add additional information to the edges. The names
    of the graph's vertices must be integers or strings.

    Attributes:
        vertices: A list with the vertices of the graph.
        aristas: A list with the edges as pairs (u,v).
        directed: A boolean indicating if the graph is directed or not.
        num_vertices: An integer that corresponds to the number of vertices in the graph.

    Methods:

    """

    def __init__(self, vertices, aristas, directed=False, recursos_nodos=None, recursos_arcos=None ,restricciones_nodos=None,costos_arcos=None):
        """Inits Grafo class"""

        self.vertices = vertices

        self.num_vertices = len(self.vertices)

        self.directed = directed

        self.aristas = set(aristas)

        self._vecinos = dict()
        # Vecinos de cada vertice del grafo (solo para grafos no dirigidos)

        self._succesors = dict()
        # Sucesores de cada vertice (solo para grafos dirigidos)

        self._predecessors = dict()
        # Predecesores de cada vertice (solo para grafos dirigidos)

        self._info_aristas = dict()
        # Informacion adicional de las aristas del grafo

        # Inicializacion de la estructura de datos _vecinos
        if self.directed:
            self._succesors = {v: set() for v in vertices}
            self._predecessors = {v: set() for v in vertices}
            for v, w in aristas:
                self._succesors[v].add(w)
                self._predecessors[w].add(v)
        else:
            self._vecinos = {v: set() for v in vertices}
            for v, w in aristas:
                self._vecinos[v].add(w)
                self._vecinos[w].add(v)

        # Pilas: pensar cómo garantizar qué haya coherencia entre recursos nodos,
        # recursos_arcos y ventanas_nodos!!

        # Inicializacion de la estructura de datos _info_aristas
        self._info_aristas = {(v, w): dict() for v, w in aristas}
        if not self.directed:
            self._info_aristas.update({(w, v): dict() for v, w in aristas})

        # Inicialización de la estructura de datos costos_arcos
        if self.directed:
            self._costos_arcos = costos_arcos
            # si un arco especificado en costos_arcos no es arista (arco) del grafo
            # se elimina
            for arco in self._costos_arcos.keys():
                if arco not in self.aristas:
                    del self._costos_arcos[arco]
            # si a una arista (arco) del grafo no se le especificó su costo,
            # entonces se agrega como cero. (todo arco del grafo debe tener costo)
            for arco in self.aristas:
                if arco not in self._costos_arcos.keys():
                    self._costos_arcos[arco] = 0

        #Recursos
        self.recursos = list(set(recursos_nodos.keys()).union(set(recursos_arcos.keys())) )


        # inicialización de la estructura de datos nodo-recursos
        self._dictio_nodo_recursos = dict()
        if directed and recursos_nodos is not None:
            for vertice in self.vertices:
                self._dictio_nodo_recursos[vertice]=dict()
                for recurso_str in recursos_nodos.keys():
                    self._dictio_nodo_recursos[vertice][recurso_str]=recursos_nodos[recurso_str][vertice]

        # inicialización de la estructura de datos arco-recursos
        self._dictio_arco_recursos = dict()
        if directed and recursos_arcos is not None:
            for arco in self.aristas:
                self._dictio_arco_recursos[arco]=dict()
                for recurso_str in recursos_arcos.keys():
                    self._dictio_arco_recursos[arco][recurso_str]=recursos_arcos[recurso_str][arco]

        # inicialización de la estructura de datos nodo-ventanas
        self._dictio_nodo_ventanas = dict()
        if directed and restricciones_nodos is not None:
            for vertice in self.vertices:
                self._dictio_nodo_ventanas[vertice] = dict()
                for recurso_str in restricciones_nodos.keys():
                    self._dictio_nodo_ventanas[vertice][recurso_str] = restricciones_nodos[recurso_str][vertice]

        #inicializar una lista que contenga los nombres de los recursos considerados
        # en determinada instancia de un Grafo_consumos
        self._recusos_names =list()
        if recursos_nodos is not None:
            self._recursos_names= list(recursos_nodos.keys())



    def vecinos(self, v):
        """ Returns the neighbors of a certain vertex

        Args:
            v: An integer corresponding to certain vertex.
        Returns:
            A list containing the neighbors of vertex v in the undirected graph.
        """

        return self._vecinos[v]

    def succesors(self, v):
        """

        Args:
            v: An integer corresponding to certain vertex.

        Returns:
            A list containing the neighbors of vertex v in the directed graph.

        """
        return self._succesors[v]

    def predecessors(self, v):
        """

        Args:
            v: An integer corresponding to certain vertex.

        Returns:
            A list containing the predecessors of vertex v in the directed graph.


        """
        return self._predecessors[v]

    def remove_edge(self, e):
        """

        Args:
            e: An edge/arc (pair) of the graph depending on whether it is directed or not

        Returns:
            The original  graph without edge/arc e.

        """
        if self.directed:
            self.aristas.remove(e)
            del self._info_aristas[e]
            v, w = e
            self._succesors[v].remove(w)
            self._predecessors[w].remove(v)
        else:
            raise NotImplementedError

    # Agregada para algoritmos de flujo
    def add_edge(self, e):
        """

        Args:
            e: Certain arc (the graph must be directed)

        Returns:


        """
        if self.directed:
            self.aristas.add(e)
            self._info_aristas.update({e: dict()})
            u, v = e
            self._succesors[u].add(v)
            self._predecessors[v].add(u)
        else:
            raise NotImplementedError

    def add_info(self, e, key, val):
        """

        Args:
            e: certain edge of the graph.
            key: A characteristic to be included in info dictionary.
            val: The value of the new characteristic in the info dictionary.

        Returns:


        """
        v, w = e
        if (v, w) not in self._info_aristas:
            raise ValueError('Arista {} no existente'.format(e))
        self._info_aristas[(v, w)][key] = val
        if not self.directed:
            self._info_aristas[(w, v)][key] = val

    def get_info(self, e, key):
        """

        Args:
            e: A certain edge in the graph.
            key: A characteristic consigned in the info dictionary.

        Returns:
            The value associated with the characteristic 'key' in the info dictionary.

        """
        v, w = e
        if (v, w) not in self._info_aristas:
            raise ValueError('Arista {} no existente'.format(e))
        return self._info_aristas[(v, w)][key]

    def delta_out(self,U):
        """

        Args:
            U: A set of vertices.

        Returns:
            The set with edges (u,w) where u in U but w not in U
        """

        if self.directed:
            delta = set()
            for u in U:
                for w in self._succesors[u]:
                    if w not in U:
                        delta.add((u, w))
            return delta
        else:
            raise NotImplementedError

    def nodo_recursos(self):
        return self._dictio_nodo_recursos

    def recurso_nodo(self,nodo):
        return self._dictio_nodo_recursos[nodo]

    def nodo_ventanas(self):
        return self._dictio_nodo_ventanas

    def arco_recursos(self):
        return self._dictio_arco_recursos

    def recurso_arco(self,arco):
        return self._dictio_arco_recursos[arco]

    def nombres_recursos(self):
        return self._recursos_names

    def costos_arcos(self,arco):
        return self._costos_arcos[arco]



    def __str__(self):
        return str(self._vecinos)

    def __copy__(self):
        return deepcopy(self)

class Grafo():
    """It contains the structure of a graph initialized from its vertices and edges..

    Consult the neighbors of a vertex operates in time O(1). We can add additional information to the edges. The names
    of the graph's vertices must be integers or strings.

    Attributes:
        vertices: A list with the vertices of the graph.
        aristas: A list with the edges as pairs (u,v).
        directed: A boolean indicating if the graph is directed or not.
        num_vertices: An integer that corresponds to the number of vertices in the graph.

    Methods:

    """

    def __init__(self, vertices, aristas, directed=False):
        """Inits Grafo class"""

        self.vertices = vertices

        self.num_vertices = len(self.vertices)

        self.directed = directed

        self.aristas = set(aristas)

        self._vecinos = dict()
        # Vecinos de cada vertice del grafo (solo para grafos no dirigidos)

        self._succesors = dict()
        # Sucesores de cada vertice (solo para grafos dirigidos)

        self._predecessors = dict()
        # Predecesores de cada vertice (solo para grafos dirigidos)

        self._info_aristas = dict()
        # Informacion adicional de las aristas del grafo

        # Inicializacion de la estructura de datos _vecinos
        if self.directed:
            self._succesors = {v: set() for v in vertices}
            self._predecessors = {v: set() for v in vertices}
            for v, w in aristas:
                self._succesors[v].add(w)
                self._predecessors[w].add(v)
        else:
            self._vecinos = {v: set() for v in vertices}
            for v, w in aristas:
                self._vecinos[v].add(w)
                self._vecinos[w].add(v)

        # Inicializacion de la estructura de datos _info_aristas
        self._info_aristas = {(v, w): dict() for v, w in aristas}
        if not self.directed:
            self._info_aristas.update({(w, v): dict() for v, w in aristas})

    def vecinos(self, v):
        """ Returns the neighbors of a certain vertex

        Args:
            v: An integer corresponding to certain vertex.
        Returns:
            A list containing the neighbors of vertex v in the undirected graph.
        """

        return self._vecinos[v]

    def succesors(self, v):
        """

        Args:
            v: An integer corresponding to certain vertex.

        Returns:
            A list containing the neighbors of vertex v in the directed graph.

        """
        return self._succesors[v]

    def predecessors(self, v):
        """

        Args:
            v: An integer corresponding to certain vertex.

        Returns:
            A list containing the predecessors of vertex v in the directed graph.


        """
        return self._predecessors[v]

    def remove_edge(self, e):
        """

        Args:
            e: An edge/arc (pair) of the graph depending on whether it is directed or not

        Returns:
            The original  graph without edge/arc e.

        """
        if self.directed:
            self.aristas.remove(e)
            del self._info_aristas[e]
            v, w = e
            self._succesors[v].remove(w)
            self._predecessors[w].remove(v)
        else:
            raise NotImplementedError

    # Agregada para algoritmos de flujo
    def add_edge(self, e):
        """

        Args:
            e: Certain arc (the graph must be directed)

        Returns:


        """
        if self.directed:
            self.aristas.add(e)
            self._info_aristas.update({e: dict()})
            u, v = e
            self._succesors[u].add(v)
            self._predecessors[v].add(u)
        else:
            raise NotImplementedError

    def add_info(self, e, key, val):
        """

        Args:
            e: certain edge of the graph.
            key: A characteristic to be included in info dictionary.
            val: The value of the new characteristic in the info dictionary.

        Returns:


        """
        v, w = e
        if (v, w) not in self._info_aristas:
            raise ValueError('Arista {} no existente'.format(e))
        self._info_aristas[(v, w)][key] = val
        if not self.directed:
            self._info_aristas[(w, v)][key] = val

    def get_info(self, e, key):
        """

        Args:
            e: A certain edge in the graph.
            key: A characteristic consigned in the info dictionary.

        Returns:
            The value associated with the characteristic 'key' in the info dictionary.

        """
        v, w = e
        if (v, w) not in self._info_aristas:
            raise ValueError('Arista {} no existente'.format(e))
        return self._info_aristas[(v, w)][key]

    def delta_out(self,U):
        """

        Args:
            U: A set of vertices.

        Returns:
            The set with edges (u,w) where u in U but w not in U
        """

        if self.directed:
            delta = set()
            for u in U:
                for w in self._succesors[u]:
                    if w not in U:
                        delta.add((u, w))
            return delta
        else:
            raise NotImplementedError


    def __str__(self):
        return str(self._vecinos)

    def __copy__(self):
        return deepcopy(self)


class Node():
    """ Defines the structure of a node in some graph.

        Attributes:
            name: The name of the node.
    """

    def __init__(self, name):

        self.name = name
        self._successors = set()


    def add_successor(self, node):
        """

        Args:
            node: A node in the graph.

        Returns:
            The list of successor updated with node.

        """
        self._successors.add(node)

    def get_successors(self):
        """

        Returns:
            The list with successors.

        """
        return self._successors


class LinkedNode():
    """ Define an object with the structure of a linked node.

        Attributes:
            name: Name of the instance.
            successor: points to the successor.

    """

    def __init__(self, name):
        self.name = name
        self.successor = None

    def linkto(self, node):
        """

        Args:
            node: A node that will be linked to the original node.

        Returns:

        """
        self.successor = node

    def tolist(self):
        """

        Returns: A list of nodes where one node is the father of the next node.

        """
        lista = [self.name]
        current_node = self
        while current_node.successor is not None:
            current_node = current_node.successor
            if current_node == self:
                break
            lista.append(current_node.name)
        return lista

