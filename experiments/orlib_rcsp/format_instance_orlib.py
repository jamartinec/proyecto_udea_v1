import os
import pickle as pkl


def give_format_instance(route_instance):
    with open(route_instance, 'r') as f:
        numbers = f.readline().split()
        num_vertices = int(numbers[0])
        num_arcs = int(numbers[1])
        num_resr = int(numbers[2])

        r_l = f.readline().split()
        r_l = list(map(int, r_l))
        r_u = f.readline().split()
        r_u = list(map(int, r_u))
        ventanas_path = [(r_l[i], r_u[i]) for i in range(len(r_u))]

        dict_vertex_rsr = dict()
        for v in range(num_vertices):
            resource_consump_int = list(map(int, f.readline().split()))
            dict_vertex_rsr[v + 1] = resource_consump_int

        lista_verticesX = list(dict_vertex_rsr.keys())

        dict_arc, dict_arc_cost, dict_arc_consump = dict(), dict(), dict()

        for a in range(num_arcs):
            arc_info_int = list(map(int, f.readline().split()))
            arco = (arc_info_int[0], arc_info_int[1])
            arc_cost = arc_info_int[2]
            arc_consump = arc_info_int[3:]
            dict_arc[a] = arco
            dict_arc_cost[arco] = arc_cost
            dict_arc_consump[arco] = arc_consump
        # Para estas instancias los recursos no tienen nombre, los estamos identificando por el índice
        # (orden) de aparición. No parece muy buena idea la estructura que propusimos para inicializar
        # grafo consumo.

        lista_arcosX = list(dict_arc_cost.keys())

        recursos_nodos = dict()
        for r in range(num_resr):
            recursos_nodos[str(r + 1)] = dict()
            for v in dict_vertex_rsr.keys():
                recursos_nodos[str(r + 1)][v] = dict_vertex_rsr[v][r]

        recursos_arcos = dict()
        for r in range(num_resr):
            recursos_arcos[str(r + 1)] = dict()
            for a in dict_arc_consump.keys():
                recursos_arcos[str(r + 1)][a] = dict_arc_consump[a][r]

        ventanas_recursos = list()
        for r in range(num_resr):
            ventanas_recursos.append([r_l[r], r_u[r]])

        restricciones_nodos = dict()
        for r in range(num_resr):
            restricciones_nodos[str(r + 1)] = dict()
            for v in dict_vertex_rsr.keys():
                restricciones_nodos[str(r + 1)][v] = ventanas_recursos[r]

    return [lista_verticesX, lista_arcosX, recursos_nodos, recursos_arcos, restricciones_nodos, dict_arc_cost]


def save_instances(name, lista_grafo):
    file_name = r'instancia_diccionarios/' +name + '.pkl'
    with open(file_name, 'wb') as a_file:
        pkl.dump(lista_grafo, a_file)

def generar_guardar_instancias():
    instancias = os.listdir('instancias')
    for inst in instancias:
        route_instance = r'instancias/' + inst
        lista_grafo = give_format_instance(route_instance)
        name = inst.split('.')[0]
        save_instances(name, lista_grafo)
    return


if __name__ == '__main__':
    generar_guardar_instancias()