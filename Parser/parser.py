from ply import lex, yacc

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
    'VALOR_TEMP_OBJ',
    'VALOR_TEMP_ACT',
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
def t_VALOR_TEMP_OBJ(t): r'(1[6-9]|2[0-9]|30)°C'; return t
def t_VALOR_TEMP_ACT(t): r'(-10|-[1-9]|[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|50)°C'; return t
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
                          | ATRIBUTOS_AIRE_TEMP_OBJ ASIGNACION VALOR_TEMP_OBJ'''
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
    '''condicion : OP_NEGACION SENSOR_TEMPERATURA identificador OP_COMPARADOR VALOR_TEMP_ACT contcondicion
                 | OP_NEGACION SENSOR_TEMPERATURA identificador OP_COMPARADOR VALOR_TEMP_ACT
                 | OP_NEGACION SENSOR_TEMPERATURA OP_COMPARADOR VALOR_TEMP_ACT contcondicion
                 | OP_NEGACION SENSOR_TEMPERATURA OP_COMPARADOR VALOR_TEMP_ACT
                 | SENSOR_TEMPERATURA identificador OP_COMPARADOR VALOR_TEMP_ACT contcondicion
                 | SENSOR_TEMPERATURA identificador OP_COMPARADOR VALOR_TEMP_ACT
                 | SENSOR_TEMPERATURA OP_COMPARADOR VALOR_TEMP_ACT contcondicion
                 | SENSOR_TEMPERATURA OP_COMPARADOR VALOR_TEMP_ACT'''
    
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
                          | ATRIBUTOS_AIRE_TEMP_OBJ OP_COMPARADOR VALOR_TEMP_OBJ
                          | ATRIBUTOS_AIRE_TEMP_ACT OP_COMPARADOR VALOR_TEMP_ACT'''
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
        # p es el token donde falló la estructura de la gramática
        line_start = p.lexer.lexdata.rfind('\n', 0, p.lexpos) + 1
        columna = (p.lexpos - line_start) + 1
        
        print(f"Error de sintaxis: No se esperaba el token {p.value} en la Línea {p.lineno}, Columna {columna}.")
    else:
        # p es None si se llegó al final del archivo sin cerrar un bloque (ej. faltó un END)
        print("Error de sintaxis: Fin de archivo inesperado.")
    
    # Esto corta el parseo inmediatamente de forma limpia
    raise SyntaxError("Error de análisis sintáctico.")

#====================================================================#
#=============================== MAIN ===============================#
#====================================================================#



#parser = yacc.yacc()
parser = yacc.yacc(debug=False, write_tables=False)

archivo_prueba = "Ejemplos/PROGRAMA_SMARTHOME_TPI.txt"
    
try:
    with open(archivo_prueba, "r", encoding="utf-8") as archivo:
        datos = archivo.read()
        datos = datos.upper()
        
    resultado = parser.parse(datos)
    print("AST:")
    print(resultado)
        
except FileNotFoundError:
    print(f"Error: No se encontro {archivo_prueba}")
except Exception as e:
    print(f"Error: {e}")






#Cosas para hacer:
#1-Agregar traductor a HTML
#2-Agregar Main para probar si deriva el ejemplo ejecutando el parser 
#3-Crear instancia del parser. parser = yacc.yacc(debug=False, write_tables=False)
