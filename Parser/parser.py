from ply import lex, yacc
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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
    'OP_COMPARADOR_BOOL', #Contiene (==|!=)
    'PERCENT',
    'TIEMPO',
    'ILUMINANCIA',
    'HORA',
    'DATE',
    'EMAIL',
    'DISCRETO',
    'NOMBRE',
    'OP_COMPARADOR_GRAL', #Contiene (>=|<=|<|>) 
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
def t_DATE(t): r'(0[1-9]|[1-2][0-9]|3[0-1])\/(0[1-9]|1[0-2])\/20[0-9][0-9]'; return t
#def t_DATE(t): r'([1-2][0-9]|3[0-1]|[0-9])\/(1[0-2]|[1-9])\/20[0-9][0-9]'; return t
def t_EMAIL(t): r'[A-Z0-9\.\+\-]+@[A-Z0-9\.\+\-]+\.[A-Z]{2,4}'; return t
def t_DISCRETO(t): r'(FRIO|CALOR|VENT)'; return t
def t_NOMBRE(t): r'(BLANCO|ROJO|AZUL|BLUE|RED|WHITE)'; return t
def t_OP_COMPARADOR_BOOL(t): r'(==|!=)'; return t
def t_OP_COMPARADOR_GRAL(t): r'(>=|=<|>|<)'; return t
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
    global error_lexer
    columna = find_column(t.lexer.lexdata, t)    
    error_lexer = f"Carácter ilegal '{str(t.value[0])}' en la Línea {str(t.lexer.lineno)}, Columna {str(columna)}"
    return(t)

lexer = lex.lex()

html = ""  #variable global para ir concatenando etiquetas para el html
nombre_archivo = "" #variable global para inicializar el nombre del archivo al generar HTML
error_lexer = ""    #para mostrar errores en la interfaz de tkinter, tomados de t_error
error_sintaxis = "" #para mostrar errores en la interfaz de tkinter, tomados de p_error
col = ""; fil = ""

def cabecera_html():
    global html
    html = "<!DOCTYPE html>\n<html lang='es'>\n<head>\n"
    html += "  <meta charset='UTF-8'>\n"
    html += "  <title>Smart-Home - Estado de Actuadores y Sensores - Binarybuilders</title>\n"
    html += "</head>\n"
    html += "<body style='margin: 0; font-family: sans-serif; background-color: #f4f6f9;'>\n"
    html += f"""
    <div style="background-color: #1a202c; padding: 25px 40px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.15); display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="color: #ffffff; font-family: 'Franklin Gothic Medium', sans-serif; font-size: 38px; text-transform: uppercase; letter-spacing: 2px; margin: 0; padding-bottom: 5px;">
                SMART-HOME - Sensores y Actuadores
            </h1>
            <h3 style="color: #e0e0e0; font-family: 'Century Gothic', 'Segoe UI', sans-serif; font-size: 16px; font-weight: 300; letter-spacing: 1px; margin: 5px 0 0 0;">
                Estado de todos los sensores y actuadores del hogar:
            </h3>
        </div>
        
        <div style="display: flex; flex-direction: column; align-items: flex-start; gap: 5px;">
            <span style="color: #a0aec0; font-family: 'Segoe UI', sans-serif; font-size: 12px; font-weight: 300; font-style: italic; letter-spacing: 0.5px;">
                Realizado por:
            </span>
            <img src="../resources/BinaryBuilders.png" alt="BinaryBuilders Logo" style="height: 70px; width: auto; border-radius: 5px;">
        </div>
        
    </div>
    """

def final_html():
    global html
    html += """
    <div style="background-color: #003d82; padding: 25px 0; text-align: center; margin-top: calc(100vh - 350px);">
        <p style="color: #ffffff; font-family: sans-serif; font-size: 14px; margin: 0; letter-spacing: 1px;">
            BinaryBuilders© 2026
        </p>
    </div>
    """ 
    html += "\n</body>\n</html>"

img_act = {
    'AIRE': {
        'ON': '../resources/aire_on.png',
        'OFF': '../resources/aire_off.png',
        'FRIO': '../resources/aire_on.png'
    },
    'ALARMA': {
        'ON': '../resources/alarma_on.png',
        'OFF': '../resources/alarma_off.png'
    },
    'ALTAVOZ': {
        'MAIL': '../resources/altavoz_mail.png',
        'MENSAJE': '../resources/altavoz_mensaje.png',
        'VOLUMEN_ON': '../resources/altavoz_volumen_on.png',
        'VOLUMEN_OFF': '../resources/altavoz_volumen_off.png'
    },
    'CERRADURA': { 
        'ON': '../resources/cerradura_on.png',
        'OFF': '../resources/cerradura_off.png'
    },
    'FOCO': {
        'ON': '../resources/foco_on.png',
        'OFF': '../resources/foco_off.png',
        'BLUE': '../resources/foco_azul.png',
        'AZUL': '../resources/foco_azul.png',
        'BLANCO': '../resources/foco_blanco.png',
        'ROJO': '../resources/foco_rojo.png',
        'RED': '../resources/foco_rojo.png'
    },
    'PERSIANA': {
        'UNICO': '../resources/persiana.png'
    },
    'RELOJ': {
        'FECHA': '../resources/reloj_fecha.png',
        'HORA': '../resources/reloj_hora.png'
    }
}

def formato_actuador_html(nombre_actuador, identif_actuador, atributo, valor_atributo):
    global html

    texto_real = valor_atributo.value if hasattr(valor_atributo, 'value') else str(valor_atributo)

    es_un_mail = (hasattr(valor_atributo, 'type') and valor_atributo.type == 'EMAIL') or (atributo == "email")
    representacion_valor = f'<a href="mailto:{texto_real}" style="color: #0056b3; text-decoration: underline; font-weight: bold;">{texto_real}</a>' if es_un_mail else texto_real

    nombre_actuador = nombre_actuador.upper().strip()
    atributo = atributo.upper().strip()
    texto_real = texto_real.upper().strip()

    imagen_actuador = ""
    if nombre_actuador == 'FOCO':
        if atributo == 'ESTADO' and texto_real == 'ON':
            imagen_actuador = img_act['FOCO']['ON']
        elif atributo == 'ESTADO' and texto_real == 'OFF':
            imagen_actuador = img_act['FOCO']['OFF']
        elif atributo == 'BRILLO' and texto_real != '0%':
            imagen_actuador = img_act['FOCO']['ON']
        elif atributo == 'BRILLO' and texto_real == '0%':
            imagen_actuador = img_act['FOCO']['OFF']
        elif atributo == 'COLOR' and (texto_real == 'BLANCO' or texto_real == 'WHITE'):
            imagen_actuador = img_act['FOCO']['BLANCO']
        elif atributo == 'COLOR' and (texto_real == 'ROJO' or texto_real == 'RED'):
            imagen_actuador = img_act['FOCO']['ROJO']
        elif atributo == 'COLOR' and (texto_real == 'AZUL' or texto_real == 'BLUE'):
            imagen_actuador = img_act['FOCO']['AZUL']
            
    elif nombre_actuador == 'AIRE': # <-- Corregido a Mayúsculas
        if atributo == 'ESTADO' and texto_real == 'ON':
            imagen_actuador = img_act['AIRE']['ON']
        elif atributo == 'ESTADO' and texto_real == 'OFF':
            imagen_actuador = img_act['AIRE']['OFF']
        elif atributo == 'MODO' or (atributo in ['TEMP_OBJ', 'TEMP_OBJETIVO', 'TEMP_ACT']):
            imagen_actuador = img_act['AIRE']['ON']
            
    elif nombre_actuador == 'PERSIANA':
        imagen_actuador = img_act['PERSIANA']['UNICO']
        
    elif nombre_actuador == 'CERRADURA':
        if atributo == 'ESTADO' and texto_real == 'ON': # <-- Corregido el espacio en 'ESTADO'
            imagen_actuador = img_act['CERRADURA']['ON']
        elif atributo == 'ESTADO' and texto_real == 'OFF':
            imagen_actuador = img_act['CERRADURA']['OFF']
            
    elif nombre_actuador == 'RELOJ':
        if atributo == 'HORA':
            imagen_actuador = img_act['RELOJ']['HORA']
        elif atributo == 'FECHA':
            imagen_actuador = img_act['RELOJ']['FECHA']
            
    elif nombre_actuador == 'ALTAVOZ':
        if atributo == 'VOLUMEN':
            if valor_atributo == '0%':
                imagen_actuador = img_act['ALTAVOZ']['VOLUMEN_OFF']
            else:
                imagen_actuador = img_act['ALTAVOZ']['VOLUMEN_ON']
        elif atributo == 'MUTE':
            if valor_atributo == 'ON':
                imagen_actuador = img_act['ALTAVOZ']['VOLUMEN_OFF']
            else:
                imagen_actuador = img_act['ALTAVOZ']['VOLUMEN_ON']
        elif atributo == 'MENSAJE':
            imagen_actuador = img_act['ALTAVOZ']['MENSAJE']
        elif atributo in ['EMAIL_NOTIF', 'EMAIL']:
            imagen_actuador = img_act['ALTAVOZ']['MAIL']
            
    elif nombre_actuador == 'ALARMA':
        if atributo == 'ESTADO' or atributo == 'ACTIVADA':
            if valor_atributo == 'ON':
                imagen_actuador = img_act['ALARMA']['ON']
            else:
                imagen_actuador = img_act['ALARMA']['OFF']

    if nombre_actuador == "FOCO": emoji = "💡"
    elif nombre_actuador == "AIRE": emoji = "❄️"
    elif nombre_actuador == "PERSIANA": emoji = "🪟"
    elif nombre_actuador == "CERRADURA": emoji = "🔒"
    elif nombre_actuador == "ALTAVOZ": emoji = "🔊"
    elif nombre_actuador == "ALARMA": emoji = "🚨"

    html_imagen = f'<img src="{imagen_actuador}" alt="{nombre_actuador}" style="height: 65px; width: auto; object-fit: contain; margin-left: 20px;">' if imagen_actuador else ""

    sufijo_identificador = f" ({identif_actuador})" if identif_actuador else ""
    html += f"""
    <div style="border: 1px solid gray; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; background-color: #ffffff; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;">{nombre_actuador}{emoji}</h1>{sufijo_identificador} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300; font-size: 14px; margin-left: 5px;">(asignado)</span>
            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                <li>{atributo}: {representacion_valor}</li>
            </ul>
        </div>
        {html_imagen}
    </div>
    """

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
        p[0] = ('BLOQUE_ACCIONES', p[1], p[2]) 
    else:
        p[0] = p[1]

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
    
    if len(p) == 4:
        p[0] = ('ASIGNACION', p[1], p[2], p[3])
        nombre_actuador = p[1]
        identif_act = p[2].replace('_', '')
        
        partes_atributo = p[3].split('=')
        atributo = partes_atributo[0].replace('.', '').strip()
        valor_atributo = partes_atributo[1].strip()
        
        formato_actuador_html(nombre_actuador, identif_act, atributo, valor_atributo)

    else:
        p[0] = ('ASIGNACION', p[1], None, p[2])
        nombre_actuador = p[1]
        
        partes_atributo = p[2].split('=')
        atributo = partes_atributo[0].replace('.', '').strip()
        valor_atributo = partes_atributo[1].strip()
        
        formato_actuador_html(nombre_actuador, None, atributo, valor_atributo)

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
    p[0] = (p[1], p[2])

def p_condicion_temperatura(p):
    '''condicion : OP_NEGACION SENSOR_TEMPERATURA identificador OP_COMPARADOR_GRAL VALOR_TEMP contcondicion
                 | OP_NEGACION SENSOR_TEMPERATURA identificador OP_COMPARADOR_BOOL VALOR_TEMP contcondicion
                 | OP_NEGACION SENSOR_TEMPERATURA identificador OP_COMPARADOR_GRAL VALOR_TEMP
                 | OP_NEGACION SENSOR_TEMPERATURA identificador OP_COMPARADOR_BOOL VALOR_TEMP
                 | OP_NEGACION SENSOR_TEMPERATURA OP_COMPARADOR_GRAL VALOR_TEMP contcondicion
                 | OP_NEGACION SENSOR_TEMPERATURA OP_COMPARADOR_BOOL VALOR_TEMP contcondicion
                 | OP_NEGACION SENSOR_TEMPERATURA OP_COMPARADOR_GRAL VALOR_TEMP
                 | OP_NEGACION SENSOR_TEMPERATURA OP_COMPARADOR_BOOL VALOR_TEMP
                 | SENSOR_TEMPERATURA identificador OP_COMPARADOR_GRAL VALOR_TEMP contcondicion
                 | SENSOR_TEMPERATURA identificador OP_COMPARADOR_BOOL VALOR_TEMP contcondicion
                 | SENSOR_TEMPERATURA identificador OP_COMPARADOR_GRAL VALOR_TEMP
                 | SENSOR_TEMPERATURA identificador OP_COMPARADOR_BOOL VALOR_TEMP
                 | SENSOR_TEMPERATURA OP_COMPARADOR_GRAL VALOR_TEMP contcondicion
                 | SENSOR_TEMPERATURA OP_COMPARADOR_BOOL VALOR_TEMP contcondicion
                 | SENSOR_TEMPERATURA OP_COMPARADOR_GRAL VALOR_TEMP
                 | SENSOR_TEMPERATURA OP_COMPARADOR_BOOL VALOR_TEMP'''
    global html
    def val(obj):
        return obj.value if hasattr(obj, 'value') else str(obj)

    elementos = [val(p[i]) for i in range(1, len(p))]
    
    negacion = None; identificador = None; cont_cond = None
    
    # 1. Detectar si tiene negación al principio
    if elementos[0] == 'NOT':
        negacion = elementos.pop(0)
        
    # Ahora el primer elemento restante SÍ O SÍ es el sensor
    sensor = elementos.pop(0) # Remueve 'SENSOR_TEMP'
    
    # 2. Detectar si el siguiente elemento es un identificador (empieza con _)
    if elementos[0].startswith('_'):
        identificador = elementos.pop(0)
        
    # 3. Los siguientes dos elementos obligatorios son el COMPARADOR y el VALOR
    comp = elementos.pop(0)
    valor = elementos.pop(0)
    comparacion_completa = comp + valor
    
    # 4. Si todavía queda algo en la lista, es el contcondicion
    if len(elementos) > 0:
        # p[len(p)-1] contiene la tupla devuelta por p_contcondicion, la dejamos intacta
        cont_cond = p[len(p)-1]
    
    # Armamos el nodo del árbol de forma consistente
    p[0] = ('CONDICION_TEMP', negacion, sensor, identificador, comparacion_completa, cont_cond)

    if identificador:
        identificador = f"({identificador.replace('_', '')})"
    else:
        identificador = ""

    html += f"""
    <div style="border: 1px solid green; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; display: flex; justify-content: space-between; align-items: center; border-radius: 8px;">
        <div>
            <h2 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;"><b>Sensor de temperatura ⚙️</b>{identificador}: {valor} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300 !important; font-size: 14px; margin-left: 5px;">(lectura)</span></h2>
        </div>
        <img src="../resources/sensor.png" alt="Sensor" style="width: 50px; height: 50px; margin-right: 10px;">
    </div>
    """

def p_condicion_humedad(p):
    '''condicion : OP_NEGACION SENSOR_HUMEDAD identificador OP_COMPARADOR_GRAL PERCENT contcondicion
                 | OP_NEGACION SENSOR_HUMEDAD identificador OP_COMPARADOR_BOOL PERCENT contcondicion
                 | OP_NEGACION SENSOR_HUMEDAD identificador OP_COMPARADOR_GRAL PERCENT
                 | OP_NEGACION SENSOR_HUMEDAD identificador OP_COMPARADOR_BOOL PERCENT
                 | OP_NEGACION SENSOR_HUMEDAD OP_COMPARADOR_GRAL PERCENT contcondicion
                 | OP_NEGACION SENSOR_HUMEDAD OP_COMPARADOR_BOOL PERCENT contcondicion
                 | OP_NEGACION SENSOR_HUMEDAD OP_COMPARADOR_GRAL PERCENT
                 | OP_NEGACION SENSOR_HUMEDAD OP_COMPARADOR_BOOL PERCENT
                 | SENSOR_HUMEDAD identificador OP_COMPARADOR_GRAL PERCENT contcondicion
                 | SENSOR_HUMEDAD identificador OP_COMPARADOR_BOOL PERCENT contcondicion
                 | SENSOR_HUMEDAD identificador OP_COMPARADOR_GRAL PERCENT
                 | SENSOR_HUMEDAD identificador OP_COMPARADOR_BOOL PERCENT
                 | SENSOR_HUMEDAD OP_COMPARADOR_GRAL PERCENT contcondicion
                 | SENSOR_HUMEDAD OP_COMPARADOR_BOOL PERCENT contcondicion
                 | SENSOR_HUMEDAD OP_COMPARADOR_GRAL PERCENT
                 | SENSOR_HUMEDAD OP_COMPARADOR_BOOL PERCENT'''
    global html
    
    if p[1] != 'SENSOR_HUMEDAD':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 7:
            p[0] = ('CONDICION_HUMEDAD', negacion, actuador, p[3], p[4] + p[5], p[6])
            valor = p[5]
        elif len(p) == 6:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_HUMEDAD', negacion, actuador, p[3], p[4] + p[5], None)
                valor = p[5]
            else:
                p[0] = ('CONDICION_HUMEDAD', negacion, actuador, None, p[3] + p[4], p[5])
                valor = p[4]
        else:
            p[0] = ('CONDICION_HUMEDAD', negacion, actuador, None, p[3] + p[4], None)
            valor = p[4]
    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 6:
            p[0] = ('CONDICION_HUMEDAD', negacion, actuador, p[2], p[3] + p[4], p[5])
            valor = p[4]
        elif len(p) == 5:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_HUMEDAD', negacion, actuador, p[2], p[3] + p[4], None)
                valor = p[4]
            else:
                p[0] = ('CONDICION_HUMEDAD', negacion, actuador, None, p[2] + p[3], p[4])
                valor = p[3]
        else:
            p[0] = ('CONDICION_HUMEDAD', negacion, actuador, None, p[2] + p[3], None)
            valor = p[3]

    identificador = p[0][3] if p[0][3] else ""

    if identificador:
        identificador = f"({identificador.replace('_', '')})"
    else:
        identificador = ""

    html += f"""
    <div style="border: 1px solid green; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; display: flex; justify-content: space-between; align-items: center; border-radius: 8px;">
        <div>
            <h2 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;"><b>Sensor de humedad ⚙️</b>{identificador}: {valor} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300 !important; font-size: 14px; margin-left: 5px;">(lectura)</span></h2>
        </div>
        <img src="../resources/sensor.png" alt="Sensor" style="width: 50px; height: 50px; margin-right: 10px;">
    </div>
    """

def p_condicion_luz(p):
    '''condicion : OP_NEGACION SENSOR_LUZ identificador OP_COMPARADOR_GRAL ILUMINANCIA contcondicion
                 | OP_NEGACION SENSOR_LUZ identificador OP_COMPARADOR_BOOL ILUMINANCIA contcondicion
                 | OP_NEGACION SENSOR_LUZ identificador OP_COMPARADOR_GRAL ILUMINANCIA
                 | OP_NEGACION SENSOR_LUZ identificador OP_COMPARADOR_BOOL ILUMINANCIA
                 | OP_NEGACION SENSOR_LUZ OP_COMPARADOR_GRAL ILUMINANCIA contcondicion
                 | OP_NEGACION SENSOR_LUZ OP_COMPARADOR_BOOL ILUMINANCIA contcondicion
                 | OP_NEGACION SENSOR_LUZ OP_COMPARADOR_GRAL ILUMINANCIA
                 | OP_NEGACION SENSOR_LUZ OP_COMPARADOR_BOOL ILUMINANCIA
                 | SENSOR_LUZ identificador OP_COMPARADOR_GRAL ILUMINANCIA contcondicion
                 | SENSOR_LUZ identificador OP_COMPARADOR_BOOL ILUMINANCIA contcondicion
                 | SENSOR_LUZ identificador OP_COMPARADOR_GRAL ILUMINANCIA
                 | SENSOR_LUZ identificador OP_COMPARADOR_BOOL ILUMINANCIA
                 | SENSOR_LUZ OP_COMPARADOR_GRAL ILUMINANCIA contcondicion
                 | SENSOR_LUZ OP_COMPARADOR_BOOL ILUMINANCIA contcondicion
                 | SENSOR_LUZ OP_COMPARADOR_GRAL ILUMINANCIA
                 | SENSOR_LUZ OP_COMPARADOR_BOOL ILUMINANCIA'''
    global html
    
    if p[1] != 'SENSOR_LUZ':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 7:
            p[0] = ('CONDICION_LUZ', negacion, actuador, p[3], p[4] + p[5], p[6])
            valor = p[5]
        elif len(p) == 6:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_LUZ', negacion, actuador, p[3], p[4] + p[5], None)
                valor = p[5]
            else:
                p[0] = ('CONDICION_LUZ', negacion, actuador, None, p[3] + p[4], p[5])
                valor = p[4]
        else:
            p[0] = ('CONDICION_LUZ', negacion, actuador, None, p[3] + p[4], None)
            valor = p[4]

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 6:
            p[0] = ('CONDICION_LUZ', negacion, actuador, p[2], p[3] + p[4], p[5])
            valor = p[4]
        elif len(p) == 5:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_LUZ', negacion, actuador, p[2], p[3] + p[4], None)
                valor = p[4]
            else:
                p[0] = ('CONDICION_LUZ', negacion, actuador, None, p[2] + p[3], p[4])
                valor = p[3]
        else:
            p[0] = ('CONDICION_LUZ', negacion, actuador, None, p[2] + p[3], None)
            valor = p[3]

    identificador = p[0][3] if p[0][3] else ""

    if identificador:
        identificador = f" ({identificador.replace('_', '')})"
    else:
        identificador = ""

    html += f"""    
    <div style="border: 1px solid green; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; display: flex; justify-content: space-between; align-items: center; border-radius: 8px;">
        <div>
            <h2 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;"><b>Sensor de luz ⚙️</b>{identificador}: {valor} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300 !important; font-size: 14px; margin-left: 5px;">(lectura)</span></h2>
        </div>
        <img src="../resources/sensor.png" alt="Sensor" style="width: 50px; height: 50px; margin-right: 10px;">
    </div>
    """

def p_condicion_movimiento(p):
    '''condicion : OP_NEGACION SENSOR_MOVIMIENTO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | OP_NEGACION SENSOR_MOVIMIENTO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO
                 | OP_NEGACION SENSOR_MOVIMIENTO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | OP_NEGACION SENSOR_MOVIMIENTO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO
                 | SENSOR_MOVIMIENTO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | SENSOR_MOVIMIENTO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO
                 | SENSOR_MOVIMIENTO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | SENSOR_MOVIMIENTO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO'''
    global html
    
    if p[1] != 'SENSOR_MOVIMIENTO':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 7:
            p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, p[3], p[4] + p[5], p[6])
            valor = p[5] 
        elif len(p) == 6:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, p[3], p[4] + p[5], None)
                valor = p[5]  
            else:
                p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, None, p[3] + p[4], p[5])
                valor = p[4]  
        else:
            p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, None, p[3] + p[4], None)
            valor = p[4] 

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 6:
            p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, p[2], p[3] + p[4], p[5])
            valor = p[4]  # Solo BOOL_DISPOSITIVO
        elif len(p) == 5:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, p[2], p[3] + p[4], None)
                valor = p[4]  # Solo BOOL_DISPOSITIVO
            else:
                p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, None, p[2] + p[3], p[4])
                valor = p[3]  # Solo BOOL_DISPOSITIVO
        else:
            p[0] = ('CONDICION_MOVIMIENTO', negacion, actuador, None, p[2] + p[3], None)
            valor = p[3]  # Solo BOOL_DISPOSITIVO

    identificador = p[0][3] if p[0][3] else ""

    if identificador:
        identificador = f" ({identificador.replace('_', '')})"
    else:
        identificador = ""

    html += f"""
    <div style="border: 1px solid green; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; display: flex; justify-content: space-between; align-items: center; border-radius: 8px;">
        <div>
            <h2 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;"><b>Sensor de movimiento ⚙️</b>{identificador}: {valor} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300 !important; font-size: 14px; margin-left: 5px;">(lectura)</span></h2>
        </div>
        <img src="../resources/sensor.png" alt="Sensor" style="width: 50px; height: 50px; margin-right: 10px;">
    </div>
    """

def p_condicion_humo(p):
    '''condicion : OP_NEGACION SENSOR_HUMO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | OP_NEGACION SENSOR_HUMO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO
                 | OP_NEGACION SENSOR_HUMO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | OP_NEGACION SENSOR_HUMO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO
                 | SENSOR_HUMO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | SENSOR_HUMO identificador OP_COMPARADOR_BOOL BOOL_DISPOSITIVO
                 | SENSOR_HUMO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO contcondicion
                 | SENSOR_HUMO OP_COMPARADOR_BOOL BOOL_DISPOSITIVO'''
    global html
    
    if p[1] != 'SENSOR_HUMO':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 7:
            p[0] = ('CONDICION_HUMO', negacion, actuador, p[3], p[4] + p[5], p[6])
            valor = p[5] 
        elif len(p) == 6:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_HUMO', negacion, actuador, p[3], p[4] + p[5], None)
                valor = p[5] 
            else:
                p[0] = ('CONDICION_HUMO', negacion, actuador, None, p[3] + p[4], p[5])
                valor = p[4]
        else:
            p[0] = ('CONDICION_HUMO', negacion, actuador, None, p[3] + p[4], None)
            valor = p[4] 

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 6:
            p[0] = ('CONDICION_HUMO', negacion, actuador, p[2], p[3] + p[4], p[5])
            valor = p[4]
        elif len(p) == 5:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_HUMO', negacion, actuador, p[2], p[3] + p[4], None)
                valor = p[4]
            else:
                p[0] = ('CONDICION_HUMO', negacion, actuador, None, p[2] + p[3], p[4])
                valor = p[3]
        else:
            p[0] = ('CONDICION_HUMO', negacion, actuador, None, p[2] + p[3], None)
            valor = p[3]

    identificador = p[0][3] if p[0][3] else ""

    if identificador:
        identificador = f" ({identificador.replace('_', '')})"
    else:
        identificador = ""

    html += f"""
    <div style="border: 1px solid green; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; display: flex; justify-content: space-between; align-items: center; border-radius: 8px;">
        <div>
            <h2 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;"><b>Sensor de humo ⚙️</b>{identificador}: {valor} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300 !important; font-size: 14px; margin-left: 5px;">(lectura)</span></h2>
        </div>
        <img src="../resources/sensor.png" alt="Sensor" style="width: 50px; height: 50px; margin-right: 10px;">
    </div>
    """

def p_condicion_foco(p):
    '''condicion : OP_NEGACION ACTUADOR_FOCO identificador atributos_lec_foco contcondicion
                 | OP_NEGACION ACTUADOR_FOCO identificador atributos_lec_foco
                 | OP_NEGACION ACTUADOR_FOCO atributos_lec_foco contcondicion
                 | OP_NEGACION ACTUADOR_FOCO atributos_lec_foco
                 | ACTUADOR_FOCO identificador atributos_lec_foco contcondicion
                 | ACTUADOR_FOCO identificador atributos_lec_foco
                 | ACTUADOR_FOCO atributos_lec_foco contcondicion
                 | ACTUADOR_FOCO atributos_lec_foco'''
    global html
    
    if p[1] != 'FOCO':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 6:
            p[0] = ('CONDICION_FOCO', negacion, actuador, p[3], p[4], p[5])
            valor = p[4]; identificador = p[3]
        elif len(p) == 5:
            p[0] = ('CONDICION_FOCO', negacion, actuador, p[3], p[4], None)
            valor = p[4]; identificador = p[3]
        else:
            p[0] = ('CONDICION_FOCO', negacion, actuador, None, p[3], None)
            valor = p[3]
    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 5: 
            p[0] = ('CONDICION_FOCO', negacion, actuador, p[2], p[3], p[4])
            valor = p[3]
        elif len(p) == 4:
            p[0] = ('CONDICION_FOCO', negacion, actuador, p[2], p[3], None)
            valor = p[3]
        else:
            p[0] = ('CONDICION_FOCO', negacion, actuador, None, p[2], None)
            valor = p[2]

    encontrado = ""
    for elemento in p[0]:
        if elemento and str(elemento).startswith('_'):
            encontrado = str(elemento).replace('_', '')
            break
    identificador = encontrado if encontrado else ""

    if identificador:
        identificador = f" ({identificador.replace('_', '')})"
    else:
        identificador = ""

    html += f"""
    <div style="border: 1px solid gray; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; background-color: #ffffff; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;">FOCO 💡</h1>{identificador} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300; font-size: 14px; margin-left: 5px;">(lectura)</span>
            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                <li>{valor}</li>
            </ul>
        </div>
        <img src="../resources/foco_on.png" alt="Foco" style="width: 50px; height: 50px; margin-right: 10px;">
    </div>
    """

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
    global html
    
    if p[1] != 'AIRE':
        negacion = p[1]
        actuador = p[2]        
        if len(p) == 6:
            p[0] = ('CONDICION_AIRE', negacion, actuador, p[3], p[4], p[5])
            valor = p[4]
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_AIRE', negacion, actuador, p[3], p[4], None)
                valor = p[4]
            else:                    
                p[0] = ('CONDICION_AIRE', negacion, actuador, None, p[3], p[4])
                valor = p[3]
        else:             
            p[0] = ('CONDICION_AIRE', negacion, actuador, None, p[3], None)
            valor = p[3]
    else:
        negacion = None
        actuador = p[1]

        if len(p) == 5:
            p[0] = ('CONDICION_AIRE', negacion, actuador, p[2], p[3], p[4])
            valor = p[3]
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_AIRE', negacion, actuador, p[2], p[3], None)
                valor = p[3]
            else:                    
                p[0] = ('CONDICION_AIRE', negacion, actuador, None, p[2], p[3])
                valor = p[2]
        else: 
            p[0] = ('CONDICION_AIRE', negacion, actuador, None, p[2], None)
            valor = p[2]

    encontrado = ""
    for elemento in p[0]:
        if elemento and str(elemento).startswith('_'):
            encontrado = str(elemento).replace('_', '')
            break
    identificador = encontrado if encontrado else ""

    if identificador:
        identificador = f" ({identificador.replace('_', '')})"
    else:
        identificador = ""

    html += f"""
    <div style="border: 1px solid gray; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; background-color: #ffffff; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;">AIRE ACONDICIONADO ❄️</h1>{identificador} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300; font-size: 14px; margin-left: 5px;">(lectura)</span>
            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                <li>{valor}</li>
            </ul>
        </div>
        <img src="../resources/aire_on.png" alt="Aire" style="height: 65px; width: auto; object-fit: contain; margin-left: 20px;">
    </div>
    """

def p_condicion_actuador_persiana(p):
    '''condicion : OP_NEGACION ACTUADOR_PERSIANA identificador atributos_lec_persiana contcondicion
                 | OP_NEGACION ACTUADOR_PERSIANA identificador atributos_lec_persiana
                 | OP_NEGACION ACTUADOR_PERSIANA atributos_lec_persiana contcondicion
                 | OP_NEGACION ACTUADOR_PERSIANA atributos_lec_persiana
                 | ACTUADOR_PERSIANA identificador atributos_lec_persiana contcondicion
                 | ACTUADOR_PERSIANA identificador atributos_lec_persiana 
                 | ACTUADOR_PERSIANA atributos_lec_persiana contcondicion
                 | ACTUADOR_PERSIANA atributos_lec_persiana'''
    global html
    
    if p[1] != 'PERSIANA':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 6:
            p[0] = ('CONDICION_PERSIANA', negacion, actuador, p[3], p[4], p[5])
            valor = p[4]
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_PERSIANA', negacion, actuador, p[3], p[4], None)
                valor = p[4]
            else:
                p[0] = ('CONDICION_PERSIANA', negacion, actuador, None, p[3], p[4])
                valor = p[3]
        else:
            p[0] = ('CONDICION_PERSIANA', negacion, actuador, None, p[3], None)
            valor = p[3]

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 5:
            p[0] = ('CONDICION_PERSIANA', negacion, actuador, p[2], p[3], p[4])
            valor = p[3]
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_PERSIANA', negacion, actuador, p[2], p[3], None)
                valor = p[3]
            else:
                p[0] = ('CONDICION_PERSIANA', negacion, actuador, None, p[2], p[3])
                valor = p[2]
        else:
            p[0] = ('CONDICION_PERSIANA', negacion, actuador, None, p[2], None)
            valor = p[2]

    encontrado = ""
    for elemento in p[0]:
        if elemento and str(elemento).startswith('_'):
            encontrado = str(elemento).replace('_', '')
            break
    identificador = encontrado if encontrado else ""

    if identificador:
        identificador = f" ({identificador.replace('_', '')})"
    else:
        identificador = ""

    html += f"""
    <div style="border: 1px solid gray; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; background-color: #ffffff; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;">PERSIANA 🪟</h1>{identificador} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300; font-size: 14px; margin-left: 5px;">(lectura)</span>
            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                <li>{valor}</li>
            </ul>
        </div>
        <img src="../resources/persiana.png" alt="Persiana" style="height: 65px; width: auto; object-fit: contain; margin-left: 20px;">
    </div>
    """

    
def p_condicion_actuador_cerradura(p):
    '''condicion : OP_NEGACION ACTUADOR_CERRADURA identificador atributos_lec_cerradura contcondicion
                 | OP_NEGACION ACTUADOR_CERRADURA identificador atributos_lec_cerradura
                 | OP_NEGACION ACTUADOR_CERRADURA atributos_lec_cerradura contcondicion
                 | OP_NEGACION ACTUADOR_CERRADURA atributos_lec_cerradura
                 | ACTUADOR_CERRADURA identificador atributos_lec_cerradura contcondicion
                 | ACTUADOR_CERRADURA identificador atributos_lec_cerradura
                 | ACTUADOR_CERRADURA atributos_lec_cerradura contcondicion
                 | ACTUADOR_CERRADURA atributos_lec_cerradura'''
    global html
    
    if p[1] != 'CERRADURA':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 6:
            p[0] = ('CONDICION_CERRADURA', negacion, actuador, p[3], p[4], p[5])
            valor = p[4]
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_CERRADURA', negacion, actuador, p[3], p[4], None)
                valor = p[4]
            else:
                p[0] = ('CONDICION_CERRADURA', negacion, actuador, None, p[3], p[4])
                valor = p[3]
        else:
            p[0] = ('CONDICION_CERRADURA', negacion, actuador, None, p[3], None)
            valor = p[3]

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 5:
            p[0] = ('CONDICION_CERRADURA', negacion, actuador, p[2], p[3], p[4])
            valor = p[3]
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_CERRADURA', negacion, actuador, p[2], p[3], None)
                valor = p[3]
            else:
                p[0] = ('CONDICION_CERRADURA', negacion, actuador, None, p[2], p[3])
                valor = p[2]
        else:
            p[0] = ('CONDICION_CERRADURA', negacion, actuador, None, p[2], None)
            valor = p[2]

    encontrado = ""
    for elemento in p[0]:
        if elemento and str(elemento).startswith('_'):
            encontrado = str(elemento).replace('_', '')
            break
    identificador = encontrado if encontrado else ""

    if identificador:
        identificador = f" ({identificador.replace('_', '')})"
    else:
        identificador = ""

    html += f"""
    <div style="border: 1px solid gray; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; background-color: #ffffff; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;">CERRADURA 🔒</h1>{identificador} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300; font-size: 14px; margin-left: 5px;">(lectura)</span>
            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                <li>{valor}</li>
            </ul>
        </div>
        <img src="../resources/cerradura_on.png" alt="Cerradura" style="height: 65px; width: auto; object-fit: contain; margin-left: 20px;">
    </div>
    """


def p_condicion_actuador_reloj(p):
    '''condicion : OP_NEGACION ACTUADOR_RELOJ identificador atributos_lec_reloj contcondicion
                 | OP_NEGACION ACTUADOR_RELOJ identificador atributos_lec_reloj
                 | OP_NEGACION ACTUADOR_RELOJ atributos_lec_reloj contcondicion
                 | OP_NEGACION ACTUADOR_RELOJ atributos_lec_reloj
                 | ACTUADOR_RELOJ identificador atributos_lec_reloj contcondicion
                 | ACTUADOR_RELOJ identificador atributos_lec_reloj
                 | ACTUADOR_RELOJ atributos_lec_reloj contcondicion
                 | ACTUADOR_RELOJ atributos_lec_reloj'''
    global html
    
    if p[1] != 'RELOJ':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 6:
            p[0] = ('CONDICION_RELOJ', negacion, actuador, p[3], p[4], p[5])
            valor = p[4]
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_RELOJ', negacion, actuador, p[3], p[4], None)
                valor = p[4]
            else:
                p[0] = ('CONDICION_RELOJ', negacion, actuador, None, p[3], p[4])
                valor = p[3]
        else:
            p[0] = ('CONDICION_RELOJ', negacion, actuador, None, p[3], None)
            valor = p[3]

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 5:
            p[0] = ('CONDICION_RELOJ', negacion, actuador, p[2], p[3], p[4])
            valor = p[3]
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_RELOJ', negacion, actuador, p[2], p[3], None)
                valor = p[3]
            else:
                p[0] = ('CONDICION_RELOJ', negacion, actuador, None, p[2], p[3])
                valor = p[2]
        else:
            p[0] = ('CONDICION_RELOJ', negacion, actuador, None, p[2], None)
            valor = p[2]

    encontrado = ""
    for elemento in p[0]:
        if elemento and str(elemento).startswith('_'):
            encontrado = str(elemento).replace('_', '')
            break
    identificador = encontrado if encontrado else ""

    if identificador:
        identificador = f" ({identificador.replace('_', '')})"
    else:
        identificador = ""

    html += f"""
    <div style="border: 1px solid gray; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; background-color: #ffffff; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;">RELOJ ⏰</h1>{identificador} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300; font-size: 14px; margin-left: 5px;">(lectura)</span>
            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                <li>{valor}</li>
            </ul>
        </div>
        <img src="../resources/reloj_hora.png" alt="Reloj" style="height: 65px; width: auto; object-fit: contain; margin-left: 20px;">
    </div>
    """

def p_condicion_actuador_altavoz(p):
    '''condicion : OP_NEGACION ACTUADOR_ALTAVOZ identificador atributos_lec_altavoz contcondicion
                 | OP_NEGACION ACTUADOR_ALTAVOZ identificador atributos_lec_altavoz
                 | OP_NEGACION ACTUADOR_ALTAVOZ atributos_lec_altavoz contcondicion
                 | OP_NEGACION ACTUADOR_ALTAVOZ atributos_lec_altavoz
                 | ACTUADOR_ALTAVOZ identificador atributos_lec_altavoz contcondicion
                 | ACTUADOR_ALTAVOZ identificador atributos_lec_altavoz
                 | ACTUADOR_ALTAVOZ atributos_lec_altavoz contcondicion
                 | ACTUADOR_ALTAVOZ atributos_lec_altavoz'''
    global html
    
    if p[1] != 'ALTAVOZ':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 6:
            p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, p[3], p[4], p[5])
            valor = p[4]
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, p[3], p[4], None)
                valor = p[4]
            else:
                p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, None, p[3], p[4])
                valor = p[3]
        else:
            p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, None, p[3], None)
            valor = p[3]

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 5:
            p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, p[2], p[3], p[4])
            valor = p[3]
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, p[2], p[3], None)
                valor = p[3]
            else:
                p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, None, p[2], p[3])
                valor = p[2]
        else:
            p[0] = ('CONDICION_ALTAVOZ', negacion, actuador, None, p[2], None)
            valor = p[2]

    encontrado = ""
    for elemento in p[0]:
        if elemento and str(elemento).startswith('_'):
            encontrado = str(elemento).replace('_', '')
            break
    identificador = encontrado if encontrado else ""

    if identificador:
        identificador = f" ({identificador.replace('_', '')})"
    else:
        identificador = ""

    html += f"""
    <div style="border: 1px solid gray; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; background-color: #ffffff; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;">ALTAVOZ 🔊</h1>{identificador} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300; font-size: 14px; margin-left: 5px;">(lectura)</span>
            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                <li>{valor}</li>
            </ul>
        </div>
        <img src="../resources/altavoz_volumen_on.png" alt="Altavoz" style="height: 65px; width: auto; object-fit: contain; margin-left: 20px;">
    </div>
    """

def p_condicion_actuador_alarma(p):
    '''condicion : OP_NEGACION ACTUADOR_ALARMA identificador atributos_lec_alarma contcondicion
                 | OP_NEGACION ACTUADOR_ALARMA identificador atributos_lec_alarma
                 | OP_NEGACION ACTUADOR_ALARMA atributos_lec_alarma contcondicion
                 | OP_NEGACION ACTUADOR_ALARMA atributos_lec_alarma
                 | ACTUADOR_ALARMA identificador atributos_lec_alarma contcondicion
                 | ACTUADOR_ALARMA identificador atributos_lec_alarma
                 | ACTUADOR_ALARMA atributos_lec_alarma contcondicion
                 | ACTUADOR_ALARMA atributos_lec_alarma'''
    global html
    
    if p[1] != 'ALARMA':
        negacion = p[1]
        actuador = p[2]
        
        if len(p) == 6:
            p[0] = ('CONDICION_ALARMA', negacion, actuador, p[3], p[4], p[5])
            valor = p[4]
        elif len(p) == 5:
            if p[3].startswith('_'):
                p[0] = ('CONDICION_ALARMA', negacion, actuador, p[3], p[4], None)
                valor = p[4]
            else:
                p[0] = ('CONDICION_ALARMA', negacion, actuador, None, p[3], p[4])
                valor = p[3]
        else:
            p[0] = ('CONDICION_ALARMA', negacion, actuador, None, p[3], None)
            valor = p[3]

    else:
        negacion = None
        actuador = p[1]
        
        if len(p) == 5:
            p[0] = ('CONDICION_ALARMA', negacion, actuador, p[2], p[3], p[4])
            valor = p[3]
        elif len(p) == 4:
            if p[2].startswith('_'):
                p[0] = ('CONDICION_ALARMA', negacion, actuador, p[2], p[3], None)
                valor = p[3]
            else:
                p[0] = ('CONDICION_ALARMA', negacion, actuador, None, p[2], p[3])
                valor = p[2]
        else:
            p[0] = ('CONDICION_ALARMA', negacion, actuador, None, p[2], None)
            valor = p[2]

    encontrado = ""
    for elemento in p[0]:
        if elemento and str(elemento).startswith('_'):
            encontrado = str(elemento).replace('_', '')
            break
    identificador = encontrado if encontrado else ""

    if identificador:
        identificador = f" ({identificador.replace('_', '')})"
    else:
        identificador = ""

    html += f"""
    <div style="border: 1px solid gray; padding: 20px 40px; margin-bottom: 15px; margin-left: 50px; margin-right: 50px; background-color: #ffffff; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="display: inline; font-family: 'Franklin Gothic Medium'; font-size: 24px; margin: 0;">ALARMA 🚨</h1>{identificador} <span style="font-family: inherit; color: #888888; font-style: italic; font-weight: 300; font-size: 14px; margin-left: 5px;">(lectura)</span>
            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                <li>{valor}</li>
            </ul>
        </div>
        <img src="../resources/alarma_on.png" alt="Alarma" style="height: 65px; width: auto; object-fit: contain; margin-left: 20px;">
    </div>
    """

def p_atributos_lectura_foco(p):
    '''atributos_lec_foco : ATRIBUTO_ESTADO OP_COMPARADOR_BOOL BOOL_ACTUADOR
                          | ATRIBUTOS_FOCO_BRILLO OP_COMPARADOR_GRAL PERCENT
                          | ATRIBUTOS_FOCO_BRILLO OP_COMPARADOR_BOOL PERCENT
                          | ATRIBUTOS_FOCO_COLOR OP_COMPARADOR_GRAL NOMBRE
                          | ATRIBUTOS_FOCO_COLOR OP_COMPARADOR_BOOL NOMBRE'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_lectura_aire(p):
    '''atributos_lec_aire : ATRIBUTO_ESTADO OP_COMPARADOR_BOOL BOOL_ACTUADOR
                          | ATRIBUTOS_AIRE_MODO OP_COMPARADOR_GRAL DISCRETO 
                          | ATRIBUTOS_AIRE_MODO OP_COMPARADOR_BOOL DISCRETO 
                          | ATRIBUTOS_AIRE_TEMP_OBJ OP_COMPARADOR_GRAL VALOR_TEMP
                          | ATRIBUTOS_AIRE_TEMP_OBJ OP_COMPARADOR_BOOL VALOR_TEMP
                          | ATRIBUTOS_AIRE_TEMP_ACT OP_COMPARADOR_GRAL VALOR_TEMP
                          | ATRIBUTOS_AIRE_TEMP_ACT OP_COMPARADOR_BOOL VALOR_TEMP'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_lectura_persiana(p):
    '''atributos_lec_persiana : ATRIBUTOS_PERSIANA OP_COMPARADOR_GRAL PERCENT
                              | ATRIBUTOS_PERSIANA OP_COMPARADOR_BOOL PERCENT'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_lectura_cerradura(p):
    '''atributos_lec_cerradura : ATRIBUTO_ESTADO OP_COMPARADOR_BOOL BOOL_ACTUADOR'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_lectura_reloj(p):
    '''atributos_lec_reloj : ATRIBUTOS_RELOJ_HORA OP_COMPARADOR_GRAL HORA
                           | ATRIBUTOS_RELOJ_HORA OP_COMPARADOR_BOOL HORA
                           | ATRIBUTOS_RELOJ_FECHA OP_COMPARADOR_GRAL DATE
                           | ATRIBUTOS_RELOJ_FECHA OP_COMPARADOR_BOOL DATE'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_lectura_altavoz(p):
    '''atributos_lec_altavoz : ATRIBUTOS_ALTAVOZ_VOLUMEN OP_COMPARADOR_GRAL PERCENT
                             | ATRIBUTOS_ALTAVOZ_VOLUMEN OP_COMPARADOR_BOOL PERCENT
                             | ATRIBUTOS_ALTAVOZ_MUTE OP_COMPARADOR_BOOL BOOL_ACTUADOR
                             | ATRIBUTOS_ALTAVOZ_MENSAJE OP_COMPARADOR_GRAL TEXTO
                             | ATRIBUTOS_ALTAVOZ_MENSAJE OP_COMPARADOR_BOOL TEXTO
                             | ATRIBUTOS_ALTAVOZ_EMAIL OP_COMPARADOR_GRAL EMAIL
                             | ATRIBUTOS_ALTAVOZ_EMAIL OP_COMPARADOR_BOOL EMAIL'''
    p[0] = p[1] + p[2] + p[3]


def p_atributos_lectura_alarma(p):
    '''atributos_lec_alarma : ATRIBUTO_ESTADO OP_COMPARADOR_BOOL BOOL_ACTUADOR
                            | ATRIBUTOS_ALARMA OP_COMPARADOR_BOOL BOOL_ACTUADOR
    '''
    p[0] = p[1] + p[2] + p[3]

#Regla para manejar errores
def p_error(p):
    global col,fil,error_sintaxis
    if p:
        line_start = p.lexer.lexdata.rfind('\n', 0, p.lexpos) + 1
        col = (p.lexpos - line_start) + 1
        fil = p.lineno
        error_sintaxis = f"Error de sintaxis: Se detectó un error en la Línea {fil} columna {col}"    
    else:
        error_sintaxis = "Error de sintaxis: Fin de archivo inesperado"
    #print(error_sintaxis)
    #print("token incorrecto", p)
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
        
        self.btn_sintactico = ttk.Button(frame_botones, text="📝 Análisis Sintáctico", command=self.estado_analisis_sintactico, width=25)
        self.btn_sintactico.pack(pady=7, ipady=7)
        
        self.btn_html = ttk.Button(frame_botones, text="💾 Guardar y abrir HTML", command=self.generar_html, width=25)
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
        
#    def buscar_archivo(self):
#        ruta = filedialog.askopenfilename(title="Seleccionar archivo de programa", filetypes=[("Archivos de texto", "*.txt", "*.smart"), ("Todos los archivos", "*.*")])
#        if ruta:
#            self.cargar_archivo(ruta)

    def buscar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de programa", 
            filetypes=[
                ("Archivos de programa (*.txt, *.smart)", "*.txt *.smart"), 
                ("Todos los archivos", "*.*")
            ]
        )
        if ruta:
            self.cargar_archivo(ruta)

    
    def cargar_archivo(self, ruta):
        global nombre_archivo
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
        global html,col,fil,error_sintaxis,error_lexer
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
            self.tab_sintactico.tag_config("error3", foreground="#ff4444", font=("Arial", 10))
            self.tab_sintactico.insert(tk.END,  "        El HTML puede derivarse incompleto o contener errores.\n", "error2")
            self.tab_sintactico.insert(tk.END,  "        ============================================\n", "error2")
            self.tab_sintactico.insert(tk.END, "        Detalle:\n", "error3")
            if error_sintaxis: 
                self.tab_sintactico.insert(tk.END, f"        {error_sintaxis}.\n", "error3")
            if error_lexer: 
                self.tab_sintactico.insert(tk.END, f"        {error_lexer}.\n", "error3")

    def generar_html(self):
        global html, nombre_archivo
        texto = self.editor.get(1.0, tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "No hay código para analizar")
            return

        lexer.lineno = 1; lexer.input(texto.upper()) # para resetear posición del lexer
        
        self.notebook.select(self.tab_sintactico)
        self.tab_sintactico.delete(1.0, tk.END)
        self.root.update()
        
        cabecera_html()

        try: 
           parser.parse(texto.upper(), lexer=lexer)
        except Exception:
            pass #para continuar por más que se detectó un error (y permitir ejecutar el html igual más abajo)

        final_html()
        
        ruta_script_actual = os.path.dirname(os.path.abspath(__file__))
        
        carpeta_destino = os.path.abspath(os.path.join(ruta_script_actual, "..", "HTMLs"))
        
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
        
        if not nombre_archivo:
            nombre_archivo = 'sin_nombre.txt'

        nombre_archivo = nombre_archivo.replace('.smart', '.html')
        ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)
        
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(html)
        
        webbrowser.open("file://" + ruta_archivo)

#====================================================================#
#=============================== MAIN ===============================#
#====================================================================#
  
root = tk.Tk()
app = InterfazAnalizador(root)
root.mainloop()

#detalles:
#1-Al derivar el HTML con errores sintácticos, al encontrar un error, se derivarárn todos bloques que estén
#antes y después del bloque del error, es decir que si el error está en la condición de un bloque, el bloque entero no se deriva,
#pero sí aquellos que estén antes, esto incluye para asignaciones, condiciones y bucles. 

#2-importante, siempre que haya un error en el programa se mostrará el mensaje de que hay un error sintáctico (en la interfaz, en rojo)
#independientemente de si es o no realmente un error de sintáxis, puede ser un error en el código. Posiblemente corregir

#----------------------------------------#

#preguntas y cosas para hacer:
#1-a qué se refiere con estado de sensores? si solo se usan para condiciones.

#2-es correcta nuestra manera de ir construyendo el HTML? se va construyendo a medida que se alcanzan las reglas, es decir
#en cada regla, se va construyendo concatenándose cada parte del html.

#3-op_comparador y op_comparador están juntos, preguntar al profe por alguna solución, dado que puede permitir
#sensor_temp >= TRUE, pero es porque una regla está contenida dentro de otra, sin importar el orden en que estén definidas,
#si se encuentran los ejemplos correctos que contrasten, por más que estén bien escritos sintácticamente, van a dar error.
#En general, esto pasa para todas las reglas que comparten elementos y no se diferencian, es decir, reglas que están contenidas
#en otras.
#(solución): hacer dos reglas aparte comp_basica (==|!=), comp_extendida (>|>=|<|<=), los comp_bool solo usan comp_básica, mientras
#que los no booleanos, usan comp_bool, y comp_extendida.

#4-para los sensores, es un cuadro donde se agrupan todos los sensores, o es un cuadrito por sensor? 

#5-Agregar todo lo pedido en la consigna en cuanto al HTML (cosas para los sensores, etc), y agregar cantidad total de
#sensores y actuadores en el HTML.

#6-Quitar partes redundantes e innecesarias del código y ordenarlo

#7-POR ALGUNA RAZÓN NO ANDA CUANDO SE COMPARA CON SENSOR_TEMP
#después de mucho tiempo buscando se solucionó pero hay que simplificar la función de las condiciones del sensor.
