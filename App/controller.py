"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
 
import config as cf
import model
import time
import tracemalloc
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    return model.new_data_structs()


# Funciones para la carga de datos

def load_data(data_structs):
    """
    Carga los datos del reto
    """
    
    vertices_archivo = cf.data_dir + 'bogota_vertices.txt'
    with open(vertices_archivo, 'r') as f:
        vertices = f.readlines()
    for vertice in vertices:
        model.add_data(data_structs, 'bogota_vertices.txt', vertice)
    
    
    estaciones_archivo = cf.data_dir + 'estacionpolicia_bogota_vertices.csv'
    f = open(estaciones_archivo, 'r', encoding='utf-8')
    estaciones = csv.DictReader(f)
    for estacion in estaciones:
        model.add_data(data_structs, 'estacionpolicia_bogota_vertices.csv', estacion)
        
        
    comparendos_archivo = cf.data_dir + 'comparendos_2019_bogota_vertices.csv'
    f = open(comparendos_archivo, 'r', encoding='utf-8')
    comparendos = csv.DictReader(f)
    for comparendo in comparendos:
        model.add_data(data_structs, 'comparendos_2019_bogota_vertices.csv', comparendo)
    model.min_pq_vehiculo_comparendos(data_structs)
    model.min_pq_gravedad_comparendos(data_structs)

    arcos_archivo = cf.data_dir + 'bogota_arcos.txt'
    with open(arcos_archivo, 'r') as f:
        arcos = f.readlines()
    for arco in arcos:
        model.add_data(data_structs, 'bogota_arcos.txt', arco)
        
      


# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(control, consulta_camaras, consulta_clase_vehiculo):
    """
    Retorna el resultado del requerimiento 5
    """
    # try:
    t0 = get_time()
    m0 = get_memory()
    total_camaras, id_vertices, arcos, extension, costo = model.req_5(control, consulta_camaras, consulta_clase_vehiculo)
    t1 = get_time()
    m1 = get_memory()
    

    dt = delta_time(t0,t1)
    dm = abs(delta_memory(m0,m1))
    return total_camaras, id_vertices, arcos, extension, costo, dt, dm
    # except Exception as exp:
    #     return None, None, None, None, None, None, None

def req_6(control):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return round(elapsed,2)

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    tracemalloc.start()
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
