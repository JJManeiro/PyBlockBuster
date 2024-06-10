import sys, re
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from modeloTaboa import ModeloTaboa
from conexionBD import ConexionBD
from InformeClientes import create_pdf
class Clientes (QMainWindow):
    def __init__(self,ref):
        super().__init__()
        # Interfaz de las entradas de los clientes.
        self.setWindowTitle("Registro de los clientes.")
        # Esta variable se encarga de la apertura y escondite de la interfaz principal.
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
        self.Tipo.setItemData(0,'Infante')
        self.Tipo.setItemData(1,'Adulto')
        self.Tipo.setItemData(2,'Anciano')
        # Este QCheckBox cobrará mucha importancia luego en varias de las acciones que explicaré.
        self.sus = QCheckBox("Suscrito?")
        self.sus.stateChanged.connect(self.suscripcion)
        self.input = None
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
        lista = self.conn.consultaSenParametros("select * from clientes")
        self.modelo = ModeloTaboa(lista)
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.modelo)
        self.Taboa.setModel(self.proxy)
        self.selector = self.Taboa.selectionModel()

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
    # Esta función indica si la entrada es de suscriptor o no.
    def suscripcion (self):
        # Si se le hace click a suscrito, pedira un input para poner la ID del subscriptor.
        if self.sus.isChecked():
           texto, ok = QInputDialog.getText(self, 'Input Dialog', 'Escribe la ID del subscriptor, por favor.')
           if ok:
               self.input=texto
        # Mientras ese boton de radio siga con el tick, la ID del subscriptor será siempre la misma. si le das de nuevo la ID se irá y quedara sin valor.       
        else:
            self.input = None      
    # Función de consulta de la tabla SQL.
    def consulta(self):
        # Un menú de objetos con todos los atributos.
        items = ['Mostrar toda la tabla', 'ID', 'Fecha', 'Tipo', 'Empleado que le atendió', 'Película', 'Precio', 'Suscriptor']
        item, ok = QInputDialog.getItem(self, 'Consulta inicial', 'Que queres consultar?', items, editable=False)
        if ok:
            # Consulta según ID.
            if item == 'ID':
                texto, ok = QInputDialog.getText(self, 'Filtro - ID', 'Di la ID de la entrada que buscas')
                if ok:
                    # Consulta preparada en SQL.
                    self.lista = self.conn.consultaConParametros("select * from Clientes where ID = ?",texto)
                    # El proxy actuará de manera más estricta debido al dolar al final, en vez de ser un patron %caracter% es un patrón %caracter
                    regex = QRegularExpression(texto+"$")
                    self.proxy.setFilterKeyColumn(0)
                    self.proxy.setFilterRegularExpression(regex)
            # Consulta según su hora exacta de compra.        
            elif item == 'Fecha':
                # Pide input
                texto, ok = QInputDialog.getText(self, 'Filtro - Fecha', 'Di el día que buscas. Debe ser en formato YYYY-MM-DD')
                if ok:
                    self.lista = self.conn.consultaConParametros("select * from Clientes where Fecha like ?","%"+texto+"%")
                    # Para que este proceso ocurra debemos convertir el string texto en un QRegularExpression.
                    regex = QRegularExpression(texto)
                    # El proxy cogerá de la segunda columna de la tabla todos los resultados que tengan que ver con el puesto en el input.
                    self.proxy.setFilterKeyColumn(1)
                    self.proxy.setFilterRegularExpression(regex)
            # Consulta según su tipo de entrada.
            elif item == 'Tipo':
                # Abre una nueva tabla de objetos, según la joranada. Según el turno, se filtrará en el proxy la tercera columna con esa palabra.
                obj = ['Infante','Adulto','Anciano']
                obx, ok = QInputDialog.getItem(self, 'Filtro - Edades', 'Que edad buscas?',obj,editable=False)
                if ok:
                    if obx == 'Infante':
                        self.lista = self.conn.consultaConParametros("select * from Clientes where Tipo = 'Infante'")
                        regex = QRegularExpression("Infante")
                        self.proxy.setFilterKeyColumn(2)
                        self.proxy.setFilterRegularExpression(regex)
                    elif obx == 'Adulto':
                        self.lista = self.conn.consultaConParametros("select * from Clientes where Tipo = 'Adulto'")
                        regex = QRegularExpression("Adulto")
                        self.proxy.setFilterKeyColumn(2)
                        self.proxy.setFilterRegularExpression(regex) 
                    elif obx == 'Anciano':
                        self.lista = self.conn.consultaConParametros("select * from Clientes where Tipo = 'Anciano'")
                        regex = QRegularExpression("Anciano")
                        self.proxy.setFilterKeyColumn(2)
                        self.proxy.setFilterRegularExpression(regex)
            # Consulta según el empleado que le atendió.            
            elif item == 'Empleado que le atendió':
                texto, ok = QInputDialog.getText(self, 'Filtro - Pelicula', 'Di la id del empleado que buscas')
                if ok:
                    self.lista = self.conn.consultaConParametros("select * from Clientes where IDEmp like ?","%"+texto+"%")
                    regex = QRegularExpression(texto)
                    self.proxy.setFilterKeyColumn(3)
                    self.proxy.setFilterRegularExpression(regex)  
            # Consulta según la pelicula que fue a ver.                          
            elif item == 'Película':
                texto, ok = QInputDialog.getText(self, 'Filtro - Pelicula', 'Di la id de la peli que buscas')
                if ok:
                    self.lista = self.conn.consultaConParametros("select * from Clientes where IDPeli like ?","%"+texto+"%")
                    regex = QRegularExpression(texto)
                    self.proxy.setFilterKeyColumn(4)
                    self.proxy.setFilterRegularExpression(regex)
            # Consulta según cuánto es su precio.        
            elif item == 'Precio':
                # Abre una nueva tabla de objetos, según la comparación. En cualquier caso, da por la línea de comandos todos los resultados de la consulta.
                obj = ['Igual a','Menor que','Mayor que']
                ineq, ok = QInputDialog.getItem(self, 'Filtro - Cantidades', 'Como lo quieres comparar?',obj,editable=False)
                if ok:
                    if ineq == 'Igual a':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Igual', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from Clientes where Precio = ?",texto)
                            print ("Las entradas son datadas en este orden:\nID, Fecha de compra, Tipo de entrada, ID del Empleado, ID de película y ID de subscriptor si tiene.")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Menor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Menor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from Clientes where Precio < ?",texto)
                            print ("Las entradas son datadas en este orden:\nID, Fecha de compra, Tipo de entrada, ID del Empleado, ID de película y ID de subscriptor si tiene.")
                            for item in self.lista:
                                print (item)
                    if ineq == 'Mayor que':
                        texto, ok = QInputDialog.getText(self, 'Filtro - Mayor cantidad', 'Di la cantidad a comparar')
                        if ok:
                            self.lista = self.conn.consultaConParametros("select * from Clientes where Precio > ?",texto) 
                            print ("Las entradas son datadas en este orden:\nID, Fecha de compra, Tipo de entrada, ID del Empleado, ID de película y ID de subscriptor si tiene.")
                            for item in self.lista:
                                print (item)
            # Consulta según es subscriptor o no.                       
            elif item == 'Suscriptor':
                texto, ok = QInputDialog.getText(self, 'Filtro - Esta suscrito?', 'Di la id de suscriptor que buscas')
                if ok:
                    self.lista = self.conn.consultaConParametros("select * from Clientes where Suscrito like ?","%"+texto+"%")
                    regex = QRegularExpression(texto)
                    self.proxy.setFilterKeyColumn(6)
                    self.proxy.setFilterRegularExpression(regex)
            # Muestra toda la tabla de nuevo, ya que estará la tabla filtrada si no se hace eso.
            elif item == 'Mostrar toda la tabla':
                if ok:
                    # Para lograrlo basta con dejar el filtro en blanco.
                    self.proxy.setFilterRegularExpression('')
    # Añade registro a la tabla de la interfaz.
    def engade (self):
        # Un array que tendrá los textos que ponemos en los QLineEdits.
        elemento = [self.ID.text(),self.Hora.text(),self.Tipo.itemData(self.Tipo.currentIndex()),self.IDEmp.text(),self.Peli.text(),int(self.Precio.text()),self.input]
        # Se hace una consulta preparada con esos datos, esta es distinta si la función de estar suscrito o no se use.
        if self.input is None:
            self.conn.engadeRexistro("insert into Clientes (ID,Fecha,Tipo,IDEmp,IDPeli,Precio) values (?,?,?,?,?,?)",
                                self.ID.text(),self.Hora.text(),self.Tipo.itemData(self.Tipo.currentIndex()),self.IDEmp.text(),self.Peli.text(),int(self.Precio.text()))    
        else:    
            self.conn.engadeRexistro("insert into Clientes (ID,Fecha,Tipo,IDEmp,IDPeli,Precio,Suscrito) values (?,?,?,?,?,?,?)",
                                self.ID.text(),self.Hora.text(),self.Tipo.itemData(self.Tipo.currentIndex()),self.IDEmp.text(),self.Peli.text(),int(self.Precio.text()),self.input)
        # Llamamos al índice actual de la tabla.           
        index = self.Taboa.currentIndex()
        # Avisamos del cambio.
        self.modelo.layoutAboutToBeChanged.emit()
        # Insertamos el nuevo registro en el índice actual de la tabla. Este aparecerá encima de todos los demás.
        self.modelo.insertRows(index.row(), 1, index, [elemento])
        # Decimos que ya se cambió.
        self.modelo.layoutChanged.emit()
    # Edita registro a la tabla de la interfaz.
    def edita (self):
        # Consulta SQL con los datos de los QLineEdits, esta es distinta si la función de estar suscrito o no se use..
        if self.input is None:
            self.conn.actualizaRexistro("update Clientes set Fecha=?,Tipo=?,IDEmp=?,IDPeli=?,Precio=?,Suscrito=NULL where ID=?",
                                self.Hora.text(),self.Tipo.itemData(self.Tipo.currentIndex()),self.IDEmp.text(),self.Peli.text(),int(self.Precio.text()),self.ID.text())
        else:
            self.conn.actualizaRexistro("update Clientes set Fecha=?,Tipo=?,IDEmp=?,IDPeli=?,Precio=?,Suscrito=? where ID=?",
                                self.Hora.text(),self.Tipo.itemData(self.Tipo.currentIndex()),self.IDEmp.text(),self.Peli.text(),int(self.Precio.text()),self.input,self.ID.text())
        # Avisamos cambio
        self.modelo.layoutAboutToBeChanged.emit()
        # Hacemos un foreach de todas las filas del índice.
        for row in range(self.proxy.rowCount()):
                # Llamamos solo a la columna con el ID.
                index = self.proxy.index(row,0)
                # Si este ID es igual al texto puesto. Haz que todos los datos de la fila sean iguales a los textos de los QLineEdits.
                if self.proxy.data(index) == self.ID.text():
                    indice = self.proxy.mapToSource(index)
                    self.modelo.datos[indice.row()]=[self.ID.text(),self.Hora.text(),self.Tipo.itemData(self.Tipo.currentIndex()),
                                                    self.IDEmp.text(),self.Peli.text(),int(self.Precio.text()),self.input]
        # Avisamos del cambio hecho.            
        self.modelo.layoutChanged.emit()
    # Borra registro de la tabla de la interfaz.
    def borra (self):
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
            self.conn.borraRexistro("delete from clientes where ID = ?",texto) 
    # Crea un informe PDF a partir de los datos en SQLite.
    def creaInforme (self):
        datos = self.conn.consultaSenParametros("select * from clientes")
        # La tarta numero 1 es un array de las cantidades de entradas en los meses de febrero y marzo.
        tarta = []
        dt11 = self.conn.consultaSenParametros("select count() ID from Clientes where Fecha like '2023-02%'")
        tarta.append(dt11[0])
        dt12 = self.conn.consultaSenParametros("select count() ID from Clientes where Fecha like '2023-03%'")
        tarta.append(dt12[0])
        # La tarta numero 2 es un array de las cantidades de entradas en cada etapa de edad.
        tarta2 = []
        dt21 = self.conn.consultaSenParametros("select count() ID from Clientes where Tipo like 'Infante'")
        tarta2.append(dt21[0])
        dt22 = self.conn.consultaSenParametros("select count() ID from Clientes where Tipo like 'Adulto'")
        tarta2.append(dt22[0])
        dt23 = self.conn.consultaSenParametros("select count() ID from Clientes where Tipo like 'Anciano'")
        tarta2.append(dt23[0])
        # La tarta numero 3 y ltarta3 son arrays en loop el cual ambos usan la cantidad total de filas para sacar cuantas fueron atendidas por cada empleado.
        tarta3 = []
        ltarta3 = []
        # Saca el total de filas.
        u1 = self.conn.consultaSenParametros("select count() ID from Empleados")
        # Este valor es sacado como como una lista, la cual convierto en String
        u1s = str(u1[0])
        # De este string le saco lo que no importa y lo dejo en numeros.
        number1 = re.findall(r'\d+', u1s)
        # Esos numeros salen como una lista, los cuales paso como int del primer ejemplo de la lista.
        u1n = int(number1[0])
        # Bucle for de 1 hasta el total de filas que hay+1
        for i in range (1,u1n+1):
            # texto para hacer una consulta preparada por cada vuelta del loop, este texto se añadirá a los nombres de ltarta3.
            texto = 'e'+str(i)
            ltarta3.append(texto)
            #Consulta preparada usando el texto.
            dt3 = self.conn.consultaConParametros("select count() ID from Clientes where IDEmp = ?",texto)
            #La misma conversion contada de antes, tupla > string > string en lista > número.
            dt3s = str(dt3[0])
            number2 = re.findall(r'\d+', dt3s)
            dt3n = int(number2[0])
            # se añade el número a la tarta.
            tarta3.append(dt3n)
        # La tarta numero 4 y ltarta4 son arrays en loop el cual ambos usan la cantidad total de filas para sacar cuantas fueron a ver una pelicula en particular.
        tarta4 = []
        ltarta4 = []
        # Usamos los mismos métodos que en la tarta 3
        u2 = self.conn.consultaSenParametros("select count() ID from Pelis")
        u2s = str(u2[0])
        number3 = re.findall(r'\d+', u2s)
        u2n = int(number3[0])
        for i in range (1,u2n+1):
            texto = 'p'+str(i)
            ltarta4.append(texto)
            dt4 = self.conn.consultaConParametros("select count() ID from Clientes where IDPeli = ?",texto)
            dt4s = str(dt4[0])
            number4 = re.findall(r'\d+', dt4s)
            dt4n = int(number4[0])
            tarta4.append(dt4n)
        # La tarta numero 5 es un array de las cantidades de clientes subscritos al cine y de los que no lo son.
        tarta5 = []
        dt51 = self.conn.consultaSenParametros("select count() ID from Clientes where Suscrito is not null")
        tarta5.append(dt51[0])
        dt52 = self.conn.consultaSenParametros("select count() ID from Clientes where Suscrito is null")
        tarta5.append(dt52[0])
        self.Informe = create_pdf(datos,tarta,tarta2,tarta3,ltarta3,tarta4,ltarta4,tarta5)        
    # Usando la variable ref,muestra la ventana principal que hemos escondido mientras se cierra la base de datos y la ventana.
    def closeEvent (self, event):
        self.ref.show()
        self.conn.pechaBD()
        self.close()      