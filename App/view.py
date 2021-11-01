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

import datetime
from typing import List
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Contar los avistamientos en una ciudad")
    print("3- Contar los avistamientos por duración")
    print("4- Contar avistamientos por Hora/Minutos del día")
    print("5- Contar los avistamientos en un rango de fechas")
    print("6- Contar los avistamientos de una Zona Geográfica")
    print("7- Visualizar los avistamientos de una zona geográfica - BONO")
    print("0- Salir")


def initCatalog():
    """
    Inicializa el catalogo
    """
    return controller.initCatalog()



def cargarData(catalog):
    """
    Carga la información en la estructura de datos
    """
    controller.cargarData(catalog)




def printReq1(result, ciudad):
    print("\nTotal de ciudades donde se han reportado avistamientos: ",result[0])
    print("\nLa ciudad con más avistamientos es: \n")
    print(me.getKey(result[1][0])," : ",result[1][1])
    print("\nTotal de avistamientos en la ciudad ",ciudad," : ",result[2])
    print('\nPrimeros tres avistamientos: \n')     
    for avistamiento in lt.iterator(result[3]):
        print("\tFecha: ",avistamiento["datetime"])
        print("\tCiudad: ",avistamiento["city"])
        print("\tPaís: ",avistamiento["country"])
        print("\tForma: ",avistamiento["shape"])
        print("\tDuración (segundos): ",avistamiento["duration (seconds)"],"\n")
    print('\nÚltimos tres avistamientos: \n')     
    for avistamiento in lt.iterator(result[4]):
        print("\tFecha: ",avistamiento["datetime"])
        print("\tCiudad: ",avistamiento["city"])
        print("\tPaís: ",avistamiento["country"])
        print("\tForma: ",avistamiento["shape"])
        print("\tDuración (segundos): ",avistamiento["duration (seconds)"],"\n")



def printReq3(result):
    print("\nEl avistamiento más tardío que se tiene registrado es: \n")
    print(result[0]," : ",result[1])
    print("\nEn el rango de horas ingresado por el usuario hay un total de ",result[2]," avistamientos. ")
    print('Primeros tres avistamientos: \n')     
    for avistamiento in lt.iterator(result[3]):
        print("\tFecha: ",avistamiento["datetime"])
        print("\tCiudad: ",avistamiento["city"])
        print("\tPaís: ",avistamiento["country"])
        print("\tForma: ",avistamiento["shape"])
        print("\tDuración (segundos): ",avistamiento["duration (seconds)"],"\n")
    print('\nÚltimos tres avistamientos: \n')     
    for avistamiento in lt.iterator(result[4]):
        print("\tFecha: ",avistamiento["datetime"])
        print("\tCiudad: ",avistamiento["city"])
        print("\tPaís: ",avistamiento["country"])
        print("\tForma: ",avistamiento["shape"])
        print("\tDuración (segundos): ",avistamiento["duration (seconds)"],"\n")






def printReq4(result):
    print("\nEl avistamiento más antiguo que se tiene registrado es: \n")
    print(result[0]," : ",result[1])
    print("\nEn el rango de fechas ingresado por el usuario hay un total de ",result[2]," avistamientos. ")
    print('Primeros tres avistamientos: \n')     
    for avistamiento in lt.iterator(result[3]):
        print("\tFecha: ",avistamiento["datetime"])
        print("\tCiudad: ",avistamiento["city"])
        print("\tPaís: ",avistamiento["country"])
        print("\tForma: ",avistamiento["shape"])
        print("\tDuración (segundos): ",avistamiento["duration (seconds)"],"\n")
    print('\nÚltimos tres avistamientos: \n')     
    for avistamiento in lt.iterator(result[4]):
        print("\tFecha: ",avistamiento["datetime"])
        print("\tCiudad: ",avistamiento["city"])
        print("\tPaís: ",avistamiento["country"])
        print("\tForma: ",avistamiento["shape"])
        print("\tDuración (segundos): ",avistamiento["duration (seconds)"],"\n")






catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        cargarData(catalog)
        print('\nTotal avistamientos cargados: ' + str(controller.avistamientosSize(catalog)))
        print('Altura del arbol: ' + str(controller.indexHeight(catalog['dateIndex'])))
        print('Elementos en el arbol: ' + str(controller.indexSize(catalog['dateIndex'])))
        primerosUFOS = controller.primerosAvistamientos(catalog, 5)
        ultimosUFOS = controller.ultimosAvistamientos(catalog, 5)
        
        print('\nPrimeros cinco avistamientos cargados: \n')     
        for avistamiento in lt.iterator(primerosUFOS):
            print("\tFecha: ",avistamiento["datetime"])
            print("\tCiudad: ",avistamiento["city"])
            print("\tEstado: ",avistamiento["state"])
            print("\tPaís: ",avistamiento["country"])
            print("\tForma: ",avistamiento["shape"])
            print("\tDuración (segundos): ",avistamiento["duration (seconds)"],"\n")

        print('\nÚltimos cinco avistamientos cargados: \n')     
        for avistamiento in lt.iterator(ultimosUFOS):
            print("\tFecha: ",avistamiento["datetime"])
            print("\tCiudad: ",avistamiento["city"])
            print("\tEstado: ",avistamiento["state"])
            print("\tPaís: ",avistamiento["country"])
            print("\tForma: ",avistamiento["shape"])
            print("\tDuración (segundos): ",avistamiento["duration (seconds)"],"\n")
        

        
    elif int(inputs[0]) == 2:
        ciudad = input("Ingrese el nombre de la ciudad a consultar: ")
        result = controller.contarAvistamientosCiudad(catalog, ciudad)
        printReq1(result, ciudad)

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        print("Para el rango de horas del día del que quiera listar los avistamientos ingrese: ")
        horaInicial = int(input("Hora inicial del rango: "))
        minutoInicial = int(input("Minuto inicial del rango: "))
        horaFinal = int(input("Hora final del rango: "))
        minutoFinal = int(input("Minuto final del rango: "))
        result = controller.contarAvistamientosHora(catalog,horaInicial,minutoInicial,horaFinal,minutoFinal)
        printReq3(result)

    elif int(inputs[0]) == 5:
        print("Para el rango de fechas del que quiera listar los avistamientos ingrese: ")
        diaInicial = int(input("Día inicial del rango: "))
        mesInicial = int(input("Mes inicial del rango: "))
        anioInicial = int(input("Hora inicial del rango: "))
        diaFinal = int(input("Día final del rango: "))
        mesFinal = int(input("Mes final del rango: "))
        anioFinal = int(input("Hora final del rango: "))
        result = controller.contarAvistamientosDia(catalog,diaInicial,mesInicial,anioInicial,diaFinal,mesFinal,anioFinal)
        printReq4(result)

    elif int(inputs[0]) == 6:
        print("Para la zona geográfica de la que quiera listar los avistamientos ingrese: ")
        longInicial = float(input("Longitud mínima del rango: "))
        longFinal = float(input("Longitud máxima del rango: "))
        latInicial = float(input("Latitud mínima del rango: "))
        latFinal = float(input("Latitud máxima del rango: "))
        result = controller.contarAvistamientosZona(catalog,longInicial,latInicial,longFinal,latFinal)
        printReq3(result)

    elif int(inputs[0]) == 7:
        pass

    else:
        sys.exit(0)
sys.exit(0)
