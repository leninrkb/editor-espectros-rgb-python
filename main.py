from PyQt5 import QtWidgets, uic
from toolkit import seleccionar_archivo

app = QtWidgets.QApplication([])
ventana = uic.loadUi('gui_main.ui')

ventana.pushButton_cargar_img.clicked.connect(seleccionar_archivo)

# ejecutar
ventana.show()
app.exec()