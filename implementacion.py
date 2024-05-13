from clases import DicomFile, ImagenFile
import matplotlib as plt 
import cv2 
import pydicom 
import os
import numpy as np 
import nibabel as nib
pac = {}
archivos = {}
clave = 0

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
        ruta_dicom = input("Ingrese la ruta de la carpeta de archivos dicom: ")
        if os.path.exists(ruta_dicom):
            clave += 1
            paciente = DicomFile()
            info = paciente.extraer_info_pacientes(ruta_dicom)
            # Extraer información de los pacientes
            print(f"Nombre: {info[0]['Nombre']}")
            print(f"Edad: {info[0]['Edad']}")
            print(f"ID: {info[0]['ID']}")
            print("-" * 30)
            pac[clave] = info
            print(pac)
        
    elif opcion == "2":
        # Implementa la opción para ingresar imágenes JPG o PNG
        ruta_imagen = input("Ingrese la ruta de la imagen (JPG/PNG): ")
        if os.path.exists(ruta_imagen):
            clave += 1
            archivos[clave] = ImagenFile(ruta_imagen)
            print("---------------------------")
            print("Imagen ingresada con éxito.")
            print("---------------------------")
            print(archivos)
            
        else:
                print("------------------------------------------------------")
                print("La ruta de la imagen no es válida. Inténtelo de nuevo.")
                print("------------------------------------------------------")
        
    elif opcion == "3":
        # Implementa la opción para realizar la transformación de rotación
        # Implementa la opción para realizar la transformación de rotación
        ruta_entrada = input("Por favor, ingresa la ruta de la carpeta que contiene los archivos DICOM de entrada: ")
        ruta_salida = input("Por favor, ingresa la ruta de la carpeta donde deseas guardar las imágenes rotadas: ")
        angulo_rotacion = int(input("Por favor, ingresa el ángulo de rotación (90, 180 o 270 grados): "))
        if angulo_rotacion in [90, 180, 270]:
             DicomFile.imagenDicom_con_rotacion(ruta_entrada, ruta_salida, angulo_rotacion)
        else:
            print("------------------------------------------------------------")
            print("Ángulo de rotación no válido. Debe ser 90, 180 o 270 grados.")
            print("------------------------------------------------------------")

    elif opcion == "4":
        # Implementa la opción para realizar binarización y transformación morfológica
        ruta_imagen = input("Ingrese la ruta de la imagen (JPG o PNG): ")
        imagen = ImagenFile(ruta_imagen)

        # Solicitar al usuario el umbral y el tamaño del kernel
        umbral = int(input("Ingrese el umbral para la binarización (0-255): "))
        tamano_kernel = int(input("Ingrese el tamaño del kernel para la morfología: "))

        # Aplicar binarización y transformación morfológica
        imagen_procesada = imagen.binarizacion_morfologia(umbral, tamano_kernel)

        # Guardar la imagen procesada
        ruta_guardado = input("Ingrese la ruta de destino para guardar la imagen procesada: ")
        imagen.guardar_imagen(imagen_procesada, ruta_guardado)
        print("---------------------------------------------------------")
        print("Imagen procesada guardada exitosamente en:", ruta_guardado)
        print("---------------------------------------------------------")
        
    elif opcion == "5":
            print("-----------")
            print("Saliendo...")
            print("-----------")
            break
    
    else:
            print("------------------------------------------------------")
            print("Opción no válida. Por favor, ingrese un número válido.")
            print("------------------------------------------------------")
