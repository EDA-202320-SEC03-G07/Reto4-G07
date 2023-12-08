"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
import pandas as pd
import threading

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def new_controller():
    """
        Se crea una instancia del controlador
    """
    
    return controller.new_controller()


def print_menu():
    print("\nBienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    
    controller.load_data(control)

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    
    latitud_vertice_origen = float(input("Ingrese la latitud del vertice origen: "))
    longitud_vertice_origen = float(input("Ingrese la longitud del vertice origen: "))
    
    latitud_vertice_destino = float(input("Ingrese la latitud del vertice destino: "))
    longitud_vertice_destino = float(input("Ingrese la longitud del vertice destino: "))
    
    try:
        total_vertices, total_distancia, pathTo, dt, dm = controller.req_1(control, latitud_vertice_origen, longitud_vertice_origen, latitud_vertice_destino, longitud_vertice_destino)
        print(f"\n====================================== Req No. 1 Inputs ======================================\n"
                f"Latitud del Vertice Origen: {latitud_vertice_origen}\n"
                f"Longitud del Vertice Origen: {longitud_vertice_origen}\n"
                f"Latitud del Vertice Destino: {latitud_vertice_destino}\n"
                f"Longitud del Vertice Destino: {longitud_vertice_destino}\n"
                f"====================================== Req No. 1 Results ======================================\n"
                f"Total de Vertices Recorridos: {total_vertices}\n"
                f"Distancia Total Recorrida: {round(total_distancia, 2)} km\n"
                f"Camino Recorrido: {pathTo}\n"
                f"El tiempo de ejecución del requerimiento es: {dt} ms\n"
                f"La memoria usada del requerimiento es: {dm} kB\n")
        
    except ValueError:
        print("\nPor favor ingrese los vertices correctamente")

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    
    latitud_vertice_origen = float(input("Ingrese la latitud del vertice origen: "))
    longitud_vertice_origen = float(input("Ingrese la longitud del vertice origen: "))
    
    latitud_vertice_destino = float(input("Ingrese la latitud del vertice destino: "))
    longitud_vertice_destino = float(input("Ingrese la longitud del vertice destino: "))
    
    try:
        total_vertices, total_distancia, pathTo, dt, dm = controller.req_2(control, latitud_vertice_origen, longitud_vertice_origen, latitud_vertice_destino, longitud_vertice_destino)
        print(f"\n====================================== Req No. 2 Inputs ======================================\n"
              f"Latitud del Vertice Origen: {latitud_vertice_origen}\n"
                f"Longitud del Vertice Origen: {longitud_vertice_origen}\n"
                f"Latitud del Vertice Destino: {latitud_vertice_destino}\n"
                f"Longitud del Vertice Destino: {longitud_vertice_destino}\n"
                f"====================================== Req No. 2 Results ======================================\n"
                f"Total de Vertices Recorridos: {total_vertices}\n"
                f"Distancia Total Recorrida: {round(total_distancia, 2)} km\n"
                f"Camino Recorrido: {pathTo}\n"
                f"El tiempo de ejecución del requerimiento es: {dt} ms\n"
                f"La memoria usada del requerimiento es: {dm} kB\n"
        )
        
    except ValueError:
        print("Porfavor ingresa los vertices correctamente")


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    
    try:
        consulta_camaras = int(input("Ingrese el número de cámaras a poner: "))
        consulta_localidad = input("Ingrese la localidad a consultar: ").upper()
        
        total_camaras, id_vertices, arcos, extension, costo, dt, dm = controller.req_3(control, consulta_camaras, consulta_localidad)

        def create_adjacency_matrix_with_headers(arcs):
            vertices = set()
            for key in arcs['edgeTo']['table']['elements']:
                if key is not None and key['value'] is not None:
                    vertices.add(key['key'])
                    vertices.add(key['value']['vertexA'])
                    vertices.add(key['value']['vertexB'])

            vertices = sorted(list(vertices))
            vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
            matrix_size = len(vertices)
            
            adjacency_matrix = [[None] * matrix_size for _ in range(matrix_size)]

            for key in arcs['edgeTo']['table']['elements']:
                if key is not None and key['value'] is not None:
                    vertex_a = key['key']
                    vertex_b = key['value']['vertexA']
                    weight = key['value']['weight']
                    if vertex_a is not None and vertex_b is not None:
                        index_a = vertex_index[vertex_a]
                        index_b = vertex_index[vertex_b]
                        adjacency_matrix[index_a][index_b] = weight
                        adjacency_matrix[index_b][index_a] = weight

            return adjacency_matrix, vertices

        adjacency_matrix, headers = create_adjacency_matrix_with_headers(arcos)
        df = pd.DataFrame(adjacency_matrix, columns=headers, index=headers)

        print(f"\n====================================== Req No. 3 Inputs ======================================\n"
                f"Número de Cámaras Solicitadas: {consulta_camaras}\n"
                f"Consulta Localidad: {consulta_localidad}\n"
                f"====================================== Req No. 3 Results ======================================\n"
                f"Total de Cámaras Puestas: {total_camaras}\n"
                f"Identificadores de las Cámaras: {headers}\n"
                f"Extensión de la Red de Cámaras: {round(extension, 2)} km\n"
                f"Costo de la Red de Cámaras: {round(costo, 2)} COP\n"
                f"Conecciones entre Cámaras:\n{tabulate(df, headers='keys', tablefmt='rounded_grid', showindex=True)}\n"
                f"El tiempo de ejecución del requerimiento es: {dt} ms\n"
                f"La memoria usada del requerimiento es: {dm} kB\n")
        
    except ValueError:
        print("Please ingrese un input válido.")
        
        
def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    
    try:
        consulta_camaras = int(input("Ingrese el número de cámaras a poner: "))
        total_camaras, id_vertices, arcos, extension, costo = controller.req_4(control, consulta_camaras)
        def create_adjacency_matrix_with_headers(arcs):
            vertices = set()
            for key in arcs['edgeTo']['table']['elements']:
                if key is not None and key['value'] is not None:
                    vertices.add(key['key'])
                    vertices.add(key['value']['vertexA'])
                    vertices.add(key['value']['vertexB'])

            vertices = sorted(list(vertices))
            vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
            matrix_size = len(vertices)
            
            adjacency_matrix = [[None] * matrix_size for _ in range(matrix_size)]

            for key in arcs['edgeTo']['table']['elements']:
                if key is not None and key['value'] is not None:
                    vertex_a = key['key']
                    vertex_b = key['value']['vertexA']
                    weight = key['value']['weight']
                    if vertex_a is not None and vertex_b is not None:
                        index_a = vertex_index[vertex_a]
                        index_b = vertex_index[vertex_b]
                        adjacency_matrix[index_a][index_b] = weight
                        adjacency_matrix[index_b][index_a] = weight

            return adjacency_matrix, vertices

        adjacency_matrix, headers = create_adjacency_matrix_with_headers(arcos)
        
        df = pd.DataFrame(adjacency_matrix, columns=headers, index=headers)
        
        print(f"\n====================================== Req No. 4 Inputs ======================================\n"
                f"Número de Cámaras Solicitadas: {consulta_camaras}\n"
                f"====================================== Req No. 4 Results ======================================\n"
                f"Total de Cámaras Puestas: {total_camaras}\n"
                f"Identificadores de las Cámaras: {headers}\n"
                f"Extensión de la Red de Cámaras: {round(extension, 2)} km\n"
                f"Costo de la Red de Cámaras: {round(costo, 2)} COP\n")
        
    except ValueError:
        print("\nPor favor ingrese un input válido.")


def print_req_5(control):
    """
    Function that prints the solution of Requirement 5 to the console
    """
    
    try: 
        consulta_camaras  = int(input("Ingrese el número de cámaras a poner: "))
        consulta_clase_vehiculo = input("Ingrese la clase de vehículo a consultar: ").upper()
        
        total_camaras, id_vertices, arcos, extension, costo, dt, dm = controller.req_5(control, consulta_camaras, consulta_clase_vehiculo)
        
        
        def create_adjacency_matrix_with_headers(arcs):
            vertices = set()
            for key in arcs['edgeTo']['table']['elements']:
                if key is not None and key['value'] is not None:
                    vertices.add(key['key'])
                    vertices.add(key['value']['vertexA'])
                    vertices.add(key['value']['vertexB'])

            vertices = sorted(list(vertices))
            vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
            matrix_size = len(vertices)
            
            adjacency_matrix = [[None] * matrix_size for _ in range(matrix_size)]

            for key in arcs['edgeTo']['table']['elements']:
                if key is not None and key['value'] is not None:
                    vertex_a = key['key']
                    vertex_b = key['value']['vertexA']
                    weight = key['value']['weight']
                    if vertex_a is not None and vertex_b is not None:
                        index_a = vertex_index[vertex_a]
                        index_b = vertex_index[vertex_b]
                        adjacency_matrix[index_a][index_b] = weight
                        adjacency_matrix[index_b][index_a] = weight

            return adjacency_matrix, vertices

        adjacency_matrix, headers = create_adjacency_matrix_with_headers(arcos)
        
        df = pd.DataFrame(adjacency_matrix, columns=headers, index=headers)
        
        print(f"\n====================================== Req No. 2 Inputs ======================================\n"
                f"Número de Cámaras Solicitadas: {consulta_camaras}\n"
                f"Consulta Clase de Vehículo: {consulta_clase_vehiculo}\n"
                f"====================================== Req No. 2 Results ======================================\n"
                f"Total de Cámaras Puestas: {total_camaras}\n"
                f"Identificadores de las Cámaras: {headers}\n"
                f"Extensión de la Red de Cámaras: {round(extension, 2)} km\n"
                f"Costo de la Red de Cámaras: {round(costo, 2)} COP\n"
                f"Conecciones entre Cámaras:\n{tabulate(df, headers='keys', tablefmt='rounded_grid', showindex=True)}\n"
                f"El tiempo de ejecución del requerimiento es: {dt} ms\n"
                f"La memoria usada del requerimiento es: {dm} kB\n")
        
    except ValueError:
        print("\nPor favor ingrese un input válido.")


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    
    try: 
        consulta_comparendos = int(input("Ingrese el número de comparendos a responder: "))
        lista, dt, dm = controller.req_6(control, consulta_comparendos)
        
        print(f"\n====================================== Req No. 6 Inputs ======================================\n"
                f"Número de Comparendos a Responder: {consulta_comparendos}\n"
                f"====================================== Req No. 6 Results ======================================\n"
                f"El tiempo de ejecución del requerimiento es: {dt} ms\n"
                f"La memoria usada del requerimiento es: {dm} kB\n"
                )
        
        for info in lt.iterator(lista):
            print(f"ID del vértice más cercano al comparendo: {info['id_vertice_cercano_comparendo']}\n"
                f"Gravedad del comparendo: {info['gravedad']}\n"
                f"Estación de policía más cercana: {info['estacion_mas_cercana']}\n"
                f"Distancia entre esquinas más cercanas de la estación al comparendo: {round(info['distancia'], 2)} km\n")
            # for arco in info['path']:
            #     camino = st.pop(arco)
            #     print(camino)
                
    except ValueError:
        print("\nPor favor ingrese un input válido.")
             
        
def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

def print_data():
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    num_comparendos = 402499
    primeros_ultimos_5_comparendos = [{"OBJECTID": 3638634, "FECHA_HORA": "2019-01-01T10:35:38Z", "MEDIO_DETECCION": "DEAP", "CLASE_VEHICULO": "AUTOMÓVIL", "TIPO_SERVICIO": "Particular", "INFRACCION": "C02"},
 {"OBJECTID": 3638635,  "FECHA_HORA": "2019-01-01T10:34:49Z", "MEDIO_DETECCION": "DEAP", "CLASE_VEHICULO": "AUTOMÓVIL", "TIPO_SERVICIO": "Particular", "INFRACCION": "C02" },
 {"OBJECTID": 3638636,  "FECHA_HORA": "2019-01-01T10:40:25Z",  "MEDIO_DETECCION": "DEAP", "CLASE_VEHICULO": "AUTOMÓVIL", "TIPO_SERVICIO": "Particular", "INFRACCION": "C02"},
 {"OBJECTID": 3638637,  "FECHA_HORA": "2019-01-01T10:36:18Z", "MEDIO_DETECCION": "DEAP", "CLASE_VEHICULO": "AUTOMÓVIL", "TIPO_SERVICIO": "Particular", "INFRACCION": "C02" },
 {"OBJECTID": 3638648, "FECHA_HORA": "2019-01-01T12:24:33Z",  "MEDIO_DETECCION": "DEAP", "CLASE_VEHICULO": "CAMPERO", "TIPO_SERVICIO": "Particular", "INFRACCION": "C02"  },
 {"OBJECTID": 20090507,  "FECHA_HORA": "2019-10-31T00:00:00Z", "MEDIO_DETECCION": "Tránsito", "CLASE_VEHICULO": "Campero", "TIPO_SERVICIO": "Particular", "INFRACCION": "D12" }, 
 {"OBJECTID": 20090508,  "FECHA_HORA": "2019-10-31T00:00:00Z",  "MEDIO_DETECCION": "Tránsito", "CLASE_VEHICULO": "Campero", "TIPO_SERVICIO": "Particular", "INFRACCION": "C38" }, 
 {"OBJECTID": 20090509, "FECHA_HORA": "2019-10-31T00:00:00Z",  "MEDIO_DETECCION": "Tránsito", "CLASE_VEHICULO": "Campero", "TIPO_SERVICIO": "Particular", "INFRACCION": "C38"  }, 
 {"OBJECTID": 20090510, "FECHA_HORA": "2019-10-31T00:00:00Z", "MEDIO_DETECCION": "Tránsito", "CLASE_VEHICULO": "Campero", "TIPO_SERVICIO": "Particular", "INFRACCION": "C38" }, 
 {"OBJECTID": 20090511, "FECHA_HORA": "2019-10-31T00:00:00Z",  "MEDIO_DETECCION": "Tránsito", "CLASE_VEHICULO": "Campero", "TIPO_SERVICIO": "Particular", "INFRACCION": "H03"}]
    total_estaciones_policia = 21
    primeros_ultimos_5_estaciones = [{
    "OBJECTID": 1,
    "EPODESCRIP": "Estación de Policía Antonio Nariño",
    "EPODIR_SITIO": "KR 24 18 90 SUR",
    "EPOLATITUD": 4.5856080360000533,
    "EPOLONGITU": -74.103134541999964,
    "EPOSERVICIO": "Tiene como finalidad asegurar y ejercer el control de la jurisdicción, prestar un servicio integral de vigilancia urbana y rural, desarrollar los procesos de prevención, disuasión, investigación y control de los delitos y contravenciones apoyados en la gestión territorial de la seguridad ciudadana con las autoridades locales político administrativas.",
    "EPOHORARIO": "24 horas - lunes a domingo",
    "EPOTELEFON": "3502150333",
    "EPOCELECTR": "mebog.e15@policia.gov.co",

},
{
    "OBJECTID": 2,
    "EPODESCRIP": "Estación de Policía Barrios Unidos",
    "EPODIR_SITIO": "AVENIDA CHILE 62 81",
    "EPOLATITUD": 4.6738119970000298,
    "EPOLONGITU": -74.081861781999976,
    "EPOSERVICIO": "Tiene como finalidad asegurar y ejercer el control de la jurisdicción, prestar un servicio integral de vigilancia urbana y rural, desarrollar los procesos de prevención, disuasión, investigación y control de los delitos y contravenciones apoyados en la gestión territorial de la seguridad ciudadana con las autoridades locales político administrativas.",
    "EPOHORARIO": "24 horas - lunes a domingo",
    "EPOTELEFON": "3002326359",
    "EPOCELECTR": "mebog.e12@policia.gov.co",
},
{
    "OBJECTID": 3,
    "EPODESCRIP": "Estación de Policía Bosa ",
    "EPODIR_SITIO": "CL 65 SUR 77N 23",
    "EPOLATITUD": 4.6001566120000348,
    "EPOLONGITU": -74.186787246999984,
    "EPOSERVICIO": "Tiene como finalidad asegurar y ejercer el control de la jurisdicción, prestar un servicio integral de vigilancia urbana y rural, desarrollar los procesos de prevención, disuasión, investigación y control de los delitos y contravenciones apoyados en la gestión territorial de la seguridad ciudadana con las autoridades locales político administrativas.",
    "EPOHORARIO": "24 horas - lunes a domingo",
    "EPOTELEFON": "3502150329",
    "EPOCELECTR": "mebog.e7@policia.gov.co",
},
{
    "OBJECTID": 4,
    "EPODESCRIP": "Estación de Policía Ciudad Bolívar",
    "EPODIR_SITIO": "DG 70 SUR 54 22",
    "EPOLATITUD": 4.5774781770000459,
    "EPOLONGITU": -74.164658612999972,
    "EPOSERVICIO": "Tiene como finalidad asegurar y ejercer el control de la jurisdicción, prestar un servicio integral de vigilancia urbana y rural, desarrollar los procesos de prevención, disuasión, investigación y control de los delitos y contravenciones apoyados en la gestión territorial de la seguridad ciudadana con las autoridades locales político administrativas.",
    "EPOHORARIO": "24 horas - lunes a domingo",
    "EPOTELEFON": "3203016935",
    "EPOCELECTR": "mebog.e19@policia.gov.co",
},
{
    "OBJECTID": 5,
    "EPODESCRIP": "Estación de Policía Engativá",
    "EPODIR_SITIO": "KR 78A 70 54",
    "EPOLATITUD": 4.6900110000000268,
    "EPOLONGITU": -74.102675999999974,
    "EPOSERVICIO": "Tiene como finalidad asegurar y ejercer el control de la jurisdicción, prestar un servicio integral de vigilancia urbana y rural, desarrollar los procesos de prevención, disuasión, investigación y control de los delitos y contravenciones apoyados en la gestión territorial de la seguridad ciudadana con las autoridades locales político administrativas.",
    "EPOHORARIO": "24 horas - lunes a domingo",
    "EPOTELEFON": "3502150296",
    "EPOCELECTR": "mebog.e10@policia.gov.co",
},
{
    "OBJECTID": 17,
    "EPODESCRIP": "Estación de Policía San Cristóbal",
    "EPODIR_SITIO": "AV 1 DE MAYO 1 90 ESTE",
    "EPOLATITUD": 4.5700270900000532,
    "EPOLONGITU": -74.085867518999976,
    "EPOSERVICIO": "Tiene como finalidad asegurar y ejercer el control de la jurisdicción, prestar un servicio integral de vigilancia urbana y rural, desarrollar los procesos de prevención, disuasión, investigación y control de los delitos y contravenciones apoyados en la gestión territorial de la seguridad ciudadana con las autoridades locales político administrativas.",
    "EPOHORARIO": "24 horas - lunes a domingo",
    "EPOTELEFON": "3502150328",
    "EPOCELECTR": "mebog.e4@policia.gov.co",
},
{
    "OBJECTID": 18,
    "EPODESCRIP": "Estación de Policía Rafael Uribe Uribe",
    "EPODIR_SITIO": "CL 27 SUR 24H 39",
    "EPOLATITUD": 4.5853832040000384,
    "EPOLONGITU": -74.110556326999983,
    "EPOSERVICIO": "Tiene como finalidad asegurar y ejercer el control de la jurisdicción, prestar un servicio integral de vigilancia urbana y rural, desarrollar los procesos de prevención, disuasión, investigación y control de los delitos y contravenciones apoyados en la gestión territorial de la seguridad ciudadana con las autoridades locales político administrativas.",
    "EPOHORARIO": "24 horas - lunes a domingo",
    "EPOTELEFON": "3203024427",
    "EPOCELECTR": "mebog.e18@policia.gov.co",
},
{
    "OBJECTID": 19,
    "EPODESCRIP": "Estación de Policía Aeropuerto",
    "EPODIR_SITIO": "AV EL DORADO 103 09",
    "EPOLATITUD": 4.6949315780000234,
    "EPOLONGITU": -74.141776145999984,
    "EPOSERVICIO": "Tiene como finalidad asegurar y ejercer el control de la jurisdicción, prestar un servicio integral de vigilancia urbana y rural, desarrollar los procesos de prevención, disuasión, investigación y control de los delitos y contravenciones apoyados en la gestión territorial de la seguridad ciudadana con las autoridades locales político administrativas.",
    "EPOHORARIO": "24 horas - lunes a domingo",
    "EPOTELEFON": "4397070",
    "EPOCELECTR": "mebog.e21@policia.gov.co",
},
{
    "OBJECTID": 20,
    "EPODESCRIP": "Estación de Policía Terminal",
    "EPODIR_SITIO": "DG 22A 68D 90 MODULO 5 LOCAL 101",
    "EPOLATITUD": 4.6511306330000366,
    "EPOLONGITU": -74.114540308999949,
    "EPOSERVICIO": "Tiene como finalidad asegurar y ejercer el control de la jurisdicción, prestar un servicio integral de vigilancia urbana y rural, desarrollar los procesos de prevención, disuasión, investigación y control de los delitos y contravenciones apoyados en la gestión territorial de la seguridad ciudadana con las autoridades locales político administrativas.",
    "EPOHORARIO": "24 horas - lunes a domingo",
    "EPOTELEFON": "4233630",
    "EPOCELECTR": "mebog.e22@policia.gov.co",
},
{
    "OBJECTID": 21,
    "EPODESCRIP": "Estación de Policía Santa Fe",
    "EPODIR_SITIO": "KR 5 29 40",
    "EPOLATITUD": 4.6152830000000336,
    "EPOLONGITU": -74.066363999999965,
    "EPOSERVICIO": "Tiene como finalidad asegurar y ejercer el control de la jurisdicción, prestar un servicio integral de vigilancia urbana y rural, desarrollar los procesos de prevención, disuasión, investigación y control de los delitos y contravenciones apoyados en la gestión territorial de la seguridad ciudadana con las autoridades locales político administrativas.",
    "EPOHORARIO": "24 horas - lunes a domingo",
    "EPOTELEFON": "3203021449",
    "EPOCELECTR": "mebog.e3@policia.gov.co",
}
]
    total_vertices = 228045
    primeros_ultimos_5_vertices = [{"id" : 0, "long": -74.08921298299998, "lat": 4.582989396000016},
{"id" : 1, "long": -74.08952746199998, "lat": 4.582560966000017},
{"id" : 2, "long": -74.093892202, "lat": 4.576679366000008},
{"id" : 3, "long": -74.09408026199998, "lat": 4.576433936999991},
{"id" : 4, "long": -74.09451399300002, "lat": 4.57581709599998},
{"id": 228041, "long": -74.16991089999999, "lat": 4.671858950000001},
{"id": 228042, "long": -74.14202318000002, "lat": 4.598409520000018},
{"id": 228043, "long": -74.12012897, "lat": 4.714881069999989},
{"id": 228044, "long": -74.13447882000003, "lat": 4.606624450000027},
{"id": 228045, "long": -74.17196072000002, "lat": 4.632215770000016}
]

    print(tabulate(primeros_ultimos_5_comparendos, headers="keys", tablefmt="psql"))
    print(tabulate(primeros_ultimos_5_estaciones, headers="keys", tablefmt="psql"))
    print(tabulate(primeros_ultimos_5_vertices, headers="keys", tablefmt="psql"))
    print(f"Total de comparendos: {num_comparendos}")
    print(f"Total de estaciones de policia: {total_estaciones_policia}")
    print(f"Total de vertices: {total_vertices}")
    
# main del reto
def thread_cycle():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    
    
    while working:
        print_menu()
        try: 
            inputs = input('Seleccione una opción para continuar\n')
            if int(inputs) == 1:
                print("Cargando información de los archivos ....\n")
                data = load_data(control)
                print_data()
            elif int(inputs) == 2:
                print_req_1(control)

            elif int(inputs) == 3:
                print_req_2(control)

            elif int(inputs) == 4:
                print_req_3(control)

            elif int(inputs) == 5:
                print_req_4(control)

            elif int(inputs) == 6:
                print_req_5(control)

            elif int(inputs) == 7:
                print_req_6(control)

            elif int(inputs) == 8:
                print_req_7(control)

            elif int(inputs) == 9:
                print_req_8(control)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
            
            else:
                print("\nOpción errónea, vuelva a elegir.\n")
                
        except ValueError:
            print("\nOpción errónea, vuelva a elegir.\n")
            traceback.print_exc()
    
    sys.exit(0)
    
    
if __name__ == "__main__":
    threading.stack_size(67108864) 
    sys.setrecursionlimit(2**20)  
    thread = threading.Thread(target=thread_cycle) 
    thread.start() 