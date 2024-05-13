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
        
    def extraer_info_paciente_dicom(ruta_dicom):
        try:
            dicom_data = pydicom.dcmread(ruta_dicom)
            nombre = dicom_data.PatientName
            edad = dicom_data.PatientAge
            ID = dicom_data.PatientID
            return {"Nombre": nombre, "Edad": edad, "ID": ID}
        
        except Exception as e:
            print(f"Error al procesar el archivo DICOM {ruta_dicom}: {e}")
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

class ImagenFile:
    def __init__(self, ruta):
        self.ruta = ruta

    def cargar_imagen(self):
        imagen = cv2.imread(self.ruta)
        return imagen

    def guardar_imagen(self, imagen, ruta_destino):
        cv2.imwrite(ruta_destino, imagen)

    def binarizacion_morfologia(self, umbral, tamano_kernel):
        pass