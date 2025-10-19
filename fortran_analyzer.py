# fortran_analyzer.py
import ply.lex as lex
import ply.yacc as yacc
import graphviz
import re

# === ANALIZADOR LÉXICO ===
tokens = [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'ASSIGN', 'COMMA', 'EQUALS',
    'NOTEQUALS', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL'
]

reserved = {
    'if': 'IF',
    'then': 'THEN', 
    'endif': 'ENDIF',
    'do': 'DO',
    'enddo': 'ENDDO',
    'read': 'READ',
    'write': 'WRITE'
}

tokens += list(reserved.values())

# Tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='
t_COMMA = r','
t_EQUALS = r'=='
t_NOTEQUALS = r'!='
t_LESS = r'<'
t_GREATER = r'>'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='

# Tokens complejos
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)

# === ANALIZADOR SINTÁCTICO ===
class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children if children is not None else []
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})" if self.value else self.type

def p_program(p):
    '''program : statement_list'''
    p[0] = Node('Program', [p[1]])

def p_statement_list(p):
    '''statement_list : statement
                     | statement statement_list'''
    if len(p) == 2:
        p[0] = Node('StatementList', [p[1]])
    else:
        p[0] = Node('StatementList', [p[1]] + p[2].children)

def p_statement(p):
    '''statement : assignment
                | if_statement
                | do_loop'''
    p[0] = p[1]

def p_assignment(p):
    'assignment : ID ASSIGN expression'
    p[0] = Node('Assignment', [Node('ID', value=p[1]), p[3]])

def p_if_statement(p):
    'if_statement : IF LPAREN expression RPAREN THEN statement_list ENDIF'
    p[0] = Node('IfStatement', [p[3], p[6]])

def p_do_loop(p):
    'do_loop : DO ID ASSIGN expression COMMA expression statement_list ENDDO'
    p[0] = Node('DoLoop', [
        Node('ID', value=p[2]), p[4], p[6], p[7]
    ])

def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression EQUALS term
                  | expression NOTEQUALS term
                  | expression LESS term
                  | expression GREATER term
                  | expression LESSEQUAL term
                  | expression GREATEREQUAL term'''
    p[0] = Node('BinOp', [p[1], p[3]], value=p[2])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = Node('BinOp', [p[1], p[3]], value=p[2])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_id(p):
    'factor : ID'
    p[0] = Node('ID', value=p[1])

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = Node('Number', value=p[1])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}', línea {p.lineno}")
    else:
        print("Error de sintaxis en EOF")

# === VISUALIZADOR ===
def visualize_ast(node, graph=None, parent=None, edge_label=""):
    if graph is None:
        graph = graphviz.Digraph()
        graph.attr('node', shape='box')
    
    node_id = str(id(node))
    label = f"{node.type}"
    if node.value is not None:
        label += f"\\n{node.value}"
    graph.node(node_id, label)
    
    if parent is not None:
        graph.edge(parent, node_id, label=edge_label)
    
    for i, child in enumerate(node.children):
        visualize_ast(child, graph, node_id, f"child{i+1}")
    
    return graph

# === ANALIZADOR PRINCIPAL ===
class FortranAnalyzer:
    def __init__(self):
        self.lexer = lex.lex()
        self.parser = yacc.yacc()
        self.ast = None
    
    def analyze(self, code):
        try:
            self.ast = self.parser.parse(code, lexer=self.lexer)
            return True, "Análisis exitoso"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def generate_ast_image(self, filename="ast"):
        if self.ast:
            graph = visualize_ast(self.ast)
            graph.render(filename, format='png', cleanup=True)
            return f"Árbol generado: {filename}.png"
        return "No hay AST para visualizar"

# === EJECUCIÓN Y PRUEBAS ===
if __name__ == "__main__":
    analyzer = FortranAnalyzer()
    
    # Casos de prueba
    test_cases = [
        # Código válido
        """
        DO I = 1, 10
            X = X + I
        ENDDO
        """,
        
        # IF válido
        """
        IF (X > 5) THEN
            Y = Y * 2
        ENDIF
        """,
        
        # Expresión compleja
        "RESULT = (A + B) * C / D",
        
        # Código inválido (para probar detección de errores)
        "DO I = 1, 10 X = X + I"  # Falta ENDDO
    ]
    
    print("=== ANALIZADOR FORTRAN77 ===")
    for i, code in enumerate(test_cases, 1):
        print(f"\n--- Prueba {i} ---")
        print(f"Código: {code.strip()}")
        
        success, message = analyzer.analyze(code)
        print(f"Resultado: {message}")
        
        if success:
            image_msg = analyzer.generate_ast_image(f"test_{i}")
            print(image_msg)