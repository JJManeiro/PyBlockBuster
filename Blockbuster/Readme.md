# Blockbuster
Esta aplicacion es un proyecto de QtPy el cual te permite manejar una base de datos a través de una interfaz sencilla con 4 botones, que te llevarán a cuatro tablas distintas. En este caso se trata del manejo de una taquillera.
## Películas
Esta tabla se encarga de las películas en stock que hay en el cine. Contiene una tabla con diversos datos de las pelis y tiene cuatro botones al lado de ella.
Consultar registros,añadirlos,editarlos y borrarlos. A la hora de hacer estas acciones, tienes encima de la tabla un formulario para poner el texto en ellos.

**Estas mecánicas se aplican para todas las demás tablas.**.Abajo de todo tienes un botón el cual crea en PDF un informe con los datos de la base de datos.

## Empleados
Esta tabla gestiona el elenco de empleados del lugar. En el formulario tiene una barra de objetos para decir que jornada laboral tienen estes empleados.

## Subscriptores
Esta tabla gestiona los subscriptores de la taquillera. No tiene casi ningún cambio sustancial en la estética de la tabla.

## Clientes
Esta tabla se encarga de las entradas de los clientes del cine. Esta la es la tabla más peculiar, tiene un botón de *si esta uno subscrito o no* el cual afecta a los comandos SQL sobre la interfaz y tiene una barra espaciadora para escoger el tipo de descuento de entrada.

Esta tabla, a la vez de ser la mas peculiar, es también la más sensible. **Si se altera en cualquier modo, ya sea una edición o borrado de las claves primarias de las otras 3 tablas, esta será afectada también en el proceso.**