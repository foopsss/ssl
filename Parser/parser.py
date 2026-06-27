from ply import lex, yacc
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tempfile
import webbrowser
import os


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
    return(t)

lexer = lex.lex()



#====================================================================#
#============================== PARSER ==============================#
#=========== (Análisis Sintáctico y construcción del HTML) ==========#
#====================================================================#

html = ""  #variable global para ir concatenando etiquetas para el html
def cabecera_html():
    global html
    html = "" #cada vez que se usa esta función, es para reiniciar la construcción del html
    html = "<!DOCTYPE html>\n<html lang='es'>\n<head>\n"
    html += "  <meta charset='UTF-8'>\n"
    html += "  <title>Smart-Home - Estado de Actuadores y Sensores - Binarybuilders</title>\n"
    html += "</head>\n"
    html += "<body style='margin: 0; font-family: sans-serif; background-color: #f4f6f9;'>\n"
    html += """
    <div style="background-color: #0056b3; padding: 25px 40px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.15);">
        <h1 style="color: #ffffff; font-family: 'Franklin Gothic Medium', sans-serif; font-size: 38px; text-transform: uppercase; letter-spacing: 2px; margin: 0; padding-bottom: 5px;">
            SMART-HOME - Sensores y Actuadores
        </h1>
        <h3 style="color: #e0e0e0; font-family: 'Century Gothic', 'Segoe UI', sans-serif; font-size: 16px; font-weight: 300; letter-spacing: 1px; margin: 5px 0 0 0;">
            Estado de todos los sensores y actuadores del hogar:
        </h3>
    </div>
    """

def final_html():
    global html
    html += """
    <div style="background-color: #003d82; margin-top: 50px; padding: 25px 0; text-align: center;">
        <p style="color: #ffffff; font-family: sans-serif; font-size: 14px; margin: 0; letter-spacing: 1px;">
            Binarybuilders© 2026
        </p>
    </div>
    """ 
    html += "\n</body>\n</html>"
    

def formato_actuador_html(nombre_actuador,identif_actuador,atributo,valor_atributo,emoji):
    global html
    if identif_actuador:
        html += f"""
        <div style="border: 1px solid gray; padding: 20px; margin-bottom: 15px;">
            <h1 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;">{nombre_actuador}{emoji}</h1> (de {identif_actuador})
            <ul>
                <li>{atributo}: {valor_atributo}</li>
            </ul>
        </div>
        """         
    else:
        html += f"""
        <div style="border: 1px solid gray; padding: 20px; margin-bottom: 15px;">
            <h1 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;">{nombre_actuador}{emoji}</h1>
            <ul>
                <li>{atributo}: {valor_atributo}</li>
            </ul>
        </div>
        """

cabecera_html()

#REGLAS DEL ANÁLISIS SINTÁCTICO
def p_programa(p):
    '''sigma : accion'''
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
    global html #var. globales van debajo de las reglas siempre sino se rompe todo
    
    if "FOCO" in p[1]: emoji = "💡"
    elif "AIRE" in p[1]: emoji = "❄️"
    elif "PERSIANA" in p[1]: emoji = "🪟"
    elif "CERRADURA" in p[1]: emoji = "🔒"
    elif "ALTAVOZ" in p[1]: emoji = "🔊"
    elif "ALARMA" in p[1]: emoji = "🚨"

    if len(p) == 4:
        p[0] = ('ASIGNACION', p[1], p[2], p[3])
        nombre_actuador = p[1]
        identif_act = p[2].replace('_', '')
        
        partes_atributo = p[3].split('=')
        atributo = partes_atributo[0].replace('.', '').strip()
        valor_atributo = partes_atributo[1].strip()
        
        formato_actuador_html(nombre_actuador, identif_act, atributo, valor_atributo, emoji)

    else:
        p[0] = ('ASIGNACION', p[1], None, p[2])
        nombre_actuador = p[1]
        
        partes_atributo = p[2].split('=')
        atributo = partes_atributo[0].replace('.', '').strip()
        valor_atributo = partes_atributo[1].strip()
        
        formato_actuador_html(nombre_actuador, None, atributo, valor_atributo, emoji)


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
        print("Error de sintaxis: Fin de archivo inesperado.")
    
    raise SyntaxError("Error de análisis sintáctico.")


parser = yacc.yacc(debug=False, write_tables=False) #Construir el parser


#====================================================================#
#========================= INTERFAZ GRÁFICA =========================#
#====================================================================#

class InterfazAnalizador:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador SmartHome - BinaryBuilders")
        self.root.geometry("1220x650")
        self.texto_actual = ""
        self.configurar_estilo()
        self.crear_widgets()

    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        self.color_fondo = "#ffffff" 
        self.color_editor = "#ffffff"
        self.color_resultados = "#1e1e1e"
        self.color_exito = "#4caf50"
        self.color_error = "#f44336"
        self.color_advertencia = "#ff9800"
        self.root.configure(bg=self.color_fondo)

        #style.configure("TFrame", background=self.color_fondo)
        #style.configure("TLabelframe", background=self.color_fondo)
        #style.configure("TLabelframe.Label", background=self.color_fondo, foreground="white")

    
    def crear_widgets(self):
        #frame principal (toda la ventana)
        frame_principal = ttk.Frame(self.root, padding="10")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        #frame grillas (divisores de la ventana)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.rowconfigure(1, weight=1)
        frame_principal.rowconfigure(2, weight=4)

        #todos los widgets
        frame_controles = ttk.LabelFrame(frame_principal, text="Indicar archivo de entrada", padding="10")
        frame_controles.grid(row=0, column=0, columnspan=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.btn_buscar = ttk.Button(frame_controles, text="📂 Buscar Archivo", command=self.buscar_archivo)
        self.btn_buscar.grid(row=0, column=0, padx=5, pady=5)
        
        self.label_archivo = ttk.Label(frame_controles, text="Ningún archivo cargado", foreground="gray")
        self.label_archivo.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        frame_editor = ttk.LabelFrame(frame_principal, text="Editor de Código", padding="5")
        frame_editor.grid(row=1, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        frame_editor.columnconfigure(0, weight=1)
        frame_editor.rowconfigure(0, weight=1)
        
        self.editor = tk.Text(frame_editor, wrap=tk.NONE, font=("Consolas", 10), bg=self.color_editor, fg="#000000", insertbackground="black")
        self.editor.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scroll_y = ttk.Scrollbar(frame_editor, orient=tk.VERTICAL, command=self.editor.yview)
        scroll_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.editor.configure(yscrollcommand=scroll_y.set)
        
        scroll_x = ttk.Scrollbar(frame_editor, orient=tk.HORIZONTAL, command=self.editor.xview)
        scroll_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.editor.configure(xscrollcommand=scroll_x.set)
        
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.grid(row=1, column=1, sticky=(tk.N, tk.S), padx=(5, 0))
        
        ttk.Label(frame_botones, text="Acciones", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        self.btn_sintactico = ttk.Button(frame_botones, text="📝 Análisis Sintáctico", command=self.estado_analisis_sintactico, width=20)
        self.btn_sintactico.pack(pady=7, ipady=7)
        
        self.btn_html = ttk.Button(frame_botones, text="🌐 Abrir HTML", command=self.generar_html, width=20)
        self.btn_html.pack(pady=7, ipady=7)    
        
        ttk.Separator(frame_botones, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        
        frame_resultados = ttk.LabelFrame(frame_principal, text="Resultados", padding="5")
        frame_resultados.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0), pady=(5, 0))
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(1, weight=3)
        
        self.notebook = ttk.Notebook(frame_resultados)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.tab_sintactico = tk.Text(self.notebook, wrap=tk.WORD, font=("Consolas", 9), bg=self.color_resultados, fg="#00ff00", insertbackground="white", height=10)
        self.notebook.add(self.tab_sintactico, text="Análisis sintáctico")
        
        scroll_sin = ttk.Scrollbar(self.tab_sintactico, orient=tk.VERTICAL, command=self.tab_sintactico.yview)
        scroll_sin.pack(side=tk.RIGHT, fill=tk.Y)
        self.tab_sintactico.configure(yscrollcommand=scroll_sin.set)
        
    def buscar_archivo(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo de programa", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if ruta:
            self.cargar_archivo(ruta)
    
    def cargar_archivo(self, ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
            self.editor.delete(1.0, tk.END)
            self.editor.insert(1.0, contenido)
            self.texto_actual = contenido
            nombre_archivo = os.path.basename(ruta)
            self.label_archivo.config(text=f"✓ cargado: '{nombre_archivo}' ", foreground="green")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    

    def estado_analisis_sintactico(self):
        global html
        texto = self.editor.get(1.0, tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "No hay código para analizar")
            return
        try:
            lexer.lineno = 1; lexer.input(texto.upper()) #para resetear posición del lexer
            
            self.notebook.select(self.tab_sintactico)
            self.tab_sintactico.delete(1.0, tk.END)
            self.root.update()
            
            parser.parse(texto.upper(), lexer=lexer)
            
            cabecera_html() 


            self.tab_sintactico.tag_config("exito1", foreground="#00ff00", font=("Arial", 15, "bold"))
            self.tab_sintactico.insert(tk.END, "✅ ANÁLISIS SINTÁCTICO EXITOSO\n", "exito1")
            self.tab_sintactico.tag_config("exito2", foreground="#008800", font=("Arial", 12))
            self.tab_sintactico.insert(tk.END, "        El HTML se puede generar de forma correcta.", "exito2")
        except Exception as e:
            self.tab_sintactico.tag_config("error1", foreground="#ff4444", font=("Arial", 15, "bold"))
            self.tab_sintactico.insert(tk.END, "❌ ERROR DE SINTAXIS\n", "error1")
            self.tab_sintactico.tag_config("error2", foreground="#ff4444", font=("Arial", 12))
            self.tab_sintactico.insert(tk.END, "        El HTML puede derivarse incompleto o contener errores.", "error2")

    def generar_html(self):
        global html
        texto = self.editor.get(1.0, tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "No hay código para analizar")
            return

        lexer.lineno = 1; lexer.input(texto.upper()) #para resetear posición del lexer
        
        self.notebook.select(self.tab_sintactico)
        self.tab_sintactico.delete(1.0, tk.END)
        self.root.update()
        
        
        cabecera_html()
        
        parser.parse(texto.upper(), lexer=lexer)
        
        final_html()
        
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html", encoding="utf-8") as archivo_temporal:
            archivo_temporal.write(html)
            ruta_temporal = archivo_temporal.name
        
        webbrowser.open("file://" + os.path.abspath(ruta_temporal))


#====================================================================#
#=============================== MAIN ===============================#
#====================================================================#
  
root = tk.Tk()
app = InterfazAnalizador(root)
root.mainloop()

#detalles:
#1-cada vez que se aprieta el botón de "análisis sintáctico" se hace el parsing, y debido a eso, se construye nuevamente el html
#cada vez que se apriete el boton, como solución para que se construya solo al apretar "abrir HTML" o "Exportar HTML",
#al acceder a la función "análisis_sintáctico()" mediante el botón "análisis sintáctico" se reinicia la variable y se vuelve a poner
#la cabecera, aunque estaría bueno que se coloque la cabecera desde sigma...

#2-Agregar imágenes a los actuadores dependiendo del actuador, atributo y valor, por ejemplo foco.estado = ON (imágen_foco_prendido)
#al html, y también agregar el ícono del grupo.

#3-Agregar todo lo pedido en la consigna en cuanto al HTML (cosas para los sensores, etc), y agregar cantidad total de
#sensores y actuadores en el HTML.

#preguntas:
#1-a qué se refiere con estado de sensores? si solo se usan para condiciones.
#2-es correcta nuestra manera de ir construyendo el HTML? se va construyendo a medida que se alcanzan las reglas, es decir
#en cada regla, se va construyendo concatenándose cada parte del html.