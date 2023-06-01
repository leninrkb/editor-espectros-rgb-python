from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QFileDialog
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class VentanaPrincipal(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        uic.loadUi('gui_main.ui', self) 
        self.modificado_canal_r = False
        self.modificado_canal_g = False
        self.modificado_canal_b = False
        self.pushButton_aplicar_cambios.setEnabled(False) 
        self.pushButton_guardar_resultante.setEnabled(False) 
        self.pushButton_aplicar_cambios.clicked.connect(self.aplicar_cambios) 
        self.pushButton_cargar_img.clicked.connect(self.seleccionar_archivo)
        self.pushButton_guardar_resultante.clicked.connect(self.guardar_resultante)
        self.horizontalSlider_valor_r.valueChanged.connect(self.nuevo_valor_slider_r)
        self.horizontalSlider_valor_g.valueChanged.connect(self.nuevo_valor_slider_g)
        self.horizontalSlider_valor_b.valueChanged.connect(self.nuevo_valor_slider_b)

    
    def guardar_resultante(self):
        cv2.imwrite('img_resultante.jpg',self.nueva_imagen)

    def nuevo_valor_slider_r(self, valor): 
        self.nuevo_canal_r = np.clip(self.canal_r + valor, 0, 255)
        self.modificado_canal_r = True
        self.pushButton_aplicar_cambios.setEnabled(True) 
        print('cambio r')

    def nuevo_valor_slider_g(self, valor): 
        self.pushButton_aplicar_cambios.setEnabled(True) 
        self.nuevo_canal_g = np.clip(self.canal_g + valor, 0, 255) 
        self.modificado_canal_g = True
        print('cambio g')

    def nuevo_valor_slider_b(self, valor): 
        self.pushButton_aplicar_cambios.setEnabled(True) 
        self.nuevo_canal_b = np.clip(self.canal_b + valor, 0, 255)
        self.modificado_canal_b = True
        print('cambio b')

    def mostrar_resultante(self):
        self.nueva_imagen = cv2.merge((self.nuevo_canal_r, self.nuevo_canal_g, self.nuevo_canal_b))
        self.mostrar_img(self.verticalLayout_img_resultante, self.nueva_imagen)

    def aplicar_cambios(self):
        if self.modificado_canal_r:
            self.mostrar_img(self.verticalLayout_canal_r, self.nuevo_canal_r)
            self.mostrar_histograma(self.verticalLayout_histograma_r, self.nuevo_canal_r,'red')
            print('hist r')
        if self.modificado_canal_g:
            self.mostrar_img(self.verticalLayout_canal_g, self.nuevo_canal_g)
            self.mostrar_histograma(self.verticalLayout_histograma_g, self.nuevo_canal_g,'green')
            print('hist g')
        if self.modificado_canal_b:
            self.mostrar_img(self.verticalLayout_canal_b, self.nuevo_canal_b)
            self.mostrar_histograma(self.verticalLayout_histograma_b, self.nuevo_canal_b,'blue')
            print('hist b')
        self.mostrar_resultante()
        self.pushButton_aplicar_cambios.setEnabled(False)
        self.pushButton_guardar_resultante.setEnabled(True) 
        self.modificado_canal_r = False
        self.modificado_canal_g = False
        self.modificado_canal_b = False

    def mostrar_img(self, elemento, img):
        figure = plt.figure()
        plot = figure.add_subplot(111)
        plot.imshow(img)
        plot.axis('off')
        canvas = FigureCanvas(figure)
        canvas.draw()
        index = elemento.count()
        if index == 0:
            elemento.addWidget(canvas)
        else:
            index = index - 1
            widget = elemento.takeAt(index).widget()
            widget.deleteLater()
            elemento.addWidget(canvas)

    def mostrar_histograma(self, elemento, canal, color_grafico):
        figure = plt.figure()
        plot = figure.add_subplot(111)
        plot.hist(canal.ravel(), bins=256, color=color_grafico, alpha=0.6)
        plot.set_xlabel('Valor de Píxel')
        canvas = FigureCanvas(figure)
        canvas.draw()
        index = elemento.count()
        if index == 0:
            elemento.addWidget(canvas)
        else:
            index = index - 1
            widget = elemento.takeAt(index).widget()
            widget.deleteLater()
            elemento.addWidget(canvas)


    def leer_img(self, ruta):
        img = cv2.imread(ruta)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # muestro original
        self.mostrar_img(self.verticalLayout_img_original, img_rgb)
        # extraigo espectros y creo los canales 
        self.canal_r, self.canal_g, self.canal_b = cv2.split(img_rgb)
        self.nuevo_canal_r = self.canal_r
        self.nuevo_canal_g = self.canal_g
        self.nuevo_canal_b = self.canal_b
        # muestro espectros
        self.mostrar_img(self.verticalLayout_canal_r, self.canal_r)
        self.mostrar_img(self.verticalLayout_canal_g, self.canal_g)
        self.mostrar_img(self.verticalLayout_canal_b, self.canal_b)
        # genero histogramas
        self.mostrar_histograma(self.verticalLayout_histograma_r, self.canal_r, 'red')
        self.mostrar_histograma(self.verticalLayout_histograma_g, self.canal_g, 'green')
        self.mostrar_histograma(self.verticalLayout_histograma_b, self.canal_b, 'blue')
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
