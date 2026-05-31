<div style="text-align: center;">
  <img src="resources/BinaryBuilders.png" alt="Logo del grupo Binary Builders" style="display: block; margin: 0 auto;">
</div>

# ssl - BinaryBuilders
Este es el repositorio utilizado por el grupo BinaryBuilders para llevar adelante las actividades de desarrollo relacionadas al trabajo práctico integrador de la materia Sintaxis y Semántica de los Lenguajes.

El trabajo consiste en el desarrollo de un analizador lexicográfico y un analizador sintáctico, los cuales deben ser capaces de revisar un archivo de texto recibido como entrada e indicar si este tiene un formato correcto, de acuerdo a una gramática escrita por el grupo. Asimismo, el programa resultante deberá ser capaz de transformar el archivo de entrada en un archivo HTML a medida que lo analiza.

## Establecimiento de un entorno de desarrollo
Para poder establecer un entorno que permita participar del desarrollo del trabajo, se deben seguir los siguientes pasos:

1. Clonar la rama principal (`main`) del repositorio, ya sea mediante git o mediante una descarga directa a través de GitHub.
2. Crear un entorno virtual de Python (`venv`) en la carpeta correspondiente a la rama clonada del repositorio, lo cual se puede hacer mediante los siguientes pasos:
    - Ubicarse en la carpeta antecesora a la carpeta donde se ha clonado el repositorio. A los efectos del ejemplo, se considerará que el repositorio ha sido clonado en la carpeta `ssl` y que este se encuentra en la ruta `C:\Users\Usuario\Downloads`.
    - En una ventana de terminal, situarse en la carpeta antecesora con `cd C:\Users\Usuario\Downloads` y ejecutar el comando `python -m venv ssl`.
3. Luego, se debe situarse en la carpeta del proyecto con `cd ssl` e ingresar al entorno virtual ejecutando `.\Scripts\Activate.ps1`.
4. Por último, se deben instalar las dependencias del proyecto con el comando `pip install -r requirements.txt`.
