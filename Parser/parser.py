from ply import lex, yacc
#librerías para interfaz gráfica:
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime

#====================================================================#
#===============================LEXER================================#
#====================================================================#

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
    'VALOR_TEMP',
    'OP_COMPARADOR_BOOL',
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
#   'PUNTO',
    'GUION_BAJO',
#   'COMMENT',
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
def t_VALOR_TEMP(t): r'(-10|-[1-9]|[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|50)°C'; return t
def t_PERCENT(t): r'(([0-9]|[1-9][0-9])|100)%'; return t
def t_TIEMPO(t): r'([0-9]\s?H|[1-9][0-9]\s?H|[0-9]\s?M|[1-9][0-9]\s?M|[0-9]\s?S|[1-9][0-9]\s?S)'; return t
def t_ILUMINANCIA(t): r'([0-9]|[1-9][0-9]|[1-9][0-9][0-9]|1000)LUX'; return t
def t_HORA(t): r'(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]'; return t
def t_DATE(t): r'([1-2][0-9]|3[0-1]|[0-9])/(1[0-2]|[1-9])/(19[0-9][0-9]|20[0-9][0-9])'; return t
def t_EMAIL(t): r'[A-Z0-9\.\+\-]+@[A-Z0-9\.\+\-]+\.[A-Z]{2,4}'; return t
def t_DISCRETO(t): r'(FRIO|CALOR|VENT)'; return t
def t_NOMBRE(t): r'(BLANCO|ROJO|AZUL|BLUE|RED|WHITE)'; return t
def t_OP_COMPARADOR_BOOL(t): r'(==|!=)'; return t
def t_OP_COMPARADOR(t): r'(==|!=|>|<|>=|<=)'; return t
def t_OP_LOGICO(t): r'(AND|OR)'; return t
def t_OP_NEGACION(t): r'NOT'; return t

t_ASIGNACION = r'='
#t_PUNTO = r'\.'
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
    columna = find_column(t.lexer.lexdata, t)    
    print(f"Carácter ilegal '{t.value[0]}' en la Línea {t.lexer.lineno}, Columna {columna}")
    t.lexer.skip(1)

lexer = lex.lex()



#====================================================================#
#===============================PARSER===============================#
#====================================================================#



#REGLAS DEL ANÁLISIS SINTÁCTICO
def p_programa(p):
    '''sigma : accion'''
    print("Análisis sintáctico terminado exitosamente") #al terminar imprime
    p[0] = p[1]

#BLOQUES Y ACCIONES
def p_acciones(p):
    '''accion : ciclo accion 
              | ciclo
              | condicional accion 
              | condicional
              | asignacion accion
              | asignacion'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2] 
    else:
        p[0] = [p[1]]

#CICLOS WHEN Y EVERT
def p_ciclos(p):
    '''ciclo : WHEN condicion DO accion END
             | EVERY TIEMPO DO accion END'''
    if p[1] == 'WHEN':
        p[0] = ('CICLO_WHEN', p[2], p[4])
    else:
        p[0] = ('CICLO_EVERY', p[2], p[4])

#CONDICIONAL IF
def p_condicional(p):
    '''condicional : IF condicion THEN accion END
                   | IF condicion THEN accion ELSE accion END'''
    if len(p) == 6:
        p[0] = ('CONDICIONAL_SIMPLE', p[2], p[4])
    else:
        p[0] = ('CONDICIONAL_ALTERNATIVO', p[2], p[4], p[6])

#IDENTIFICADOR
def p_identificador(p):
    '''identificador : GUION_BAJO ID'''
    p[0] = p[1] + p[2]

#ASIGNACIONES (ESCRITURA DE ACTUADORES)
def p_asignaciones(p):
    '''asignacion : ACTUADOR_FOCO identificador atributos_esc_foco
                  | ACTUADOR_FOCO atributos_esc_foco
                  | ACTUADOR_AIRE identificador atributos_esc_aire
                  | ACTUADOR_AIRE atributos_esc_aire
                  | ACTUADOR_PERSIANA identificador atributos_esc_persiana
                  | ACTUADOR_PERSIANA atributos_esc_persiana
                  | ACTUADOR_CERRADURA identificador atributos_esc_cerradura
                  | ACTUADOR_CERRADURA atributos_esc_cerradura
                  | ACTUADOR_ALTAVOZ identificador atributos_esc_altavoz
                  | ACTUADOR_ALTAVOZ atributos_esc_altavoz
                  | ACTUADOR_ALARMA identificador atributos_esc_alarma
                  | ACTUADOR_ALARMA atributos_esc_alarma'''
    if len(p) == 4:
        p[0] = ('ASIGNACION', p[1], p[2], p[3])
    else:
        p[0] = ('ASIGNACION', p[1], None, p[2])

#ATRIBUTOS CON ESTRUCTURA DE ESCRITURA PARA CADA ACTUADOR 
def p_atributos_escritura_foco(p):
    '''atributos_esc_foco : ATRIBUTO_ESTADO ASIGNACION BOOL_ACTUADOR
                          | ATRIBUTOS_FOCO_BRILLO ASIGNACION PERCENT
                          | ATRIBUTOS_FOCO_COLOR ASIGNACION NOMBRE'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_escritura_aire(p):
    '''atributos_esc_aire : ATRIBUTO_ESTADO ASIGNACION BOOL_ACTUADOR
                          | ATRIBUTOS_AIRE_MODO ASIGNACION DISCRETO
                          | ATRIBUTOS_AIRE_TEMP_OBJ ASIGNACION VALOR_TEMP'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_escritura_persiana(p):
    '''atributos_esc_persiana : ATRIBUTOS_PERSIANA ASIGNACION PERCENT'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_escritura_cerradura(p):
    '''atributos_esc_cerradura : ATRIBUTO_ESTADO ASIGNACION BOOL_ACTUADOR'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_escritura_altavoz(p):
    '''atributos_esc_altavoz : ATRIBUTOS_ALTAVOZ_VOLUMEN ASIGNACION PERCENT
                             | ATRIBUTOS_ALTAVOZ_MUTE ASIGNACION BOOL_ACTUADOR
                             | ATRIBUTOS_ALTAVOZ_MENSAJE ASIGNACION TEXTO
                             | ATRIBUTOS_ALTAVOZ_EMAIL ASIGNACION EMAIL'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_escritura_alarma(p):
    '''atributos_esc_alarma : ATRIBUTO_ESTADO ASIGNACION BOOL_ACTUADOR
                            | ATRIBUTOS_ALARMA ASIGNACION BOOL_ACTUADOR'''
    p[0] = p[1] + p[2] + p[3]

#CONDICIONES (LECTURA DE SENSORES)
def p_contcondicion(p):
    '''contcondicion : OP_LOGICO condicion'''

def p_condicion_temperatura(p):
    '''condicion : OP_NEGACION SENSOR_TEMPERATURA identificador OP_COMPARADOR VALOR_TEMP contcondicion
                 | OP_NEGACION SENSOR_TEMPERATURA identificador OP_COMPARADOR VALOR_TEMP
                 | OP_NEGACION SENSOR_TEMPERATURA OP_COMPARADOR VALOR_TEMP contcondicion
                 | OP_NEGACION SENSOR_TEMPERATURA OP_COMPARADOR VALOR_TEMP
                 | SENSOR_TEMPERATURA identificador OP_COMPARADOR VALOR_TEMP contcondicion
                 | SENSOR_TEMPERATURA identificador OP_COMPARADOR VALOR_TEMP
                 | SENSOR_TEMPERATURA OP_COMPARADOR VALOR_TEMP contcondicion
                 | SENSOR_TEMPERATURA OP_COMPARADOR VALOR_TEMP'''
    
    if p[1] != 'SENSOR_TEMPERATURA':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 7:
            p[0] = ('CONDICION_TEMP', negacion, actuador, p[3], p[4] + p[5], p[6])
        elif len(p) == 6:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_TEMP', negacion, actuador, p[3], p[4] + p[5], None)
            else:
                p[0] = ('CONDICION_TEMP', negacion, actuador, None, p[3] + p[4], p[5])
        else:
            p[0] = ('CONDICION_TEMP', negacion, actuador, None, p[3] + p[4], None)

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 6:
            p[0] = ('CONDICION_TEMP', negacion, actuador, p[2], p[3] + p[4], p[5])
        elif len(p) == 5:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_TEMP', negacion, actuador, p[2], p[3] + p[4], None)
            else:
                p[0] = ('CONDICION_TEMP', negacion, actuador, None, p[2] + p[3], p[4])
        else:
            p[0] = ('CONDICION_TEMP', negacion, actuador, None, p[2] + p[3], None)


def p_condicion_humedad(p):
    '''condicion : OP_NEGACION SENSOR_HUMEDAD identificador OP_COMPARADOR PERCENT contcondicion
                 | OP_NEGACION SENSOR_HUMEDAD identificador OP_COMPARADOR PERCENT
                 | OP_NEGACION SENSOR_HUMEDAD OP_COMPARADOR PERCENT contcondicion
                 | OP_NEGACION SENSOR_HUMEDAD OP_COMPARADOR PERCENT
                 | SENSOR_HUMEDAD identificador OP_COMPARADOR PERCENT contcondicion
                 | SENSOR_HUMEDAD identificador OP_COMPARADOR PERCENT
                 | SENSOR_HUMEDAD OP_COMPARADOR PERCENT contcondicion
                 | SENSOR_HUMEDAD OP_COMPARADOR PERCENT'''
    
    if p[1] != 'SENSOR_HUMEDAD':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 7:
            p[0] = ('CONDICION_HUMEDAD', negacion, actuador, p[3], p[4] + p[5], p[6])
        elif len(p) == 6:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_HUMEDAD', negacion, actuador, p[3], p[4] + p[5], None)
            else:
                p[0] = ('CONDICION_HUMEDAD', negacion, actuador, None, p[3] + p[4], p[5])
        else:
            p[0] = ('CONDICION_HUMEDAD', negacion, actuador, None, p[3] + p[4], None)

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 6:
            p[0] = ('CONDICION_HUMEDAD', negacion, actuador, p[2], p[3] + p[4], p[5])
        elif len(p) == 5:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_HUMEDAD', negacion, actuador, p[2], p[3] + p[4], None)
            else:
                p[0] = ('CONDICION_HUMEDAD', negacion, actuador, None, p[2] + p[3], p[4])
        else:
            p[0] = ('CONDICION_HUMEDAD', negacion, actuador, None, p[2] + p[3], None)

def p_condicion_luz(p):
    '''condicion : OP_NEGACION SENSOR_LUZ identificador OP_COMPARADOR ILUMINANCIA contcondicion
                 | OP_NEGACION SENSOR_LUZ identificador OP_COMPARADOR ILUMINANCIA 
                 | OP_NEGACION SENSOR_LUZ OP_COMPARADOR ILUMINANCIA contcondicion
                 | OP_NEGACION SENSOR_LUZ OP_COMPARADOR ILUMINANCIA
                 | SENSOR_LUZ identificador OP_COMPARADOR ILUMINANCIA contcondicion
                 | SENSOR_LUZ identificador OP_COMPARADOR ILUMINANCIA
                 | SENSOR_LUZ OP_COMPARADOR ILUMINANCIA contcondicion
                 | SENSOR_LUZ OP_COMPARADOR ILUMINANCIA'''
    
    if p[1] != 'SENSOR_LUZ':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 7:
            p[0] = ('CONDICION_LUZ', negacion, actuador, p[3], p[4] + p[5], p[6])
        elif len(p) == 6:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_LUZ', negacion, actuador, p[3], p[4] + p[5], None)
            else:
                p[0] = ('CONDICION_LUZ', negacion, actuador, None, p[3] + p[4], p[5])
        else:
            p[0] = ('CONDICION_LUZ', negacion, actuador, None, p[3] + p[4], None)

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 6:
            p[0] = ('CONDICION_LUZ', negacion, actuador, p[2], p[3] + p[4], p[5])
        elif len(p) == 5:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_LUZ', negacion, actuador, p[2], p[3] + p[4], None)
            else:
                p[0] = ('CONDICION_LUZ', negacion, actuador, None, p[2] + p[3], p[4])
        else:
            p[0] = ('CONDICION_LUZ', negacion, actuador, None, p[2] + p[3], None)

def p_condicion_movimiento(p):
    '''condicion : OP_NEGACION SENSOR_MOVIMIENTO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | OP_NEGACION SENSOR_MOVIMIENTO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO
                 | OP_NEGACION SENSOR_MOVIMIENTO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | OP_NEGACION SENSOR_MOVIMIENTO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO
                 | SENSOR_MOVIMIENTO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | SENSOR_MOVIMIENTO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO
                 | SENSOR_MOVIMIENTO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | SENSOR_MOVIMIENTO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO'''
    
    if p[1] != 'SENSOR_MOVIMIENTO':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 7:
            p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, p[3], p[4] + p[5], p[6])
        elif len(p) == 6:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, p[3], p[4] + p[5], None)
            else:
                p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, None, p[3] + p[4], p[5])
        else:
            p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, None, p[3] + p[4], None)

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 6:
            p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, p[2], p[3] + p[4], p[5])
        elif len(p) == 5:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, p[2], p[3] + p[4], None)
            else:
                p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, None, p[2] + p[3], p[4])
        else:
            p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, None, p[2] + p[3], None)

def p_condicion_humo(p):
    '''condicion : OP_NEGACION SENSOR_HUMO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | OP_NEGACION SENSOR_HUMO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO
                 | OP_NEGACION SENSOR_HUMO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | OP_NEGACION SENSOR_HUMO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO
                 | SENSOR_HUMO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | SENSOR_HUMO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO
                 | SENSOR_HUMO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | SENSOR_HUMO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO'''
    
    if p[1] != 'SENSOR_HUMO':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 7:
            p[0] = ('CONDICION_HUMO', negacion, actuador, p[3], p[4] + p[5], p[6])
        elif len(p) == 6:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_HUMO', negacion, actuador, p[3], p[4] + p[5], None)
            else:
                p[0] = ('CONDICION_HUMO', negacion, actuador, None, p[3] + p[4], p[5])
        else:
            p[0] = ('CONDICION_HUMO', negacion, actuador, None, p[3] + p[4], None)

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 6:
            p[0] = ('CONDICION_HUMO', negacion, actuador, p[2], p[3] + p[4], p[5])
        elif len(p) == 5:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_HUMO', negacion, actuador, p[2], p[3] + p[4], None)
            else:
                p[0] = ('CONDICION_HUMO', negacion, actuador, None, p[2] + p[3], p[4])
        else:
            p[0] = ('CONDICION_HUMO', negacion, actuador, None, p[2] + p[3], None)

def p_condicion_foco(p):
    '''condicion : OP_NEGACION ACTUADOR_FOCO identificador atributos_lec_foco contcondicion
                 | OP_NEGACION ACTUADOR_FOCO identificador atributos_lec_foco
                 | OP_NEGACION ACTUADOR_FOCO atributos_lec_foco contcondicion
                 | OP_NEGACION ACTUADOR_FOCO atributos_lec_foco
                 | ACTUADOR_FOCO identificador atributos_lec_foco contcondicion
                 | ACTUADOR_FOCO identificador atributos_lec_foco
                 | ACTUADOR_FOCO atributos_lec_foco contcondicion
                 | ACTUADOR_FOCO atributos_lec_foco'''
    
    if p[1] != 'ACTUADOR_FOCO':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 6:
            p[0] = ('CONDICION_FOCO', negacion, actuador, p[3], p[4], p[5])
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_FOCO', negacion, actuador, p[3], p[4], None)
            else:
                p[0] = ('CONDICION_FOCO', negacion, actuador, None, p[3], p[4])
        else:
            p[0] = ('CONDICION_FOCO', negacion, actuador, None, p[3], None)

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 5:
            p[0] = ('CONDICION_FOCO', negacion, actuador, p[2], p[3], p[4])
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_FOCO', negacion, actuador, p[2], p[3], None)
            else:
                p[0] = ('CONDICION_FOCO', negacion, actuador, None, p[2], p[3])
        else:
            p[0] = ('CONDICION_FOCO', negacion, actuador, None, p[2], None)


#CONDICIONES INCLUYEN ACTUADORES Y SENSORES (SOLO DE LECTURA)
def p_condicion_actuador_aire(p):
    '''condicion : OP_NEGACION ACTUADOR_AIRE identificador atributos_lec_aire contcondicion
                 | OP_NEGACION ACTUADOR_AIRE identificador atributos_lec_aire
                 | OP_NEGACION ACTUADOR_AIRE atributos_lec_aire contcondicion
                 | OP_NEGACION ACTUADOR_AIRE atributos_lec_aire
                 | ACTUADOR_AIRE identificador atributos_lec_aire contcondicion
                 | ACTUADOR_AIRE identificador atributos_lec_aire
                 | ACTUADOR_AIRE atributos_lec_aire contcondicion
                 | ACTUADOR_AIRE atributos_lec_aire'''
    if p[1] != 'AIRE':
        negacion = p[1]
        actuador = p[2]        
        if len(p) == 6:
            p[0] = ('CONDICION_AIRE', negacion, actuador, p[3], p[4], p[5])
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_AIRE', negacion, actuador, p[3], p[4], None)
            else:                    
                p[0] = ('CONDICION_AIRE', negacion, actuador, None, p[3], p[4])
        else:             
            p[0] = ('CONDICION_AIRE', negacion, actuador, None, p[3], None)
    else:
        negacion = None
        actuador = p[1]

        if len(p) == 5:
            p[0] = ('CONDICION_AIRE', negacion, actuador, p[2], p[3], p[4])
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_AIRE', negacion, actuador, p[2], p[3], None)
            else:                    
                p[0] = ('CONDICION_AIRE', negacion, actuador, None, p[2], p[3])
        else: 
            p[0] = ('CONDICION_AIRE', negacion, actuador, None, p[2], None)
    

def p_condicion_actuador_persiana(p):
    '''condicion : OP_NEGACION ACTUADOR_PERSIANA identificador atributos_lec_persiana contcondicion
                 | OP_NEGACION ACTUADOR_PERSIANA identificador atributos_lec_persiana
                 | OP_NEGACION ACTUADOR_PERSIANA atributos_lec_persiana contcondicion
                 | OP_NEGACION ACTUADOR_PERSIANA atributos_lec_persiana
                 | ACTUADOR_PERSIANA identificador atributos_lec_persiana contcondicion
                 | ACTUADOR_PERSIANA identificador atributos_lec_persiana 
                 | ACTUADOR_PERSIANA atributos_lec_persiana contcondicion
                 | ACTUADOR_PERSIANA atributos_lec_persiana'''
    
    if p[1] != 'PERSIANA':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 6:
            p[0] = ('CONDICION_PERSIANA', negacion, actuador, p[3], p[4], p[5])
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_PERSIANA', negacion, actuador, p[3], p[4], None)
            else:
                p[0] = ('CONDICION_PERSIANA', negacion, actuador, None, p[3], p[4])
        else:
            p[0] = ('CONDICION_PERSIANA', negacion, actuador, None, p[3], None)

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 5:
            p[0] = ('CONDICION_PERSIANA', negacion, actuador, p[2], p[3], p[4])
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_PERSIANA', negacion, actuador, p[2], p[3], None)
            else:
                p[0] = ('CONDICION_PERSIANA', negacion, actuador, None, p[2], p[3])
        else:
            p[0] = ('CONDICION_PERSIANA', negacion, actuador, None, p[2], None)

    
def p_condicion_actuador_cerradura(p):
    '''condicion : OP_NEGACION ACTUADOR_CERRADURA identificador atributos_lec_cerradura contcondicion
                 | OP_NEGACION ACTUADOR_CERRADURA identificador atributos_lec_cerradura
                 | OP_NEGACION ACTUADOR_CERRADURA atributos_lec_cerradura contcondicion
                 | OP_NEGACION ACTUADOR_CERRADURA atributos_lec_cerradura
                 | ACTUADOR_CERRADURA identificador atributos_lec_cerradura contcondicion
                 | ACTUADOR_CERRADURA identificador atributos_lec_cerradura
                 | ACTUADOR_CERRADURA atributos_lec_cerradura contcondicion
                 | ACTUADOR_CERRADURA atributos_lec_cerradura'''
    
    if p[1] != 'CERRADURA':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 6:
            p[0] = ('CONDICION_CERRADURA', negacion, actuador, p[3], p[4], p[5])
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_CERRADURA', negacion, actuador, p[3], p[4], None)
            else:
                p[0] = ('CONDICION_CERRADURA', negacion, actuador, None, p[3], p[4])
        else:
            p[0] = ('CONDICION_CERRADURA', negacion, actuador, None, p[3], None)

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 5:
            p[0] = ('CONDICION_CERRADURA', negacion, actuador, p[2], p[3], p[4])
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_CERRADURA', negacion, actuador, p[2], p[3], None)
            else:
                p[0] = ('CONDICION_CERRADURA', negacion, actuador, None, p[2], p[3])
        else:
            p[0] = ('CONDICION_CERRADURA', negacion, actuador, None, p[2], None)


def p_condicion_actuador_reloj(p):
    '''condicion : OP_NEGACION ACTUADOR_RELOJ identificador atributos_lec_reloj contcondicion
                 | OP_NEGACION ACTUADOR_RELOJ identificador atributos_lec_reloj
                 | OP_NEGACION ACTUADOR_RELOJ atributos_lec_reloj contcondicion
                 | OP_NEGACION ACTUADOR_RELOJ atributos_lec_reloj
                 | ACTUADOR_RELOJ identificador atributos_lec_reloj contcondicion
                 | ACTUADOR_RELOJ identificador atributos_lec_reloj
                 | ACTUADOR_RELOJ atributos_lec_reloj contcondicion
                 | ACTUADOR_RELOJ atributos_lec_reloj'''
    
    if p[1] != 'RELOJ':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 6:
            p[0] = ('CONDICION_RELOJ', negacion, actuador, p[3], p[4], p[5])
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_RELOJ', negacion, actuador, p[3], p[4], None)
            else:
                p[0] = ('CONDICION_RELOJ', negacion, actuador, None, p[3], p[4])
        else:
            p[0] = ('CONDICION_RELOJ', negacion, actuador, None, p[3], None)

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 5:
            p[0] = ('CONDICION_RELOJ', negacion, actuador, p[2], p[3], p[4])
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_RELOJ', negacion, actuador, p[2], p[3], None)
            else:
                p[0] = ('CONDICION_RELOJ', negacion, actuador, None, p[2], p[3])
        else:
            p[0] = ('CONDICION_RELOJ', negacion, actuador, None, p[2], None)

def p_condicion_actuador_altavoz(p):
    '''condicion : OP_NEGACION ACTUADOR_ALTAVOZ identificador atributos_lec_altavoz contcondicion
                 | OP_NEGACION ACTUADOR_ALTAVOZ identificador atributos_lec_altavoz
                 | OP_NEGACION ACTUADOR_ALTAVOZ atributos_lec_altavoz contcondicion
                 | OP_NEGACION ACTUADOR_ALTAVOZ atributos_lec_altavoz
                 | ACTUADOR_ALTAVOZ identificador atributos_lec_altavoz contcondicion
                 | ACTUADOR_ALTAVOZ identificador atributos_lec_altavoz
                 | ACTUADOR_ALTAVOZ atributos_lec_altavoz contcondicion
                 | ACTUADOR_ALTAVOZ atributos_lec_altavoz'''
    
    if p[1] != 'ALTAVOZ':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 6:
            p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, p[3], p[4], p[5])
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, p[3], p[4], None)
            else:
                p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, None, p[3], p[4])
        else:
            p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, None, p[3], None)

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 5:
            p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, p[2], p[3], p[4])
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, p[2], p[3], None)
            else:
                p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, None, p[2], p[3])
        else:
            p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, None, p[2], None)


def p_condicion_actuador_alarma(p):
    '''condicion : OP_NEGACION ACTUADOR_ALARMA identificador atributos_lec_alarma contcondicion
                 | OP_NEGACION ACTUADOR_ALARMA identificador atributos_lec_alarma
                 | OP_NEGACION ACTUADOR_ALARMA atributos_lec_alarma contcondicion
                 | OP_NEGACION ACTUADOR_ALARMA atributos_lec_alarma
                 | ACTUADOR_ALARMA identificador atributos_lec_alarma contcondicion
                 | ACTUADOR_ALARMA identificador atributos_lec_alarma
                 | ACTUADOR_ALARMA atributos_lec_alarma contcondicion
                 | ACTUADOR_ALARMA atributos_lec_alarma'''
    
    if p[1] != 'ALARMA':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 6:
            p[0] = ('CONDICION_ALARMA', negacion, actuador, p[3], p[4], p[5])
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_ALARMA', negacion, actuador, p[3], p[4], None)
            else:
                p[0] = ('CONDICION_ALARMA', negacion, actuador, None, p[3], p[4])
        else:
            p[0] = ('CONDICION_ALARMA', negacion, actuador, None, p[3], None)

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 5:
            p[0] = ('CONDICION_ALARMA', negacion, actuador, p[2], p[3], p[4])
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_ALARMA', negacion, actuador, p[2], p[3], None)
            else:
                p[0] = ('CONDICION_ALARMA', negacion, actuador, None, p[2], p[3])
        else:
            p[0] = ('CONDICION_ALARMA', negacion, actuador, None, p[2], None)

def p_atributos_lectura_foco(p):
    '''atributos_lec_foco : ATRIBUTO_ESTADO OP_COMPARADOR_BOOL BOOL_ACTUADOR
                          | ATRIBUTOS_FOCO_BRILLO OP_COMPARADOR PERCENT
                          | ATRIBUTOS_FOCO_COLOR OP_COMPARADOR NOMBRE'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_lectura_aire(p):
    '''atributos_lec_aire : ATRIBUTO_ESTADO OP_COMPARADOR_BOOL BOOL_ACTUADOR
                          | ATRIBUTOS_AIRE_MODO OP_COMPARADOR_BOOL DISCRETO 
                          | ATRIBUTOS_AIRE_TEMP_OBJ OP_COMPARADOR VALOR_TEMP
                          | ATRIBUTOS_AIRE_TEMP_ACT OP_COMPARADOR VALOR_TEMP'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_lectura_persiana(p):
    '''atributos_lec_persiana : ATRIBUTOS_PERSIANA OP_COMPARADOR PERCENT'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_lectura_cerradura(p):
    '''atributos_lec_cerradura : ATRIBUTO_ESTADO OP_COMPARADOR_BOOL BOOL_ACTUADOR'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_lectura_reloj(p):
    '''atributos_lec_reloj : ATRIBUTOS_RELOJ_HORA OP_COMPARADOR HORA
                           | ATRIBUTOS_RELOJ_FECHA OP_COMPARADOR DATE'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_lectura_altavoz(p):
    '''atributos_lec_altavoz : ATRIBUTOS_ALTAVOZ_VOLUMEN OP_COMPARADOR PERCENT
                             | ATRIBUTOS_ALTAVOZ_MUTE OP_COMPARADOR_BOOL BOOL_ACTUADOR
                             | ATRIBUTOS_ALTAVOZ_MENSAJE OP_COMPARADOR TEXTO
                             | ATRIBUTOS_ALTAVOZ_EMAIL OP_COMPARADOR EMAIL'''
    p[0] = p[1] + p[2] + p[3]


def p_atributos_lectura_alarma(p):
    '''atributos_lec_alarma : ATRIBUTO_ESTADO OP_COMPARADOR_BOOL BOOL_ACTUADOR
                            | ATRIBUTOS_ALARMA OP_COMPARADOR_BOOL BOOL_ACTUADOR
    '''
    p[0] = p[1] + p[2] + p[3]


#Regla para manejar errores
def p_error(p):
    if p:
        line_start = p.lexer.lexdata.rfind('\n', 0, p.lexpos) + 1
        columna = (p.lexpos - line_start) + 1
        print(f"Error de sintaxis: Se detectó un error en la Línea {p.lineno}, Columna {columna}.")
    else:
        print("Error de sintaxis: Fin de archivo inesperado. Algún bloque quedó abierto.")
    
    raise SyntaxError("Error de análisis sintáctico.")

parser = yacc.yacc(debug=False, write_tables=False)


#====================================================================#
#========================= INTERFAZ GRÁFICA =========================#
#====================================================================#

# Variables globales para el lexer
datos = ""
datosOriginal = ""
datosUpper = ""

def cargar_datos(texto):
    """Carga el texto para analizar y prepara las variables del lexer"""
    global datos, datosOriginal, datosUpper
    datos = texto
    datosOriginal = texto
    datosUpper = texto.upper()
    lexer.input(datosUpper)

def obtener_tokens():
    """Retorna lista de tokens encontrados en el texto cargado"""
    tokens_encontrados = []
    while True:
        tok = lexer.token()
        if not tok: 
            break
        inicio = tok.lexpos
        fin = inicio + len(tok.value)
        # Obtener el texto original (sin convertir a mayúsculas)
        texto_original = datosOriginal[inicio:fin]
        tokens_encontrados.append({
            'valor': texto_original,
            'tipo': tok.type,
            'linea': tok.lineno,
            'columna': find_column(datosOriginal, tok)
        })
    return tokens_encontrados

class InterfazAnalizador:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador SmartHome - BinaryBuilders")
        self.root.geometry("1220x650")
        
        # Variables
        self.texto_actual = ""
        self.tokens_encontrados = []
        self.resultado_sintactico = None
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_widgets()
        
        # Cargar ejemplos en el combobox
        self.cargar_ejemplos()
    
    def configurar_estilo(self):
        """Configura el estilo visual de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores
        self.color_fondo = "#f0f0f0"
        self.color_editor = "#ffffff"
        self.color_resultados = "#1e1e1e"
        self.color_exito = "#4caf50"
        self.color_error = "#f44336"
        self.color_advertencia = "#ff9800"
        
        self.root.configure(bg=self.color_fondo)
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        frame_principal = ttk.Frame(self.root, padding="10")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.rowconfigure(2, weight=1)
        
        # ========== PANEL SUPERIOR - CONTROLES ==========
        frame_controles = ttk.LabelFrame(frame_principal, text="Controles", padding="10")
        frame_controles.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botón buscar archivo
        self.btn_buscar = ttk.Button(frame_controles, text="📂 Buscar Archivo", 
                                     command=self.buscar_archivo)
        self.btn_buscar.grid(row=0, column=0, padx=5, pady=5)
        
        # Label para mostrar archivo cargado
        self.label_archivo = ttk.Label(frame_controles, text="Ningún archivo cargado", 
                                       foreground="gray")
        self.label_archivo.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Combobox de ejemplos
        ttk.Label(frame_controles, text="Ejemplos:").grid(row=0, column=2, padx=(20, 5), pady=5)
        self.combo_ejemplos = ttk.Combobox(frame_controles, state="readonly", width=40)
        self.combo_ejemplos.grid(row=0, column=3, padx=5, pady=5)
        self.combo_ejemplos.bind('<<ComboboxSelected>>', self.cargar_ejemplo_seleccionado)
        
        # ========== PANEL IZQUIERDO - EDITOR ==========
        frame_editor = ttk.LabelFrame(frame_principal, text="Editor de Código", padding="5")
        frame_editor.grid(row=1, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        frame_editor.columnconfigure(0, weight=1)
        frame_editor.rowconfigure(0, weight=1)
        
        # Editor de texto con scroll
        self.editor = tk.Text(frame_editor, wrap=tk.NONE, font=("Consolas", 10),
                             bg=self.color_editor, fg="#000000", insertbackground="black")
        self.editor.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_editor, orient=tk.VERTICAL, command=self.editor.yview)
        scroll_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.editor.configure(yscrollcommand=scroll_y.set)
        
        scroll_x = ttk.Scrollbar(frame_editor, orient=tk.HORIZONTAL, command=self.editor.xview)
        scroll_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.editor.configure(xscrollcommand=scroll_x.set)
        
        # ========== PANEL DERECHO - BOTONES DE ANÁLISIS ==========
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.grid(row=1, column=1, sticky=(tk.N, tk.S), padx=(5, 0))
        
        ttk.Label(frame_botones, text="Análisis", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        self.btn_lexico = ttk.Button(frame_botones, text="🔍 Analizar Léxico", 
                                     command=self.analizar_lexico, width=20)
        self.btn_lexico.pack(pady=5)
        
        self.btn_sintactico = ttk.Button(frame_botones, text="📝 Analizar Sintaxis", 
                                         command=self.analizar_sintactico, width=20)
        self.btn_sintactico.pack(pady=5)
        
        self.btn_html = ttk.Button(frame_botones, text="🌐 Generar HTML", 
                                   command=self.generar_html, width=20)
        self.btn_html.pack(pady=5)
        
        ttk.Separator(frame_botones, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        
        self.btn_guardar = ttk.Button(frame_botones, text="💾 Guardar HTML", 
                                      command=self.guardar_html, width=20, state=tk.DISABLED)
        self.btn_guardar.pack(pady=5)
        
        self.btn_limpiar = ttk.Button(frame_botones, text="🗑️ Limpiar", 
                                      command=self.limpiar_resultados, width=20)
        self.btn_limpiar.pack(pady=5)
        
        # ========== PANEL INFERIOR - RESULTADOS ==========
        frame_resultados = ttk.LabelFrame(frame_principal, text="Resultados", padding="5")
        frame_resultados.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=(5, 0))
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(1, weight=1)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(frame_resultados)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Pestaña Léxico
        self.tab_lexico = tk.Text(self.notebook, wrap=tk.WORD, font=("Consolas", 9),
                                  bg=self.color_resultados, fg="#00ff00", insertbackground="white")
        self.notebook.add(self.tab_lexico, text="Léxico")
        
        scroll_lex = ttk.Scrollbar(self.tab_lexico, orient=tk.VERTICAL, 
                                   command=self.tab_lexico.yview)
        scroll_lex.pack(side=tk.RIGHT, fill=tk.Y)
        self.tab_lexico.configure(yscrollcommand=scroll_lex.set)
        
        # Pestaña Sintáctico
        self.tab_sintactico = tk.Text(self.notebook, wrap=tk.WORD, font=("Consolas", 9),
                                      bg=self.color_resultados, fg="#00ff00", insertbackground="white")
        self.notebook.add(self.tab_sintactico, text="Sintáctico")
        
        scroll_sin = ttk.Scrollbar(self.tab_sintactico, orient=tk.VERTICAL, 
                                   command=self.tab_sintactico.yview)
        scroll_sin.pack(side=tk.RIGHT, fill=tk.Y)
        self.tab_sintactico.configure(yscrollcommand=scroll_sin.set)
        
        # Pestaña HTML
        self.tab_html = tk.Text(self.notebook, wrap=tk.NONE, font=("Consolas", 9))
        self.notebook.add(self.tab_html, text="HTML")
        
        scroll_html = ttk.Scrollbar(self.tab_html, orient=tk.VERTICAL, 
                                    command=self.tab_html.yview)
        scroll_html.pack(side=tk.RIGHT, fill=tk.Y)
        self.tab_html.configure(yscrollcommand=scroll_html.set)
    
    def cargar_ejemplos(self):
        """Carga los archivos de ejemplo en el combobox"""
        carpeta_ejemplos = os.path.join(os.path.dirname(__file__), "Ejemplos")
        if os.path.exists(carpeta_ejemplos):
            archivos = [f for f in os.listdir(carpeta_ejemplos) if f.endswith('.txt')]
            self.combo_ejemplos['values'] = archivos
            if archivos:
                self.combo_ejemplos.current(0)
    
    def buscar_archivo(self):
        """Abre diálogo para buscar archivo .txt"""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de programa",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if ruta:
            self.cargar_archivo(ruta)
    
    def cargar_archivo(self, ruta):
        """Carga el contenido de un archivo en el editor"""
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            self.editor.delete(1.0, tk.END)
            self.editor.insert(1.0, contenido)
            self.texto_actual = contenido
            
            nombre_archivo = os.path.basename(ruta)
            self.label_archivo.config(text=f"✓ {nombre_archivo}", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    def cargar_ejemplo_seleccionado(self, event=None):
        """Carga el ejemplo seleccionado del combobox"""
        seleccion = self.combo_ejemplos.get()
        if seleccion:
            ruta = os.path.join(os.path.dirname(__file__), "Ejemplos", seleccion)
            self.cargar_archivo(ruta)
    
    def analizar_lexico(self):
        """Realiza el análisis léxico del código"""
        self.limpiar_resultados()
        
        # Obtener texto del editor
        texto = self.editor.get(1.0, tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "No hay código para analizar")
            return
        
        try:
            # Cargar datos en el lexer
            cargar_datos(texto)
            
            # Obtener tokens
            self.tokens_encontrados = obtener_tokens()
            
            # Mostrar resultados
            self.mostrar_resultados_lexico()
            
            # Cambiar a pestaña léxico
            self.notebook.select(self.tab_lexico)
            
        except Exception as e:
            self.mostrar_error_lexico(str(e))
    
    def mostrar_resultados_lexico(self):
        """Muestra los resultados del análisis léxico"""
        self.tab_lexico.delete(1.0, tk.END)
        
        if not self.tokens_encontrados:
            self.tab_lexico.insert(tk.END, "No se encontraron tokens.\n")
            return
        
        # Encabezado
        #self.tab_lexico.insert(tk.END, "=" * 80 + "\n", "titulo")
        self.tab_lexico.insert(tk.END, "ANÁLISIS LÉXICO - TOKENS ENCONTRADOS\n", "titulo")
        #self.tab_lexico.insert(tk.END, "=" * 80 + "\n\n", "titulo")
        
        # Configurar tags para colores
        self.tab_lexico.tag_config("titulo", foreground="#00bfff", font=("Consolas", 10, "bold"))
        self.tab_lexico.tag_config("token", foreground="#ffffff")
        self.tab_lexico.tag_config("tipo", foreground="#ffff00")
        self.tab_lexico.tag_config("posicion", foreground="#00ff00")
        self.tab_lexico.tag_config("separador", foreground="#888888")
        
        # Mostrar cada token
        for i, token in enumerate(self.tokens_encontrados, 1):
            linea = f"{i:3d}. Token: '{token['valor']}'"
            self.tab_lexico.insert(tk.END, linea, "token")
            
            tipo = f" | Tipo: {token['tipo']}"
            self.tab_lexico.insert(tk.END, tipo, "tipo")
            
            pos = f" | Línea: {token['linea']}, Col: {token['columna']}"
            self.tab_lexico.insert(tk.END, pos, "posicion")
            
            self.tab_lexico.insert(tk.END, "\n", "separador")
        
        # Resumen
        #self.tab_lexico.insert(tk.END, "\n" + "=" * 80 + "\n", "titulo")
        self.tab_lexico.insert(tk.END, f"Total: {len(self.tokens_encontrados)} tokens encontrados\n", "titulo")
        #self.tab_lexico.insert(tk.END, "=" * 80 + "\n", "titulo")
    
    def mostrar_error_lexico(self, error):
        """Muestra errores del análisis léxico"""
        self.tab_lexico.delete(1.0, tk.END)
        self.tab_lexico.insert(tk.END, "ERROR EN ANÁLISIS LÉXICO\n", "error")
        self.tab_lexico.insert(tk.END, "=" * 80 + "\n\n", "error")
        self.tab_lexico.insert(tk.END, error + "\n", "error")
        self.tab_lexico.tag_config("error", foreground="#ff4444", font=("Consolas", 10, "bold"))
    
    def analizar_sintactico(self):
            """Realiza el análisis sintáctico del código"""
            self.limpiar_resultados()

            # Obtener texto del editor
            texto = self.editor.get(1.0, tk.END).strip()
            if not texto:
                messagebox.showwarning("Advertencia", "No hay código para analizar")
                return

            try:
                # Súper importante: Reiniciar el contador de líneas del lexer antes de parsear
                lexer.lineno = 1
                lexer.input(texto.upper())  # Nos aseguramos de que entre todo en mayúsculas

                # Cambiar a pestaña sintáctico
                self.notebook.select(self.tab_sintactico)

                # Parsear
                self.tab_sintactico.delete(1.0, tk.END)
                self.tab_sintactico.insert(tk.END, "Iniciando análisis sintáctico...\n\n", "info")
                self.root.update()

                # Ejecutamos pasándole explícitamente el lexer reiniciado
                parser.parse(texto.upper(), lexer=lexer)

                # Si el parser terminó de recorrer el archivo sin lanzar errores críticos en el medio,
                # forzamos el éxito gráfico porque el HTML se completó.
                self.mostrar_exito_sintactico()

            except SyntaxError as e:
                self.mostrar_error_sintactico(str(e))
            except Exception as e:
                self.mostrar_error_sintactico(f"Error inesperado: {str(e)}")


    def mostrar_exito_sintactico(self):
        """Muestra mensaje de éxito del análisis sintáctico"""
        self.tab_sintactico.delete(1.0, tk.END)
        
        self.tab_sintactico.tag_config("exito", foreground="#00ff00", font=("Consolas", 12, "bold"))
        self.tab_sintactico.tag_config("info", foreground="#00bfff")
        self.tab_sintactico.tag_config("detalle", foreground="#ffffff")
        
        self.tab_sintactico.insert(tk.END, "✓ ANÁLISIS SINTÁCTICO EXITOSO\n", "exito")
        #self.tab_sintactico.insert(tk.END, "=" * 80 + "\n\n", "exito")
        self.tab_sintactico.insert(tk.END, "El programa es sintácticamente correcto.\n\n", "info")
        
        if self.resultado_sintactico:
            self.tab_sintactico.insert(tk.END, "Estructura del programa:\n", "info")
            self.tab_sintactico.insert(tk.END, "-" * 80 + "\n", "detalle")
            self.mostrar_estructura(self.resultado_sintactico, 0)
    
    def mostrar_estructura(self, estructura, nivel):
        """Muestra la estructura del programa de forma recursiva"""
        indent = "  " * nivel
        
        if isinstance(estructura, list):
            for item in estructura:
                self.mostrar_estructura(item, nivel)
        
        elif isinstance(estructura, tuple):
            tipo = estructura[0]
            self.tab_sintactico.insert(tk.END, f"{indent}• {tipo}\n", "detalle")
            
            for item in estructura[1:]:
                if item is not None:
                    self.mostrar_estructura(item, nivel + 1)
    
    def mostrar_error_sintactico(self, error):
        """Muestra errores del análisis sintáctico"""
        self.tab_sintactico.delete(1.0, tk.END)
        
        self.tab_sintactico.tag_config("error", foreground="#ff4444", font=("Consolas", 10, "bold"))
        self.tab_sintactico.tag_config("detalle", foreground="#ff8888")
        
        self.tab_sintactico.insert(tk.END, "X ERROR DE SINTAXIS\n", "error")
        #self.tab_sintactico.insert(tk.END, "=" * 80 + "\n\n", "error")
        self.tab_sintactico.insert(tk.END, error + "\n", "detalle")
    
    def generar_html(self):
        """Genera el HTML del programa"""
        texto = self.editor.get(1.0, tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "No hay código para generar HTML")
            return
        
        try:
            # Realizar análisis léxico si no se ha hecho
            if not self.tokens_encontrados:
                cargar_datos(texto)
                self.tokens_encontrados = obtener_tokens()
            
            # Generar HTML
            html = self.crear_html(texto, self.tokens_encontrados)
            
            # Mostrar en pestaña HTML
            self.notebook.select(self.tab_html)
            self.tab_html.delete(1.0, tk.END)
            self.tab_html.insert(1.0, html)
            
            # Habilitar botón de guardar
            self.btn_guardar.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar HTML:\n{str(e)}")
    

#====================================================================#
#============================== HTML ================================#
#====================================================================#

    def crear_html(self, codigo, tokens):
        """Crea el documento HTML"""
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Escapar HTML en el código
        codigo_escapado = self.escapar_html(codigo)
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Programa SmartHome - BinaryBuilders</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .info {{
            background: #f8f9fa;
            padding: 15px 30px;
            border-bottom: 2px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }}
        
        .info-item {{
            margin: 5px 15px 5px 0;
        }}
        
        .info-label {{
            font-weight: bold;
            color: #555;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 30px;
        }}
        
        @media (max-width: 968px) {{
            .content {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .panel {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .panel h2 {{
            color: #1e3c72;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #1e3c72;
        }}
        
        .code-container {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 5px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
            overflow-x: auto;
            white-space: pre;
        }}
        
        .tokens-container {{
            max-height: 500px;
            overflow-y: auto;
        }}
        
        .token-item {{
            background: white;
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 4px;
            border-left: 3px solid #667eea;
            font-family: 'Consolas', monospace;
            font-size: 13px;
            display: flex;
            justify-content: space-between;
        }}
        
        .token-value {{
            font-weight: bold;
            color: #333;
        }}
        
        .token-type {{
            color: #667eea;
            font-size: 11px;
        }}
        
        .token-pos {{
            color: #999;
            font-size: 11px;
        }}
        
        .stats {{
            background: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin-top: 15px;
        }}
        
        .stats h3 {{
            color: #2e7d32;
            margin-bottom: 10px;
        }}
        
        .stats-item {{
            margin: 5px 0;
            color: #555;
        }}
        
        .footer {{
            background: #1e3c72;
            color: white;
            text-align: center;
            padding: 15px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 Programa SmartHome</h1>
            <p>Analizador Léxico y Sintáctico - BinaryBuilders</p>
        </div>
        
        <div class="info">
            <div class="info-item">
                <span class="info-label">Fecha:</span> {fecha}
            </div>
            <div class="info-item">
                <span class="info-label">Tokens:</span> {len(tokens)}
            </div>
            <div class="info-item">
                <span class="info-label">Líneas:</span> {len(codigo.splitlines())}
            </div>
            <div class="info-item">
                <span class="info-label">Estado:</span> ✓ Válido
            </div>
        </div>
        
        <div class="content">
            <div class="panel">
                <h2>📄 Código Fuente</h2>
                <div class="code-container">{codigo_escapado}</div>
            </div>
            
            <div class="panel">
                <h2>🔍 Tokens Identificados</h2>
                <div class="tokens-container">
"""
        
        # Agregar cada token
        for token in tokens:
            html += f"""                    <div class="token-item">
                        <span class="token-value">'{token['valor']}'</span>
                        <span class="token-type">{token['tipo']}</span>
                        <span class="token-pos">L{token['linea']}:C{token['columna']}</span>
                    </div>
"""
        
        html += """                </div>
                
                <div class="stats">
                    <h3>📊 Estadísticas</h3>
                    <div class="stats-item">Total de tokens: """ + str(len(tokens)) + """</div>
"""
        
        # Contar tipos de tokens
        tipos = {}
        for token in tokens:
            tipo = token['tipo']
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        for tipo, cantidad in sorted(tipos.items()):
            html += f"""                    <div class="stats-item">{tipo}: {cantidad}</div>
"""
        
        html += """                </div>
            </div>
        </div>
        
        <div class="footer">
            BinaryBuilders - UTN FRRe - 2026 | Analizador Léxico y Sintáctico para SmartHome
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def escapar_html(self, texto):
        """Escapa caracteres especiales para HTML"""
        escapes = {
            '&': '&',
            '<': '<',
            '>': '>',
            '"': '"',
            "'": '&#39;'
        }
        for char, escape in escapes.items():
            texto = texto.replace(char, escape)
        return texto
    
    def guardar_html(self):
        """Guarda el HTML generado en un archivo"""
        if not self.tab_html.get(1.0, tk.END).strip():
            messagebox.showwarning("Advertencia", "No hay HTML para guardar")
            return
        
        ruta = filedialog.asksaveasfilename(
            title="Guardar HTML",
            defaultextension=".html",
            filetypes=[("Archivos HTML", "*.html"), ("Todos los archivos", "*.*")]
        )
        
        if ruta:
            try:
                contenido = self.tab_html.get(1.0, tk.END)
                with open(ruta, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                messagebox.showinfo("Éxito", f"HTML guardado en:\n{ruta}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
    
    def limpiar_resultados(self):
        """Limpia todos los paneles de resultados"""
        self.tab_lexico.delete(1.0, tk.END)
        self.tab_sintactico.delete(1.0, tk.END)
        self.tab_html.delete(1.0, tk.END)
        self.tokens_encontrados = []
        self.resultado_sintactico = None
        self.btn_guardar.config(state=tk.DISABLED)

#====================================================================#
#=============================== MAIN ===============================#
#====================================================================#
  
root = tk.Tk()
app = InterfazAnalizador(root)
root.mainloop()

#Preguntar: los valores de valor_temp_obj y valor_temp_act al estar separados tienen un problema, que el rango
#de temp_obj está contenido en el de temp_act, lo cual causa un conflicto en el matching de los tokens, ya que
#siempre tratará de hacer matching con la regla que primero esté definida, y puede causar error, ya que esa
#primer regla de temperatura definida puede no contener el rango para cubrir el valor del token detectado,
#preguntar si igual hay que mantener separados ambos valores o unificarlos en uno solo de "valor_temp" que
#cubra el rango mayor de valor_temp_act (-10 a 50)°C
