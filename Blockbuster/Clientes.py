import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
class Clientes (QMainWindow):
    def __init__(self,ref):
        super().__init__()
        self.setWindowTitle("Registro de los clientes.")
        self.ref = ref
        caixaV = QVBoxLayout()
        caixaTaboa = QVBoxLayout()
        caixaH = QHBoxLayout()
        grid = QGridLayout()
        
        lid = QLabel("ID")
        lhora = QLabel("Hora")
        lpeli = QLabel("Peli")
        lidemp = QLabel ("Empleado")
        lprecio = QLabel("Precio")
        ltipo = QLabel("Tipo de cliente")
        self.ID = QLineEdit()
        self.Hora = QLineEdit()
        self.Peli = QLineEdit()
        self.IDEmp = QLineEdit()
        self.Precio = QLineEdit()
        self.Tipo = QComboBox(self)
        self.Tipo.addItem("Infante")
        self.Tipo.addItem("Adulto")
        self.Tipo.addItem("Anciano")
        self.sus = QCheckBox("Suscrito?")

        self.Taboa = QTableView()
        self.btnEngadir = QPushButton("Engadir")
        self.btnEditar = QPushButton("Editar")
        self.btnBorrar = QPushButton("Borrar")

        grid.addWidget(lid,0,0,1,1)
        grid.addWidget(self.ID,0,1,1,1)
        grid.addWidget(lhora,1,0,1,1)
        grid.addWidget(self.Hora,1,1,1,1)
        grid.addWidget(lpeli,0,2,1,1)
        grid.addWidget(self.Peli,0,3,1,1)
        grid.addWidget(lidemp,2,0,1,1)
        grid.addWidget(self.IDEmp,2,1,1,1)
        grid.addWidget(lprecio, 1,2,1,1)
        grid.addWidget(self.Precio,1,3,1,1)
        grid.addWidget(ltipo, 2,2,1,1)
        grid.addWidget(self.Tipo,2,3,1,2)
        grid.addWidget(self.sus,3,1,1,1)

        caixaTaboa.addWidget(self.btnEngadir)
        caixaTaboa.addWidget(self.btnEditar)
        caixaTaboa.addWidget(self.btnBorrar)
        caixaH.addWidget(self.Taboa)
        caixaH.addLayout(caixaTaboa)
        caixaV.addLayout(grid)
        caixaV.addLayout(caixaH)
        container = QWidget()
        container.setLayout(caixaV)
        self.setCentralWidget(container)
        self.setFixedSize (800,600)
        self.show()
    def closeEvent (self, event):
        self.ref.show()
        self.close()    
'''
if __name__=="__main__":

    app = QApplication(sys.argv)
    Clientes = Clientes()
    app.exec()
'''    