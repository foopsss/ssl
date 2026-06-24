import ply.yacc as yacc
import lexer_rev

tokens= lexer_rev.tokens


#Reglas principales que manejan la estructura del programa (smart-home)

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

#ASIGNACIONES (ESCRITURA DE ACTUADORES)
def p_asignaciones(p):
    '''asignacion : ACTUADOR_FOCO identificador atributos_esc_foco
                  | ACTUADOR_FOCO atributos_esc_foco
                  | AIRE identificador atributos_esc_aire
                  | AIRE atributos_esc_aire
                  | PERSIANA identificador atributos_esc_persiana
                  | PERSIANA atributos_esc_persiana
                  | CERRADURA identificador atributos_esc_cerradura
                  | CERRADURA atributos_esc_cerradura
                  | ALTAVOZ identificador atributos_esc_altavoz
                  | ALTAVOZ atributos_esc_altavoz
                  | ALARMA identificador atributos_esc_alarma
                  | ALARMA atributos_esc_alarma'''
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
                 | SENSOR_TEMPERATURA identificador OP_COMPARADOR VALOR_TEMP_ACT contcondicion
                 | SENSOR_TEMPERATURA identificador OP_COMPARADOR VALOR_TEMP_ACT
                 | SENSOR_TEMPERATURA OP_COMPARADOR VALOR_TEMP_ACT contcondicion
                 | SENSOR_TEMPERATURA OP_COMPARADOR VALOR_TEMP_ACT'''

def p_condicion_humedad(p):
    ''' condicion : OP_NEGACION SENSOR_HUMEDAD identificador OP_COMPARADOR PERCENT contcondicion
                  | OP_NEGACION SENSOR_HUMEDAD OP_COMPARADOR PERCENT contcondicion
                  | OP_NEGACION SENSOR_HUMEDAD OP_COMPARADOR PERCENT
                  | SENSOR_HUMEDAD identificador OP_COMPARADOR PERCENT contcondicion
                  | SENSOR_HUMEDAD identificador OP_COMPARADOR PERCENT
                  | SENSOR_HUMEDAD OP_COMPARADOR PERCENT contcondicion
                  | SENSOR_HUMEDAD OP_COMPARADOR PERCENT'''

def p_condicion_luz(p):
    ''' condicion : OP_NEGACION SENSOR_LUZ identificador OP_COMPARADOR iluminancia contcondicion
                  | OP_NEGACION SENSOR_LUZ OP_COMPARADOR iluminancia contcondicion
                  | OP_NEGACION SENSOR_LUZ OP_COMPARADOR iluminancia
                  | OP_NEGACION SENSOR_LUZ OP_COMPARADOR iluminancia
                  | SENSOR_LUZ identificador OP_COMPARADOR iluminancia contcondicion
                  | SENSOR_LUZ identificador OP_COMPARADOR iluminancia
                  | SENSOR_LUZ OP_COMPARADOR iluminancia contcondicion
                  | SENSOR_LUZ OP_COMPARADOR iluminancia'''

def p_condicion_movimiento(p):
    ''' condicion : OP_NEGACION SENSOR_MOVIMIENTO identificador OP_COMPARADOR_BOOL bool_dispositivo contcondicion
                  | OP_NEGACION SENSOR_MOVIMIENTO identificador OP_COMPARADOR_BOOL bool_dispositivo
                  | OP_NEGACION SENSOR_MOVIMIENTO OP_COMPARADOR_BOOL bool_dispositivo contcondicion
                  | OP_NEGACION SENSOR_MOVIMIENTO OP_COMPARADOR_BOOL bool_dispositivo
                  | SENSOR_MOVIMIENTO identificador OP_COMPARADOR_BOOL bool_dispositivo contcondicion
                  | SENSOR_MOVIMIENTO identificador OP_COMPARADOR_BOOL bool_dispositivo
                  | SENSOR_MOVIMIENTO OP_COMPARADOR_BOOL bool_dispositivo contcondicion
                  | SENSOR_MOVIMIENTO OP_COMPARADOR_BOOL bool_dispositivo'''

def p_condicion_humo(p):
    '''condicion : OP_NEGACION SENSOR_HUMO identificador OP_COMPARADOR_BOOL bool_dispositivo contcondicion
                 | OP_NEGACION SENSOR_HUMO identificador OP_COMPARADOR_BOOL bool_dispositivo
                 | OP_NEGACION SENSOR_HUMO OP_COMPARADOR_BOOL bool_dispositivo contcondicion
                 | OP_NEGACION SENSOR_HUMO OP_COMPARADOR_BOOL bool_dispositivo
                 | SENSOR_HUMO identificador OP_COMPARADOR_BOOL bool_dispositivo contcondicion
                 | SENSOR_HUMO identificador OP_COMPARADOR_BOOL bool_dispositivo
                 | SENSOR_HUMO OP_COMPARADOR_BOOL bool_dispositivo contcondicion
                 | SENSOR_HUMO OP_COMPARADOR_BOOL bool_dispositivo'''

def p_condicion_foco(p):
    '''condicion : OP_NEGACION ACTUADOR_FOCO identificador atributos_lec_foco contcondicion
                 | OP_NEGACION ACTUADOR_FOCO identificador atributos_lec_foco
                 | OP_NEGACION ACTUADOR_FOCO atributos_lec_foco contcondicion
                 | OP_NEGACION ACTUADOR_FOCO atributos_lec_foco
                 | ACTUADOR_FOCO identificador atributos_lec_foco contcondicion
                 | ACTUADOR_FOCO identificador atributos_lec_foco
                 | ACTUADOR_FOCO atributos_lec_foco contcondicion
                 | ACTUADOR_FOCO atributos_lec_foco'''



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






#anotaciones:

#(1)
#todos los no terminales van en minúsculas.
#todos los terminales en mayúsculas

#(2)
#p[n] se lee así:
#p[0] actual
#[p[1]] tupla convertida en lista
# + [p2] se concatena con la siguiente lista que vendrá (cuando se obtenga el resultado de la recursión por derecha)

#(3)
#recordar que p[0] cuenta como un elemento en la regla también, es decir
#en p[0] + p[1] + p[2] hay 3 elementos.

#(4)
#para el caso de esta regla:
#def p_identificador(p):
#    '''identificador : GUION_BAJO ID'''
#    p[0] = f"{p[1]}{p[2]}"
#dado que se se derivan directamente en caracteres, se los concatena así: p[0] = f"{p[1]}{p[2]}"

#(5)
#todas las acciones compuestas llevan etiquetas (bucles, condiciones, asignaciones, etc.)

#(6)
#cuando se tiene la misma etiqueta, se tiene que guardar en p[0] una lista con la misma longitud para ambos "caminos" en la condición (if y else)

#Cosas para hacer:
#-Controlar que en las reglas se enuncie los tokens especificados en el lexer
tuki