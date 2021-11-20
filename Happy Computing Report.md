## Happy Computing

Happy Computing es un taller de reparaciones electronicas, donde se realizan las siguientes actividades:

1. Reparacion por garantia (Gratis)
2. Reparacion fuera de garantia (350$)
3. Cambio de equipo (500$)
4. Venta de equipos reparados (750$)

Se conoce ademas que el taller cuenta con 3 tipos de empleados: Vendedor, Tecnico y Tecnico Especializado.

Para su funcionamiento, cuando un cliente llega al taller, es atendido por un vendedor y en caso de que el servicio que requiera sea una Reparacion (sea de tipo 1 o 2) el cliente debe ser atendido por un tecnico (especializado o no). Ademas en caso de que el cliente quiera un cambio de equipo este debe ser atendido por un tecnico especilizado. Si todos los empleados que pueden atender al cliente estan ocupados, entonces se establece una cola para sus servicios. Un tecnico especializado solo realizara Reparaciones si no hay ningun cliente que desee un cambio de equipo en la cola.

Se conoce que los clientes arriban al local con un interbalo de tiempo que distribuye poisson con **λ=20** minutos y que el tipo de servicios que requieren pueden ser descrito mediante la tabla de probabilidades.

| Tipos de Servicios | Probabilidad |
|--------------------|--------------|
| 1                  | 0.45         |
| 2                  | 0.25         |
| 3                  | 0.1          |
| 4                  | 0.2          |

Ademas se conoce que un tecnico tarda un tiempo que distribuye exponencial con **λ = 20** minutos, en realizar una Reparacion Cualquiera. Un tecnico especializado tarda un tiempo que distribuye exponencial con **λ = 15** minutos, para realizar un cambio de equipos y la vendedora puede atender cualquier servicio en un tiempo que distribuye normal (N(5 min, 2 min)).

El dueño del lugar desea realizar una simulacion de la ganancia que tendria en una jornada laboral si tuviera 2 vendedores, 3 tecnicos y 1 tecnico especializado.

## Modelo de Simulación de Eventos Discretos.

Para realizar el modelo de la simulación se declararon las siguientes variables:
-	**T**: Tiempo total de simulación
-	**time**: Para llevar el tiempo de simulacion
-	**n**: Contador de clientes atendidos en el Taller
-	**profit**: Ganacia que vamos calculando
-	**ta**: Tiempo de arribo del proximo cliente
-	**nextTA**: Tiempo de arribo del siguiente cliente, una vez un vendedor procesa a uno en cola
-	**s**: Tipo de servicio escogido para el cliente actual
-	**client**: Hacer referencia al cliente que recien sacamos del Heap
-	**ts**: Tiempo que le toma a un vendedor asignar correctamente un cliente
-	**tt**: Tiempo que le toma a un técnico resolver una reparación correctamente
-	**tst**: Tiempo que le toma a un técnico especializado resolver un cambio de equipo
-	**third**: Variable booleana para saber si hay alguien para el servicio 3 en cola
-	**SS**: Lista de vendedores
-	**SST**: Lista de técnicos
-	**SSTE**: Liste de técnicos especializado
-	**timeHeap**: Heap para llevar los tiempos de cada evento

Ademas creamos una clase evento para describir a los clientes, la cual tiene las siguientes variables:
- **ctime**: Para estar al tanto del tiempo que realiza una acción
- **stype**: El tipo de servicio escogido
- **exitTime**: Tiempo con que el cliente sale del Taller
- **worker**: Para saber que trabajador los atendio
- **job**: Para al sacarlo del heap, si ya termino, saber que tipo de técnico lo atendio para poder liberarlo
- **state**: Para saber en todo momento en que estado esta el cliente


Posibles eventos a tratar durante la Simulación:
1. LLega un cliente a la tienda
2. El cliente quiere una Reparación por garantía
3. El cliente quiere una Reparación fuera de garantía
4. El cliente quiere un Cambio de equipo
5. El cliente quiere Comprar un Equipo Reparado

### Generar un primer cliente:
Primero generamos un primer tiempo de llega, y lo encolamos en **timeHeap**. 
1. **ta** = **time** + **poisson(20)**
2. **s** <= Tipo de servicio seleccionado para ese cliente
3. Luego encolamos  el cliente creado en **timeHeap**

### Caso 1 - Llega un cliente a la tienda
1. **client**  = **timeHeap.pop()**
2. si **client.state** == **Vendor** significa que todavia no lo ha atendido un vendedor
	- **time** = **client.ctime**
	- **n** += 1
	- llamamos al método **vendorAttend** el cual se encarga de asignar el cliente a su respectivo trabajador, manejando todos los casos posibles de los vendedores.
	- Y generamos el proximo cliente que entrará a la tienda **nextTA** = **generateNewArrival()**. 
3. si **client.state** == **Technician** significa ya lo atendió un vendedor y lo redirigio a un técnico, luego actualizamos el tiempo
	- **time** = **client.ctime**
	- llamamos al método **techAttend(client)** que maneja a que técnico le asigna el nuevo cliente.
4. si **client.state** == **Spec Technician** significa ya lo atendió un vendedor y lo redirigio a un técnico especializado, luego actualizamos el tiempo
	- **time** = **client.ctime**
	- llamamos al método **spetechAttend(client)** que maneja a que técnico le asigna el nuevo cliente.
5. si **client.state** == **Finish** significa ya termino todo su paso por la fabrica. Luego actualizamos el tiempo, como el mínimo entre el tiempo de salida del cliente que recién termino y el próximo a salir del Heap.
	- **time** = **min(Htime, client.time)** siendo Htime el que va a salir proximo en el heap.
	- Como ya este cliente terminó, usando su propiedad **job** sabemos  a quien liberar de los técnicos. Si es un técnico normal sabemos cual es por la propiedad **worker**.
	- Y despues en dependencia de su tipo de servicio actualzamos la ganancia

### Caso General: Manejo del cliente:
El método **vendorAttend(client)** asigno el cliente a un vendedor, y este usa el método **vendorAction** el cual en dependencia del tipo de servicio le actualiza el  **state** y el **ctime**. Y vuelve a ser encolado en el heap de tiempos **timeHeap**. Luego se repite el caso 1.
1. En caso que el cliente sacado del heap tenga **state** == **Technician**, se llama al método que maneja a la asignación de técnicos, es decir solo se manejan aqui las Reparaciones. **techAttend(client)**, este mira la disponibilidad de los técnicos y asigna al primero libre que encuentra. En caso que ninguno este libre, verifica si no hay ningun servicio de **Cambio de equipo** en cola, y ádemas el técnico especializado no esta ocupado. En este caso se lo manda a al técnico especializado, sino lo encola otra vez, con el mismo tiempo.
2. En caso que el cliente sacado del heap tenga  **state** == **Spec Technician**, se llama al método **spetechAttend(client)** el cual hace lo mismo que el anterior, solo que asigna tareas del tipo **Cambio de equipo** a los técnicos especializados solamente.

### Ideas Generales Seguidas:
-	LLevar siempre un heap con el tiempo que he pasado en la simulación. De esta forma saber el espacio de tiempo en cada momento.
-	Llevar 3 listas **SS** una para cada tipo de empleado, esto hace mas fácil el trabajo con los empleados y las colas.
-	Mantener ocupado a los empleaos hasta que el cliente que ellos manejan pase a la siguiente fase.
-	Separar los eventos por etapas, esto hace mas fácil  el manejo de los casos en el código, y una mayor legibilidad.

### Resultados Generales Estádisticos:
- Media: 6600
- Desviación Estandar: 1460
- Varianza: 2 160 300
- Cantidad de clientes: 25+-2
- Tiempo de Simulación: 480+-10
- Número de Iteraciones: 1000+-100 

### README
Para correr la simulación basta con correr. **python stats.py**

Dependencias:
- **matplotlib**
- **numpy**


