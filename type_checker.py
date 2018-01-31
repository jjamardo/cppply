
INT      = "int"
FLOAT    = "float"
BOOL     = "bool"
STR      = "str"
REGISTER = "register"
VECTOR   = "vector"
NONE     = "None"

registers = {}
types = {}


## Statement ##


def chk_binary_cmp_expr(p):
    binary_cmp_cond("binary cmp", p)
    p[0].type = BOOL


def chk_add_binary_l3_expr(p):
    p[0].type = binary_str_or_num_cond("binary add", p)


def chk_binary_num_expr(p):
    p[0].type = binary_num_cond("binary num", p)


def chk_binary_bool_expr(p):
    binary_bool_cond("binary bool", p)
    p[0].type = BOOL


def chk_assign_num_vector_expr(p):
    binary_vec_assign_cond("assign num", p)


def chk_assign_num_id_expr(p):
    binary_str_or_num_cond("assign num", p)


def chk_initializer_vector_expr(p):
    value = p[1].formatted_code.rsplit('[', 1)[0]
    if (not value in types):
        types[value] = vector_of(p[3].type)
    else:
        elems_type = vector_type(types[value])
        if (not elems_type == p[3].type):
            if (not is_numeric(elems_type) and is_numeric(p[3].type)):
                raise TypeError("El vector ya tenia tipo " + elems_type + " y se quiere asignar algo de tipo " + p[3].type + " - linea: " + str(p.lineno(2)))
    p[0].type = vector_of(p[3].type)


def chk_initializer_id_expr(p):
    if (p[3].type == REGISTER):
        if not p[3].register_fields:
            raise TypeError("Se crea registro pero la lista de campos esta vacia! - linea: " + str(p.lineno(2)))
        else:
            registers[p[1].formatted_code] = p[3].register_fields
            # TODO: Esto con el diccionario de registros creeria que no es necesario.
            for key in p[3].register_fields.keys():
                types[p[1].formatted_code + "." + key] = p[3].register_fields[key]
    if (p[3].type == vector_of(REGISTER)):
        if not p[3].register_fields:
            raise TypeError("Se crea registro pero la lista de campos esta vacia! - linea: " + str(p.lineno(2)))
        else:
            registers[p[1].formatted_code] = p[3].register_fields
    types[p[1].formatted_code] = p[3].type
    p[0].formatted_code = p[1].formatted_code + " = " + p[3].formatted_code


def chk_prefix_unary_expr(p):
    unary_num_cond("unary prefix num", p, 2)
    p[0].type = p[2].type


def chk_postfix_unary_expr(p):
    unary_num_cond("unary postfix num", p, 1)
    p[0].type = p[1].type


def chk_not_unary_expr(p):
    unary_bool_cond("unary not", p, 2)
    p[0].type = BOOL

    
def chk_parenthesized_expr(p):
    p[0].type = p[2].type


def chk_vector_access_expr(p):
    if (not p[3].type == INT):
        raise TypeError("Se espera un int como indice del vector - linea: " + str(p.lineno(2)))
    # Assumption: Todo la expresion toma el tipo del identifier del vector.
    if (p[1].type and is_vector(p[1].type)):
        vec_type = vector_type(p[1].type)
    elif (p[1].formatted_code in types):
        if (not is_vector(types[p[1].formatted_code])):
            print(types)
            raise TypeError("Error, acceso a variable " + p[1].formatted_code + " como vector, pero es del tipo " + types[p[1].formatted_code] + " - linea:" + str(p.lineno(2)))
        vec_type = vector_type(types[p[1].formatted_code])
    else:
        vec_type = NONE #Todavia no lo sabemos
    regs = {}
    if (vec_type == REGISTER):
            if (p[1].formatted_code in registers):
                regs = registers[p[1].formatted_code]
            else:
                raise TypeError("Acceso a vector ya inicializado de registros pero no se encontraron los registros!" + str(p.lineno(2)))
    p[0].type = vec_type
    p[0].register_fields = regs


def chk_vector_declaration_expr(p):
    p[0].type = vector_of(p[2].type)
    p[0].register_fields = p[2].register_fields


def chk_vector_index_expr(p):
    if (not p[3].type == INT):
        raise TypeError("El indice del vector debe ser entero! - linea: " + str(p.lineno(2)))
    p[0].type = vector_type(p[1].type)
    p[0].register_fields = p[1].register_fields


def chk_register_access_expr(p):
    register_access = p[1].formatted_code + "." + p[3];
    # HACK: Si es un objeto anonimo y le pedimos un registro no existe en types, porque no se
    # asigno, entonces lo creamos en el momento.
    if (p[1].type == REGISTER):
        if not p[1].register_fields:
            raise TypeError("Se accede a registro pero la lista de campos esta vacia! - linea: " + str(p.lineno(2)))
        else:
            for key in p[1].register_fields.keys():
                types[p[1].formatted_code + "." + key] = p[1].register_fields[key]
    if (not register_access in types):
        raise TypeError("No existe el tipo del registro que se quiere acceder")
    p[0].type = types[register_access]


def chk_anonymous_obj_ctor_expr(p):
    p[0].type = REGISTER
    p[0].register_fields = p[2].register_fields


def chk_ternary_condition_expr(p):
    equivalent_types("ternary condition", p, 3, 5)
    if (not p[1].type == BOOL):
        raise TypeError("La condicion de la expresion ternaria debe ser booleana - linea: " + str(p.lineno(2)))
    p[0].type = p[3].type


def chk_identifier_expr(p): 
    if (p[1] in types):
        type = types[p[1]]
    else:
        type = NONE
    p[0].type = type


def chk_vector_multiple_elements(p):
    type = equivalent_types("vector elements", p, 1, 3)
    if (type == REGISTER):
        if (not p[1].register_fields):
            if (not p[1].formatted_code in registers):
                TypeError("Acceso a registro vacio! - linea: " + str(p.lineno(2)))
            else:
                regs1 = registers[p[1].formatted_code]
        else:
            regs1 = p[1].register_fields

        if (not p[3].register_fields):
            if (not p[3].formatted_code in registers):
                TypeError("Acceso a registro vacio! - linea: " + str(p.lineno(2)))
            else:
                regs2 = registers[p[3].formatted_code]
        else:
            regs2 = p[3].register_fields

        if (cmp_register(regs1, regs2) == -1):
            raise TypeError("Registro con distinto tipo! - linea: " + str(p.lineno(2)))
    p[0].type = type
    p[0].register_fields = p[1].register_fields


def chk_register_multiple_decl_elems(p):
    if not p[5].register_fields:
        reg_dict = {p[1]:p[3].type}
    else:
        reg_dict = p[5].register_fields
        reg_dict[p[1]] = p[3].type
    p[0].register_fields = reg_dict


def chk_register_single_decl_elems(p):
    p[0].register_fields = {p[1]:p[3].type}


## Invocations ## 

def chk_multiplicacion_escalar_3_params(p):
    if (not (p[3].type == vector_of(INT) or p[3].type == vector_of(FLOAT))):
        raise TypeError("multiplicacion_escalar: El vector de entrada debe ser numerico! - linea: " + str(p.lineno(2)))
    if (not is_numeric(p[5].type)):
        raise TypeError("multiplicacion_escalar: El escalar debe ser numerico! - linea: " + str(p.lineno(2)))
    if (not p[7].type == BOOL):
        raise TypeError("multiplicacion_escalar: Tercer parametro debe ser bool! - linea: " + str(p.lineno(2)))
    p[0].type = vector_of(FLOAT)


def chk_multiplicacion_escalar_2_params(p):
    if (not (p[3].type == vector_of(INT) or p[3].type == vector_of(FLOAT))):
        raise TypeError("multiplicacion_escalar: El vector de entrada debe ser numerico! - linea: " + str(p.lineno(2)))
    if (not is_numeric(p[5].type)):
        raise TypeError("multiplicacion_escalar: El escalar debe ser numerico! - linea: " + str(p.lineno(2)))
    p[0].type = vector_of(FLOAT)


def chk_capitalizar(p):
    if (not p[3].type == STR):
        raise TypeError("capitalizar: El parametro solo puede ser str! - linea: " + str(p.lineno(2)))
    p[0].type = STR


def chk_colineales(p):
    if (not (p[3].type == vector_of(INT) or p[3].type == vector_of(FLOAT))):
        raise TypeError("colineales: El primer vector debe ser numerico! - linea: " + str(p.lineno(2)))
    if (not (p[3].type == vector_of(INT) or p[3].type == vector_of(FLOAT))):
        raise TypeError("colineales: El segundo vector debe ser numerico! - linea: " + str(p.lineno(2)))
    p[0].type = BOOL


def chk_print(p):
    p[0].formatted_code = p[1] + "(" + p[3].formatted_code + ")"


def chk_length(p):
    if (not (is_vector(p[3].type) or p[3].type == STR)):
        raise TypeError("length: El parametro debe ser un vector o un str! - linea: " + str(p.lineno(2)))
    p[0].type = INT


## Terms ##

def chk_int_term(p):
    p[0].type = INT


def chk_float_term(p):
    p[0].type = FLOAT


def chk_string_term(p):
    p[0].type = STR


def chk_boolean_term(p):
    p[0].type = BOOL


## Auxiliares ##

def is_numeric(type):
    return (type == INT or type == FLOAT)


def cmp_register(register1, register2):
    for key in register1.keys():
        if (not key in register2):
            return -1
        if (not register1[key] == register2[key]):
            return -1
    for key in register2.keys():
        if (not key in register1):
            return -1
        if (not register1[key] == register2[key]):
            return -1
    return 0


def binary_num_cond(op, p):
    # Utilizada en las expresiones binarias numericas.
    if (not is_numeric(p[1].type)):
        raise TypeError(op + ": " + "Operando derecho debe ser numerico pero es " + p[1].type + " - linea: " + str(p.lineno(2)))
    if (not is_numeric(p[3].type)):
        raise TypeError(op + ": " + "Operando izquierdo debe ser numerico pero es " + p[3].type + " - linea: " + str(p.lineno(2)))
    return binary_result_type(p[1].type, p[3].type)


def binary_result_type(type1, type2):
    if (type1 == FLOAT or type2 == FLOAT):
        type = FLOAT
    else:
        type = INT
    return type


def binary_str_or_num_cond(op, p):
    # Utilizada en las expresiones binarias + y +=.
    if (is_numeric(p[1].type)):
        if(is_numeric(p[3].type)):
            bin_type = binary_result_type(p[1].type, p[3].type)
        else:
            raise TypeError(op + ": " + "Operando derecho es numerico, operando izquierdo debe ser numerico pero es " + p[3].type + " - linea: " + str(p.lineno(2)))
    elif (p[1].type == STR):
        if (p[3].type == STR):
            bin_type = p[3].type
        else:
            raise TypeError(op + ": " + "Operando derecho es str, operando izquierdo debe ser str pero es " + p[3].type + " - linea: " + str(p.lineno(2)))
    else:
        raise TypeError(op + ": " + "Error, operando derecho con tipo " + p[1].type + " no permitido - linea: " + str(p.lineno(2)))
    return bin_type


def binary_bool_cond(op, p):
    # Utilizada en las expresiones binarias booleanas.
    if (not p[1].type == BOOL):
        raise TypeError(op + ": " + "Operando derecho debe ser bool pero es " + p[1].type + " - linea: " + str(p.lineno(2)))
    if (not p[3].type == BOOL):
        raise TypeError(op + ": " + "Operando izquierdo debe ser bool pero es " + p[3].type + " - linea: " + str(p.lineno(2)))


def binary_cmp_cond(op, p):
    # Utilizada en las operacion binarias de comparacion.
    if (not p[1].type == p[3].type):
        raise TypeError(op + ": " + "Operandos de distinto tipo, derecho " + p[1].type + ", izquierdo " + p[3].type + " - linea: " + str(p.lineno(2)))


def equivalent_types(op, p, index1, index2):
    # Compara que dos elementos sean del mismo tipo, si no lo son, prueba si son numericos.
    if (p[index1].type == p[index2].type):
        type = p[index1].type
    else:
        if (is_numeric(p[index1].type) and is_numeric(p[index2].type)):
            type = binary_result_type(p[index1].type, p[index2].type)
        else:
            raise TypeError("Los elementos deben ser del mismo tipo! - linea: " + str(p.lineno(2)))
    return type

        
def unary_num_cond(op, p, index):
    # Utilizada en operaciones unarias numericas.
    if (not is_numeric(p[index].type)):
        raise TypeError(op + ": La expresion debe ser tipo numerico pero es " + p[index].type + " - linea: " + str(p.lineno(index)))


def unary_bool_cond(op, p, index):
    # Utilizada en NOT.
    if (not p[index].type == BOOL):
        raise TypeError(op + ": La expresion debe ser tipo bool pero es " + p[index].type + " - linea: " + str(p.lineno(index)))


def binary_vec_assign_cond(op, p):
    value = p[1].formatted_code.rsplit('[', 1)[0]
    if (not value in types):
        raise TypeError(op + ": " + "Acceso a vector pero no tiene tipo - linea: " + str(p.lineno(2)))
    if (not is_numeric(vector_type(types[value]))):
        raise TypeError(op + ": " + "El vector debe contener tipo numerico pero es " + vector_type(types[value]) + " - linea: " + str(p.lineno(2)))
    if (not is_numeric(p[3].type)):
        raise TypeError(op + ": " + "El operando izquierdo debe ser numerico pero es " + p[3].type + " - linea: " + str(p.lineno(2)))


def vector_of(type):
    # Arma un vector de un tipo
    return VECTOR + "<" + type + ">"


def vector_type(tvector):
    # Extrae el tipo del vector
    type = tvector.split('<',1)[1]
    type = type.rsplit('>',1)[0]
    return type


def is_vector(type):
    if "vector" not in type:
        return False
    else:
        return True