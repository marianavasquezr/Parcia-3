import matplotlib.pyplot as plt 
import cv2 
import pydicom 
import os
import numpy as np 
import nibabel as nib
import dicom2nifti

class DicomFile:
    def __init__(self):
        self.nombre = ""
        self.edad = 0
        self.ID = 0
        self.ruta_imagenNift = ""
        self.clave = 1
        
    def extraer_info_paciente_dicom(self, ruta_dicom):
        try:
            dicom_data = pydicom.dcmread(ruta_dicom)
            self.nombre = dicom_data.PatientName
            self.edad = dicom_data.PatientAge
            self.ID = dicom_data.PatientID
            #self.ruta_imagenNift = self.convert_directory(carpeta_dicom, carpeta_nifti)
            return {"Nombre": self.nombre, "Edad": self.edad, "ID": self.ID }


        except Exception as e:
            print("-----------------------------------------------------")
            print(f"Error al procesar el archivo DICOM {ruta_dicom}: {e}")
            print("-----------------------------------------------------")
            return None
        
    def convert_directory(self,ruta_dicom, carpeta_nifti):
        try:
            os.makedirs(carpeta_nifti, exist_ok=True)
            dicom2nifti.convert_directory(ruta_dicom,carpeta_nifti)
            ruta_carpetaNifti = os.path.abspath(carpeta_nifti)
            return ruta_carpetaNifti
        except Exception as e:
            print(f"Error al convertir directorio DICOM a NIfTI: {e}")


    def extraer_info_pacientes(self, carpeta_dicom):
        pacientes = []

        # Iterar sobre todos los archivos en la carpeta DICOM
        #raiz representa la ruta del directorio actual, _ es una lista de subdirectorios (que no necesitamos en este caso), y archivos es una lista de archivos en el directorio actual.
        for raiz, _, archivos in os.walk(carpeta_dicom):
            for archivo in archivos:
                if archivo.endswith('.dcm'):
                    ruta_dicom = os.path.join(raiz, archivo)
                    paciente = self.extraer_info_paciente_dicom(ruta_dicom)
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
        

        
    def imagenDicom_con_rotacion(self, ruta_entrada, ruta_salida, angulo_rotacion):
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