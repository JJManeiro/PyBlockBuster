=========
Portada
=========
.. _Portada:

Es un menú principal muy simple, te encontrarás con una hoja en blanco que tendrá 4 botones.
Cada uno de ellos te llevará a una sección distinta sobre los datos de la taquillera.

Así como des a uno de ellos, el menu principal se esconderá y mostrará la tabla.
*Estas 4 secciones son:*

* Películas, que tiene la fila Pelis.py.
* Empleados, que tiene la fila Empleados.py.
* Clientes subscritos a la taquillera,que tiene la fila Suscritos.py.
* Entradas de los clientes,que tiene la fila Clientes.py.

----------
Películas
----------
.. _Pelis:

En esta clase vas a encontrar estos 6 métodos:

1. Evento de cierre.

  * Este es muy sencillo de usar.Una vez le das al botón de cerrar, cerrará la conexión a la base de datos y la pestaña de pelis, reapareciendo así el menú principal.

2. Consulta

  * Este botón abrirá un menú secundario de barra. Te dará las siguientes opciones para hacer tu consulta.
  
   2.1. Mostrar toda la tabla, este se explica por sí solo.

   2.2. ID (Busca las películas por el código unico que llevan.)

   2.3. Título (Buscará todas las películas que tengan las mismas letras que el título.)

   2.4. Presupuesto (Buscará por cuanto fué su presupuesto)

    .. Important::
      Esta pestaña, junto con Recaudaciones, Óscares, Razzis y Nominados, abrirá un menú de barras secundario.
      Este preguntará si buscas una cantidad exacta, o si buscas una cantidad menor o mayor del numero que pondrás después.

      **El resultado de hacer estas consultas no será mostrado en la tabla de la aplicación. La lista se mostrará en la línea de comandos, película por peĺicula.**
    
   2.5. Recaudaciones (Buscará cuanto recaudaron sus ventas)

   2.6. Director (Buscará por el nombre del director)

   2.7. Actores (Buscará por el nombre del actor.)

   2.8. Óscares (Buscará cuantos Óscares gano la película)

   2.9. Razzis (Buscará cuantos Razzis gano la peĺicula)

   2.10. Nominados (Buscará cuantas veces fue nominada a los óscar)

3. Añade

  * Este botón añadirá la película sólo si has rellenado todos los datos en el formulario de la interfaz encima de la tabla.
  Una vez lo hayas hecho, se mostrará la película que hayas creado en la tabla *encima del primer resultado que veas de ella.
  Este cambio es temporal y volverá a su respectivo lugar una vez cierres la tabla del menú.*

4. Edita

  * Este botón editará los datos de la pelicula a la que le hayas puesto el ID en ella. **Necesitas rellenar todos los datos del formulario para hacer la edición**

5. Borra

  * Este botón abrirá un menú de input donde te pedirá la ID de la película que quieras borrar. Si lo haces la fila será borrada de la tabla.

6. Crea Informe

  * Este enorme botón está debajo de la tabla de datos generará en la carpeta que tengas este código un informe sobre la tabla en la que estés en PDF usando reportlab.
  *Cada informe de la tabla es distinto a los otros.*

----------
Empleados
----------
.. _Empleados:

Esta clase es muy parecida a la clase anterior, solo tiene este cambio en el método de las consultas.
1. Consulta. Este botón dará las siguientes opciones para hacer tu consulta, tambíen en menú de barras:

 1.1. ID (Busca a los empleados por el código unico que llevan.)

 1.2. DNI (Busca a los empleados por su Documento Nacional de Identidad.)
 
 1.3. Nombre (Busca a los empleados por su nombre)

 1.4. Apellido (Busca a los empleados por el apellido que tengan)

 1.5. Clientes atendidos (Buscará a los empleados cuantos según cuantos clientes atendió este mes.)

  * Este abrirá un menú de barras que pedirá una comparación o bien la cantidad exacta. 
  Este te dará tambien una lista con los resultados por la línea de comandos.

 1.6. Salario (Busca a los empleados según su salario mensual. *Este funciona de la misma manera que los clientes atendidos*)  

 1.7. Jornada (Busca a los empleados según su turno de trabajo.)

.. Note::
  Este abrirá un menu de barras que pedirá el turno del empleado (Matutino,Vespertino o Nocturno)
  Mostrará todos los empleados en la tabla de datos que tengan ese horario de trabajo.

----------
Suscritos
----------
.. _Suscritos:

En esta clase tampoco hay grandes diferencias, solo cambió consultas también.
1. Consulta. Este botón dará las siguientes opciones para hacer tu consulta, tambíen en menú de barras:

 1.1. ID (Busca a los subscriptores por el código unico que llevan.)

 1.2. DNI (Busca a los subscriptores por su Documento Nacional de Identidad.)

 1.3. Nombre (Busca a los subscriptores por su nombre)

 1.4. Apellido (Busca a los subscriptores por el apellido que tengan)

 1.5. Edad (Busca a los subscriptores por los años que tengan)

  * Este abrirá un menú de barras que pedirá una comparación o bien la cantidad exacta. 
  Dará tambien una lista con los resultados por la línea de comandos.

 1.6. Pelis vistas (Busca a los subscriptores por la cantidad de películas que vió este mes, usando la misma forma que por su edad)

---------
Clientes
---------
.. _Clientes:
Esta clase tiene sus detalles que merecen mención. Ahora hablaremos de las diferencias entre estes métodos de los demás.

Tiene, aparte de los otros 6 métodos, uno específico en caso de que el cliente sea subscriptor o no de la taquillera. *Veamos cuales son:*

1. Evento de cierre, ya mencionada su función. Está en todas las clases.

2. Suscripción

.. Important::
  Este método, único de la tabla Clientes. Se mostrará si le damos al botón de chequeo si el cliente está suscrito o no.
  Una vez presionado, te pedirá que insertes la ID del suscriptor que necesites.

  **Una vez puesto el ID del suscriptor, esta ID permanecerá ahí hasta que le des al botón de chequeo de nuevo.**

3. Consulta. También en menú de barras, te dará estas opciones:

 3.1. ID (Busca por la ID de la entrada)

 3.2. Fecha (Busca por el día y hasta por la hora y minutos que se compro la entrada.)

 3.3. Tipo (Busca según el tipo de edad de la entrada. *Si tuvo descuento de anciano o infantil, etc.*)

  .. Note::
    Este abrirá un menú de barras con los 3 tipos de entrada (Infante,Adulto y Anciano).
    **Mostrará los resultados por la tabla de datos una vez escogido el tipo.**

 3.4. Empleado que le atendió (Busca por la ID del empleado que le atendiera.)

 3.5. Película (Busca por la ID de la película a ver)

 3.6. Precio (Busca según cuanto haya costado la entrada a la gran pantalla.)

  * También abrirá un menú de barras que pedirá una comparación. 
  Dará tambien la lista de resultados por la línea de comandos.

 3.7. Suscriptor (Busca según la ID del suscriptor que tenga.)

4. Añade

  * Este botón *actuará de manera diferente si estás suscrito o no.*
    **Si no le diste al botón de chequeo de subscripción, dejará el campo vacío como None,** si le has dado una ID de subscriptor, la pondra ahí.

5. Edita

  * Este botón editará también *de forma distinta según le hayas dado una ID de suscriptor o no.*
    **Editará el campo vacío si te has hecho suscriptor,** y si no lo eres. No lo hará.

6. Borra, este campo borra preguntando por la ID primero, como en las demás tablas.

7. Crea Informe, crea un informe con datos sobre las entradas de la taquillera de este mes.

Para crear el informe sin problemas a la hora de mostrar los gráficos en rueda, es recomendable que el ID de empleado y de las Películas
estén dentro del rango que tienen. *Por ejemplo:* Si hay 15 películas, **la última ID de peli que se verá será la ID p15. No se verán otras después de eso.**

Fuera de eso hay algo interesante a contar. *Si una película o empleado* es actualizad@ o borrad@, **este cambio afectará a la tabla de las entradas.**