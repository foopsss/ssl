from rich.console import Console
import msvcrt
import os
import sys
import re
import ply.lex as lex

#=================================================================================
#=====================================LEXER=======================================
#=================================================================================

tokens = [
    'ATRIBUTOS_FOCO',
    'ATRIBUTOS_AIRE',
    'ATRIBUTOS_PERSIANA',
    'ATRIBUTOS_RELOJ',
    'ATRIBUTOS_ALTAVOZ',
    'ATRIBUTOS_ALARMA',
    'ATRIBUTO_ESTADO',
    'SENSOR_TEMPERATURA',
    'SENSOR_HUMEDAD',
    'SENSOR_LUZ',
    'SENSOR_MOVIMIENTO',
    'SENSOR_HUMO',
    'ACTUADOR_FOCO',
    'ACTUADOR_AIRE',
    'ACTUADOR_PERSIANA',
    'ACTUADOR_CERRADURA',
    'ACTUADOR_RELOJ',
    'ACTUADOR_ALTAVOZ',
    'ACTUADOR_ALARMA',
    'TEXTO',
    'BOOL_DISPOSITIVO',
    'BOOL_ACTUADOR',
    'VALOR_TEMPERATURA',
    'PERCENT',
    'TIEMPO',
    'ILUMINANCIA',
    'HORA',
    'DATE',
    'EMAIL',
    'DISCRETO',
    'NOMBRE',
    'OP_COMPARADOR',
    'OP_LOGICO',
    'OP_NEGACION',
    'ASIGNACION',
    'PUNTO',
    'GUION_BAJO',
    'COMMENT',
    'ID'
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
}

tokens = tokens + list(reservado.values())

#=================================================================================
#=========================REGLAS PARA RECONOCER TOKENS============================
#=================================================================================

#Atributos posibles.

def t_ATRIBUTOS_FOCO(t):
    r'(.BRILLO|.COLOR)'
    return t

def t_ATRIBUTOS_AIRE(t):
    r'(.MODO|.TEMP_ACT|.TEMP_OBJETIVO|.TEMP_OBJ)'
    return t

def t_ATRIBUTOS_PERSIANA(t):
    r'.POSICION'
    return t

def t_ATRIBUTOS_RELOJ(t):
    r'(.HORA|.FECHA)'
    return t

def t_ATRIBUTOS_ALTAVOZ(t):
    r'(.VOLUMEN|.MUTE|.MENSAJE|.EMAIL_NOTIF|.EMAIL)' 
    return t

def t_ATRIBUTOS_ALARMA(t):
    r'.ACTIVADA'
    return t


def t_ATRIBUTO_ESTADO(t):
    r'.ESTADO'
    return t

#Sensores.

#sensor_temp
def t_SENSOR_TEMPERATURA(t):
    r'SENSOR_TEMP'
    return t

#sensor humedad
def t_SENSOR_HUMEDAD(t):
    r'SENSOR_HUMEDAD'
    return t

#sensor_luz
def t_SENSOR_LUZ(t):
    r'SENSOR_LUZ'
    return t

#sensor_movimiento
def t_SENSOR_MOVIMIENTO(t):
    r'SENSOR_MOVIMIENTO'
    return t

#sensor_humo
def t_SENSOR_HUMO(t):
    r'SENSOR_HUMO'
    return t

#Actuadores.

#foco_
def t_ACTUADOR_FOCO(t):
    r'FOCO'
    return t
#aire_
def t_ACTUADOR_AIRE(t):
    r'AIRE'
    return t

#persiana_
def t_ACTUADOR_PERSIANA(t):
    r'PERSIANA'
    return t

#cerradura_
def t_ACTUADOR_CERRADURA(t):
    r'CERRADURA'
    return t

#reloj_
def t_ACTUADOR_RELOJ(t):
    r'RELOJ'
    return t

#altavoz_
def t_ACTUADOR_ALTAVOZ(t):
    r'ALTAVOZ'
    return t

#alarma_
def t_ACTUADOR_ALARMA(t):
    r'ALARMA'
    return t

#Tokens Compuestos

#<TEXTO> -> "cadena"
def t_TEXTO(t):
    r'[\"“\'][^\"\n“”\']*[\"”\']'  
    return t

#<BOOL_DISPOSITIVO> -> 'TRUE' | 'FALSE' 
def t_BOOL_DISPOSITIVO(t):
    r'(TRUE|FALSE)'
    return t

#<BOOL_ACTUADOR> -> 'ON' | 'OFF'  
def t_BOOL_ACTUADOR(t):
    r'(ON|OFF)'
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

#<HORA> -> numint ':' numint
def t_HORA(t):
    r'(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]'
    return t

#<DATE> -> numint '/' numint '/' numint
def t_DATE(t):
    r'([1-2][0-9]|3[0-1]|[0-9])/(1[0-2]|[1-9])/(19[0-9][0-9]|20[0-9][0-9])'
    return t

#<EMAIL> -> nombre_usuario '@' #dominio'.'extension
def t_EMAIL(t):
    r'[a-zA-Z0-9\.\+\-]+@[a-zA-Z0-9\.\+\-]+\.[a-zA-Z]{2,4}'
    return t

#<DISCRETO> -> 'FRIO' | 'CALOR' | 'VENT' 
def t_DISCRETO(t):
    r'(FRIO|CALOR|VENT)'
    return t

#<NOMBRE_COLORES -> 'blanco' | 'rojo' | 'azul'
def t_NOMBRE(t):
    r'(BLANCO|ROJO|AZUL|BLUE|RED|WHITE)'
    return t

#Operadores comparadores

#<opcomparador> -> '==' | '!=' | '>' | '<' | '>=' | '<=' Operadores comparadores en general
def t_OP_COMPARADOR(t):
    r'(==|!=|>|<|>=|<=)' 
    return t

#Operadores logicos

#<oplogico> -> 'AND' | 'OR'
def t_OP_LOGICO(t):
    r'(AND|OR)'
    return t

#<opnot> -> 'NOT'
def t_OP_NEGACION(t):
    r'NOT'
    return t

#-------------Tokens Simples-------------

t_ASIGNACION = r'='
t_PUNTO = r'\.'
t_GUION_BAJO = r'_'

#-------Reglas varias para el análisis léxico-------

#Reglas para ignorar caracteres
t_ignore  = ' \t'            #Ignora espacios y tabs
t_ignore_COMMENT = r'\/\/.*' #Ignorar comentarios (desde un numeral hasta cualquier caracter seguido del numeral)

#Regla para manejar palabras reservadas e identificadores (palabras que son tokens pero no son pal. reservadas ni tienen reglas).
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reservado.get(t.value.upper(),'ID')
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
#=====================FUNCIONES PARA MOSTRAR DATOS POR PANTALLA===================
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
    limpiarPantalla();recuadrosMenu();dibujoCarpeta()
    gotoxy(27,18)
    console.print(f"[bold italic u grey70]Analizador léxico (Lexer)[/bold italic u grey70]")
    gotoxy(23,21)
    console.print(f"[bold italic dim white]Presione el numero de la opción...[/bold italic dim white]")
    gotoxy(24,23)
    print("1- Especificar ruta de archivo.")
    gotoxy(23,24)
    print("2- Escribir programa manualmente.")
    gotoxy(xMaxPantalla-32,yMaxPantalla-2)
    gotoxy(35,25)
    print("3- Salir.")
    gotoxy(xMaxPantalla-32,yMaxPantalla-2)
    console.print(f"[bold italic dim white]BinaryBuilders. UTN FRRe. 2026[/bold italic dim white]")
    gotoxy(1,yMaxPantalla+1)


def especificarRutaArchivo():
    global datos
    
    limpiarPantalla()
    entrada = input("Ingrese la ruta o arrastre el archivo .txt y presione ENTER: ").strip()
    ruta = entrada.lstrip('& ').strip('"\'')
    
    if not (os.path.exists(ruta) and ruta.lower().endswith('.txt')):
        limpiarPantalla()
        print("Error: La ruta no existe o el archivo no es un .txt")
        print("Presione una tecla para salir")
        msvcrt.getch()
        sys.exit()
        return False

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
    except Exception:
        contenido = None

    match contenido:
        case None:
            limpiarPantalla()
            print("Error: No se pudo leer el archivo.")
            print("Presione una tecla para salir")
            msvcrt.getch()
            sys.exit()
            return False
        case _:
            datos = contenido
            return True


def escribirProgramaManualmente():
    global datos

    lines = []
    str_input = ""

    limpiarPantalla()
    mostrar_cursor()
    console.print(f"[bold italic dim white]Escriba el programa manualmente a continuación.[/bold italic dim white]")
    console.print(f"[bold italic dim white]Cuando no quiera introducir más líneas, escriba 'FIN' y presione Enter.[/bold italic dim white]")

    while str_input != "FIN":
        str_input = input()
        lines.append(str_input)

    # Se unen todas las líneas en una sola cadena,
    # excluyendo la última línea, "FIN", que finaliza
    # la captación de strings.
    datos = "\n".join(lines[:-1])

def iniciarLexer():

    lexer.input(datos)

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
    console.print(f"[bold italic dim white]Presione una tecla para volver al menú...[/bold italic dim white]")
    #mostrar_cursor()
    msvcrt.getch()
    
#=================================================================================
#=============================COMIENZO DEL PROGRAMA===============================
#=================================================================================

option = 0 #solo para que no se rompa antes del while
while (option != 3):

    lexer = lex.lex(reflags=re.IGNORECASE)   #Construir el lexer
    xMaxPantalla = 80; yMaxPantalla = 30; console = Console() #Solo para mostrar títulos con estilos
    ocultar_cursor(); dibujarMenu()

    option = selecOpcion()
    if option == '1':
        especificarRutaArchivo()
        limpiarPantalla()
        if datos:
            iniciarLexer()
    elif option == '2':
        escribirProgramaManualmente()
        limpiarPantalla()
        if datos:
            iniciarLexer()
    elif option == '3':
        limpiarPantalla()
        sys.exit()



'''
#---------TODOS LOS TOKENS SOLICITADOS EN EL TPI-----------#

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
sensor_humedad
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

Atributos: Diferenciados para cada actuador.

Operadores y Delimitadores:
Comparación
Lógicos
Asignación
Puntuación

#=================ACLARACIONES DEL CÓDIGO==================#

#Aclaración de la regla (función) para el atributo de estado "t_ATRIBUTO_ESTADO". El mismo compartido entre: foco, aire, cerradura, alarma.
#Por ello lo colocamos como una sola regla, dado que, si incluimos la cadena ".ESTADO" en las
#demás funciones (reglas para reconocer cada token) el lexer va a decir que es del tipo de token
#de la función que primero esté definida que reconozca ese token, es decir, siempre dirá que es: "atributo_foco".

#Aclaracion para atributos de aire (t_ATRIBUTOS_AIRE)
#también irían atributos de temperatura, pero por ahora con la regla de "temperatura" es suficiente para cubrir ambos atributos.

#Aclaración para atributo de cerradura (no lo definimos)
#No colocamos atributo de cerradura en esta instancia, ya que tiene solo ".estado" y ese atributo es compartido por 4 actuadores más.

#Notamos que hay varias cosas mal escritas en el ejemplo del TPI, como son el caso de:
- foco_patio.color = blue //debería ser "azul" en vez de "blue"
- altavoz_comedor.email = bomberos@smart-home.com.ar //debería ser atributo ".email_notif" en vez de ".email"
- aire_acondicionado.temp_objetivo = 22°C //debería ser "temp_obj"

'''