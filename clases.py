import matplotlib.pyplot as plt 
import cv2 
import pydicom 
import os
import numpy as np 
import nibabel as nib

class DicomFile:
    def __init__(self, nombre, edad, ID, imagen_nifti):
        self.nombre = nombre
        self.edad = edad
        self.ID = ID
        self.imagen = imagen_nifti
        self.clave = 1
        
    def extraer_info_paciente_dicom(self, ruta_dicom):
        try:
            dicom_data = pydicom.dcmread(ruta_dicom)
            nombre = dicom_data.PatientName
            edad = dicom_data.PatientAge
            ID = dicom_data.PatientID
            return {"Nombre": nombre, "Edad": edad, "ID": ID}
        
        
        except Exception as e:
            print("-----------------------------------------------------")
            print(f"Error al procesar el archivo DICOM {ruta_dicom}: {e}")
            print("-----------------------------------------------------")
            return None

    def extraer_info_pacientes(carpeta_dicom):
        pacientes = []

        # Iterar sobre todos los archivos en la carpeta DICOM
        for raiz, _, archivos in os.walk(carpeta_dicom):
            for archivo in archivos:
                if archivo.endswith('.dcm'):
                    ruta_dicom = os.path.join(raiz, archivo)
                    paciente = DicomFile.extraer_info_paciente_dicom(ruta_dicom)
                    if paciente:
                        pacientes.append(paciente)

        return pacientes
        
    def convertir_a_nifti(self):
        try:
            dicom_data = pydicom.dcmread(self.ruta_dicom)
            imagen_nifti = nib.Nifti1Image(dicom_data.pixel_array, dicom_data.get_affine())
            return imagen_nifti
        except Exception as e:
            print("--------------------------------------------------------")
            print(f"Error al convertir DICOM a NIfTI {self.ruta_dicom}: {e}")
            print("--------------------------------------------------------")
            return None
        
    def convert_directory(carpeta_entrada, carpeta_salida):
        try:
            os.makedirs(carpeta_salida, exist_ok=True)
            for root, _, files in os.walk(carpeta_entrada):
                for file in files:
                    if file.endswith('.dcm'):
                        input_path = os.path.join(root, file)
                        output_path = os.path.join(carpeta_salida, file.replace('.dcm', '.nii.gz'))
                        dicom_file = DicomFile(input_path)
                        if dicom_file.imagen_nifti:
                            nib.save(dicom_file.imagen_nifti, output_path)
        except Exception as e:
            print("-------------------------------------------------")
            print(f"Error al convertir directorio DICOM a NIfTI: {e}")
            print("-------------------------------------------------")
        
    def imagenDicom_con_rotacion(ruta_entrada, ruta_salida, angulo_rotacion):
        if not os.path.exists(ruta_salida):
            os.makedirs(ruta_salida)
        # Lista los archivos DICOM en la carpeta de entrada
        for archivo in os.listdir(ruta_entrada):
            if archivo.endswith('.dcm'):
                archivo_entrada = os.path.join(ruta_entrada, archivo)
                archivo_salida = os.path.join(ruta_salida, archivo)
                print("------------------------------------------")
                print("Procesando archivo DICOM:", archivo_entrada)
                print("Guardando imagen rotada en:", archivo_salida)
                dicom = pydicom.dcmread(archivo_entrada)
                imagen_array = dicom.pixel_array
            
                # Calcular el centro de la imagen
                rows, cols = imagen_array.shape
                center = (cols / 2, rows / 2)
                
                # Calcular la matriz de rotación
                matriz_rotacion = cv2.getRotationMatrix2D(center, angulo_rotacion, 1)
                
                # Aplicar la transformación de rotación a la imagen
                imagenRotada = cv2.warpAffine(imagen_array, matriz_rotacion, (cols, rows))
                
                try:
                    dicom.PixelData = imagenRotada.tobytes()
                    dicom.save_as(archivo_salida)
                    print("----------------------------------------------------------")
                    print("Imagen rotada guardada correctamente como:", archivo_salida)
                except Exception as e:
                    print("------------------------------------------")
                    print("Error al guardar la imagen rotada:", str(e))
                    print("------------------------------------------")


class ImagenFile:
    def __init__(self, ruta):
        self.ruta = ruta

    def cargar_imagen(self):
        imagen = cv2.imread(self.ruta)
        return imagen

    def guardar_imagen(self, imagen, ruta_destino):
        cv2.imwrite(ruta_destino, imagen)

    def binarizacion_morfologia(self, umbral, tamano_kernel):
        imagen = self.cargar_imagen()

        # Convertir a escala de grises
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

        # Aplicar binarización
        _, imagen_binarizada = cv2.threshold(imagen_gris, umbral, 255, cv2.THRESH_BINARY)

        # Aplicar transformación morfológica
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (tamano_kernel, tamano_kernel))
        imaEro = cv2.erode(imagen_binarizada,kernel,iterations = 1)

        # Añadir texto a la imagen
        texto = f"Imagen binarizada (umbral: {umbral}, tamano de kernel: {tamano_kernel})"
        cv2.putText(imaEro, texto,  (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return imaEro