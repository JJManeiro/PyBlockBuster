import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
class Suscritos (QMainWindow):
    def __init__(self,ref):
        super().__init__()
        self.setWindowTitle("Cartilla de los suscritos.")
        self.ref = ref
        caixaV = QVBoxLayout()
        caixaTaboa = QVBoxLayout()
        caixaH = QHBoxLayout()
        grid = QGridLayout()
        
        lid = QLabel("ID")
        ldni = QLabel("DNI")
        lnome = QLabel("Nome")
        lapellido = QLabel ("Apellido")
        lidade = QLabel("Edad")
        lpelis = QLabel("Pelis vistas este mes")
        self.ID = QLineEdit()
        self.DNI = QLineEdit()
        self.Nome = QLineEdit()
        self.Apellido = QLineEdit()
        self.Idade = QLineEdit()
        self.Pelis = QLineEdit()
        
        self.Taboa = QTableView()
        self.btnEngadir = QPushButton("Engadir")
        self.btnEditar = QPushButton("Editar")
        self.btnBorrar = QPushButton("Borrar")

        grid.addWidget(lid,0,2,1,1)
        grid.addWidget(self.ID,0,3,1,1)
        grid.addWidget(lnome,0,0,1,1)
        grid.addWidget(self.Nome,0,1,1,1)
        grid.addWidget(ldni,2,0,1,1)
        grid.addWidget(self.DNI,2,1,1,1)
        grid.addWidget(lapellido, 1,0,1,1)
        grid.addWidget(self.Apellido,1,1,1,1)
        grid.addWidget(lidade, 1,2,1,1)
        grid.addWidget(self.Idade,1,3,1,1)
        grid.addWidget(lpelis, 2,2,1,1)
        grid.addWidget(self.Pelis,2,3,1,1)

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