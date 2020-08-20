# coding: utf8

import gurobipy as gp
from gurobipy import GRB
from gurobipy import Column

from pytest import raises
from sortedcontainers import SortedList

#import numpy as np

from src.combopt.shortest_paths import covering_model,initial_covering_model,compute_dual_variables, update_covering_model

def test_initial_covering_model():
    customers = [1,2,3]
    fleet = 10
    model = initial_covering_model(customers,fleet)
    print(model.display())

def test_compute_dual_variables():
    customers = [1, 2, 3]
    fleet = 10
    model = initial_covering_model(customers, fleet)
    dual_variables = compute_dual_variables(model)
    print('dual_variables',dual_variables)
    # las variables duales del problema inicial son [0, 100, 100 ,100]
    # TAL VEZ ESE SEA EL PROBLEMA.

def test_update_covering_model():
    customers = [1, 2, 3]
    fleet = 10
    model = initial_covering_model(customers, fleet)
    Dictio_Paths_inner={(2,2):[1], (2.8,2.8):[2]}
    num_columns = 0
    model_up, num_columns_up = update_covering_model(model, Dictio_Paths_inner, num_columns)
    print(model_up.display())
    print('numero de variables', num_columns_up)





#def test_covering_model():
#    covering_model()




