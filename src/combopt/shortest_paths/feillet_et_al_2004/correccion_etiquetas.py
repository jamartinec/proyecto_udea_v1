# coding: utf8
from cProfile import label
from calendar import c
import heapq
# import pickle as pkl
from src.combopt.graph import Grafo,Grafo_consumos
#from src.combopt.shortest_paths.pareto_frontier_structure import Pareto_Frontier
from src.combopt.shortest_paths.pareto_frontier_optimizado import ParetoFrontier, Label_feillet2004
from sortedcontainers import SortedList
from collections import deque




def comparacion_etiqueta_par(etiquetaA: label, etiquetaB: label):
    # Comparar etiquetaA con etiquetaB.
    # Número de entradas de una etiqueta, contando indicadores, recursos, costo y número de visitas:
    # EtiquetaA: label_new
    # EtiquetaB: label old

    if etiquetaA.longitud != etiquetaB.longitud or etiquetaA.nodo_rel != etiquetaB.nodo_rel:
        raise ValueError('Las etiquetas no están asociadas al mismo nodo o tienen longitud'
                         'distinta')

    num_entradas = etiquetaA.longitud

    A_domina, B_domina, AB_igual = list(), list(), list()

    if etiquetaA.costo_acumulado < etiquetaB.costo_acumulado:
        # B no puede dominar a A, nos preguntamos si A domina a B:

        if etiquetaA.conteo <= etiquetaB.conteo:

            for visita in etiquetaA.label_visitas.keys():
                if etiquetaA.label_visitas[visita] <= etiquetaB.label_visitas[visita]:
                    A_domina.append(visita)

            # si longitud longitud de A domina es igual al número de nodos, entonces A restringido a las
            # etiquetas de visitas domina a la correspondiente restricción de B, y podemos continuar verificando
            # si A domina a B, mirando ahora los recursos:

            if len(A_domina) == len(etiquetaA.label_visitas):

                for recurso in etiquetaA.label_recursos.keys():
                    if etiquetaA.label_recursos[recurso] <= etiquetaB.label_recursos[recurso]:
                        A_domina.append(recurso)
                if len(A_domina) == len(etiquetaA.label_visitas) + len(etiquetaA.label_recursos):
                    # print('PARECE QUE A DOMINA A B')
                    # print('label_new domina a label_old')

                    return 1

            else:
                # En este caso concluimos que A no domina a B, pues hay al menos una etiqueta de
                # visita de B que es menor que la correspondiente etiqueta de A.
                # print('A NO DOMINA A B Y B NO DOMINA A A')
                # print('ninguno entre labelnew y labelold domina')

                return 0

        elif etiquetaA.conteo > etiquetaB.conteo:
            # print('A NO DOMINA A B Y B NO DOMINA A A')
            # print('ninguno entre labelnew y labelold domina')

            return 0

    elif etiquetaB.costo_acumulado < etiquetaA.costo_acumulado:
        # A no puede dominar a B, nos preguntamos si B domina a A:

        if etiquetaB.conteo <= etiquetaA.conteo:

            for visita in etiquetaB.label_visitas.keys():
                if etiquetaB.label_visitas[visita] <= etiquetaA.label_visitas[visita]:
                    B_domina.append(visita)

            # si longitud de B_domina es igual al número de nodos, entonces B restringido a las
            # etiquetas de visitas domina a la correspondiente restricción de A, y podemos continuar verificando
            # si B domina a A, mirando ahora los recursos:

            if len(B_domina) == len(etiquetaB.label_visitas):

                for recurso in etiquetaB.label_recursos.keys():
                    if etiquetaB.label_recursos[recurso] <= etiquetaA.label_recursos[recurso]:
                        B_domina.append(recurso)
                if len(B_domina) == len(etiquetaB.label_visitas) + len(etiquetaB.label_recursos):
                    # print('PARECE QUE B DOMINA A A')
                    # print('label old domina a label new')
                    return -1

            else:
                # En este caso concluimos que B no domina a A, pues hay al menos una etiqueta de
                # visita de A que es menor que la correspondiente etiqueta de B.
                # print('B NO DOMINA A A Y A NO DOMINA A B')
                # print('ninguno entre labelnew y labelold domina')
                return 0


        elif etiquetaB.conteo > etiquetaA.conteo:
            # print('A NO DOMINA A B Y B NO DOMINA A A')
            # print('ninguno entre labelnew y labelold domina')
            return 0

    else:
        # los costos acumulados de A y B son iguales
        if etiquetaA.conteo < etiquetaB.conteo:
            # nos preguntamos si A domina a B

            for visita in etiquetaA.label_visitas.keys():
                if etiquetaA.label_visitas[visita] <= etiquetaB.label_visitas[visita]:
                    A_domina.append(visita)

            # si longitud longitud de A domina es igual al número de nodos, entonces A restringido a las
            # etiquetas de visitas domina a la correspondiente restricción de B, y podemos continuar verificando
            # si A domina a B, mirando ahora los recursos:

            if len(A_domina) == len(etiquetaA.label_visitas):

                for recurso in etiquetaA.label_recursos.keys():
                    if etiquetaA.label_recursos[recurso] <= etiquetaB.label_recursos[recurso]:
                        A_domina.append(recurso)
                if len(A_domina) == len(etiquetaA.label_visitas) + len(etiquetaA.label_recursos):
                    # print('PARECE QUE A DOMINA A B')
                    # print('label_new domina a label_old')

                    return 1
            else:
                # En este caso concluimos que A no domina a B, pues hay al menos una etiqueta de
                # visita de B que es menor que la correspondiente etiqueta de A.
                # print('A NO DOMINA A B Y B NO DOMINA A A')
                # print('ninguno entre labelnew y labelold domina')
                return 0

        elif etiquetaB.conteo < etiquetaA.conteo:
            # nos preguntamos si B domina a A
            for visita in etiquetaB.label_visitas.keys():
                if etiquetaB.label_visitas[visita] <= etiquetaA.label_visitas[visita]:
                    B_domina.append(visita)

            # si longitud longitud de B domina es igual al número de nodos, entonces B restringido a las
            # etiquetas de visitas domina a la correspondiente restricción de A, y podemos continuar verificando
            # si B domina a A, mirando ahora los recursos:

            if len(B_domina) == len(etiquetaB.label_visitas):

                for recurso in etiquetaB.label_recursos.keys():
                    if etiquetaB.label_recursos[recurso] <= etiquetaA.label_recursos[recurso]:
                        B_domina.append(recurso)
                if len(B_domina) == len(etiquetaB.label_visitas) + len(etiquetaB.label_recursos):
                    # print('PARECE QUE B DOMINA A A')
                    # print('label old domina a label new')
                    return -1

            else:
                # En este caso concluimos que B no domina a A, pues hay al menos una etiqueta de
                # visita de A que es menor que la correspondiente etiqueta de B.
                # print('A NO DOMINA A B Y B NO DOMINA A A')
                # print('ninguno entre labelnew y labelold domina')

                return 0

        else:
            # los conteos de A y B son iguales. # miramos en cuantas A domina a B, en cuantas B domina a A
            # y en cuantas son iguales.
            for visita in etiquetaA.label_visitas.keys():
                if etiquetaB.label_visitas[visita] < etiquetaA.label_visitas[visita]:
                    B_domina.append(visita)
                elif etiquetaA.label_visitas[visita] < etiquetaB.label_visitas[visita]:
                    A_domina.append(visita)
                else:
                    AB_igual.append(visita)
            # Si ningún recurso en B domina al correspondiente recurso en A, y si hay al menos un recurso de A
            # que domine a B, entonces A domina a B
            if len(B_domina) == 0 and len(A_domina) > 0:
                # print('A DOMINA A B')
                # print('label_new domina a label_old')

                return 1


            elif len(A_domina) == 0 and len(B_domina) > 0:
                # print('B DOMINA A A')
                # print('label old domina a label new')
                return -1


            elif len(A_domina) == 0 and len(B_domina) == 0:
                # print('A ES IDENTICO A B')
                return 2

            else:
                # print('A NO DOMINA A B Y B NO DOMINA A A')
                # print('ninguno entre labelnew y labelold domina')

                return 0


def EFF_function_feillet2004(delta_set: set, just_extended: set):
    # Esta función recibe dos conjuntos de etiquetas:
    # delta_set: es el conjunto de etiquetas asociado a cierto nodo j. La invariante de delta_set es un conjunto de Pareto.
    # just_extended: es el conjunto de etiquetas que recien se obtuvieron como extensión de las etiquetas
    # de cierto nodo i al nodo j (F_{ij}) en la notación del artículo de Feillet.

    # Esta función corresponde al procedimiento denotado como EFF(Delta) en el artículo de Feillet2004:
    # Procedimiento que mantiene sólo etiquetas no dominadas (preserva el frente de Pareto).

    # Itera sobre just_extended y delta_set . Desarmamos el conjunto delta_set actual, para volverlo a armar :)

    ind_change_front = 0
    condicion_nodominado = dict()

    # antes de iniciar la actualización, todas las etiquetas en delta_set (pareto set) tienen la característica
    # de ser no dominadas
    for label_old in delta_set:
        condicion_nodominado[label_old] = 1
    # print('condicion_nodominado: ')
    # print(condicion_nodominado)

    while just_extended:
        label_new = just_extended.pop()
        # print('label_new: ', label_new.label)
        # print('tipo de label_new: ', type(label_new))
        # label new es NO dominado (i.e. miembro del frente de Pareto hasta que se verifique lo contrario)
        condicion_nodominado[label_new] = 1

        # delta_set_copy = deepcopy(delta_set)
        # while delta_set_copy:
        for label_old in delta_set:
            # print('delta_set: ')
            # print([etiqueta.label for etiqueta in delta_set_copy])

            # pilas, se usa con el while, no con el for
            # label_old = delta_set_copy.pop()

            # print('label_old: ', label_old.label)
            msj = comparacion_etiqueta_par(label_new, label_old)

            # si label_new es idéntico a label_old, no se registra cambio en el frente de Pareto y se continúa

            # print('msj: ', msj)
            if msj == 2:
                # ind_change_front=0
                break

            # si label_old  < (domina a) label_new, éste último no entra al frente de Pareto. No se registra cambio
            # en el frente de pareto delta_set.
            elif msj == -1:
                condicion_nodominado[label_new] = 0
                # NOTAR QUE PODRÍAMOS ELIMINAR A label_new
                break


            # si label_new < (domina a ) label_old, label_old sale del conjunto delta_set y label_new entra a
            # delta_set (por la condición invariante no es posible que lo domine otro elemento en delta_set).
            # PERO PILAS, es posible que label_new domine también a OTROS ELEMENTOS PRESENTES en delta_set
            # Se registra cambio en el frente de pareto delta_set.

            elif msj == 1:
                condicion_nodominado[label_old] = 0
                # NOTAR QUE PODRÍAMOS ELIMINAR A label_old
                continue

            # si label old (NO DOMINA A) label new y label_new (NO DOMINA A) label old.  Label_old no sale, pero
            # aun es posible que label_new domine a otro elemento actual en el frente de pareto delta_set. Por tanto continua
            # la comparación

            elif msj == 0:
                continue

        # print('entra al bloque de abajo')
        # Cuando termine este ciclo for es porque todos los elementos del conjunto delta_set actual fueron comparados
        # contra label new. En ese punto se debe actualizar el conjunto delta set_actual y registrar si hubo cambios respecto
        # al anterior.

        delta_set_incr = delta_set.union({label_new})
        # print('delta set incr', delta_set_incr)
        new_delta_set = set()
        for label in delta_set_incr:
            if condicion_nodominado[label] == 1:
                new_delta_set.add(label)
            # no necesitamos etiquetas dominadas. Una vez dominada, no vuelve a entrar al frente.

        # print('new_delta_set: ', [etiqueta.label for etiqueta in new_delta_set])

        s = 0
        for label in delta_set:
            s += condicion_nodominado[label] - 1
        # si el frente de pareto (delta set) cambió (algún viejo salió o el nuevo entró)
        if s != 0 or condicion_nodominado[label_new] == 1:
            ind_change_front += 1
            delta_set = new_delta_set

        # ¿podemos borrar delta_set incrementado?
        del delta_set_incr

    return ind_change_front, delta_set


def espptw_feillet2004(G: Grafo_consumos, s):
    # a partir del grafo dado y los recursos necesito crear una estructura
    # para las etiquetas. De pronto conviene crear una clase, porque las etiquetas
    # guardan información pero no están cambiando de dimensiones.

    # pensemos que pasamos los diccionarios de recursos en una lista
    # y las correspondientes restricciones o ventanas en otra, relacionadas por la posición

    # ruta de los archivos pkl que contienen las etiquetas o estados:

    #################################################################################
    # ruta_absoluta = r'D:\UdeA\estados_pd'
    ###############################################################################
    # crear un diccionario cuyas llaves sean los vértices y cuyos valores sean listas.
    Delta = {vertice: set() for vertice in G.vertices}
    # ¿cuál es el método para encontrar el conjunto de sucesores de un nodo? G.succesors(nodo)

    Conteo = {vertice: 0 for vertice in G.vertices}

    ##########################################################################################
    # Delta[s].add(Label_feillet2004(nodo_rel = s, G = G))
    Delta[s].add(Label_feillet2004(nodo_rel=s, G=G, nombre_label='origen'))
    # GENERAR UN DICCIONARIO ALTERNATIVO QUE SÓLO GUARDE EL NOMBRE DE LAS ETIQUETAS, PARA SER
    # LEÍDOS COMO .pkl CUANDO SEA REQUERIDO

    # Delta_nombres = {vertice: set() for vertice in G.vertices}
    # Delta[s].add('origen')
    # Guardar etiqueta origen como pkl:
    # ruta = ruta_absoluta + '/' + 'origen'
    # with open(ruta, 'wb') as file_obj:
    #    pkl.dump(self, file_obj)

    ############################################################################################

    # En el artículo: F_{ij} es el conjunto de etiquetas extendidas del nodo vi al nodo vj
    F = dict()

    # Conjunto de nodos esperando a ser tratados. No se especifica cuál es la estructura adecuada,
    # podríamos tratarlo como un cola FIFO siguiendo la mejora de moore para el algoritmo de Bellman Ford.
    # muy importante: if maxlen is not specified, deques may grow up to an arbitrary length.

    control_visitados = {s}
    E = deque([s])

    # Con pop() sale un elemento del frente (cabeza). La modificación que se requiere es llevar un
    # registro de los nodos que ya han estado en E. Si un nodo ya ha estado en E, entonces se envía al
    # frente haciendo appendright, y si no ha estado previamente en el frente se envía a la cola
    # haciendo append left. Esto se puede combinar con muchas otras heurísticas.
    alpha = 0
    while E:
        print('\nEl deque E es: ', E)
        actual = E.pop()
        alpha += 1
        print('\nse está procesando el nodo: ', actual)
        beta = 0
        for sucesor in G.succesors(actual):
            beta += 1
            # print('\nexploraremos extensiones del nodo actual al nodo: ', sucesor)
            F[(actual, sucesor)] = set()

            gamma = 0
            ######################################################################################
            for etiqueta in Delta[actual]:
                # for etiqueta_nombre in Delta_nombres[actual]:
                # Leer el archivo pkl correspondiente
                # ruta = ruta_absoluta + '/' + etiqueta_nombre
                # with open(ruta, 'rb') as read_file:
                #    etiqueta = pkl.load(read_file)

                #######################################################################################
                # si el nodo sucesor no es un nodo 'inalcanzable'
                if etiqueta.label_visitas[sucesor] == 0:
                    gamma += 1
                    # print('considerando la etiqueta: ')
                    # print(etiqueta.label)
                    new_name = 'label' + '_' + str(alpha) + '_' + str(beta) + '_' + str(gamma)

                    # new_label = etiqueta.extend_function_feillet(sucesor)
                    new_label = etiqueta.extend_function_feillet(sucesor, new_name)

                    # print('la nueva etiqueta obtenida es: ')
                    # print(new_label.label)
                    F[(actual, sucesor)].add(new_label)

            if F[(actual, sucesor)]:
                # conteo de cambios (indicador) en el frente de pareto de Delta[sucesor],
                # y el frente actualizado
                ind_change_front, Delta[sucesor] = \
                    EFF_function_feillet2004(delta_set=Delta[sucesor], just_extended=F[(actual, sucesor)])
            else:
                ind_change_front = 0
            # print('\nEl indicador de cambio del frente de pareto de sucesor {} es: '.format(str(sucesor)), ind_change_front)
            if ind_change_front > 0:
                if sucesor not in E:
                    E.appendleft(sucesor)

                    # AGREGAR LO SIGUIENTE SI SE QUIERE LA IMPLEMENTACIÓN DEQUE PURA
                    # if sucesor in control_visitados:
                    # if 1 <= Conteo[sucesor] <= 5:
                    # E.append(sucesor)
                    # Conteo[sucesor] += 1
                    # else:
                    # E.appendleft(sucesor)
                    # Conteo[sucesor] = (Conteo[sucesor] + 1) % 5
                    control_visitados.add(sucesor)
                    # NO VA!!:
                    # else:
                    # E.append(sucesor)
                    print('sucesor {} se agregó a E'.format(str(sucesor)))

            del F[(actual, sucesor)]
        # E.remove(actual)

    return Delta




def espptw_feillet2004_version2(G: Grafo_consumos, s):
    # a partir del grafo dado y los recursos necesito crear una estructura
    # para las etiquetas. EVITO GENERAR UNA CLASE PARA LAS ETIQUETAS. PARECE QUE ESTO GENERÓ PROBLEMAS
    # EN LA VERSIÓN ANTERIOR. INTENTAREMOS ACÁ MANTENER LAS ETIQUETAS COMO ESTRUCTURAS SIMPLES (no instancias de clases)

    # pensemos que pasamos los diccionarios de recursos en una lista
    # y las correspondientes restricciones o ventanas en otra, relacionadas por la posición

    # ruta de los archivos pkl que contienen las etiquetas o estados:

    #################################################################################
    # ruta_absoluta = r'D:\UdeA\estados_pd'
    ###############################################################################
    # crear un diccionario cuyas llaves sean los vértices y cuyos valores sean listas.
    Delta = {vertice: set() for vertice in G.vertices}
    # ¿cuál es el método para encontrar el conjunto de sucesores de un nodo? G.succesors(nodo)

    Conteo = {vertice: 0 for vertice in G.vertices}

    ##########################################################################################
    # Delta[s].add(Label_feillet2004(nodo_rel = s, G = G))
    Delta[s].add(Label_feillet2004(nodo_rel=s, G=G, nombre_label='origen'))
    # GENERAR UN DICCIONARIO ALTERNATIVO QUE SÓLO GUARDE EL NOMBRE DE LAS ETIQUETAS, PARA SER
    # LEÍDOS COMO .pkl CUANDO SEA REQUERIDO

    # Delta_nombres = {vertice: set() for vertice in G.vertices}
    # Delta[s].add('origen')
    # Guardar etiqueta origen como pkl:
    # ruta = ruta_absoluta + '/' + 'origen'
    # with open(ruta, 'wb') as file_obj:
    #    pkl.dump(self, file_obj)

    ############################################################################################

    # En el artículo: F_{ij} es el conjunto de etiquetas extendidas del nodo vi al nodo vj
    F = dict()

    # Conjunto de nodos esperando a ser tratados. No se especifica cuál es la estructura adecuada,
    # podríamos tratarlo como un cola FIFO siguiendo la mejora de moore para el algoritmo de Bellman Ford.
    # muy importante: if maxlen is not specified, deques may grow up to an arbitrary length.

    control_visitados = {s}
    E = deque([s])

    # Con pop() sale un elemento del frente (cabeza). La modificación que se requiere es llevar un
    # registro de los nodos que ya han estado en E. Si un nodo ya ha estado en E, entonces se envía al
    # frente haciendo appendright, y si no ha estado previamente en el frente se envía a la cola
    # haciendo append left. Esto se puede combinar con muchas otras heurísticas.
    alpha = 0
    while E:
        print('\nEl deque E es: ', E)
        actual = E.pop()
        alpha += 1
        print('\nse está procesando el nodo: ', actual)
        beta = 0
        for sucesor in G.succesors(actual):
            beta += 1
            # print('\nexploraremos extensiones del nodo actual al nodo: ', sucesor)
            F[(actual, sucesor)] = set()

            gamma = 0
            ######################################################################################
            for etiqueta in Delta[actual]:
                # for etiqueta_nombre in Delta_nombres[actual]:
                # Leer el archivo pkl correspondiente
                # ruta = ruta_absoluta + '/' + etiqueta_nombre
                # with open(ruta, 'rb') as read_file:
                #    etiqueta = pkl.load(read_file)

                #######################################################################################
                # si el nodo sucesor no es un nodo 'inalcanzable'
                if etiqueta.label_visitas[sucesor] == 0:
                    gamma += 1
                    # print('considerando la etiqueta: ')
                    # print(etiqueta.label)
                    new_name = 'label' + '_' + str(alpha) + '_' + str(beta) + '_' + str(gamma)

                    # new_label = etiqueta.extend_function_feillet(sucesor)
                    new_label = etiqueta.extend_function_feillet(sucesor, new_name)

                    # print('la nueva etiqueta obtenida es: ')
                    # print(new_label.label)
                    F[(actual, sucesor)].add(new_label)

            if F[(actual, sucesor)]:
                # conteo de cambios (indicador) en el frente de pareto de Delta[sucesor],
                # y el frente actualizado
                ind_change_front, Delta[sucesor] = \
                    EFF_function_feillet2004(delta_set=Delta[sucesor], just_extended=F[(actual, sucesor)])
            else:
                ind_change_front = 0
            # print('\nEl indicador de cambio del frente de pareto de sucesor {} es: '.format(str(sucesor)), ind_change_front)
            if ind_change_front > 0:
                if sucesor not in E:
                    E.appendleft(sucesor)

                    # AGREGAR LO SIGUIENTE SI SE QUIERE LA IMPLEMENTACIÓN DEQUE PURA
                    # if sucesor in control_visitados:
                    # if 1 <= Conteo[sucesor] <= 5:
                    # E.append(sucesor)
                    # Conteo[sucesor] += 1
                    # else:
                    # E.appendleft(sucesor)
                    # Conteo[sucesor] = (Conteo[sucesor] + 1) % 5
                    control_visitados.add(sucesor)
                    # NO VA!!:
                    # else:
                    # E.append(sucesor)
                    print('sucesor {} se agregó a E'.format(str(sucesor)))

            del F[(actual, sucesor)]
        # E.remove(actual)

    return Delta