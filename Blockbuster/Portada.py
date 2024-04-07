import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from Pelis import Pelis
from Empleados import Empleados
from Clientes import Clientes
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
        
        caixaH.addWidget(self.Pelis)
        caixaH.addWidget(self.Empleados)
        caixaH.addWidget(self.Clientes)
        container = QWidget()
        container.setLayout(caixaH)
        self.setCentralWidget(container)
        self.setFixedSize (800,600)
        self.show()
    
    def ConPelis(self):
        Pelis()
    def ConEmpleados(self):
        Empleados()
    def ConClientes(self):
        Clientes()    

if __name__=="__main__":

    app = QApplication(sys.argv)
    Blockbuster = Blockbuster()
    app.exec()        