# Tarea 02: DDCafé

## Consideraciones generales

* Estimado corrector/a, espero que le guste mi tárea y no sea tan frustante de entender! :smiley:
* Tenia pensado en implementar el bonus de las configuraciones, pero al final no lo hice, asi que el boton no tiene utilidad.
* Todas mis ventanas las realice con designer. El window principal deberia ser incompresible (no crece ni achica).
* No entendí muy bien como funcionaba el tema del reloj del programa, espero que esté bien como lo dejé. Eso si, no implementé el parámetro que controla este reloj.
* La mayor interacción del programa se encuentra en el front_end y el controlador AI, que esta diseñado para controlar el flujo del programa, los clientes, chefs, supersicion de labels y demas.
* Algo que no consideré en el programa, es el hecho de que hay veces que dos threads acceden al mismo recurso (atributo) y que suman o restan valores, por lo que podria haber inconsistencias.
* El juego se puede correr, de hecho, juegue unas partidas pequeñas, sin embargo, podría crashear o haber errores con los labels. Hasta el momento que lo envie, el unico crasheo/error que tenia era cuando perdia la ronda y reiniciaba el juego. A veces aparecia labels de la partida pasada. :sweat: También al implementar las teclas trampa, las que hacen que la partida termine antes, puede traer errores tambien.
* Implemente las funcionalidades trampa en el juego, sin embargo, las que termina subitamente la partida es la más inestable (por asi decirlo).
* No implemente ningún bonus en el juego.
* Los clientes esperan en la entrada del restoran hasta que aparezca una mesa, luego entran caminando y se sientan. Cuando comen o se acaba su tiempo salen por la puerta.

### Cosas implementadas y no implementadas

* Ventana de Inicio: Hecha completa
* Ventana de Juego: 
    * Ventana Pre-Ronda: Hecha completa
    * Ventana Ronda: Hecha completa
    * Ventana Post-Ronda: Hecha completa
* Entidades:
    * Jugador: Hecha completa
    * Chef: Hecha completa (no comprobe bien si cambia los tiempos de cocción)
    * Bocadillos: Hecha completo (aunque no comprobe si cambian los tiempos y calidades de los bocadillos)
    * Clientes: Hecha completa
    * DCCafe: Hecha completa
* Tiempo:
    * Reloj: No lo sé
    * Pausa: No la implemente (si es tan amable, me podria decir una manera para realizarla??)
* Funcionalidades Extra:
    * M+O+N: Hecha completa
    * F+I+N: Creo que puede crashear o aparecer algun error
    * R+T+G: Hecha completa
* Extras: No hice ninguna

## Ejecución
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se tienen que tener los siguientes archivos:
1. ```datos.csv``` en ```T02```
2. ```mapa.csv``` en ```T02```
3. ```sprites``` en ````T02``` que es la carpeta con todos los sprites entregados al inicio de la tarea
4. ```post_ronda.ui``` en ```T02``` que es una ventana
5. ```preronda.ui``` en ```T02``` que es una ventana
6. ```ronda.ui``` en ```T02``` que es una ventana
7. ```ventana_inicial.ui``` en ```T02``` que es una ventana

## Librerías
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```sys```: ```__excepthook__``` ```exit()```
2. ```random```: ```random()``` ```randint()```
3. ```os``` : ```path```
4. ```time``` : ```time()``` ```sleep()```
5. ```math``` : ```floor```
6. ```PyQt5``` : ```uic```,  
               : ```QtWidgets``` : ```QWidget``` ```QLabel``` ```QApplication```,   
               : ```QtGui``` : ```QPixmap``` ```QMoveEvent``` ```QDrag```,  
               :```QtCore``` : ```pyqtSignal``` ```QMimeData``` ```Qt``` ```QRect``` ```QObject``` ```QThread``` ```QTimer```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```front_end```: Contiene las clases que representan la parte visual del juego. Las clases que incluye son ```RondaVentanaPrincipal```, ```VentanaInicio```, ```VentanaTienda```, ```VentanaPostRonda```.
2. ```entidades```: Incluye las entidades con mayor cantidad de lineas, ```Clientes``` y ```DCCafe```.
3. ```entidades_2```: Es la extension del archivo ```entidades```, ya que contiene el resto de las entidades (sin esto supero las 400 lineas por lejos). Incluye a ```Mesa```, ```Mesero```, ```Chef``` y ```Bocadillo```.
4. ```controladores```: contiene la clase que más interactua con el front_end y estructura el flujo del juego. Solo contiene a ```AI```.
5. ```base_datos```: contiene la clase que interactua con los archivos ```.csv```. Tiene la clase ```BaseDatos```.
6. ```parametros```: contiene la mayoría de las variables globales, aunque me faltaron muchas más.

## Supuestos y consideraciones adicionales
Los supuestos que realicé durante la tarea son los siguientes:

1. Para comenzar las rondas, hay que apretar el boton que está dentro de la ventana principal, si se cierra alguna ventana con la x superior derecha se cerrará el programa sin guardar.
2. Cuando los personajes cambian de frame, algunas dimensiones de las imagenes son distintas a las otras, por lo que se puede ver algo raro, pero no influye en el juego, es algo que no dedique tiempo al detalle.
3. Otro detalle que no arreglé, es que cuando el mesero choca contra el chef o mesa, se tiene que mover denuevo para que el mesero cambie de frame a cargar o depositar la comida.
4. Sobre el punto de referencia de mi juego, es respecto a la esquina superior izquierda del label del restoran.

## Muchas Gracias por Corregir mi Tarea :raised_hands: espero que te haya servido el README