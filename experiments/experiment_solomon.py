# coding: utf8

from pytest import raises
from sortedcontainers import SortedList
import pickle as pkl

from src.combopt.shortest_paths import Pareto_Frontier
from src.combopt.graph import Grafo, Grafo_consumos
from src.combopt.shortest_paths import spptw_desrochers1988_imp_fullpareto, \
    retrieve_path, retrieve_paths_inpareto, slave_function, Label_feillet2004,\
    comparacion_etiqueta_par, EFF_function_feillet2004, espptw_feillet2004  # ,verificar_recursos, Extend_function_feillet2004,


## rcsp1 ###

ruta_general = r'./solomon/solomon_25_diccionarios/'
instancia = 'C101_25.pkl'
ruta = ruta_general+instancia

with open(ruta, 'rb') as inst_file:
    [vertices, arcos, recursos_nodos, recursos_arcos, restricciones_nodos, costos_arcos] = pkl.load(inst_file)


grafo_consum_c101_25 = Grafo_consumos(vertices,
                                   arcos,
                                   directed=True,
                                   recursos_nodos=recursos_nodos,
                                   recursos_arcos=recursos_arcos,
                                   restricciones_nodos=restricciones_nodos,
                                   costos_arcos=costos_arcos)

Delta = espptw_feillet2004(grafo_consum_c101_25, 0)
#print(Delta)
Delta_explicit = dict()
for vertice, pareto in Delta.items():
    Delta_explicit[vertice] = [etiqueta.label for etiqueta in pareto]

print(Delta_explicit)

#for vertice, pareto in Delta_explicit.items():
#    print('vertice ', vertice)
#    print('\n', len(pareto))

