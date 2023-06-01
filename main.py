from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QFileDialog
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui_main.ui', self)
        self.pushButton_cargar_img.clicked.connect(self.seleccionar_archivo)
        
    def mostrar_img(self, elemento, img):
        figure = plt.figure()
        plot = figure.add_subplot(111)
        plot.imshow(img)
        plot.axis('off')
        canvas = FigureCanvas(figure)
        canvas.draw()
        elemento.addWidget(canvas)

    def leer_img(self, ruta):
        img = cv2.imread(ruta)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.mostrar_img(self.verticalLayout_img_original, img_rgb)
        self.mostrar_img(self.verticalLayout_img_resultante, img_rgb)

    def seleccionar_archivo(self):
        archivo = QFileDialog()
        archivo.setWindowTitle("Seleccionar archivo")
        archivo.setFileMode(QFileDialog.ExistingFile)
        if archivo.exec_():
            ruta = archivo.selectedFiles()
            print(ruta[0])
            self.leer_img(ruta[0])

app = QApplication([])
ventana = VentanaPrincipal()
ventana.show()
app.exec()
