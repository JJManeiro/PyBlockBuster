import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
class Empleados (QMainWindow):
    def __init__(self,ref):
        super().__init__()
        self.setWindowTitle("Cartilla de los empleados.")
        self.ref = ref
        caixaV = QVBoxLayout()
        caixaTaboa = QVBoxLayout()
        caixaH = QHBoxLayout()
        grid = QGridLayout()
        
        lid = QLabel("ID")
        ldni = QLabel("DNI")
        lnome = QLabel("Nome")
        lapellido = QLabel ("Apellido")
        lclientes = QLabel("Clientes atendidos")
        lsalario = QLabel("Salario")
        ljornada = QLabel("Jornada")
        self.ID = QLineEdit()
        self.DNI = QLineEdit()
        self.Nome = QLineEdit()
        self.Apellido = QLineEdit()
        self.Clientes = QLineEdit()
        self.Salario = QLineEdit()
        self.Jornada = QComboBox(self)
        self.Jornada.addItem("Matutina")
        self.Jornada.addItem("Vespertina")
        self.Jornada.addItem("Nocturna")
        
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
        grid.addWidget(lclientes, 1,2,1,1)
        grid.addWidget(self.Clientes,1,3,1,1)
        grid.addWidget(lsalario, 2,2,1,1)
        grid.addWidget(self.Salario,2,3,1,1)
        grid.addWidget(ljornada, 3,0,1,1)
        grid.addWidget(self.Jornada,3,2,1,2)

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
    Empleados = Empleados()
    app.exec()
'''    