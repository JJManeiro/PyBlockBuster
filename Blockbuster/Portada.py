import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from Pelis import Pelis
from Empleados import Empleados
from Clientes import Clientes
from Suscritos import Suscritos
class Blockbuster (QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de los clientes.")
        
        caixaH = QHBoxLayout()
        self.Pelis = QPushButton("Pelis")
        self.Pelis.pressed.connect(self.ConPelis)
        self.Empleados = QPushButton("Empleados")
        self.Empleados.pressed.connect(self.ConEmpleados)
        self.Clientes = QPushButton("Clientes")
        self.Clientes.pressed.connect(self.ConClientes)
        self.Suscritos = QPushButton("Suscritos")
        self.Suscritos.pressed.connect(self.ConSuscritos)
        
        caixaH.addWidget(self.Pelis)
        caixaH.addWidget(self.Empleados)
        caixaH.addWidget(self.Clientes)
        caixaH.addWidget(self.Suscritos)
        container = QWidget()
        container.setLayout(caixaH)
        self.setCentralWidget(container)
        self.setFixedSize (600,450)
        self.show()
    
    def ConPelis(self):
        self.P = Pelis(self)
        self.hide()
    def ConEmpleados(self):
        self.E = Empleados(self)
        self.hide()
    def ConClientes(self):
        self.C = Clientes(self)   
        self.hide()
    def ConSuscritos(self):
        self.S = Suscritos(self)
        self.hide()         
        
                     
if __name__=="__main__":
    app = QApplication([])
    Blockbuster = Blockbuster()
    app.exec()        