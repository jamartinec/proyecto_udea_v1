# coding: utf8
import heapq
import gurobipy as gp
from gurobipy import GRB
from gurobipy import Column
import numpy as np
def initial_covering_model(customers, fleet):
    # El modelo inicial solamente tiene las variables de holgura para la inicialización
    # (Método de la gran M) y tiene las restricciones, comenzando con la de tamaño de flota
    # correspondiente al nodo depósito inicial.

    model = gp.Model('covering')
    y = list()
    for custom in customers:
        y.append(model.addVar(lb=0.0, obj=100, vtype=GRB.CONTINUOUS, name='y' + str(custom)))
    model.update()

    model.addConstr(sum(y) <= fleet, name='fleet')
    for custom in customers:
        nombre_var = 'y' + str(custom)
        nombre_rest = 'v' + str(custom)
        model.addConstr(model.getVarByName(nombre_var) >= 1, name=nombre_rest)

    model.modelSense = GRB.MINIMIZE
    model.update()

    return model

def compute_dual_variables(modelo):
    # toma un modelo, lo resuelve y retorna el vector de variables duales
    modelo.update()
    modelo.display()
    modelo.optimize()
    dual_variables = modelo.getAttr(GRB.Attr.Pi)
    print('duales',dual_variables)
    return dual_variables



def covering_model():
    # 0 es source (depot inicial)
    # 4 es sink (depot final)
    m = gp.Model('covering')

    U = 10
    customers = [1, 2, 3]

    y = list()
    for custom in customers:
        y.append(m.addVar(lb=0.0, obj=100, vtype=GRB.CONTINUOUS, name='y' + str(custom)))

    m.update()

    m.addConstr(sum(y) <= U, name='fleet')

    for custom in customers:
        m.addConstr(m.getVarByName('y' + str(custom)) >= 1, name='v' + str(custom))

    m.update()

    print('TRINES')
    for c in m.getConstrs():
        print('constraintname', c.constrName)

    Rutas = [((2, 2), [1], {1}), ((2.8, 2.8), [2], {2}), ((2, 2), [3], {3})]
    num_colum = 1
    Diccionario_Rutas = dict()

    for i in range(len(Rutas)):
        Diccionario_Rutas['r' + str(num_colum)] = Rutas[i]
        num_colum += 1
    # print('Diccionario_Rutas', Diccionario_Rutas)

    theta = list()
    for ruta in Diccionario_Rutas:
        restric = Diccionario_Rutas[ruta][1]
        print('restric', restric)
        constrs_names = ['v' + str(restric[i]) for i in range(len(restric))]
        print('constrs_names', constrs_names)
        constrs = [m.getConstrByName(cons) for cons in constrs_names] + [m.getConstrByName('fleet')]
        print('constrs', constrs)
        coeffs = [1] * len(constrs)
        theta.append(m.addVar(lb=0.0, obj=Diccionario_Rutas[ruta][0][1], vtype=GRB.CONTINUOUS, name=ruta,
                              column=Column(coeffs, constrs)))

    # Agregar la restricción de vehículos
    m.modelSense = GRB.MINIMIZE
    m.update()

    print('función objetivo', m.getObjective())

    m.optimize()

    print(m.display())
    # Print solution
    print('\nTOTAL COSTS: %g' % m.objVal)

    dual_variables = m.getAttr(GRB.Attr.Pi)
    print('Dual variables', dual_variables)

    X_all = m.getAttr('X', m.getVars())
    print('xall', X_all)

    return

# Crear una nueva función que reciba un modelo y un diccionario de caminos, cree variables nuevas
# por cada camino recibido, y actualice las restricciones y la función objetivo.

def update_covering_model(m, Dictio_Paths_inner, num_columns):

    for key in Dictio_Paths_inner:
        # aumentar el contador de columnas(variables)
        num_columns += 1
        # Crear el nombre de la variable
        nombre_var = 'r'+ str(num_columns)
        restric = Dictio_Paths_inner[key]
        # nombre de las restricciones que serán actualizadas
        constrs_names = ['v' + str(restric[i]) for i in range(len(restric))]
        # restricciones que serán actualizadas
        constrs = [m.getConstrByName(cons) for cons in constrs_names] + [m.getConstrByName('fleet')]
        # coeficientes de las nuevas variables en las restricciones correspondientes.
        coeffs = [1] * len(constrs)
        # coeficiente de la nueva variable en la función objetivo
        coe_of = key[1]
        m.addVar(lb=0.0, obj=coe_of, vtype=GRB.CONTINUOUS, name=nombre_var, column=Column(coeffs, constrs))
        m.update()
    return m, num_columns







# def build_parameters(rutas_set,customers):
#     Rutas = list()
#     Costos = list()
#     Tiempos = list()
#     for key in rutas_set:
#         Tiempos.append(key[0])
#         Costos.append(key[1])
#         Rutas.append(rutas_set[key])
#
#     l = len(customers)
#     m = len(Rutas)
#
#     paramA = np.zeros(shape=(l,m), dtype=int)
#     for v in customers:
#         a_param.append([])
#         for ruta in Rutas:
#             if v in ruta:
#                 a[v].append(1)
#             else:
#                 a[v].append(0)
#
#
#
#
#
#
#
#
# def refactor_master_model(rutas_list, rutas_set):
#     # rutas_list es un diccionario con las rutas (como listas) resultantes de resolver el subproblema.
#     # rutas_set es un diccionario con los conjuntos de vértices en cada ruta resultante de resolver el subproblema.
#
#     vertices=[1,2,3,4,5,6]
#
#     Rutas = list()
#     for key in rutas_set:
#         Rutas.append((key,rutas_set[key]))
#
#     c=[]
#     for par in Rutas:
#         c.append(par[0][1])
#
#     a_param = list()
#     for v in vertices:
#         a_param.append([])
#         for ruta in Rutas:
#             a_param[v].append(m.addVar())
#
#
#
#
#
