from rich.console import Console
import msvcrt
import os
import sys
import ply.lex as lex

#=================================================================================
#=================================LISTA DE TOKENS=================================
#=================================================================================
tokens = [
    'IGUAL',
    'DISTINTO',
    'MAYORIGUAL',
    'MENORIGUAL',
    'ASIGNACION',
    'PUNTO',
    'GUIONBAJO',
    'MAYOR',
    'MENOR',
    'ATRIBUTO',
    'TEXTO',
    'VALOR_TEMPERATURA',
    'PERCENT',
    'HORA',
    'TIEMPO',
    'ILUMINANCIA',
    'DATE',
    'EMAIL',
    'COMMENT',
    'ID',
]

#Palabras reservadas
reservado = {
    'IF': 'IF',
    'THEN': 'THEN',
    'ELSE': 'ELSE',
    'WHEN' : 'WHEN',
    'END': 'END',
    'EVERY': 'EVERY',
    'DO' : 'DO',
    #<BOOL_DISPOSITIVO> -> 'TRUE' | 'FALSE' 
    'TRUE' : 'TRUE',
    'FALSE' : 'FALSE',
    #<BOOL_ACTUADOR> -> 'ON' | 'OFF'  
    'ON' : 'ON',
    'OFF' : 'OFF',
    #<DISCRETO> -> 'FRIO' | 'CALOR' | 'VENT' 
    'FRIO' : 'FRIO',
    'CALOR' : 'CALOR',
    'VENT' : 'VENT',
    #<NOMBRE_COLORES -> 'blanco' | 'rojo' | 'azul'
    'BLANCO' : 'BLANCO',
    'ROJO' : 'ROJO',
    'AZUL' : 'AZUL',
}

tokens = tokens + list(reservado.values())

#=================================================================================
#=====================================REGLAS======================================
#=================================================================================

#------------Tokens Compuestos------------

#Atributos posibles.
def t_ATRIBUTO(t):
    r'\.(ESTADO|BRILLO|COLOR|TEMP_OBJ|TEMP_ACT|HORA|MODO|FECHA|POSICION|VOLUMEN|MUTE|MENSAJE|EMAIL_NOTIF|ACTIVADA)'
    return t

#<TEXTO> -> "cadena"
def t_TEXTO(t):
    r'".*?"'
    return t

#<TEMP> -> numreal '°C'
def t_VALOR_TEMPERATURA(t):
    #Rango mayor de temp. act, abarca ambas tem. act y obj.
    r'(-10|-[1-9]|[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|50)°C'
    return t

#<PERCENT> -> numint '%'
def t_PERCENT(t):
    r'(([0-9]|[1-9][0-9])|100)%'
    return t

#<HORA> -> numint ':' numint
def t_HORA(t):
    r'(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]'
    return t

#<TIEMPO> -> numint 'h' | numint 'm' | numint 's' 
def t_TIEMPO(t):
    #(hasta dos dígitos, se puede poner más)
    r'([0-9] h|[1-9][0-9]h|[0-9]m|[1-9][0-9]m|[0-9]s|[1-9][0-9]s)'
    return t

#<ILUMINANCIA> -> numint'lux'
def t_ILUMINANCIA(t):
    #numint'lux'
    r'([0-9]|[1-9][0-9]|[1-9][0-9][0-9]|1000)lux'
    return t

#<DATE> -> numint '/' numint '/' numint
def t_DATE(t):
    r'([1-2][0-9]|3[0-1]|[0-9])/(1[0-2]|[1-9])/(19[0-9][0-9]|20[0-9][0-9])'
    return t

#<EMAIL> -> nombre_usuario '@' #dominio'.'extension
def t_EMAIL(t):
    r'[a-zA-Z0-9\.\+\-]+@[a-zA-Z0-9\.\+\-]+\.[a-zA-Z]{2,4}'
    return t

#-------------Tokens Simples-------------
def t_IGUAL(t):
    r'\=='
    return t

def t_DISTINTO(t):
    r'\!='
    return t

def t_MAYORIGUAL(t):
    r'\>='
    return t

def t_MENORIGUAL(t):
    r'\<='
    return t

t_ASIGNACION = r'='
t_PUNTO = r'\.'
t_GUIONBAJO = r'_'
t_MAYOR = r'>'
t_MENOR = r'<'

#-------Reglas varias para el análisis-------

#Reglas para ignorar caracteres
t_ignore  = ' \t'            #Ignora espacios y tabs
t_ignore_COMMENT = r'\/\/.*' #Ignorar comentarios (desde un numeral hasta cualquier caracter seguido del numeral)

#Regla para manejar palabras reservadas e identificadores (palabras que son tokens pero no son pal. reservadas).
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservado.get(t.value,'ID')
    return t

#Regla para trackear num. de linea:
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Regla para trackear num. de columna: (va al final del bucle, sirve para determinar en qué columna ocurrió un error)
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

#Regla para trackear errores (caracteres ilegales)
def t_error(t):
    columna = find_column(t.lexer.lexdata, t)    
    print(f"Carácter ilegal '{t.value[0]}' en la Línea {t.lexer.lineno}, Columna {columna}")
    t.lexer.skip(1)

#=================================================================================
#===================================FUNCIONES=====================================
#=================================================================================

#Clean Screen (Limpiar pantalla)
def limpiarPantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

#Gotoxy (se posiciona en un punto específico de la pantalla)
def gotoxy(x, y):
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()                              

#Lee un caracter ingresado desde el teclado directamente desde el buffer de entrada
def read_single_key_windows():
    tecla_bytes = msvcrt.getch()
    if tecla_bytes == b'\xe0' or tecla_bytes == b'\x00':
        return tecla_bytes.decode('latin-1') + msvcrt.getch().decode('latin-1')  
    return tecla_bytes.decode('latin-1')

# Oculta el cursor parpadeante de la terminal
def ocultar_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

# Vuelve a mostrar el cursor
def mostrar_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def recuadrosMenu():
    gotoxy(1, 1)
    for y in range(1, yMaxPantalla):
        for x in range(1, xMaxPantalla):
            if (x == 1) or (x == xMaxPantalla-1):
                gotoxy(x,y)
                print("▓", end="")
            if (y == 1) or (y == yMaxPantalla-1):
                gotoxy(x,y)
                print("▓", end="")

def dibujoCarpeta():
    gotoxy(25,5)
    print('************ ')
    gotoxy(25,6)
    print('*************=================')
    gotoxy(25,7)
    print('-=============================')
    gotoxy(25,8)
    print('==============================')
    gotoxy(25,9)
    print('========####==================')
    gotoxy(25,10)
    print('======########================')
    gotoxy(25,11)
    print('====############==============')
    gotoxy(25,12)
    print('==################============')
    gotoxy(25,13)
    print('####################==========')
    gotoxy(25,14)
    print('######################========')
    gotoxy(25,15)
    print('########################======')


def selecOpcion():
    num = {'1','2','3','4','5','8','9','0'}
    while True:
        tecla = msvcrt.getch().decode('utf-8')    
        if tecla in num:
            return tecla


def dibujarMenu():
    limpiarPantalla()
    recuadrosMenu()
    dibujoCarpeta()
    gotoxy(27,18)
    console.print(f"[bold italic u grey70]Analizador léxico (Lexer)[/bold italic u grey70]")
    gotoxy(29,21)
    console.print(f"[bold italic dim white]Seleccione una opción...[/bold italic dim white]")
    gotoxy(17,23)
    print("1- Seleccionar archivo (del directorio actual)")
    gotoxy(23,24)
    print("2- Escribir programa manualmente")
    gotoxy(xMaxPantalla-32,yMaxPantalla-2)
    console.print(f"[bold italic dim white]BinaryBuilders. UTN FRRe. 2026[/bold italic dim white]")
    gotoxy(1,yMaxPantalla+1)

def leerArchivosEnDirectorio():
    global datos
    global nombreArch
    global lecturaDeArch
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    todos_los_archivos = os.listdir(ruta_script)
    lista_txt = [archivo for archivo in todos_los_archivos if archivo.endswith('.txt')]
    
    limpiarPantalla()
                
    if not lista_txt:
        limpiarPantalla()
        print("No se encontraron archivos .txt en el directorio del ejecutable.")
        print("Cierre el programa, coloque archivos .txt e inicie de nuevo...")
        msvcrt.getch()
        #limpiarPantalla()
        sys.exit()
        return None

    else:
        dibujoCarpeta(); recuadrosMenu()
        while True:
            gotoxy(29, 18)
            console.print(f"[bold italic dim white]Seleccione un archivo...[/bold italic dim white]")
            gotoxy(xMaxPantalla-32, yMaxPantalla-2)
            console.print(f"[bold italic dim white]BinaryBuilders. UTN FRRe. 2026[/bold italic dim white]")
            
            x = 25; y = 21
            for i in range(len(lista_txt)):
                gotoxy(x, y+i)
                print(f"\033[32m{f'{i+1} - {lista_txt[i]}'.center(30)}\033[0m")

            op = int(selecOpcion())-1
            if op in range(len(lista_txt)):
    
                nombreArch = lista_txt[op]
                if os.path.exists(nombreArch):
                    with open(nombreArch, "r", encoding="utf-8") as f:
                        datos = f.read()
                        limpiarPantalla()
                        recuadrosMenu()
                        dibujoCarpeta()
                        gotoxy(29, 19)
                        console.print(f"[bold italic dim white]Archivo leido con éxito[/bold italic dim white]")
                        gotoxy(17, 20)
                        console.print(f"[bold italic dim white]Presione una tecla para iniciar análisis léxico...[/bold italic dim white]")
                        msvcrt.getch()
                        lecturaDeArch=True
                        return False
                    
def escribirProgramaManualmente():
    global datos
    global lecturaDeArch
    limpiarPantalla()
    mostrar_cursor()
    console.print(f"[bold italic dim white]Escriba el programa manualmente a continuación:[/bold italic dim white]")
    datos = input()
    lecturaDeArch=False

def iniciarLexer():

    lexer.input(datos)
    if lecturaDeArch: #lectura de arch sirve solo para indicar qué archivo se está analizando actualmente al seleccionar analisis mediante .txt, sin que tire error si se escribe el programa manualmente
        print("Analisis de archivo: ",nombreArch); print()
    
    #Tokenizar el programa (hacer analisis lexico a toda la cadena del programa y encontrar tokens)
    while True:
        tok = lexer.token()
        if not tok: 
            break
        #printear el token con toda su información (todos los atributos a la vez):    
        #print(tok) 
        #printear cada atributo por separado:
        #print(tok.type, tok.value, tok.lineno, tok.lexpos)
        print(f"Token encontrado: {tok.value:<10} de tipo: {tok.type}")
    
    print()
    console.print(f"[bold italic dim white]Terminado.[/bold italic dim white]")
    console.print(f"[bold italic dim white]Presione una tecla para cerrar el programa...[/bold italic dim white]")
    #mostrar_cursor()
    msvcrt.getch()
    

#=================================================================================
#=============================COMIENZO DEL PROGRAMA===============================
#=================================================================================

lexer = lex.lex()   #Construir el lexer
xMaxPantalla = 80; yMaxPantalla = 30; console = Console() #Solo para mostrar títulos con estilos
ocultar_cursor(); dibujarMenu()


if selecOpcion() == '1':
    leerArchivosEnDirectorio()
else:
    escribirProgramaManualmente()
limpiarPantalla()

iniciarLexer()


'''
------------------ANOTACIONES PARA HACER------------------#

-Leer la consigna para ver qué se pide que haga el lexer...



-Agregar tokens BOOLEANOS (TRUE,FALSE,ON,OFF, quitarlos de palabras clave
y diferenciarlos), PUNTO (.) y operadores lógicos AND,OR,NOT, posiblemente
agregar también identificadores que empiezan con '_'. Al igual que con todas
las demás reglas que están en palabras reservadas (las que tienen anotaciones).

-Para los caracteres ilegales hay que mostrar en qué linea y columna se los encontró.

-Hacer que analice el ejemplo del TPI.

-(posiblemente haya que hacer esto) Para los tokens compuestos, 
En las expresiones regulares, para las partes que tienen "opciones"
poner las opciones más largas primero (para que el lexer no se confunda).



-Estos tokens se deben tener:

//No se deben distinguir entre mayúsculas y minúsculas
//Las palabras reservadas no se podrán usar como identificadores

Palabras reservadas:
WHEN
IF/THEN/ELSE
DO
END
EVERY

Identificadores de Sensores, Dispositivos y Atributos:

Sensores:
sensor_temp
sensor humedad
sensor_luz
sensor_movimiento
sensor_humo

Actuadores:
foco_
aire_
persiana_
cerradura_
reloj_
altavoz_
alarma_

Literales y Unidades (Tokens Compuestos):
texto
Booleanos
Numéricos con Unidad:
	TEMPERATURA
	PORCENTAJE
	TIEMPO
	ILUMINANCIA
HORA
FECHA
Email

Operadores y Delimitadores:
Comparación
Lógicos
Asignación
Puntuación

-------------------------PREGUNTAS------------------------#

-Hace falta diferenciar en esta instancia TEMP_OBJ y TEMP_ACT dado que
ambas son temperaturas pero con distinto rango, o solo las incluimos en una sola regla de "TEMPERATURA"?
Dado que puede ocurrir que, se encuente una temperatura que entre en el rango de ambas, pero se
reconocerá el token como la primer regla que se encuentre, por más que no sea el tipo de temperatura
verdadera, solo se diferenciaría cada una si, dicha temperatura excede el rango de la temperatura 
de menor rango.

-Hay que tener en cuenta a los distintos actuadores como tokens o basta con que sean IDs?
Al igual que con los sensores e identificadores para actuadores y para sensores.

-Las palabras como FRIO, CALOR, ROJO, BLANCO, las tratamos como tokens de categorías separadas
(es decir, por ejemplo: ROJO token de tipo "color") o los tratamos a esas palabras 
como "palabras reservadas"?

-Qué cosas deben ser ID y qué cosas deben ser Tokens con reglas (como las mencionadas anteriormente)?
'''