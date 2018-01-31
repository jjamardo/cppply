

## Statement ##

def format_simple_stmt(p):
    p[0].formatted_code = p[1].formatted_code + ";" + "\n"
    p[0].lineno = p.lineno(2)


def format_return_stmt(p):
    p[0].formatted_code = "return;\n"
    p[0].lineno = p.lineno(2)


def format_begin_stmt(p):
    p[0].formatted_code = "begin;\n"
    p[0].lineno = p.lineno(2)


def format_end_stmt(p):
    p[0].formatted_code = "end;\n"
    p[0].lineno = p.lineno(2)


def format_do_while_stmt(p):
    s = "do"
    s = apply_tabs(s, p[2].formatted_code)
    if (p[2].formatted_code[-2:] == "}\n"):
        s = rreplace(s, "\n", "", 1)
    if (s[len(s)-1] == "}"):
        s = s + " "
    p[0].formatted_code = s +"while (" + p[5].formatted_code + ");" + "\n"
    p[0].lineno = p.lineno(5)


def format_if_stmt(p):
    s = "if (" + p[3].formatted_code + ")"
    s = apply_tabs(s, p[5].formatted_code)
    p[0].formatted_code = s


def format_if_else_stmt(p):
    s = "if (" + p[3].formatted_code + ")"
    s = apply_tabs(s, p[5].formatted_code)
    s = s + "else"
    s = apply_tabs(s, p[7].formatted_code)
    p[0].formatted_code = s


def format_while_stmt(p):
    s = "while (" + p[3].formatted_code + ")"
    s = apply_tabs(s, p[5].formatted_code)
    p[0].formatted_code = s


def format_for_stmt(p):
    s = "for (" + p[3].formatted_code + p[4].formatted_code + p[5].formatted_code + ")"
    s = apply_tabs(s, p[7].formatted_code)
    p[0].formatted_code = s


def format_block_stmt(p):
    s = p[2].formatted_code.replace("\n","\n\t")
    s = rreplace(s, "\n\t", "\n", 1)
    p[0].formatted_code = "{\n\t" + s + "}" + "\n"


def format_block_body_lines(p):
    if (p[2].is_comment and p[2].lineno == p[1].lineno):
        s = rreplace(p[1].formatted_code, "\n", "", 1)
        s = s + " " + p[2].formatted_code
    else:
        s = p[1].formatted_code + p[2].formatted_code
    p[0].formatted_code = s


def format_block_body_comments(p):
    p[0].formatted_code = p[1] + "\n" + p[2].formatted_code
    p[0].lineno = p.lineno(1)
    p[0].is_comment = True


def format_block_body_comment(p):
    p[0].formatted_code = p[1] + "\n"
    p[0].lineno = p.lineno(1)
    p[0].is_comment = True


def format_commented_comments_body(p):
    p[0].formatted_code = p[1].formatted_code + p[2].formatted_code


def format_multiple_comments(p):
    p[0].formatted_code = p[1] + "\n" + p[2].formatted_code


def format_single_comment(p):
    p[0].formatted_code = p[1] + "\n"


def format_for_initializer(p):
    p[0].formatted_code = p[1].formatted_code + "; "


def format_for_non_initializer(p):
    p[0].formatted_code = "; "


def format_for_condition_subexpr(p):
    p[0].formatted_code = p[1].formatted_code + "; "


## Expressions ##


def format_eq_binary_l1_expr(p):
    p[0].formatted_code = p[1].formatted_code + " == " + p[3].formatted_code


def format_noteq_binary_l1_expr(p):
    p[0].formatted_code = p[1].formatted_code + " != " + p[3].formatted_code


def format_leq_binary_l2_expr(p):
    p[0].formatted_code = p[1].formatted_code + " < " + p[3].formatted_code


def format_gre_binary_l2_expr(p):
    p[0].formatted_code = p[1].formatted_code + " > " + p[3].formatted_code


def format_add_binary_l3_expr(p):
    p[0].formatted_code = p[1].formatted_code + " + " + p[3].formatted_code


def format_sub_binary_l3_expr(p):
    p[0].formatted_code = p[1].formatted_code + " - " + p[3].formatted_code


def format_mul_binary_l4_expr(p):
    p[0].formatted_code = p[1].formatted_code + " * " + p[3].formatted_code


def format_div_binary_l4_expr(p):
    p[0].formatted_code = p[1].formatted_code + " / " + p[3].formatted_code


def format_mod_binary_l4_expr(p):
    p[0].formatted_code = p[1].formatted_code + " % " + p[3].formatted_code


def format_pow_binary_l5_expr(p):
    p[0].formatted_code = p[1].formatted_code + " ^ " + p[3].formatted_code


def format_and_binary_l6_expr(p):
    p[0].formatted_code = p[1].formatted_code + " AND " + p[3].formatted_code


def format_or_binary_l7_expr(p):
    p[0].formatted_code = p[1].formatted_code + " OR " + p[3].formatted_code


def format_add_assign_expr(p):
    p[0].formatted_code = p[1].formatted_code + " += " + p[3].formatted_code


def format_sub_assign_expr(p):
    p[0].formatted_code = p[1].formatted_code + " -= " + p[3].formatted_code


def format_mul_assign_expr(p):
    p[0].formatted_code = p[1].formatted_code + " *= " + p[3].formatted_code


def format_div_assign_expr(p):
    p[0].formatted_code = p[1].formatted_code + " /= " + p[3].formatted_code


def format_initializer_expr(p):
    p[0].formatted_code = p[1].formatted_code + " = " + p[3].formatted_code


def format_positive_unary_expr(p):
    p[0].formatted_code = "+" + p[2].formatted_code


def format_negative_unary_expr(p):
    p[0].formatted_code = "-" + p[2].formatted_code


def format_not_unary_expr(p):
    p[0].formatted_code = "NOT " + p[2].formatted_code


def format_postfix_inc_expr(p):
    p[0].formatted_code = p[1].formatted_code + "++"


def format_postfix_dec_expr(p):
    p[0].formatted_code = p[1].formatted_code + "--"


def format_prefix_inc_expr(p):
    p[0].formatted_code = "++" + p[2].formatted_code


def format_prefix_dec_expr(p):
    p[0].formatted_code = "--" + p[2].formatted_code


def format_parenthesized_expr(p):
    p[0].formatted_code = "(" + p[2].formatted_code + ")"


def format_vector_access_expr(p):
    p[0].formatted_code = p[1].formatted_code + "[" + p[3].formatted_code + "]"


def format_vector_declaration_expr(p):
    p[0].formatted_code = "[" + p[2].formatted_code + "]"


def format_vector_index_expr(p):
    p[0].formatted_code = p[1].formatted_code + "[" + p[3].formatted_code + "]"


def format_register_access_expr(p):
    p[0].formatted_code = p[1].formatted_code + "." + p[3];


def format_anonymous_obj_ctor_expr(p):
    p[0].formatted_code = "{" + p[2].formatted_code + "}"


def format_ternary_condition_expr(p):
    p[0].formatted_code = p[1].formatted_code + " ? " + p[3].formatted_code + " : " + p[5].formatted_code


def format_identifier_expr(p): 
    p[0].formatted_code = p[1]


def format_vector_multiple_elements(p):
    p[0].formatted_code = p[1].formatted_code + ", " + p[3].formatted_code


def format_register_multiple_decl_elems(p):
    p[0].formatted_code = p[1] + ":" + p[3].formatted_code + ", " + p[5].formatted_code


def format_register_single_decl_elems(p):
    p[0].formatted_code = p[1] + ":" + p[3].formatted_code



## Sub expressions ##

def format_register_access_id_subexpr(p):
    p[0].formatted_code = p[1]


## Invocations ## 

def format_3_params_func(p):
    p[0].formatted_code = p[1] + "(" + p[3].formatted_code + ", " + p[5].formatted_code + ", " + p[7].formatted_code + ")"


def format_2_params_func(p):
    p[0].formatted_code = p[1] + "(" + p[3].formatted_code + ", " + p[5].formatted_code + ")"


def format_1_params_func(p):
    p[0].formatted_code = p[1] + "(" + p[3].formatted_code + ")"


## Terms ##

def format_term(p):
    p[0].formatted_code = p[1]


## Auxiliares ##

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def apply_tabs(head, code):
    if (not code[0] == "{"):
        s = head + "\n\t" + code.replace("\n","\n\t")
        s = rreplace(s, "\n\t", "\n", 1)
    else:
        s = head + " " + code
    return s