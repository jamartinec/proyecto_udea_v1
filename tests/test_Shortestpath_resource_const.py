# coding: utf8

from pytest import raises
from sortedcontainers import SortedList

from src.combopt.shortest_paths import Pareto_Frontier
from src.combopt.graph import Grafo, Grafo_consumos
from src.combopt.shortest_paths import spptw_desrochers1988_imp_fullpareto, \
    retrieve_path, retrieve_paths_inpareto, slave_function, Label_feillet2004,\
    comparacion_etiqueta_par, EFF_function_feillet2004, espptw_feillet2004, build_generalized_bucket  # ,verificar_recursos, Extend_function_feillet2004,


my_graph2 = Grafo([0,1,2,3,4],[(0,1),(0,2),(0,3),(1,4),(2,4),(3,4)],directed=True)
time = {(0,1):8,(0,2):5,(0,3):12,(1,4):4,(2,4):2,(3,4):4}
cost  = {(0,1):3,(0,2):5,(0,3):2,(1,4):7,(2,4):6,(3,4):3}
window = {0:[0,0],1:[6,14],2:[9,12],3:[8,12],4:[9,15]}
demanda ={0:1,1:1,2:1,3:1,4:1}


def test_spptw_desrochers1988_imp_fullpareto():
    assert spptw_desrochers1988_imp_fullpareto(my_graph2, 0, time, cost, window) == \
           {0: [(0, 0)], 1: [(8, 3)], 2: [(9, 5)], 3: [(12, 2)], 4: [(11, 11), (12, 10)]}

def test_retrieve_path():
    Frentes = \
        spptw_desrochers1988_imp_fullpareto(my_graph2, 0, time, cost, window,False)

    camino_inner, camino, camino_set = retrieve_path((11,11),4,Frentes)
    assert camino_inner == [2] and camino== [0,2,4] and camino_set == {0,2,4}
    camino_inner, camino, camino_set = retrieve_path((12,10),4,Frentes)
    assert camino_inner == [1] and camino == [0,1,4] and camino_set == {0,1,4}

def test_retrieve_paths_inpareto():
    Frentes = \
        spptw_desrochers1988_imp_fullpareto(my_graph2, 0, time, cost, window, False)
    Dictio_inner, Dictio, Dictio_sets = retrieve_paths_inpareto(4,Frentes)
    assert Dictio_inner== {(12,10):[1], (11,11):[2]} and Dictio == {(12,10):[0,1,4], (11,11):[0,2,4]} and \
           Dictio_sets == {(12,10):{0,1,4}, (11,11):{0,2,4}}

def test_slave_functions():
    Dictio_inner, Dictio_Paths, Dictio_Paths_set = slave_function(my_graph2,0,4,time, cost, window)
    assert Dictio_Paths == {(12,10):[0,1,4], (11,11):[0,2,4] } and \
           Dictio_Paths_set == {(12,10): {0,1,4}, (11,11):{0,2,4}} and \
           Dictio_inner =={(12,10):[1], (11,11):[2]}

def test_build_generalized_bucket():
    width = min(time.values())
    print(width)

    sub_intervalos = build_generalized_bucket(window, width)
    assert sub_intervalos == [[6, 8], [8, 10], [8, 10],
                              [9, 10], [9, 10],
                              [10, 12], [10, 12], [10, 12], [10, 12],
                              [12, 14], [12, 14],
                              [14, 15]]






'''
def test_verificar_recursos():

    # Verificar recursos recibe grafo G y etiqueta.
    # Crear un grafo de la clase grafo recursos:
    vertices = [1, 2, 3, 4]
    arcos = [(1, 2), (1, 3), (2, 3), (3, 2), (2, 4), (3, 4)]
    tiempo_nodos = {v: 0 for v in vertices}  # no hay tiempo de espera en los nodos
    demanda_nodos = {v: 1 for v in vertices}  # supongamos demanda unitaria
    tiempo_arcos = {(1, 2): 2, (1, 3): 2, (2, 3): 1, (3, 2): 1, (2, 4): 2, (3, 4): 2}
    demanda_arcos = {a: 0 for a in arcos}  # no hay demanda en los arcos, sólo en los nodos
    ventanas_tiempo = {1: [0, 10], 2: [0, 10], 3: [0, 10], 4: [0, 10], }
    ventanas_demanda = {v: [0,5] for v in vertices}
    # costos_arcos = {arco: 1 for arco in arcos}

    # será qué se puede incluir en las etiquetas de las aristas¡? mirar networkx
    costos_arcos = {(1, 2): 2, (1, 3): 2, (2, 3): 1, (3, 2): 1, (2, 4): 2, (3, 4): 2}

    recursos_nodos = {'tiempo': tiempo_nodos, 'demanda': demanda_nodos}
    recursos_arcos = {'tiempo': tiempo_arcos, 'demanda': demanda_arcos}
    restricciones_nodos = {'tiempo': ventanas_tiempo, 'demanda': ventanas_demanda}

    mi_grafo_consumos = Grafo_consumos(vertices,
                                       arcos,
                                       directed=True,
                                       recursos_nodos=recursos_nodos,
                                       recursos_arcos=recursos_arcos,
                                       restricciones_nodos=restricciones_nodos,
                                       costos_arcos=costos_arcos)
    # Crear una etiqueta

    nombres_recursos = ['tiempo', 'demanda']
    etiqueta = Label_feillet2004(nodo_rel=1, name_recursos=nombres_recursos, nodos=vertices)

    assert etiqueta.visited_nodes() == {1}
    assert etiqueta.is_visited_node(1) == 1
    assert etiqueta.is_visited_node(2) == 0
    assert etiqueta.costo_acumulado == 0

    indicador, nuevos_valores = verificar_recursos(actual=1, sucesor=2, etiqueta=etiqueta, G=mi_grafo_consumos)

    assert indicador == True
    assert nuevos_valores['tiempo']==2
    assert nuevos_valores['demanda'] ==2'''


'''def test_Extended_function_feillet2004():
    # basado en el ejemplo consignado en la fig2 del artículo de Feillet2004
    # Verificar recursos recibe grafo G y etiqueta.
    # Crear un grafo de la clase grafo recursos:
    vertices = [1, 2, 3, 4, 5]
    arcos = [(1, 2), (1, 3), (2, 3), (3, 2), (2, 4), (3, 4), (4,5)]
    tiempo_nodos = {v: 0 for v in vertices}  # no hay tiempo de espera en los nodos
    demanda_nodos = {v: 1 for v in vertices}  # supongamos demanda unitaria
    tiempo_arcos = {(1, 2): 2, (1, 3): 2, (2, 3): 1, (3, 2): 1, (2, 4): 2, (3, 4): 2, (4, 5): 2, }
    demanda_arcos = {a: 0 for a in arcos}  # no hay demanda en los arcos, sólo en los nodos
    ventanas_tiempo = {1: [0, 10], 2: [0, 10], 3: [0, 10], 4: [0, 10], 5: [0, 6], }
    ventanas_demanda = {v: [0, 5] for v in vertices}
    # costos_arcos = {arco: 1 for arco in arcos}

    # será qué se puede incluir en las etiquetas de las aristas¡? mirar networkx
    costos_arcos = {(1, 2): 2, (1, 3): 2, (2, 3): -2, (3, 2): 1, (2, 4): 2, (3, 4): 2, (4, 5): 2,}

    recursos_nodos = {'tiempo': tiempo_nodos, 'demanda': demanda_nodos}
    recursos_arcos = {'tiempo': tiempo_arcos, 'demanda': demanda_arcos}
    restricciones_nodos = {'tiempo': ventanas_tiempo, 'demanda': ventanas_demanda}

    mi_grafo_consumos = Grafo_consumos(vertices,
                                       arcos,
                                       directed=True,
                                       recursos_nodos=recursos_nodos,
                                       recursos_arcos=recursos_arcos,
                                       restricciones_nodos=restricciones_nodos,
                                       costos_arcos=costos_arcos)
    # Crear una etiqueta
    etiqueta = Label_feillet2004(nodo_rel=1, G=mi_grafo_consumos)

    new_etiqueta = Extend_function_feillet2004(mi_grafo_consumos, etiqueta,2)
    assert new_etiqueta.nodo_rel == 2
    assert new_etiqueta.visited_nodes() == {1,2}
    assert new_etiqueta.costo_acumulado == 2

    new_etiqueta3 = Extend_function_feillet2004(mi_grafo_consumos, etiqueta, 3)
    assert new_etiqueta3.nodo_rel == 3
    assert new_etiqueta3.visited_nodes() == {1, 3}
    assert new_etiqueta3.costo_acumulado == 2
    assert new_etiqueta3.label == {'tiempo': 2, 'demanda': 2, 1: 1, 2: 0, 3: 1, 4: 0, 5: 0}

    new_etiqueta4 = Extend_function_feillet2004(mi_grafo_consumos, new_etiqueta, 3)
    assert new_etiqueta4.nodo_rel == 3
    assert new_etiqueta4.visited_nodes() == {1, 2, 3}
    assert new_etiqueta4.costo_acumulado == 0
    assert new_etiqueta4.label == {'tiempo': 3, 'demanda': 3, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0}

    new_etiqueta5 = Extend_function_feillet2004(mi_grafo_consumos, new_etiqueta, 4)
    assert new_etiqueta5.nodo_rel == 4
    assert new_etiqueta5.visited_nodes() == {1, 2, 4}
    assert new_etiqueta5.costo_acumulado == 4
    assert new_etiqueta5.label == {'tiempo': 4, 'demanda': 3, 1: 1, 2: 1, 3: 0, 4: 1, 5: 0}

    new_etiqueta6 = Extend_function_feillet2004(mi_grafo_consumos, new_etiqueta3, 4)
    assert new_etiqueta6.nodo_rel == 4
    assert new_etiqueta6.visited_nodes() == {1, 3, 4}
    assert new_etiqueta6.costo_acumulado == 4
    assert new_etiqueta6.label == {'tiempo': 4, 'demanda': 3, 1: 1, 2: 0, 3: 1, 4: 1, 5: 0}

    new_etiqueta7 = Extend_function_feillet2004(mi_grafo_consumos, new_etiqueta4, 4)
    assert new_etiqueta7.nodo_rel == 4
    assert new_etiqueta7.visited_nodes() == {1, 2, 3, 4}
    assert new_etiqueta7.costo_acumulado == 2
    assert new_etiqueta7.label == {'tiempo': 5, 'demanda': 4, 1: 1, 2: 1, 3: 1, 4: 1, 5: 0}'''
#####################################################################################
# basado en el ejemplo consignado en la fig2 del artículo de Feillet2004
# Verificar recursos recibe grafo G y etiqueta.
# Crear un grafo de la clase grafo recursos:
vertices = [1, 2, 3, 4, 5]
arcos = [(1, 2), (1, 3), (2, 3), (3, 2), (2, 4), (3, 4), (4, 5)]
tiempo_nodos = {v: 0 for v in vertices}  # no hay tiempo de espera en los nodos
demanda_nodos = {v: 1 for v in vertices}  # supongamos demanda unitaria
tiempo_arcos = {(1, 2): 2, (1, 3): 2, (2, 3): 1, (3, 2): 1, (2, 4): 2, (3, 4): 2, (4, 5): 2, }
demanda_arcos = {a: 0 for a in arcos}  # no hay demanda en los arcos, sólo en los nodos
ventanas_tiempo = {1: [0, 10], 2: [0, 10], 3: [0, 10], 4: [0, 10], 5: [0, 6], }
ventanas_demanda = {v: [0, 5] for v in vertices}
# costos_arcos = {arco: 1 for arco in arcos}

# será qué se puede incluir en las etiquetas de las aristas¡? mirar networkx
costos_arcos = {(1, 2): 2, (1, 3): 2, (2, 3): -2, (3, 2): 1, (2, 4): 2, (3, 4): 2, (4, 5): 2, }

recursos_nodos = {'tiempo': tiempo_nodos, 'demanda': demanda_nodos}
recursos_arcos = {'tiempo': tiempo_arcos, 'demanda': demanda_arcos}
restricciones_nodos = {'tiempo': ventanas_tiempo, 'demanda': ventanas_demanda}

mi_grafo_consumos = Grafo_consumos(vertices,
                                   arcos,
                                   directed=True,
                                   recursos_nodos=recursos_nodos,
                                   recursos_arcos=recursos_arcos,
                                   restricciones_nodos=restricciones_nodos,
                                   costos_arcos=costos_arcos)

# Crear una etiqueta
etiqueta = Label_feillet2004(nodo_rel=1, G=mi_grafo_consumos, nombre_label='origen')
label2 = etiqueta.extend_function_feillet(2, 'label2')
label3 = etiqueta.extend_function_feillet(3, 'label3')
label4 = label2.extend_function_feillet(3, 'label4')
label5 = label2.extend_function_feillet(4, 'label5')
label6 = label3.extend_function_feillet(4, 'label6')
label7 = label4.extend_function_feillet(4, 'label7')


def test_Extended_function_feillet2004_2():

    print('conteo:')
    print(etiqueta.conteo)


    assert label2.nodo_rel == 2
    assert label2.visited_nodes() == {1,2}
    assert label2.costo_acumulado == 2
    print(label2.recursos_sucesores)
    print('conteo:')
    print(label2.conteo)


    assert label3.nodo_rel == 3
    assert label3.visited_nodes() == {1, 3}
    assert label3.costo_acumulado == 2
    assert label3.label == {'tiempo': 2, 'demanda': 2, 1: 1, 2: 0, 3: 1, 4: 0, 5: 0}
    print(label3.recursos_sucesores)
    print('conteo:')
    print(label3.conteo)


    assert label4.nodo_rel == 3
    assert label4.visited_nodes() == {1, 2, 3}
    assert label4.costo_acumulado == 0
    assert label4.label == {'tiempo': 3, 'demanda': 3, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0}
    print(label4.recursos_sucesores)
    print('conteo:')
    print(label4.conteo)

    assert label5.nodo_rel == 4
    assert label5.visited_nodes() == {1, 2, 4}
    assert label5.costo_acumulado == 4
    assert label5.label == {'tiempo': 4, 'demanda': 3, 1: 1, 2: 1, 3: 0, 4: 1, 5: 0}
    print('recursos_sucesores label5')
    print(label5.recursos_sucesores)
    print('conteo:')
    print(label5.conteo)


    assert label6.nodo_rel == 4
    assert label6.visited_nodes() == {1, 3, 4}
    assert label6.costo_acumulado == 4
    assert label6.label == {'tiempo': 4, 'demanda': 3, 1: 1, 2: 0, 3: 1, 4: 1, 5: 0}
    print('label6 recursos sucesores: ')
    print(label6.recursos_sucesores)
    print('conteo:')
    print(label6.conteo)

    assert label7.nodo_rel == 4
    assert label7.visited_nodes() == {1, 2, 3, 4, 5} # el nodo 5 queda marcado como unreachable
    assert label7.costo_acumulado == 2
    assert label7.label == {'tiempo': 5, 'demanda': 4, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
    print('label7 recursos_sucesores')
    print(label7.recursos_sucesores)
    print('conteo:')
    print(label7.conteo)


def test_comparacion_etiqueta_par():
    # Replicar la etiqueta 5 usando los métodos auxiliares de label_feillet
    label5_d = Label_feillet2004(nodo_rel=4, G=mi_grafo_consumos, nombre_label='label_5d')
    label5_d.update_label_visitas([1, 2, 4])
    label5_d.update_label_recursos({'tiempo':4,'demanda': 3})
    dic_resource_succ = {2: {'tiempo': 2, 'demanda': 2}, 3: {'tiempo': 3, 'demanda': 3},
                              4: {'tiempo': 4, 'demanda': 3}, 5: {'tiempo': 6, 'demanda': 4}}
    label5_d.update_recursos_sucesores(dic_resource_succ)
    label5_d.update_cost(4)

    assert label5.longitud == label5_d.longitud
    assert label5.nodo_rel == label5_d.nodo_rel
    assert label5.visited_nodes() == label5_d.visited_nodes()
    assert label5.conteo == label5_d.conteo
    assert label5.costo_acumulado == label5_d.costo_acumulado
    assert label5.label == label5_d.label
    u = comparacion_etiqueta_par(label5, label5_d)

    v = comparacion_etiqueta_par(label6, label7)

    w = comparacion_etiqueta_par(label3,label4)

def test_EFF_funcion_feillet2004():
    delta_set = {label5}
    just_extended = {label6, label7}
    ind_change_front, new_delta_set = EFF_function_feillet2004(delta_set=delta_set,just_extended=just_extended)
    print('ind_change_front: ')
    print(ind_change_front)

    print('new_delta_set: ')
    print(new_delta_set)
    print([etiqueta.label for etiqueta in new_delta_set])
    assert len(new_delta_set) == 3



######## Segunda instancia test ###############################################
# Este ejemplo no satisface la desigualdad triangular, la cual es hipótesis para el algoritmo
vertices2 = [1, 2, 3, 4, 5, 6]
arcos2 = [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 4), (3, 5), (4, 2), (4, 5), (6, 5)]
tiempo_nodos2 = {v: 0 for v in vertices2}  # no hay tiempo de espera en los nodos
demanda_nodos2 = {v: 1 for v in vertices2}  # supongamos demanda unitaria
tiempo_arcos2 = {(1, 2): 2, (1, 3): 2, (1, 4): 1, (2, 5): 8, (2, 6): 4, (3, 4): -2,
                 (3, 5): 7, (4, 2): 1, (4, 5): -3, (6, 5): -4, }
demanda_arcos2 = {a: 0 for a in arcos2}  # no hay demanda en los arcos, sólo en los nodos
ventanas_tiempo2 = {1: [0, 10], 2: [0, 10], 3: [0, 10], 4: [0, 10], 5: [0, 5], 6: [0, 5], }
ventanas_demanda2 = {v: [0, 6] for v in vertices2}
# costos_arcos = {arco: 1 for arco in arcos}

# será qué se puede incluir en las etiquetas de las aristas¡? mirar networkx
costos_arcos2 = {(1, 2): 2, (1, 3): 2, (1, 4): 1, (2, 5): 3, (2, 6): 4, (3, 4): -2,
                 (3, 5): 1, (4, 2): 1, (4, 5): 1, (6, 5): 1, }

recursos_nodos2 = {'tiempo': tiempo_nodos2, 'demanda': demanda_nodos2}
recursos_arcos2 = {'tiempo': tiempo_arcos2, 'demanda': demanda_arcos2}
restricciones_nodos2 = {'tiempo': ventanas_tiempo2, 'demanda': ventanas_demanda2}

mi_grafo_consumos2 = Grafo_consumos(vertices2,
                                   arcos2,
                                   directed=True,
                                   recursos_nodos=recursos_nodos2,
                                   recursos_arcos=recursos_arcos2,
                                   restricciones_nodos=restricciones_nodos2,
                                   costos_arcos=costos_arcos2)
def test_mixture():
    # Crear una etiqueta
    v2_label0 = Label_feillet2004(nodo_rel = 1, G = mi_grafo_consumos2, nombre_label = 'v2_label0')
    v2_label1 = v2_label0.extend_function_feillet(2, 'v2_label1')
    v2_label2 = v2_label0.extend_function_feillet(3, 'v2_label2')
    v2_label3 = v2_label0.extend_function_feillet(4, 'v2_label3')
    v2_label4 = v2_label2.extend_function_feillet(4, 'v2_label4')
    v2_label5 = v2_label4.extend_function_feillet(2, 'v2_label5')
    v2_label6 = v2_label3.extend_function_feillet(2, 'v2_label6')

    delta_set = {v2_label1}
    just_extended = {v2_label5}
    ind_change_front, new_delta_set = EFF_function_feillet2004(delta_set=delta_set, just_extended=just_extended)
    print('ind_change_front: ')
    print(ind_change_front)

    print('new_delta_set: ')
    print(new_delta_set)
    print([etiqueta.label for etiqueta in new_delta_set])


def test_espptw_feillet2004():
    Delta = espptw_feillet2004(mi_grafo_consumos, 1)
    #print(Delta)
    Delta_explicit = dict()
    for vertice, pareto in Delta.items():
        Delta_explicit[vertice] = [etiqueta.label for etiqueta in pareto]
    #print(Delta_explicit)

    for vertice, pareto in Delta_explicit.items():
        print('vertice ', vertice)
        print('\n', len(pareto))



    print('#########################')
    print(Delta_explicit[4])

def test_espptw_feillet2004_2():
    Delta = espptw_feillet2004(mi_grafo_consumos2, 1)
    #print(Delta)
    Delta_explicit = dict()
    for vertice, pareto in Delta.items():
        Delta_explicit[vertice] = [etiqueta.label for etiqueta in pareto]
    #print(Delta_explicit)

    for vertice, pareto in Delta_explicit.items():
        print('vertice ', vertice)
        print('\n', len(pareto))

    print('#########################')
    #print(Delta_explicit[4])
