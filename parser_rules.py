# coding=utf-8

from lexer_rules import tokens
from collections import deque

from type_checker import *
from code_formatter import *

## Atributos ##

class Node:
    def __init__(self):
        # Usados para el formateo.
        self.formatted_code = ""
        self.lineno = -1
        self.is_comment = False
        # Usados para el chequeo de tipos.
        self.type = NONE
        self.register_fields = {}


## Syntax ##

# El codigo puede tener statements y comentarios mezclados
def p_syntax(p):
    ''' syntax : block_body '''
    p[0] = p[1]


## Statement ##

def p_assign_stmt(p):
    ''' stmt : assign_expr ';' '''
    p[0] = Node()
    format_simple_stmt(p)


def p_inc_or_dec_stmt(p):
    ''' stmt : inc_or_dec_expr ';' '''
    p[0] = Node()
    format_simple_stmt(p)


def p_invocation_stmt(p):
    ''' stmt : invocation_expr ';' '''
    p[0] = Node()
    format_simple_stmt(p)


def p_return_stmt(p):
    ''' stmt : RETURN ';' '''
    p[0] = Node()
    format_return_stmt(p)


def p_begin_stmt(p):
    ''' stmt : BEGIN ';' '''
    p[0] = Node()
    format_begin_stmt(p)


def p_end_stmt(p):
    ''' stmt : END ';' '''
    p[0] = Node()
    format_end_stmt(p)


def p_do_while_stmt(p):
    ''' stmt : DO commented_body WHILE '(' condition_subexpr ')' ';' '''
    p[0] = Node()
    format_do_while_stmt(p)


def p_if_stmt(p):
    ''' stmt : IF '(' condition_subexpr ')' commented_body '''
    p[0] = Node()
    format_if_stmt(p)


def p_if_else_stmt(p):
    ''' stmt :  IF '(' condition_subexpr ')' commented_body ELSE commented_body '''
    p[0] = Node()
    format_if_else_stmt(p)


def p_while_stmt(p):
    ''' stmt : WHILE '(' condition_subexpr ')' commented_body '''
    p[0] = Node()
    format_while_stmt(p)


def p_for_stmt(p):
    ''' stmt : FOR '(' for_initializer for_condition_subexpr for_incrementor ')' commented_body '''
    p[0] = Node()
    format_for_stmt(p)


def p_block_stmt(p):
    ''' stmt : '{' block_body '}'  '''
    p[0] = Node()
    format_block_stmt(p)


def p_block_body_lines(p):
    ''' block_body : stmt block_body '''
    p[0] = Node()
    format_block_body_lines(p)


def p_block_body_stmt(p):
    ''' block_body : stmt '''
    p[0] = p[1]


def p_block_body_comments(p):
    ''' block_body : COMMENT block_body '''
    p[0] = Node()
    format_block_body_comments(p)


def p_block_body_comment(p):
    ''' block_body : COMMENT '''
    p[0] = Node()
    format_block_body_comment(p)


def p_commented_comments_body(p):
    ''' commented_body : comments stmt '''
    p[0] = Node()
    format_commented_comments_body(p)


def p_commented_stmt_body(p):
    ''' commented_body : stmt '''
    p[0] = p[1]


def p_multiple_comments(p):
    ''' comments : COMMENT comments '''
    p[0] = Node()
    format_multiple_comments(p)


def p_single_comment(p):
    ''' comments : COMMENT '''
    p[0] = Node()
    format_single_comment(p)


def p_for_initializer(p):
    ''' for_initializer : assign_expr ';' '''
    p[0] = Node()
    format_for_initializer(p)


def p_for_non_initializer(p):
    ''' for_initializer : ';' '''
    p[0] = Node()
    format_for_non_initializer(p)


def p_for_condition_subexpr(p):
    ''' for_condition_subexpr : condition_subexpr ';' '''
    p[0] = Node()
    format_for_condition_subexpr(p)


def p_for_assign_incrementor(p):
    ''' for_incrementor : assign_expr '''
    p[0] = p[1] 


def p_for_inc_dec_incrementor(p):
    ''' for_incrementor : inc_or_dec_expr '''
    p[0] = p[1]


def p_for_incrementor(p):
    ''' for_incrementor : '''
    p[0] = Node()


## Expressions ##

def p_eq_binary_l1_expr(p):
    ''' binary_expr : binary_expr EQ binary_l2_expr '''
    p[0] = Node()
    chk_binary_cmp_expr(p)
    format_eq_binary_l1_expr(p)


def p_noteq_binary_l1_expr(p):
    ''' binary_expr : binary_expr NOTEQ binary_l2_expr '''
    p[0] = Node()
    chk_binary_cmp_expr(p)
    format_noteq_binary_l1_expr(p)


def p_binary_l1_expr(p):
    ''' binary_expr : binary_l2_expr '''
    p[0] = p[1]


def p_leq_binary_l2_expr(p):
    ''' binary_l2_expr : binary_l2_expr '<' binary_l3_expr '''
    p[0] = Node()
    chk_binary_cmp_expr(p)
    format_leq_binary_l2_expr(p)

    
def p_gre_binary_l2_expr(p):
    ''' binary_l2_expr : binary_l2_expr '>' binary_l3_expr '''
    p[0] = Node()
    chk_binary_cmp_expr(p)
    format_gre_binary_l2_expr(p)

    
def p_binary_l2_expr(p):
    ''' binary_l2_expr : binary_l3_expr '''
    p[0] = p[1]


def p_add_binary_l3_expr(p):
    ''' binary_l3_expr : binary_l3_expr '+' binary_l4_expr '''
    p[0] = Node()
    chk_add_binary_l3_expr(p)
    format_add_binary_l3_expr(p)


def p_sub_binary_l3_expr(p):
    ''' binary_l3_expr : binary_l3_expr '-' binary_l4_expr '''
    p[0] = Node()
    chk_binary_num_expr(p)
    format_sub_binary_l3_expr(p)

    
def p_binary_l3_expr(p):
    ''' binary_l3_expr : binary_l4_expr '''
    p[0] = p[1]


def p_mul_binary_l4_expr(p):
    ''' binary_l4_expr : binary_l4_expr '*' binary_l5_expr '''
    p[0] = Node()
    chk_binary_num_expr(p)
    format_mul_binary_l4_expr(p)

    
def p_div_binary_l4_expr(p):
    ''' binary_l4_expr : binary_l4_expr '/' binary_l5_expr '''
    p[0] = Node()
    chk_binary_num_expr(p)
    format_div_binary_l4_expr(p)

    
def p_mod_binary_l4_expr(p):
    ''' binary_l4_expr : binary_l4_expr '%' binary_l5_expr '''
    p[0] = Node()
    chk_binary_num_expr(p)
    format_mod_binary_l4_expr(p)

    
def p_binary_l4_expr(p):
    ''' binary_l4_expr : binary_l5_expr '''
    p[0] = p[1]


def p_pow_binary_l5_expr(p):
    ''' binary_l5_expr : binary_l5_expr '^' binary_l6_expr '''
    p[0] = Node()
    chk_binary_num_expr(p)
    format_pow_binary_l5_expr(p)

    
def p_binary_l5_expr(p):
    ''' binary_l5_expr : binary_l6_expr '''
    p[0] = p[1]


def p_and_binary_l6_expr(p):
    ''' binary_l6_expr : binary_l6_expr AND binary_l7_expr '''
    p[0] = Node()
    chk_binary_bool_expr(p)
    format_and_binary_l6_expr(p)


def p_binary_l6_expr(p):
    ''' binary_l6_expr : binary_l7_expr '''
    p[0] = p[1]


def p_or_binary_l7_expr(p):
    ''' binary_l7_expr : binary_l7_expr OR binary_subexpr '''
    p[0] = Node()
    chk_binary_bool_expr(p)
    format_or_binary_l7_expr(p)

    
def p_binary_l7_expr(p):
    ''' binary_l7_expr : binary_subexpr '''
    p[0] = p[1]


def p_add_assign_vector_expr(p):
    ''' assign_expr : vector_access_expr ADDASSIGN subexpr '''
    p[0] = Node()
    chk_assign_num_vector_expr(p)
    format_add_assign_expr(p)


def p_add_assign_id_expr(p):
    ''' assign_expr : identifier_expr ADDASSIGN subexpr '''
    p[0] = Node()
    chk_assign_num_id_expr(p)
    format_add_assign_expr(p)


def p_sub_assign_vector_expr(p):
    ''' assign_expr : vector_access_expr SUBASSIGN subexpr '''
    p[0] = Node()
    chk_assign_num_vector_expr(p)
    format_sub_assign_expr(p)


def p_sub_assign_id_expr(p):
    ''' assign_expr : identifier_expr SUBASSIGN subexpr '''
    p[0] = Node()
    chk_assign_num_id_expr(p)
    format_sub_assign_expr(p)


def p_mul_assign_vector_expr(p):
    ''' assign_expr : vector_access_expr MULASSIGN subexpr '''
    p[0] = Node()
    chk_assign_num_vector_expr(p)
    format_mul_assign_expr(p)


def p_mul_assign_id_expr(p):
    ''' assign_expr : identifier_expr MULASSIGN subexpr '''
    p[0] = Node()
    chk_assign_num_id_expr(p)
    format_mul_assign_expr(p)

    
def p_div_assign_vector_expr(p):
    ''' assign_expr : vector_access_expr DIVASSIGN subexpr '''
    p[0] = Node()
    chk_assign_num_vector_expr(p)
    format_div_assign_expr(p)


def p_div_assign_id_expr(p):
    ''' assign_expr : identifier_expr DIVASSIGN subexpr '''
    p[0] = Node()
    chk_assign_num_id_expr(p)
    format_div_assign_expr(p)


def p_initializer_vector_expr(p):
    ''' assign_expr : vector_access_expr '=' subexpr '''
    p[0] = Node()
    chk_initializer_vector_expr(p)
    format_initializer_expr(p)


def p_initializer_id_expr(p):
    ''' assign_expr : identifier_expr '=' subexpr '''
    p[0] = Node()
    chk_initializer_id_expr(p)
    format_initializer_expr(p)


def p_positive_unary_expr(p):
    ''' unary_expr : '+' unary_subexpr '''
    p[0] = Node()
    chk_prefix_unary_expr(p)
    format_positive_unary_expr(p)


def p_negative_unary_expr(p):
    ''' unary_expr :  '-' unary_subexpr '''
    p[0] = Node()
    chk_prefix_unary_expr(p)
    format_negative_unary_expr(p)


def p_not_unary_expr(p):
    ''' unary_expr : NOT unary_subexpr '''
    p[0] = Node()
    chk_not_unary_expr(p)
    format_not_unary_expr(p)


def p_postfix_inc_expr(p):
    ''' inc_or_dec_expr : binary_expr INC '''
    p[0] = Node()
    chk_postfix_unary_expr(p)
    format_postfix_inc_expr(p)


def p_postfix_dec_expr(p):
    ''' inc_or_dec_expr : binary_expr DEC '''
    p[0] = Node()
    chk_postfix_unary_expr(p)
    format_postfix_dec_expr(p)

    
def p_prefix_inc_expr(p):
    ''' inc_or_dec_expr : INC binary_expr '''
    p[0] = Node()
    chk_prefix_unary_expr(p)
    format_prefix_inc_expr(p)

    
def p_prefix_dec_expr(p):
    ''' inc_or_dec_expr : DEC binary_expr '''
    p[0] = Node()
    chk_prefix_unary_expr(p)
    format_prefix_dec_expr(p)

    
def p_invocation_expr(p):
    ''' invocation_expr : multiplicacion_escalar
                        | capitalizar
                        | colineales
                        | length
                        | print '''
    p[0] = p[1]


def p_parenthesized_expr(p):
    ''' parenthesized_expr : '(' subexpr ')' '''
    p[0] = Node()
    chk_parenthesized_expr(p)
    format_parenthesized_expr(p)


def p_vector_access_expr(p):
    ''' vector_access_expr : vector_subexpr '[' condition_subexpr ']' '''
    p[0] = Node()
    chk_vector_access_expr(p)
    format_vector_access_expr(p)


def p_vector_declaration_expr(p):
    ''' vector_declaration_expr : '[' vector_elements ']' '''
    p[0] = Node()
    chk_vector_declaration_expr(p)
    format_vector_declaration_expr(p)


def p_vector_index_expr(p):
    ''' vector_index_expr : vector_declaration_expr '[' condition_subexpr ']' '''
    p[0] = Node()
    chk_vector_index_expr(p)
    format_vector_index_expr(p)


def p_register_access_expr(p):
    ''' register_access_expr : register_access_subexpr '.' ID '''
    p[0] = Node()
    chk_register_access_expr(p)
    format_register_access_expr(p)


def p_anonymous_obj_ctor_expr(p):
    ''' anonymous_obj_ctor_expr : '{' register_declaration_elements '}' '''
    p[0] = Node()
    chk_anonymous_obj_ctor_expr(p)
    format_anonymous_obj_ctor_expr(p)


def p_ternary_condition_expr(p):
    ''' ternary_condition_expr : binary_expr '?' subexpr ':' subexpr '''
    p[0] = Node()
    chk_ternary_condition_expr(p)
    format_ternary_condition_expr(p)


def p_identifier_reg_expr(p):
    ''' identifier_expr : register_access_expr '''
    p[0] = p[1]


def p_identifier_expr(p): 
    ''' identifier_expr : ID
                        | RES '''
    p[0] = Node()
    chk_identifier_expr(p)
    format_identifier_expr(p)


def p_vector_multiple_elements(p):
    ''' vector_elements : subexpr ',' vector_elements '''
    p[0] = Node()
    chk_vector_multiple_elements(p)
    format_vector_multiple_elements(p)


def p_vector_single_elements(p):
    ''' vector_elements : subexpr '''
    p[0] = p[1]


def p_register_multiple_decl_elems(p):
    ''' register_declaration_elements : ID ':' subexpr ',' register_declaration_elements '''
    p[0] = Node()
    chk_register_multiple_decl_elems(p)
    format_register_multiple_decl_elems(p)


def p_register_single_decl_elems(p):
    ''' register_declaration_elements : ID ':' subexpr '''
    p[0] = Node()
    chk_register_single_decl_elems(p)
    format_register_single_decl_elems(p)


## Sub expressions ##

def p_subexpr(p):
    ''' subexpr : binary_expr
                | ternary_condition_expr
                | vector_declaration_expr
                | anonymous_obj_ctor_expr '''
    p[0] = p[1]


def p_condition_subexpr(p):
    ''' condition_subexpr : binary_expr
                          | ternary_condition_expr '''
    p[0] = p[1]


def p_binary_subexpr(p):
    ''' binary_subexpr : unary_expr
                       | unary_subexpr '''
    p[0] = p[1]


def p_vector_subexpr(p):
    ''' vector_subexpr : identifier_expr
                       | parenthesized_expr
                       | invocation_expr
                       | vector_index_expr
                       | vector_access_expr '''
    p[0] = p[1]


def p_unary_subexpr(p):
    ''' unary_subexpr : term
                      | parenthesized_expr
                      | invocation_expr
                      | vector_index_expr
                      | vector_access_expr '''
    p[0] = p[1]


def p_register_access_subexpr(p):
    ''' register_access_subexpr : anonymous_obj_ctor_expr 
                                | vector_access_expr '''
    p[0] = p[1]


def p_register_access_id_subexpr(p):
    ''' register_access_subexpr : ID '''
    p[0] = Node()
    format_register_access_id_subexpr(p)



## Invocations ## 

def p_multiplicacion_escalar_3_params(p):
    ''' multiplicacion_escalar : MULESCALAR '(' subexpr ',' subexpr ','  subexpr ')' '''
    p[0] = Node()
    chk_multiplicacion_escalar_3_params(p)
    format_3_params_func(p)


def p_multiplicacion_escalar_2_params(p):
    ''' multiplicacion_escalar : MULESCALAR '(' subexpr ',' subexpr ')' '''
    p[0] = Node()
    chk_multiplicacion_escalar_2_params(p)
    format_2_params_func(p)


def p_capitalizar(p):
    ''' capitalizar : CAPITALIZAR '(' subexpr ')' '''
    p[0] = Node()
    chk_capitalizar(p)
    format_1_params_func(p)


def p_colineales(p):
    ''' colineales : COLINEALES '(' subexpr ',' subexpr ')' '''
    p[0] = Node()
    chk_colineales(p)
    format_2_params_func(p)


def p_print(p):
    ''' print : PRINT '(' subexpr ')' '''
    p[0] = Node()
    format_1_params_func(p)


def p_length(p):
    ''' length : LENGTH '(' subexpr ')' '''
    p[0] = Node()
    chk_length(p)
    format_1_params_func(p)


## Terms ##

def p_int_term(p):
    ''' term : INT '''
    p[0] = Node()
    chk_int_term(p)
    format_term(p)


def p_float_term(p):
    ''' term : FLOAT '''
    p[0] = Node()
    chk_float_term(p)
    format_term(p)


def p_string_term(p):
    ''' term : STRING '''
    p[0] = Node()
    chk_string_term(p)
    format_term(p)


def p_boolean_term(p):
    ''' term : BOOL '''
    p[0] = Node()
    chk_boolean_term(p)
    format_term(p)


def p_id_term(p):
    ''' term : identifier_expr '''
    p[0] = p[1]


## Other ##

def p_error(p):
    if not (p is None) :
        error_msg = "Error de sintaxis antes del token: " + str(p.value) + " linea: " + str(p.lineno)
    else:
        error_msg = "Error de sintaxis al final del archivo!"
    raise SyntaxError(error_msg)