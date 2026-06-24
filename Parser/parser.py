# Importar lexer desde lexer_rev para evitar duplicación
from Parser.lexer_rev import tokens, reservado, lexer
from ply import yacc



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
             | EVERY tiempo DO accion END'''
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

#TIEMPO (para ciclos EVERY)
def p_tiempo(p):
    '''tiempo : TIEMPO'''
    p[0] = p[1]

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


# Crear instancia del parser
parser = yacc.yacc(debug=False, write_tables=False)

#Cosas para hacer:
#1-Agregar traductor a HTML
#2-Agregar Main para probar si deriva el ejemplo ejecutando el parser 
