# coding: utf8

from pytest import raises
from sortedcontainers import SortedList
import pickle as pkl
import time

from src.combopt.shortest_paths import Pareto_Frontier
from src.combopt.graph import Grafo, Grafo_consumos
from src.combopt.shortest_paths import spptw_desrochers1988_imp_fullpareto, \
    retrieve_path, retrieve_paths_inpareto, slave_function, Label_feillet2004,\
    comparacion_etiqueta_par, EFF_function_feillet2004, espptw_feillet2004  # ,verificar_recursos, Extend_function_feillet2004,


## rcsp1 ###

ruta_general = r'./solomon/solomon_50_diccionarios/'
ruta_resultados = r'./solomon/solomon_50_resultados/'
instancia_short = 'R105_50' #'C101_50'
instancia = 'R105_50.pkl' #'C101_50.pkl'
ruta = ruta_general+instancia

with open(ruta, 'rb') as inst_file:
    [vertices, arcos, recursos_nodos, recursos_arcos, restricciones_nodos, costos_arcos] = pkl.load(inst_file)

print('el número de arcos es: ', len(arcos))

conteo_negativos = 0
for arco in costos_arcos.keys():
    if costos_arcos[arco] < 0:
        conteo_negativos += 1
print('el número de arcos negativos es {}'.format(conteo_negativos))
print('el porcentaje de arcos negativos es {}'.format((conteo_negativos/len(arcos))*100))


grafo_consum_R105_50 = Grafo_consumos(vertices,
                                   arcos,
                                   directed=True,
                                   recursos_nodos=recursos_nodos,
                                   recursos_arcos=recursos_arcos,
                                   restricciones_nodos=restricciones_nodos,
                                   costos_arcos=costos_arcos)

num_vertices = grafo_consum_R105_50.num_vertices

start_time = time.time()
Delta = espptw_feillet2004(grafo_consum_R105_50, 0)
end_time = time.time()
#print(Delta)
Delta_explicit = dict()
for vertice, pareto in Delta.items():
    Delta_explicit[vertice] = [(etiqueta.label, etiqueta.costo_acumulado) for etiqueta in pareto]

print(Delta_explicit)

print('################################################################')
for vertice, pareto in Delta_explicit.items():
    print('vertice ', vertice)
    print('\n', len(pareto))
print('################################################################')



# Guardar resultados como pkl:
ruta = ruta_resultados + instancia_short
with open(ruta, 'wb') as file_obj:
    pkl.dump(Delta_explicit, file_obj)

#with open(ruta, 'rb') as read_file:
#    results = pkl.load(read_file)

print('#########################################################################')
#print('resultados:')
#print(results)
print('############################################################################')
print('el tiempo requerido fue {} segundos'.format(end_time-start_time))