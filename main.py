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

    def mostrar_histograma(self, elemento, canal, color_grafico):
        figure = plt.figure()
        plot = figure.add_subplot(111)
        plot.hist(canal.ravel(), bins=256, color=color_grafico, alpha=0.6)
        # plot.xlabel('Valor de Píxel')
        # plot.ylabel('Frecuencia')
        # plot.imshow(img)
        # plot.show()
        plot.axis('off')
        canvas = FigureCanvas(figure)
        canvas.draw()
        elemento.addWidget(canvas)

        # plt.hist(canal.ravel(), bins=256, color='red', alpha=0.6)
        # plt.title('Histograma del Canal R')


    def leer_img(self, ruta):
        img = cv2.imread(ruta)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # muestro original
        self.mostrar_img(self.verticalLayout_img_original, img_rgb)
        # extraigo espectros
        canal_r, canal_g, canal_b = cv2.split(img_rgb)
        # muestro espectros
        self.mostrar_img(self.verticalLayout_canal_r, canal_r)
        self.mostrar_img(self.verticalLayout_canal_g, canal_g)
        self.mostrar_img(self.verticalLayout_canal_b, canal_b)
        # genero histogramas
        self.mostrar_histograma(self.verticalLayout_histograma_r, canal_r, 'red')
        self.mostrar_histograma(self.verticalLayout_histograma_g, canal_g, 'green')
        self.mostrar_histograma(self.verticalLayout_histograma_b, canal_b, 'blue')
        # muestro resultante
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
