import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from modeloTaboa import ModeloTaboa
from conexionBD import ConexionBD
from InformeSuscritos import create_pdf
class Suscritos (QMainWindow):
    def __init__(self,ref):
        super().__init__()
        # Interfaz de los subscriptores.
        self.setWindowTitle("Cartilla de los suscritos.")
        # Esta variable se encarga de la apertura y escondite de la interfaz principal.
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
        # Tiene 5 botones con sus acciones, que detalllaré a continuación.
        self.Taboa = QTableView()
        self.btnEngadir = QPushButton("Engadir")
        self.btnConsultar = QPushButton("Consultar",self)
        self.btnEditar = QPushButton("Editar")
        self.btnBorrar = QPushButton("Borrar")
        self.btnCrear = QPushButton("Crear Informe")
        self.btnEngadir.clicked.connect(self.engade)
        self.btnConsultar.clicked.connect(self.consulta)
        self.btnEditar.clicked.connect(self.edita)
        self.btnBorrar.clicked.connect(self.borra)
        self.btnCrear.clicked.connect(self.creaInforme)
        # Conexión a la base en SQLite y conexion de la tabla al proxy que se conecta al QAbstractTableModel.
        self.conn = ConexionBD("Pelis.db") 
        self.conn.conectaBD()
        self.conn.creaCursor()
        self.lista = self.conn.consultaSenParametros("select * from suscritos")
        self.modelo = ModeloTaboa(self.lista)
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.modelo)
        self.Taboa.setModel(self.proxy)
        self.selector = self.Taboa.selectionModel()

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
        caixaTaboa.addWidget(self.btnConsultar)
        caixaTaboa.addWidget(self.btnEditar)
        caixaTaboa.addWidget(self.btnBorrar)
        caixaH.addWidget(self.Taboa)
        caixaH.addLayout(caixaTaboa)
        caixaV.addLayout(grid)
        caixaV.addLayout(caixaH)
        caixaV.addWidget(self.btnCrear)
        container = QWidget()
        container.setLayout(caixaV)
        self.setCentralWidget(container)
        self.setFixedSize (800,600)
        self.show()
    # Función de consulta de la tabla SQL.    
    def consulta(self):
        # Un menú de objetos con todos los atributos.
        items = ['Mostrar toda la tabla','ID', 'DNI', 'Nombre', 'Apellido', 'Edad' , 'Pelis vistas']
        item, ok = QInputDialog.getItem(self, 'Consulta inicial', 'Que queres consultar?', items, editable=False)
        if ok:
            # Consulta según ID.
            if item == 'ID':
                # Pide un input
                texto, ok = QInputDialog.getText(self, 'Filtro - ID', 'Di la ID del suscriptor que buscas')
                if ok:
                    # Consulta preparada en SQL.
                    self.lista = self.conn.consultaConParametros("select * from Suscritos where ID = ?",texto)
                    # El proxy actuará de manera más estricta debido al dolar al final, en vez de ser un patron %caracter% es un patrón %caracter
                    regex = QRegularExpression(texto+"$")
                    self.proxy.setFilterKeyColumn(0)
                    self.proxy.setFilterRegularExpression(regex)
            # Consulta según su DNI.
            elif item == 'DNI':
                # Pide input
                texto, ok = QInputDialog.getText(self, 'Filtro - Título', 'Di el DNI que buscas')
                if ok:
                    self.lista = self.conn.consultaConParametros("select * from Suscritos where DNI like ?","%"+texto+"%")
                    regex = QRegularExpression(texto)
                    # El proxy cogerá de la segunda columna de la tabla todos los resultados que tengan que ver con el puesto en el input.
                    self.proxy.setFilterKeyColumn(1)
                    self.proxy.setFilterRegularExpression(regex)
            # Consulta según su nombre.         
            elif item == 'Nombre':
                texto, ok = QInputDialog.getText(self, 'Filtro - Nombres', 'Di el nombre que buscas')
                if ok:
                    self.lista = self.conn.consultaConParametros("select * from Suscritos where Nombre like ?","%"+texto+"%")
                    # Para que este proceso ocurra debemos convertir el string texto en un QRegularExpression.
                    regex = QRegularExpression(texto)
                    # El proxy cogerá de la tercera columna de la tabla todos los resultados que tengan que ver con el puesto en el input.
                    self.proxy.setFilterKeyColumn(2)
                    self.proxy.setFilterRegularExpression(regex)
            # Consulta según su apellido.      
            elif item == 'Apellido':
                texto, ok = QInputDialog.getText(self, 'Filtro - Apellidos', 'Di el apellido que buscas')
                if ok:
                    self.lista = self.conn.consultaConParametros("select * from Suscritos where Apellido like ?","%"+texto+"%")
                    regex = QRegularExpression(texto)
                    self.proxy.setFilterKeyColumn(3)
                    self.proxy.setFilterRegularExpression(regex)
            # Consulta según su edad.        
            elif item == 'Edad':
                # Abre una nueva tabla de objetos, según la comparación. En cualquier caso, da por la línea de comandos todos los resultados de la consulta.
                obj = ['Igual a','Menor que','Mayor que']
                ineq, ok = QInputDialog.getItem(self, 'Filtro - Cantidades', 'Como lo quieres comparar?',obj,editable=False)
                if ok:
                    if ineq == 'Igual a':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Igual', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from suscritos where Edad = ?",texto)
                            print ("Los subscriptores son datados en este orden:\nID, DNI, Nombre, Apellido, Edad, Pelis que ha visto.")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Menor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Menor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from suscritos where Edad < ?",texto)
                            print ("Los subscriptores son datados en este orden:\nID, DNI, Nombre, Apellido, Edad, Pelis que ha visto.")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Mayor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Mayor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from suscritos where Edad > ?",texto) 
                            print ("Los subscriptores son datados en este orden:\nID, DNI, Nombre, Apellido, Edad, Pelis que ha visto.")
                            for item in self.lista:
                                print (item)
            # Consulta según cuántas pelis vió este mes.                    
            elif item == 'Pelis vistas':
                obj = ['Igual a','Menor que','Mayor que']
                ineq, ok = QInputDialog.getItem(self, 'Filtro - Cantidades', 'Como lo quieres comparar?',obj,editable=False)
                if ok:
                    if ineq == 'Igual a':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Igual', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from suscritos where Pelis = ?",texto)
                            print ("Los subscriptores son datados en este orden:\nID, DNI, Nombre, Apellido, Edad, Pelis que ha visto.")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Menor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Menor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from suscritos where Pelis < ?",texto)
                            print ("Los subscriptores son datados en este orden:\nID, DNI, Nombre, Apellido, Edad, Pelis que ha visto.")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Mayor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Mayor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from suscritos where Pelis > ?",texto) 
                            print ("Los subscriptores son datados en este orden:\nID, DNI, Nombre, Apellido, Edad, Pelis que ha visto.")
                            for item in self.lista:
                                print (item) 
            # Muestra toda la tabla de nuevo, ya que estará la tabla filtrada si no se hace eso.                                               
            elif item == 'Mostrar toda la tabla':
                if ok:
                    # Para lograrlo basta con dejar el filtro en blanco.
                    self.proxy.setFilterRegularExpression('')
    # Añade registro a la tabla de la interfaz.
    def engade (self):
        # Un array que tendrá los textos que ponemos en los QLineEdits.
        elemento = [self.ID.text(),self.DNI.text(),self.Nome.text(),self.Apellido.text(),int(self.Idade.text()),int(self.Pelis.text())]
        # Se hace una consulta preparada con esos datos.
        self.conn.engadeRexistro("insert into suscritos (ID,DNI,Nombre,Apellido,Edad,Pelis) values (?,?,?,?,?,?)",
                                 self.ID.text(),self.DNI.text(),self.Nome.text(),self.Apellido.text(),int(self.Idade.text()),int(self.Pelis.text()))
        # Llamamos al índice actual de la tabla.
        index = self.Taboa.currentIndex()
        # Avisamos del cambio.
        self.modelo.layoutAboutToBeChanged.emit()
        # Insertamos el nuevo registro en el índice actual de la tabla. Este aparecerá encima de todos los demás.
        self.modelo.insertRows(index.row(), 1, index, [elemento])
        # Decimos que ya se cambió.
        self.modelo.layoutChanged.emit()
    # Edita registro a la tabla de la interfaz.
    def edita(self):
        # Consulta SQL con los datos de los QLineEdits.
        self.conn.actualizaRexistro("update suscritos set DNI=?,Nombre=?,Apellido=?,Edad=?,Pelis=? where ID=?",
                                self.DNI.text(),self.Nome.text(),self.Apellido.text(),int(self.Idade.text()),int(self.Pelis.text()),self.ID.text())
        # Avisamos cambio
        self.modelo.layoutAboutToBeChanged.emit()
        # Hacemos un foreach de todas las filas del índice.
        for row in range(self.proxy.rowCount()):
                # Llamamos solo a la columna con el ID.
                index = self.proxy.index(row,0)
                # Si este ID es igual al texto puesto. Haz que todos los datos de la fila sean iguales a los textos de los QLineEdits.
                if self.proxy.data(index) == self.ID.text():
                    indice = self.proxy.mapToSource(index)
                    self.modelo.datos[indice.row()]= [self.ID.text(),self.DNI.text(),self.Nome.text(),self.Apellido.text(),int(self.Idade.text()),int(self.Pelis.text())]
        # Avisamos del cambio hecho. 
        self.modelo.layoutChanged.emit()
    # Borra registro de la tabla de la interfaz.
    def borra(self):
        # Un cuadro de input, debes poner la ID del subscriptor.
        texto, ok = QInputDialog.getText(self, 'Borrado de datos', 'Poña o ID do rexistro que queres borrar.')      
        if ok:
            # Se recorre todas las filas del índice.
            for row in range(self.proxy.rowCount()):
                    # Se coge de las filas la columna con el ID.
                    index = self.proxy.index(row,0)
                    # Si es igual al texto, saca esa fila en específico. Y rompe el bucle.
                    if self.proxy.data(index) == texto:
                        indice = self.proxy.mapToSource(index)
                        self.modelo.removeRows(indice.row(),1, indice)
                        break  
            # Consulta SQL.                 
            self.conn.borraRexistro("delete from suscritos where ID = ?",texto) 
    # Crea un informe PDF a partir de los datos en SQLite.
    def creaInforme (self):
        # Crea una tabla con todos los datos de las películas.
        datos = self.conn.consultaSenParametros("select * from suscritos")
        # Crea tartas a partir de las parejas de datos (títulos y cantidades) de las películas.
        tarta = self.conn.consultaSenParametros("select ID,Pelis from suscritos")
        # Esta tarta numero 2 es un array de las cantidades de gente entre menos de 30 años, entre 30 y 60, y de 60 a más.
        tarta2 = []
        dato1 = self.conn.consultaSenParametros("select count() ID from suscritos where Edad < 31")
        tarta2.append(dato1[0])
        dato2 = self.conn.consultaSenParametros("select count() ID from suscritos where Edad > 30 and Edad < 61")
        tarta2.append(dato2[0])
        dato3 = self.conn.consultaSenParametros("select count() ID from suscritos where Edad > 60")
        tarta2.append(dato3[0])  
        self.Informe = create_pdf(datos,tarta,tarta2)      
    # Usando la variable ref,muestra la ventana principal que hemos escondido mientras se cierra la base de datos y la ventana.
    def closeEvent (self, event):
        self.ref.show()
        self.conn.pechaBD()
        self.close()