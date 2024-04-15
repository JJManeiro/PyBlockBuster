import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
class Pelis (QMainWindow):
    def __init__(self,ref):
        super().__init__()
        self.setWindowTitle("Pelis de la taquillera")
        self.ref = ref
        caixaV = QVBoxLayout()
        caixaTaboa = QVBoxLayout()
        caixaH = QHBoxLayout()
        grid = QGridLayout()

        lid = QLabel("ID")
        lnome = QLabel("Título")
        lprecio = QLabel ("Presupuesto")
        ldirector = QLabel("Director")
        lactores = QLabel("Actores principales")
        loscar = QLabel("Oscares")
        lrazzi = QLabel("Ganó el razzi?")
        lnomi = QLabel ("Fue nominado?")
        self.ID = QLineEdit()
        self.Nome = QLineEdit()
        self.Precio = QLineEdit()
        self.Director = QLineEdit()
        self.Actores = QLineEdit()
        self.Oscar = QLineEdit()
        self.Razzi = QLineEdit()
        self.Nomi = QLineEdit()
        
        self.Taboa = QTableView()
        self.btnEngadir = QPushButton("Engadir")
        self.btnEditar = QPushButton("Editar")
        self.btnBorrar = QPushButton("Borrar")

        grid.addWidget(lid,0,0,1,1)
        grid.addWidget(self.ID,0,1,1,1)
        grid.addWidget(lnome,1,0,1,1)
        grid.addWidget(self.Nome,1,1,1,1)
        grid.addWidget(lprecio,2,0,1,1)
        grid.addWidget(self.Precio,2,1,1,1)
        grid.addWidget(ldirector, 3,0,1,1)
        grid.addWidget(self.Director,3,1,1,1)
        grid.addWidget(lactores, 0,2,1,1)
        grid.addWidget(self.Actores,0,3,1,1)
        grid.addWidget(loscar, 1,2,1,1)
        grid.addWidget(self.Oscar,1,3,1,1)
        grid.addWidget(lrazzi, 2,2,1,1)
        grid.addWidget(self.Razzi,2,3,1,1)
        grid.addWidget(lnomi, 3,2,1,1)
        grid.addWidget(self.Nomi,3,3,1,1)

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
    Pelis = Pelis()
    app.exec()
'''    