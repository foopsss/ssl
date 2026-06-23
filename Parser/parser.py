import ply.yacc as yacc
import lexer_rev

tokens= lexer_rev.tokens


#Reglas principales que manejan la estructura del programa (smart-home)

#Bloques y acciones
def p_programa(p):
    '''sigma : accion'''
    print("Análisis sintáctico terminado exitosamente") #al terminar imprime
    p[0] = p[1]

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

def p_ciclos(p):
    '''ciclo : WHEN condicion DO accion END
             | EVERY tiempo DO accion END'''
    if p[1] == 'WHEN':
        p[0] = ('CICLO_WHEN', p[2], p[4])
    else:
        p[0] = ('CICLO_EVERY', p[2], p[4])

def p_condicional(p):
    '''condicional : IF condicion THEN accion END
                   | IF condicion THEN accion ELSE accion END'''
    if len(p) == 6:
        p[0] = ('CONDICIONAL_SIMPLE', p[2], p[4])
    else:
        p[0] = ('CONDICIONAL_ALTERNATIVO', p[2], p[4], p[6])

def p_identificador(p):
    '''identificador : GUION_BAJO ID'''
    p[0] = p[1] + p[2]


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

def p_atributos_escritura_foco(p):
    '''atributos_esc_foco : ATRIBUTO_ESTADO ASIGNACION BOOL_ACTUADOR
                          | ATRIBUTOS_FOCO_BRILLO ASIGNACION PERCENT
                          | ATRIBUTOS_FOCO_COLOR ASIGNACION NOMBRE'''
    p[0] = p[1] + p[2] + p[3]

def p_atributos_escritura_aire(p):
    '''atributos_esc_aire : ATRIBUTO_ESTADO ASIGNACION BOOL_ACTUADOR
                          | ATRIBUTOS_AIRE_MODO ASIGNACION DISCRETO
                          | 
                          |
                          |
    
    '''
def p_atributos_escritura_persiana(p):
def p_atributos_escritura_cerradura(p):
def p_atributos_escritura_altavoz(p):
def p_atributos_escritura_alarma(p):













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