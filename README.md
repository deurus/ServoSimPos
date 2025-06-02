# Modelado y Control de Posición de un Servo Simulado (2ªParte)

<h2>Introducción</h2>
Esta es la segunda parte del control del servo simulado. En la primera parte modelamos y sintonizamos un control de velocidad. El control de velocidad a excepción de la ausencia de tiempo muerto, no tuvo mayor complicación, nos enfrentamos a un proceso con respuesta autorregulada fácil de identificar y sintonizar. Ahora es el turno de controlar la posición y afrontar una respuesta completamente diferente, ¿no te lo crees? Pues sigue leyendo.

<h2>Funcionamiento</h2>
Recordemos que disponemos de un servo de 5 voltios que en su eje lleva acoplado un disco graduado entre 0 y 360 grados. El voltaje aplicado sobre el motor hace que éste gire en un sentido de forma continua pudiéndose invertir la polaridad para que el servo gire en sentido contrario. A medida que aplicamos más voltaje, más rápido gira el disco.

<h2>Control de posición</h2>
Atendiendo al simulador, el rango de la posición (PV) va de 0 a 359 grados y el voltaje del motor (OP) va de -5 a 5 voltios. El voltaje positivo y negativo hace que el servo pueda girar en ambos sentidos pero como punto de consigna (SP) sólo admite grados positivos.

<h2>Identificación</h2>
Tras jugar un poco con el simulador enseguida llegamos a la conclusión de que nos enfrentamos a un integrador puro en el que cada nivel de tensión produce una nueva velocidad constante, y por tanto, la posición crece linealmente en el tiempo.
<p align="center">
  <img src="https://garikoitz.info/blog/wp-content/uploads/2025/04/Test_v1-1024x476.webp" width="450" alt="ident">
</p>

Mediante un script de Python se ha identificado que la posición crece a una velocidad proporcional al voltaje aplicado, y esa proporción es de aproximadamente 5.72 º/s por voltio.
...

<h2>Resultados</h2>
<p align="center">
  <img src="https://garikoitz.info/blog/wp-content/uploads/2025/04/Test_v1-Sintonias-png.webp" width="450" alt="resultados">
</p>

...

Tenéis más información en la entrada del blog:
https://garikoitz.info/blog/2025/04/modelado-y-control-de-posicion-de-un-servo-simulado/
