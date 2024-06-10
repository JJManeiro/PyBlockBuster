from PyQt6.QtCore import QAbstractTableModel, Qt

class ModeloTaboa(QAbstractTableModel):
    def __init__(self, datos):
        super().__init__()
        # Saca los datos SQL en una lista llamada datos.
        self.datos = datos
    # Cuenta la cantidad de filas y columnas que hay en el modelo.
    def rowCount(self, index):
        return len(self.datos)

    def columnCount(self, index):
        return len(self.datos[0])
    # Muestran todas las filas de la tabla. 
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self.datos[index.row()][index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self.datos[index.row()][index.column()] = value
            return True
        return False
    # Se encarga de borrar las filas de la tabla.    
    def removeRows (self, row, numRows, parent):
            # Informa del borrado de fila
            self.layoutAboutToBeChanged.emit()
            # Comienza el borrado de filas de la tabla.
            self.beginRemoveRows(parent, row, row+numRows-1)
            #hace un bucle de cuantas filas debe borrar.
            for i in range(numRows):
                #Borra del array la fila con el numero en el que está.
                self.datos.pop(row+i)
            # Finaliza el borrado.    
            self.endRemoveRows()
            # Avisa del cambio en la tabla y trae todos los demás datos de vuelta.
            self.layoutChanged.emit()
            return True
    # Se encarga de añadir las filas de la tabla.
    def insertRows(self, position, rows, QModelIndex, parent):
        # Informa de la inserción de fila.
        self.layoutAboutToBeChanged.emit()
        # Comienza la inserción.
        self.beginInsertRows(QModelIndex, position, position+rows-1)
        # Por cada registro en la clase padre, añade una nueva fila en la siguiente zona a la de la posición marcada en el array.
        for elemento in parent:
            self.datos.insert(position+1, elemento)
        # Acaba la inserción.
        self.endInsertRows()
        # Avisa del cambio en la tabla y trae todos los datos de vuelta.
        self.layoutChanged.emit()
        return True    