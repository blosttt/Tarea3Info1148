# ll1_parser.py
# Parser LL(1) Descendente Recursivo para Fortran77 simplificado
import ply.lex as lex
import re

# === ANALIZADOR LÉXICO (reutilizado) ===
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

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_COMMENT(t):
    r'![^\n]*'
    pass  # Ignorar comentarios estilo !

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def find_column(input_text, token):
    line_start = input_text.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def t_error(t):
    col = find_column(t.lexer.lexdata, t)
    print(f"Error léxico: Carácter ilegal '{t.value[0]}' en línea {t.lexer.lineno}, columna {col}")
    t.lexer.skip(1)

# === NODO DEL AST ===
class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children if children is not None else []
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})" if self.value else self.type

# === PARSER LL(1) DESCENDENTE RECURSIVO ===
class LL1Parser:
    """
    Gramática LL(1) sin recursividad izquierda:
    
    program → statement_list
    statement_list → statement statement_list'
    statement_list' → statement statement_list' | ε
    statement → assignment | if_statement | do_loop
    assignment → ID ASSIGN expression
    if_statement → IF LPAREN expression RPAREN THEN statement_list ENDIF
    do_loop → DO ID ASSIGN expression COMMA expression statement_list ENDDO
    
    expression → term expression'
    expression' → addop term expression' | relop term expression' | ε
    addop → PLUS | MINUS
    relop → EQUALS | NOTEQUALS | LESS | GREATER | LESSEQUAL | GREATEREQUAL
    
    term → factor term'
    term' → mulop factor term' | ε
    mulop → TIMES | DIVIDE
    
    factor → ID | NUMBER | LPAREN expression RPAREN
    """
    
    def __init__(self):
        self.lexer = lex.lex()
        self.tokens = []
        self.pos = 0
        self.current_token = None
        self.input_code = ""
    
    def error(self, expected=""):
        if self.current_token:
            col = find_column(self.input_code, self.current_token)
            msg = f"Error sintáctico en línea {self.current_token.lineno}, columna {col}: "
            msg += f"token inesperado '{self.current_token.value}'"
            if expected:
                msg += f", se esperaba {expected}"
        else:
            msg = "Error sintáctico: fin inesperado del archivo"
            if expected:
                msg += f", se esperaba {expected}"
        raise SyntaxError(msg)
    
    def peek(self):
        """Devuelve el token actual sin consumirlo (lookahead)"""
        return self.current_token
    
    def consume(self, expected_type=None):
        """Consume el token actual y avanza al siguiente"""
        if expected_type and (not self.current_token or self.current_token.type != expected_type):
            self.error(expected_type)
        
        token = self.current_token
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = None
        return token
    
    def parse(self, code):
        """Punto de entrada del parser"""
        self.input_code = code
        # Reiniciar el lexer para este código
        self.lexer = lex.lex()  # Crear un nuevo lexer cada vez
        self.lexer.input(code)
        self.tokens = list(self.lexer)
        self.pos = 1  # Empezar en 1 porque current_token ya tiene el primer token
        self.current_token = self.tokens[0] if self.tokens else None
        
        return self.program()
    
    # === PRODUCCIONES ===
    
    def program(self):
        """program → statement_list"""
        stmts = self.statement_list()
        return Node('Program', [stmts])
    
    def statement_list(self):
        """statement_list → statement statement_list'"""
        statements = []
        
        # FIRST(statement) = {ID, IF, DO}
        if self.peek() and self.peek().type in ['ID', 'IF', 'DO']:
            statements.append(self.statement())
            statements.extend(self.statement_list_prime())
        
        return Node('StatementList', statements)
    
    def statement_list_prime(self):
        """statement_list' → statement statement_list' | ε"""
        statements = []
        
        # FIRST(statement) = {ID, IF, DO}
        # FOLLOW(statement_list') = {ENDIF, ENDDO, $}
        if self.peek() and self.peek().type in ['ID', 'IF', 'DO']:
            statements.append(self.statement())
            statements.extend(self.statement_list_prime())
        
        return statements
    
    def statement(self):
        """statement → assignment | if_statement | do_loop"""
        if not self.peek():
            self.error("sentencia (ID, IF o DO)")
        
        token_type = self.peek().type
        
        if token_type == 'ID':
            return self.assignment()
        elif token_type == 'IF':
            return self.if_statement()
        elif token_type == 'DO':
            return self.do_loop()
        else:
            self.error("ID, IF o DO")
    
    def assignment(self):
        """assignment → ID ASSIGN expression"""
        id_token = self.consume('ID')
        self.consume('ASSIGN')
        expr = self.expression()
        return Node('Assignment', [Node('ID', value=id_token.value), expr])
    
    def if_statement(self):
        """if_statement → IF LPAREN expression RPAREN THEN statement_list ENDIF"""
        self.consume('IF')
        self.consume('LPAREN')
        condition = self.expression()
        self.consume('RPAREN')
        self.consume('THEN')
        body = self.statement_list()
        self.consume('ENDIF')
        return Node('IfStatement', [condition, body])
    
    def do_loop(self):
        """do_loop → DO ID ASSIGN expression COMMA expression statement_list ENDDO"""
        self.consume('DO')
        loop_var = self.consume('ID')
        self.consume('ASSIGN')
        start = self.expression()
        self.consume('COMMA')
        end = self.expression()
        body = self.statement_list()
        self.consume('ENDDO')
        return Node('DoLoop', [Node('ID', value=loop_var.value), start, end, body])
    
    def expression(self):
        """expression → term expression'"""
        left = self.term()
        return self.expression_prime(left)
    
    def expression_prime(self, left):
        """expression' → addop term expression' | relop term expression' | ε"""
        if not self.peek():
            return left
        
        token_type = self.peek().type
        
        # addop o relop
        if token_type in ['PLUS', 'MINUS', 'EQUALS', 'NOTEQUALS', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL']:
            op_token = self.consume()
            right = self.term()
            node = Node('BinOp', [left, right], value=op_token.value)
            return self.expression_prime(node)
        
        # ε (epsilon)
        return left
    
    def term(self):
        """term → factor term'"""
        left = self.factor()
        return self.term_prime(left)
    
    def term_prime(self, left):
        """term' → mulop factor term' | ε"""
        if not self.peek():
            return left
        
        token_type = self.peek().type
        
        # mulop
        if token_type in ['TIMES', 'DIVIDE']:
            op_token = self.consume()
            right = self.factor()
            node = Node('BinOp', [left, right], value=op_token.value)
            return self.term_prime(node)
        
        # ε (epsilon)
        return left
    
    def factor(self):
        """factor → ID | NUMBER | LPAREN expression RPAREN"""
        if not self.peek():
            self.error("ID, NUMBER o '('")
        
        token_type = self.peek().type
        
        if token_type == 'ID':
            token = self.consume('ID')
            return Node('ID', value=token.value)
        elif token_type == 'NUMBER':
            token = self.consume('NUMBER')
            return Node('Number', value=token.value)
        elif token_type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.expression()
            self.consume('RPAREN')
            return expr
        else:
            self.error("ID, NUMBER o '('")

# === CLASE INTEGRADORA ===
class FortranLL1Analyzer:
    def __init__(self):
        self.parser = LL1Parser()
        self.ast = None
    
    def analyze(self, code):
        try:
            self.ast = self.parser.parse(code)
            return True, "Análisis exitoso (Parser LL(1))"
        except SyntaxError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error: {str(e)}"

# === PRUEBAS ===
if __name__ == "__main__":
    analyzer = FortranLL1Analyzer()
    
    test_cases = [
        """
        DO I = 1, 10
            X = X + I
        ENDDO
        """,
        
        """
        IF (X > 5) THEN
            Y = Y * 2
        ENDIF
        """,
        
        "RESULT = (A + B) * C / D",
        
        # Caso con error
        "DO I = 1, 10 X = X + I"  # Falta ENDDO
    ]
    
    print("=== ANALIZADOR FORTRAN77 LL(1) ===")
    for i, code in enumerate(test_cases, 1):
        print(f"\n--- Prueba {i} ---")
        print(f"Código: {code.strip()}")
        
        success, message = analyzer.analyze(code)
        print(f"Resultado: {message}")
        
        if success and analyzer.ast:
            print(f"AST generado: {analyzer.ast}")
