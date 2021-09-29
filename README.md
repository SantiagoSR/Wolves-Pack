# Wolves-Pack
Proyecto 1 de telematica

### Integrantes:

- Isabel Piedrahita
- Santiago Santacruz
- Duvan Ramirez


## 1. Especificación del Servicio

El presente es un servicio de transferencia de archivos. Esto se hizo con la intención de que el usuario pueda enviar y recibir archivos a otros clientes que requieran de estos. Para la arquitectura simulamos una red peer to peer centralizada. Todas las transacciones se hacen a través de un único servidor que sirve de punto de enlace entre dos nodos y que, a la vez, almacena y distribuye los nodos donde se almacenan los contenidos.


Para efectos de facilidad de uso se desarrolló una shell interactiva llamada ShortyShell para el cliente, en la que se implementaron además de los comandos básicos de ShortyShell comandos de ayuda para el usuario. Estos comandos de ayuda listan la sintaxis correcta de cada una de estas operaciones y explican lo que cada una hace. Las instrucciones para llamar a estas ayudas son visibles cuando el cliente accede a ShortyShell.

Según el teorema de CAP o Conjetura de Brewer nuestro sistema cumplira con la con ser consistente y altamente disponible (cualquier petición recibe una respuesta no errónea). 

Usamos un tipo de almacenamiento tipo WORM (Write once, read many), es decir, los archivos cargados ya no pueden ser borrados, regrabados o sobre-escritos posteriormente. La importancia de esto es que garantizan la integridad y conservación de la información allí guardada. 

Dentro de las caracteristicas el sistema es transparente de acceso cuando se establece una conexión se comunica con el servidor central. Por lo tanto, el usuario percibirá que el servidor es un único sistema y no se comunica con varios componentes separados. Transparente a replicaciones, Aunque los archivos estén copiados en diferentes servidores, el usuario es agnóstico a esto. El sistema es escalable, en cualquier momento se pueden crear más instancias del servidor central y comunicarlas mediante un balanceador de cargas, estableciendo algo similar a una red peer to peer híbrida, pero creemos que esto está fuera del alcance de nuestro proyecto. Nadie se encarga de mantener todos los archivos, y por ende todas las peticiones largas, por lo que es más rápido, sin embargo, el servidor central es un cuello de botella significativo. Debido a restricciones de recursos solo se crearán a lo sumo un servidor central y 4 peers.

Finalmente, algunas consideraciones adicionales sobre el servicio. El comportamiento del servidor se presta para manejar a multiples clientes de manera concurrente por medio de threads, cada cliente puede conectarse y desconectarse del servidor en el momento que lo considere. Por último, para garantizar la transparencia en operaciones. 


## 2. Vocabulario del Mensaje

ShortyShell utiliza una misma estructura de mensaje para todas sus comunicaciones;
| Mensaje | Descripción   |
|------|------|
| FILE <FILE_NAME> | Busca un archivo y lo descarga  |
| UPLOAD <FILE_NAME> | Registra un archivo al servidor |
| bye | termina la sesión |

Los mensajes que puede enviar el cliente están definidos de la siguiente forma. En la tabla verá significado semántico en la columna de procedimiento, mientras que en la columna de URL encontrará el URL correspondiente, en la que es muy fácil deducir a que se refiere el código y por ende no se pondrá entre paréntesis su significado. Todas estas peticiones de cliente son independientes entre si y el servidor no requiere mantener información de estado para manejar estas.

## 3. Regla de Procedimientos

La estructura general del protocolo se explica en el siguiente diagrama.

![image](https://user-images.githubusercontent.com/46933082/135185469-d63c906d-2ae8-45c0-a871-14734f7a3a77.png)




Los mensajes recibidos son todos muy similares en estructura, contienen un output que representa la información que se le debe mostrar al cliente. Este output es una string. Siempre que se envía un mensaje, se debe esperar un mensaje de respuesta.

Los errores en ShortyShell se manejan mediante la captura de excepciones, hay principalmente tres tipos de error, error de conección y error en tipo de dato. Los errores de coneccion se manejan levantando una excepción de tipo RuntimeError("socket connection broken"), no retornan nada al cliente. Los mensajes de falla en tipo de dato se manejan capturando la excepción y retornando al usuario un mensaje de error que quiere decir que alguno de los valores ingresados no se encuentra en la forma correcta.A continuación hay una tabla con cada error y los mensajes que imprime en la consola interactiva.
| Error | Mensaje   |
|------|------|
| Error de conexión | 400  |
| Error de comando| Lo sentimos, no estamos esperando <code>|

### 4. Tolerancia a fallos

TTL
En cualquier momento cualquier instancia puede caer y esta no bloqueará el funcionamiento completo del sistema.
Redundancia: Al cada base de datos tener la totalidad de los archivos y cada servidor tener la totalidad de la lógica de negocios, cualquiera de estos puede funcionar de manera independiente, generando tolerancia a particiones.

### 5. Regla de protocolo

Para la comunicacion entre los diferentes nodos y cliente, se utilizó un protocolo básico de comunicación construido sobre HTTP (concretamente las librerías request y http.server de python). Este mecanismo nos permite cominicarnos y sincronizar las acciones entre los diferentes nodos, manteniendo la ilusión de union para el cliente, es decir, el sistema a pesar de estar distribuido se comporta como si fuese un solo monolito de cara al usuario final. En nuestra arquitectura de comunicacion, estamos usando el protocolo HTTP, que se está soportado sobre los servicios de conexión TCP/IP. El protocolo funciona de la siguiente manera: un proceso servidor escucha en un puerto de comuniaciones, y espera las solicitudes de conexión de los clientes Web. una vez se establece la conexión, el protocolo se encarga de mantener la comunicación. El protocolo se basa en operaciones solicitud/respuesta. 
  
Otra decisión de arquitectura relevante es que los servidores de cara al cliente, pueden ser internamente clientes dentro de nuestro sistema. Por ejemplo, el cliente accede al servidor central que sirve com intermediario, el servidor central hace peticiones como cliente a otros peers que tiene el archivo solicitados.
  
A gran escala, en la totalidad del proyecto, únicamente se implementaron las palabras clave GET y POST, con estas se puedo estructurar completamente el protocolo de comunicación, ya que permiten cubrir todos los casos de uso de nuestro sistema como está planteado actualmetne.

### 6. Etapas de transacción del protocolo

  1. Un usuario solicita un servicio (FILE, UPLOAD). La solicitud del servicio genera una URL con la informacion de la petición.
  
  2. El servidor identifica el protocolo de acceso, la dirección DNS, el puerto y el objeto requerido del servidor.
  
  3. Se abre una conexión HTTP con el servidor llamando al puerto HTTP 3000 y se envia la petición con el comando GET o POST dependiendo del servicio.
  
  4. El servidor devuelve la respuesta al cliente. Que Consiste en un código de estado y el tipo de dato MIME de la información de retorno, seguido de la propia información.
  
  5. Se cierra la conexión. 

 #### NOTA: Este proceso se repite en cada acceso al servidor.
