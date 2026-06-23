import ply.yacc as yacc
import lexer_rev

tokens = lexer_rev.tokens

# ==============================================================================
# 1. REGLAS DE ALTO NIVEL (La estructura global del script)
# ==============================================================================

def p_programa(p):
    '''programa : instrucciones'''
    print("\n[PARSER] ¡Análisis sintáctico finalizado con ÉXITO!")
    p[0] = p[1]

def p_instrucciones_lista(p):
    '''instrucciones : instrucciones instruccion
                     | instruccion'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_instruccion(p):
    '''instruccion : bloque_when
                   | bloque_if
                   | bloque_every
                   | asignacion'''
    p[0] = p[1]


# ==============================================================================
# 2. BLOQUES DE CONTROL Y EVENTOS (WHEN, IF, EVERY)
# ==============================================================================

def p_bloque_when(p):
    '''bloque_when : WHEN condicion DO instrucciones END'''
    p[0] = ('BLOQUE_WHEN', p[2], p[4])
    print(f"-> Parser reconoció un bloque de evento: WHEN [condicion] DO...")

def p_bloque_if(p):
    '''bloque_if : IF condicion THEN instrucciones END
                 | IF condicion THEN instrucciones ELSE instrucciones END'''
    if len(p) == 6:
        p[0] = ('BLOQUE_IF', p[2], p[4])
    else:
        p[0] = ('BLOQUE_IF_ELSE', p[2], p[4], p[6])
    print(f"-> Parser reconoció una estructura condicional IF")

def p_bloque_every(p):
    '''bloque_every : EVERY TIEMPO DO instrucciones END'''
    p[0] = ('BLOQUE_EVERY', p[2], p[4])
    print(f"-> Parser reconoció un bucle temporal: EVERY {p[2]} DO...")


# ==============================================================================
# 3. REGLAS DE CONDICIONES Y EXPRESIONES LÓGICAS
# ==============================================================================

def p_condicion_logica(p):
    '''condicion : condicion OP_LOGICO condicion
                 | OP_NEGACION condicion'''
    if len(p) == 4:
        p[0] = ('EXP_LOGICA', p[2], p[1], p[3])
    else:
        p[0] = ('NEGACION', p[2])

def p_condicion_comparacion(p):
    '''condicion : expresion_sensor OP_COMPARADOR valor_comparable'''
    p[0] = ('COMPARACION', p[1], p[2], p[3])

def p_condicion_parentesis(p):
    # Por si en el TPI les piden o quieren soportar condiciones agrupadas: (sensor_luz < 200LUX)
    # Si no usan paréntesis en su gramática, podés comentar esta regla.
    '''condicion : ID condicion ID'''
    # Nota: Si agregás tokens de paréntesis, cambias los 'ID' por 'PAR_IZQ'/'PAR_DER'
    p[0] = p[2]


# ==============================================================================
# 4. REGLAS PARA MANEJAR SENSORES Y ACTUADORES (Lado izquierdo de las expresiones)
# ==============================================================================

def p_expresion_sensor(p):
    '''expresion_sensor : SENSOR_TEMPERATURA
                        | SENSOR_HUMEDAD
                        | SENSOR_LUZ
                        | SENSOR_MOVIMIENTO
                        | SENSOR_HUMO'''
    p[0] = ('SENSOR', p[1])

def p_dispositivo_con_id(p):
    '''dispositivo : id_actuador
                   | id_actuador GUION_BAJO ID'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        # Esto soporta estructuras de nombres compuestos como: foco_entrada, actuador_alarma_living
        p[0] = f"{p[1]}_{p[3]}"

def p_id_actuador(p):
    '''id_actuador : ACTUADOR_FOCO
                   | ACTUADOR_AIRE
                   | ACTUADOR_PERSIANA
                   | ACTUADOR_CERRADURA
                   | ACTUADOR_RELOJ
                   | ACTUADOR_ALTAVOZ
                   | ACTUADOR_ALARMA'''
    p[0] = p[1]


# ==============================================================================
# 5. REGLAS DE ASIGNACIÓN Y ATRIBUTOS (El núcleo de la acción domótica)
# ==============================================================================

def p_asignacion(p):
    '''asignacion : dispositivo atributo ASIGNACION valor_asignable'''
    p[0] = ('ASIGNACION', p[1], p[2], p[4])
    print(f"-> Parser reconoció asignación sobre: {p[1]} -> Atributo: {p[2]}")

def p_atributo(p):
    '''atributo : ATRIBUTOS_FOCO_BRILLO
                | ATRIBUTOS_FOCO_COLOR
                | ATRIBUTOS_AIRE_MODO
                | ATRIBUTOS_AIRE_TEMP_ACT
                | ATRIBUTOS_AIRE_TEMP_OBJ
                | ATRIBUTOS_PERSIANA
                | ATRIBUTOS_RELOJ_HORA
                | ATRIBUTOS_RELOJ_FECHA
                | ATRIBUTOS_ALTAVOZ_VOLUMEN
                | ATRIBUTOS_ALTAVOZ_MUTE
                | ATRIBUTOS_ALTAVOZ_MENSAJE
                | ATRIBUTOS_ALTAVOZ_EMAIL
                | ATRIBUTOS_ALARMA
                | ATRIBUTO_ESTADO'''
    p[0] = p[1]


# ==============================================================================
# 6. HOJAS DEL ÁRBOL: VALORES COMPATIBLES (Sintaxis de magnitudes)
# ==============================================================================

def p_valor_comparable(p):
    '''valor_comparable : ILUMINANCIA
                        | VALOR_TEMPERATURA
                        | PERCENT
                        | HORA
                        | DATE
                        | BOOL_DISPOSITIVO
                        | BOOL_ACTUADOR'''
    p[0] = p[1]

def p_valor_asignable(p):
    '''valor_asignable : valor_comparable
                       | TEXTO
                       | DISCRETO
                       | NOMBRE
                       | EMAIL'''
    p[0] = p[1]


# ==============================================================================
# 7. MANEJO DE ERRORES SINTÁCTICOS
# ==============================================================================
def p_error(p):
    if p:
        columna = lexer_rev.find_column(p.lexer.lexdata, p)
        texto_fuente = getattr(p.lexer, 'datos_originales', p.lexer.lexdata)
        palabra_original = texto_fuente[p.lexpos : p.lexpos + len(str(p.value))]
        
        print(f"[ERROR SINTÁCTICO] No se esperaba '{palabra_original}' (Tipo: {p.type}) "
              f"en la Línea {p.lineno}, Columna {columna}")
    else:
        print("[ERROR SINTÁCTICO] Fin de archivo inesperado (EOF). Revisá las llaves o cierres 'END'.")

# Construimos el objeto parser definitivo
parser = yacc.yacc()