# coding=utf-8

# Palabras reservadas
# "..
# Se cargan las palabras reservadas como propone la documentacion.
# To handle reserved words, you should write a single rule to match an identifier and do a special
# name lookup in a function.
# .."
# "..
# This approach greatly reduces the number of regular expression rules and is likely to make things
# a little faster.
# .."
reserved = {
    'begin'                 : 'BEGIN',
    'end'                   : 'END',
    'while'                 : 'WHILE',
    'for'                   : 'FOR',
    'if'                    : 'IF',
    'else'                  : 'ELSE',
    'do'                    : 'DO',
    'res'                   : 'RES',
    'return'                : 'RETURN',
    'AND'                   : 'AND',
    'OR'                    : 'OR',
    'NOT'                   : 'NOT',
    'multiplicacionEscalar' : 'MULESCALAR',
    'capitalizar'           : 'CAPITALIZAR',
    'colineales'            : 'COLINEALES',
    'print'                 : 'PRINT',
    'length'                : 'LENGTH',
}

# Literales
# Se carga la tabla de literales como propne la documentacion (+= tiene precedencia sobre +).
# "..
# A literal character is simply a single character that is returned "as is" when encountered by the
# lexer. Literals are checked after all of the defined regular expression rules. Thus, if a rule
# starts with one of the literal characters, it will always take precedence. When a literal token
# is returned, both its type and value attributes are set to the character itself. For example, '+'.
# .."
literals = [
    '{',
    '}',
    '(',
    ')',
    '[',
    ']',
    '-',
    '*',
    '^',
    '%',
    '/',
    '+',
    '<',
    '>',
    '=',
    '?',
    ':',
    ';',
    '.',
    '!',
    ','
]

# Tokens
tokens = [
    # Tipos.
    'BOOL',
    'FLOAT',
    'INT',
    'STRING',
    # Identificadores.
    'ID',
    # Operadores de asignacion.
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    # Operadores de comparacion.
    'EQ',
    'NOTEQ',
    # Operadores Matematicos.
    'INC',
    'DEC',
    # Comentarios
    'COMMENT',
] + list(reserved.values())

# Tipos.
def t_BOOL(t): 
    r"false | true"
    return t

def t_FLOAT(t):
    r"\d+\.\d+"
    return t

def t_INT(t):
    r"\d+"
    return t

t_STRING = r'(\'|\")(.+?)?(\'|\")'

# Identificadores.
# t_ID se encuentra luego de t_BOOL para que true y false los tome como BOOL
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Operadores de asignacion.
t_ADDASSIGN = r"\+="
t_SUBASSIGN = r"-="
t_MULASSIGN = r"\*="
t_DIVASSIGN = r"/="

# Operadores de comparacion.
t_EQ = r"=="
t_NOTEQ = r"!="

# Operadores Matematicos.
t_INC = r"\+\+"
t_DEC = r"--"

# Se ignoran los espacios y tabs.
t_ignore  = ' \t'

# Los comentarios se retornan como esta.
def t_COMMENT(t):
    r'\#.*'
    return t

# Se pasa por alto si hay un caracter ilegal.
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    print("Line number '%s'" % t.lexer.lineno)
    t.lexer.skip(1)

# Para definir los numeros de linea.
# By default, lex.py knows nothing about line numbers. This is because lex.py doesn't know anything
# about what constitutes a "line" of input (e.g., the newline character or even if the input is
# textual data). To update this information, you need to write a special rule. In the example, the
# t_newline() rule shows how to do this.
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)