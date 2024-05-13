from clases import DicomFile
pacientes = {}
archivos = {}

while True:
    print("\nMenú Principal:")
    print("1. Ingresar Paciente (DICOM)")
    print("2. Ingresar Imagen (JPG/PNG)")
    print("3. Realizar Transformación de Rotación")
    print("4. Realizar Binarización y Transformación Morfológica")
    print("5. Salir")
    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == "1":
        # Implementa la opción para ingresar pacientes con archivos DICOM
        pass
        
    elif opcion == "2":
        # Implementa la opción para ingresar imágenes JPG o PNG
        pass
        
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
