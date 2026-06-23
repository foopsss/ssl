import ply.lex as lex

tokens = [
    'ATRIBUTOS_FOCO_BRILLO',
    'ATRIBUTOS_FOCO_COLOR',
    'ATRIBUTOS_AIRE_MODO',
    'ATRIBUTOS_AIRE_TEMP_ACT',
    'ATRIBUTOS_AIRE_TEMP_OBJ',
    'ATRIBUTOS_PERSIANA',
    'ATRIBUTOS_RELOJ_HORA',
    'ATRIBUTOS_RELOJ_FECHA',
    'ATRIBUTOS_ALTAVOZ_VOLUMEN',
    'ATRIBUTOS_ALTAVOZ_MUTE',
    'ATRIBUTOS_ALTAVOZ_MENSAJE',
    'ATRIBUTOS_ALTAVOZ_EMAIL',
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
    'TEXTO', 'BOOL_DISPOSITIVO',
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

reservado = {
    'IF': 'IF', 'THEN': 'THEN', 'ELSE': 'ELSE',
    'WHEN' : 'WHEN', 'END': 'END', 'EVERY': 'EVERY', 'DO' : 'DO',
}
tokens = tokens + list(reservado.values())

def t_ATRIBUTOS_FOCO_BRILLO(t): r'\.BRILLO'; return t
def t_ATRIBUTOS_FOCO_COLOR(t): r'\.COLOR'; return t
def t_ATRIBUTOS_AIRE_MODO(t): r'\.MODO'; return t
def t_ATRIBUTOS_AIRE_TEMP_ACT(t): r'\.TEMP_ACT'; return t
def t_ATRIBUTOS_AIRE_TEMP_OBJ(t): r'(\.TEMP_OBJETIVO|\.TEMP_OBJ)'; return t
def t_ATRIBUTOS_PERSIANA(t): r'\.POSICION'; return t
def t_ATRIBUTOS_RELOJ_HORA(t): r'\.HORA'; return t
def t_ATRIBUTOS_RELOJ_FECHA(t): r'\.FECHA'; return t
def t_ATRIBUTOS_ALTAVOZ_VOLUMEN(t): r'\.VOLUMEN'; return t
def t_ATRIBUTOS_ALTAVOZ_MUTE(t): r'\.MUTE'; return t
def t_ATRIBUTOS_ALTAVOZ_MENSAJE(t): r'\.MENSAJE'; return t
def t_ATRIBUTOS_ALTAVOZ_EMAIL(t): r'(\.EMAIL_NOTIF|\.EMAIL)'; return t
def t_ATRIBUTOS_ALARMA(t): r'\.ACTIVADA'; return t
def t_ATRIBUTO_ESTADO(t): r'\.ESTADO'; return t

def t_SENSOR_TEMPERATURA(t): r'SENSOR_TEMP'; return t
def t_SENSOR_HUMEDAD(t): r'SENSOR_HUMEDAD'; return t
def t_SENSOR_LUZ(t): r'SENSOR_LUZ'; return t
def t_SENSOR_MOVIMIENTO(t): r'SENSOR_MOVIMIENTO'; return t
def t_SENSOR_HUMO(t): r'SENSOR_HUMO'; return t

def t_ACTUADOR_FOCO(t): r'FOCO'; return t
def t_ACTUADOR_AIRE(t): r'AIRE'; return t
def t_ACTUADOR_PERSIANA(t): r'PERSIANA'; return t
def t_ACTUADOR_CERRADURA(t): r'CERRADURA'; return t
def t_ACTUADOR_RELOJ(t): r'RELOJ'; return t
def t_ACTUADOR_ALTAVOZ(t): r'ALTAVOZ'; return t
def t_ACTUADOR_ALARMA(t): r'ALARMA'; return t

def t_TEXTO(t): r'[\"“\'][^\"\n“”\']*[\"”\']'; return t
def t_BOOL_DISPOSITIVO(t): r'(TRUE|FALSE)'; return t
def t_BOOL_ACTUADOR(t): r'(ON|OFF)'; return t
def t_VALOR_TEMPERATURA(t): r'(-10|-[1-9]|[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|50)°C'; return t
def t_PERCENT(t): r'(([0-9]|[1-9][0-9])|100)%'; return t
def t_TIEMPO(t): r'([0-9]\s?H|[1-9][0-9]\s?H|[0-9]\s?M|[1-9][0-9]\s?M|[0-9]\s?S|[1-9][0-9]\s?S)'; return t
def t_ILUMINANCIA(t): r'([0-9]|[1-9][0-9]|[1-9][0-9][0-9]|1000)LUX'; return t
def t_HORA(t): r'(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]'; return t
def t_DATE(t): r'([1-2][0-9]|3[0-1]|[0-9])/(1[0-2]|[1-9])/(19[0-9][0-9]|20[0-9][0-9])'; return t
def t_EMAIL(t): r'[A-Z0-9\.\+\-]+@[A-Z0-9\.\+\-]+\.[A-Z]{2,4}'; return t
def t_DISCRETO(t): r'(FRIO|CALOR|VENT)'; return t
def t_NOMBRE(t): r'(BLANCO|ROJO|AZUL|BLUE|RED|WHITE)'; return t
def t_OP_COMPARADOR(t): r'(==|!=|>|<|>=|<=)'; return t
def t_OP_LOGICO(t): r'(AND|OR)'; return t
def t_OP_NEGACION(t): r'NOT'; return t

t_ASIGNACION = r'='
t_PUNTO = r'\.'
t_GUION_BAJO = r'_'
t_ignore = ' \t'
t_ignore_COMMENT = r'\/\/.*'

def t_ID(t): 
    r'[A-Z][A-Z0-9_]*'
    t.type = reservado.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def find_column(input_data, token):
    line_start = input_data.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def t_error(t):
    #columna = find_column(t.lexer.lexdata, t)    
    #caracterOriginal = datosOriginal[t.lexpos]
    #print(f"Carácter ilegal '{caracterOriginal}' en la Línea {t.lexer.lineno}, Columna {columna}")
    t.lexer.skip(1)


#==================================== MAIN ====================================#

lexer = lex.lex() #esto es lo único que queda para el parser, lo que sigue se quita o se comenta.

#datos = "WHEN sensor_luz < 250lux DO"
#datosOriginal = datos               #Para mostrar palabra original en pantalla
#datosMayusculas = datos.upper()     #Cadena total transformada en mayúsculas

#lexer.input(datosMayusculas)

#while True:
#    tok = lexer.token()
#    if not tok: 
#        break
#    inicio = tok.lexpos
#    fin = inicio + len(tok.value)
#    print(f"Token encontrado: {datosOriginal[inicio:fin]:<15} de tipo: {tok.type}")











#==========================Anotaciones y aclaraciones==========================#

#Aclaraciones de código:
#Todas las palabras se convierten a mayúscula para analizar cada token
#Se muestra la palabra original por pantalla, pero por detras todo se hace con la cadena convertida todo a mayúsculas

#Cosas para hacer:
#Revisar que el lexer actual tenga todas las reglas para derivar lo que se pide en la consigna junto con su expresión regular
#Agregar reglas de valores específicos faltantes tales como ambos tipos de temperatura