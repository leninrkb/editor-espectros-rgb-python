from PyQt5 import QtWidgets, uic
app = QtWidgets.QApplication([])
ventana = uic.loadUi('gui_main.ui')
ventana.show()
app.exec()