from PyQt5.QtWidgets import QFileDialog
import cv2
import matplotlib.pyplot as plt

def leer_img(ruta):
    img = cv2.imread(ruta)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.show()

def seleccionar_archivo():
    archivo = QFileDialog()
    archivo.setWindowTitle("Seleccionar archivo")
    archivo.setFileMode(QFileDialog.ExistingFile)
    if archivo.exec_(): 
        ruta = archivo.selectedFiles()
        print(ruta[0])
        leer_img(ruta[0])

