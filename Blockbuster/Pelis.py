import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from modeloTaboa import ModeloTaboa
from conexionBD import ConexionBD
from InformePelis import create_pdf
class Pelis (QMainWindow):
    def __init__(self,ref):
        super().__init__()
        # Interfaz de las películas
        self.setWindowTitle("Pelis de la taquillera")
        # Esta variable se encarga de la apertura y escondite de la interfaz principal.
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
        # Tiene 5 botones con sus acciones, que detalllaré a continuación.
        self.Taboa = QTableView()
        self.btnEngadir = QPushButton("Engadir")
        self.btnConsultar = QPushButton('Consultar', self)
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
        self.lista = self.conn.consultaSenParametros("select * from pelis")
        self.modelo = ModeloTaboa(self.lista)
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.modelo)
        self.Taboa.setModel(self.proxy)
        self.selector = self.Taboa.selectionModel()

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
        items = ['Mostrar toda la tabla','ID', 'Título', 'Presupuesto', 'Recaudaciones','Director', 'Actores', 'Oscar', 'Razzi', 'Nominados']
        item, ok = QInputDialog.getItem(self, 'Consulta inicial', 'Que queres consultar?', items, editable=False)
        if ok:
            # Consulta según ID.
            if item == 'ID':
                # Pide un input
                texto, ok = QInputDialog.getText(self, 'Filtro - ID', 'Di la ID de la peli que buscas')
                if ok:
                    # Consulta preparada en SQL.
                    self.lista = self.conn.consultaConParametros("select * from pelis where ID = ?",texto)
                    # El proxy actuará de manera más estricta debido al dolar al final, en vez de ser un patron %caracter% es un patrón %caracter
                    regex = QRegularExpression(texto+"$")
                    self.proxy.setFilterKeyColumn(0)
                    self.proxy.setFilterRegularExpression(regex)
            # Consulta según su titulo        
            elif item == 'Título':
                # Pide input
                texto, ok = QInputDialog.getText(self, 'Filtro - Título', 'Di el título de la peli que buscas')
                if ok:
                    self.lista = self.conn.consultaConParametros("select * from pelis where Titulo like ?","%"+texto+"%")
                    regex = QRegularExpression(texto)
                    #El proxy cogerá de la segunda columna de la tabla todos los resultados que tengan que ver con el puesto en el input.
                    self.proxy.setFilterKeyColumn(1)
                    self.proxy.setFilterRegularExpression(regex)
            # Consulta según presupuesto.      
            elif item == 'Presupuesto':
                # Abre una nueva tabla de objetos, según la comparación. En cualquier caso, da por la línea de comandos todos los resultados de la consulta.
                obj = ['Igual a','Menor que','Mayor que']
                ineq, ok = QInputDialog.getItem(self, 'Filtro - Cantidades', 'Como lo quieres comparar?',obj,editable=False)
                if ok:
                    if ineq == 'Igual a':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Igual', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from pelis where Presupuesto = ?",texto)
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Menor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Menor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from pelis where Presupuesto < ?",texto)
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones,Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Mayor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Mayor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from pelis where Presupuesto > ?",texto) 
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item) 
            # Mismo método que el anterior, pregunta cuanto dinero recaudó ahora.                  
            elif item == 'Recaudaciones':
                obj = ['Igual a','Menor que','Mayor que']
                ineq, ok = QInputDialog.getItem(self, 'Filtro - Cantidades', 'Como lo quieres comparar?',obj,editable=False)
                if ok:
                    if ineq == 'Igual a':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Igual', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from pelis where Recaudacion = ?",texto)
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Menor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Menor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from pelis where Recaudacion < ?",texto)
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Mayor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Mayor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from pelis where Recaudacion > ?",texto) 
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
            # Consulta por el nombre o apellido del director/a.                                                                         
            elif item == 'Director':
                texto, ok = QInputDialog.getText(self, 'Filtro - Directores', 'Di el director que buscas')
                if ok:
                    self.lista = self.conn.consultaConParametros("select * from pelis where Director like ?","%"+texto+"%")
                    regex = QRegularExpression(texto)
                    #Busca en la cuarta columna un resultado conteniendo al patrón.
                    self.proxy.setFilterKeyColumn(4)
                    self.proxy.setFilterRegularExpression(regex)
            # Consulta por el nombre o apellido de los actores.       
            elif item == 'Actores':
                texto, ok = QInputDialog.getText(self, 'Filtro - Autores', 'Di el actor que buscas')
                if ok:
                    self.lista = self.conn.consultaConParametros("select * from pelis where Actores like ?","%"+texto+"%")
                    regex = QRegularExpression(texto)
                    self.proxy.setFilterKeyColumn(5)
                    self.proxy.setFilterRegularExpression(regex)
            # Mismo método que con el presupuesto y recaudaciones, verás que se aplica para otros atributos en referencia a cantidades en los demás archivos.        
            elif item == 'Oscar':
                #Tabla de comparaciones
                obj = ['Igual a','Menor que','Mayor que']
                ineq, ok = QInputDialog.getItem(self, 'Filtro - Cantidades', 'Como lo quieres comparar?',obj,editable=False)
                if ok:
                    if ineq == 'Igual a':
                        # Input
                        texto, ok = QInputDialog.getText(self, 'Filtro - Igual', 'Di la cantidad a comparar')
                        if ok:
                            #Consulta SQL.
                            self.lista = self.conn.consultaConParametros("select * from pelis where Oscar = ?",texto)
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Menor que':
                        # Input
                        texto, ok = QInputDialog.getText(self, 'Filtro - Menor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            # Consulta SQL.
                            self.lista = self.conn.consultaConParametros("select * from pelis where Oscar < ?",texto)
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Mayor que':
                        # Input
                        texto, ok = QInputDialog.getText(self, 'Filtro - Mayor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            # Consulta SQL.
                            self.lista = self.conn.consultaConParametros("select * from pelis where Oscar > ?",texto) 
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item) 
            # El objeto anterior se aplicó a cuantos premios óscar gano la película. Aquí se dice cuanto premios Razzi.
            elif item == 'Razzi':
                obj = ['Igual a','Menor que','Mayor que']
                ineq, ok = QInputDialog.getItem(self, 'Filtro - Cantidades', 'Como lo quieres comparar?',obj,editable=False)
                if ok:
                    if ineq == 'Igual a':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Igual', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from pelis where Razzi = ?",texto)
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Menor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Menor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from pelis where Razzi < ?",texto)
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Mayor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Mayor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from pelis where Razzi > ?",texto) 
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
            # Cuantas veces fue nominado al óscar?                    
            elif item == 'Nominados':
                obj = ['Igual a','Menor que','Mayor que']
                ineq, ok = QInputDialog.getItem(self, 'Filtro - Cantidades', 'Como lo quieres comparar?',obj,editable=False)
                if ok:
                    if ineq == 'Igual a':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Igual', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from pelis where Nominados = ?",texto)
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Menor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Menor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from pelis where Nominados < ?",texto)
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Mayor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Mayor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from pelis where Nominados > ?",texto) 
                            print ("Las películas son datadas en este orden:\nID, Título, Presupuesto, Recaudaciones, Director, Actores, Oscares, Razzis, Nominados")
                            for item in self.lista:
                                print (item)
            # Muestra toda la tabla de nuevo, ya que estará la tabla filtrada si no se hace eso.                 
            elif item == 'Mostrar toda la tabla':
                if ok:
                    # Para lograrlo basta con dejar el filtro en blanco.
                    self.proxy.setFilterRegularExpression('')
    # Añade registro a la tabla de la interfaz.
    def engade(self):
        # Un array que tendrá los textos que ponemos en los QLineEdits.
        elemento = [self.ID.text(),self.Nome.text(),float(self.Precio.text()),self.Director.text(),
                                 self.Actores.text(),int(self.Oscar.text()),int(self.Razzi.text()),int(self.Nomi.text())]
        # Se hace una consulta preparada con esos datos.
        self.conn.engadeRexistro("insert into pelis (ID,Titulo,Presupuesto,Director,Actores,Oscar,Razzi,Nominados) values (?,?,?,?,?,?,?,?)",
                                 self.ID.text(),self.Nome.text(),float(self.Precio.text()),self.Director.text(),
                                 self.Actores.text(),int(self.Oscar.text()),int(self.Razzi.text()),int(self.Nomi.text()))
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
        self.conn.actualizaRexistro("update pelis set Titulo=?,Presupuesto=?,Director=?,Actores=?,Oscar=?,Razzi=?,Nominados=? where ID=?",
                                self.Nome.text(),float(self.Precio.text()),self.Director.text(),
                                self.Actores.text(),int(self.Oscar.text()),int(self.Razzi.text()),int(self.Nomi.text()),self.ID.text())
        # Avisamos cambio
        self.modelo.layoutAboutToBeChanged.emit()
        # Hacemos un foreach de todas las filas del índice.
        for row in range(self.proxy.rowCount()):
                # Llamamos solo a la columna con el ID.
                index = self.proxy.index(row,0)
                # Si este ID es igual al texto puesto. Haz que todos los datos de la fila sean iguales a los textos de los QLineEdits.
                if self.proxy.data(index) == self.ID.text():
                    indice = self.proxy.mapToSource(index)
                    self.modelo.datos[indice.row()]= [self.ID.text(),self.Nome.text(),float(self.Precio.text()),self.Director.text(),
                                 self.Actores.text(),int(self.Oscar.text()),int(self.Razzi.text()),int(self.Nomi.text())]
        # Avisamos del cambio hecho.            
        self.modelo.layoutChanged.emit()            
    # Borra registro de la tabla de la interfaz.
    def borra(self):
        # Un cuadro de input, debes poner la ID de la película.
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
            self.conn.borraRexistro("delete from pelis where ID = ?",texto)
    # Crea un informe PDF a partir de los datos en SQLite.
    def creaInforme(self):
        # Crea una tabla con todos los datos de las películas.
        datos = self.conn.consultaSenParametros("select * from pelis")
        # Crea tartas a partir de las parejas de datos (títulos y cantidades) de las películas.
        tarta = self.conn.consultaSenParametros("select Titulo,Presupuesto from pelis")
        tarta2 = self.conn.consultaSenParametros("select Titulo,Recaudacion from pelis")
        tarta3 = self.conn.consultaSenParametros("select Titulo,Oscar from pelis")
        tarta4 = self.conn.consultaSenParametros("select Titulo,Razzi from pelis")
        tarta5 = self.conn.consultaSenParametros("select Titulo,Nominados from pelis")
        self.Informe = create_pdf(datos,tarta,tarta2,tarta3,tarta4,tarta5) 
    # Usando la variable ref,muestra la ventana principal que hemos escondido mientras se cierra la base de datos y la ventana.
    def closeEvent (self, event):
        self.ref.show()
        self.conn.pechaBD()
        self.close()
 