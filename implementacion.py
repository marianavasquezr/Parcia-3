from clases import DicomFile, ImagenFile
import matplotlib as plt 
import cv2 
import pydicom 
import os
import numpy as np 
import nibabel as nib
pacientes = {}
archivos = {}

while True:
    print("\n----------------Menú Principal:--------------------")
    print("1. Ingresar Paciente (DICOM)")
    print("2. Ingresar Imagen (JPG/PNG)")
    print("3. Realizar Transformación de Rotación")
    print("4. Realizar Binarización y Transformación Morfológica")
    print("5. Salir")
    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == "1":
        # Implementa la opción para ingresar pacientes con archivos DICOM
        # Ruta de la carpeta que contiene los archivos DICOM
        carpeta_dicom = input("Ingrese la ruta de la carpeta de archivos dicom: ")

        # Extraer información de los pacientes
        pacientes = DicomFile.extraer_info_pacientes(carpeta_dicom)

        # Mostrar información de los pacientes
        for idx, paciente in enumerate(pacientes, start=1):
            print(f"Paciente {idx}:")
            print(f"Nombre: {paciente['Nombre']}")
            print(f"Edad: {paciente['Edad']}")
            print(f"ID: {paciente['ID']}")
            print("-" * 30)
        
    elif opcion == "2":
        # Implementa la opción para ingresar imágenes JPG o PNG
        ruta_imagen = input("Ingrese la ruta de la imagen (JPG/PNG): ")
        if os.path.exists(ruta_imagen):
            archivos[ruta_imagen] = ImagenFile(ruta_imagen)
            print("---------------------------")
            print("Imagen ingresada con éxito.")
            print("---------------------------")
            
        else:
                print("------------------------------------------------------")
                print("La ruta de la imagen no es válida. Inténtelo de nuevo.")
                print("------------------------------------------------------")
        
    elif opcion == "3":
        # Implementa la opción para realizar la transformación de rotación
        pass

    
    elif opcion == "4":
        # Implementa la opción para realizar binarización y transformación morfológica
        pass
        
    elif opcion == "5":
            print("-----------")
            print("Saliendo...")
            print("-----------")
            break
    
    else:
            print("------------------------------------------------------")
            print("Opción no válida. Por favor, ingrese un número válido.")
            print("------------------------------------------------------")
