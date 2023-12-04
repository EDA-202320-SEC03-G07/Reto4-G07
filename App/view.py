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
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    return controller.new_controller()


def print_menu():
    print("Bienvenido")
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
    #TODO: Realizar la carga de datos
    controller.load_data(control)


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    try:
        consulta_camaras = int(input("Ingrese el número de cámaras a poner: "))
        consulta_localidad = input("Ingrese la localidad a consultar: ")
        
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

        # Convert adjacency_matrix and headers to DataFrame
        df = pd.DataFrame(adjacency_matrix, columns=headers, index=headers)

        
        print(f"\n====================================== Req No. 3 Inputs ======================================\n"
                f"Número de Cámaras Solicitadas: {consulta_camaras}\n"
                f"Consulta Localidad: {consulta_localidad}\n"
                f"====================================== Req No. 3 Results ======================================\n"
                f"Total de Cámaras Puestas: {total_camaras}\n"
                f"Identificadores de las Cámaras: {id_vertices}\n"
                f"Extensión de la Red de Cámaras: {round(extension, 2)} km\n"
                f"Costo de la Red de Cámaras: {round(costo, 2)} COP\n"
                f"Conecciones entre Cámaras:\n{df}\n"
                f"El tiempo de ejecución del requerimiento es: {dt} ms\n"
                f"La memoria usada del requerimiento es: {dm} kB\n"
                
        )
    except ValueError:
        print("Please enter valid input for the number of cameras.")
def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
    Function that prints the solution of Requirement 5 to the console
    """
    try: 
        consulta_camaras  = int(input("Ingrese el número de cámaras a poner: "))
        consulta_clase_vehiculo = input("Ingrese la clase de vehículo a consultar: ")
        
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

        # Convert adjacency_matrix and headers to DataFrame
        df = pd.DataFrame(adjacency_matrix, columns=headers, index=headers)
        



        print(f"\n====================================== Req No. 2 Inputs ======================================\n"
                f"Número de Cámaras Solicitadas: {consulta_camaras}\n"
                f"Consulta Clase de Vehículo: {consulta_clase_vehiculo}\n"
                f"====================================== Req No. 2 Results ======================================\n"
                f"Total de Cámaras Puestas: {total_camaras}\n"
                f"Identificadores de las Cámaras: {id_vertices}\n"
                f"Extensión de la Red de Cámaras: {round(extension, 2)} km\n"
                f"Costo de la Red de Cámaras: {round(costo, 2)} COP\n"
                f"Conecciones entre Cámaras:\n{df}\n"
                f"El tiempo de ejecución del requerimiento es: {dt} ms\n"
                f"La memoria usada del requerimiento es: {dm} kB\n"
                
        )
        
        # Printing adjacency matrix
        

    except ValueError:
        print("Please enter valid input for the number of cameras.")

    
    # except Exception as exp:
    #     print(f"Error en la ejecución del requerimiento 5: {exp}\n")


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    


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

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
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
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
