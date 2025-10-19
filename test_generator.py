# test_generator.py
import random

class FortranTestGenerator:
    def __init__(self):
        self.variables = ['X', 'Y', 'Z', 'A', 'B', 'C', 'I', 'J', 'K']
        self.operators = ['+', '-', '*', '/']
        self.comparisons = ['==', '!=', '<', '>', '<=', '>=']
    
    def generate_expression(self, depth=0):
        """Genera una expresión aritmética aleatoria"""
        if depth > 2 or random.random() < 0.3:
            # Hoja: variable o número
            if random.random() < 0.5:
                return random.choice(self.variables)
            else:
                return str(random.randint(1, 100))
        
        # Expresión binaria
        left = self.generate_expression(depth + 1)
        right = self.generate_expression(depth + 1)
        op = random.choice(self.operators)
        
        if random.random() < 0.2 and depth == 0:
            return f"({left} {op} {right})"
        return f"{left} {op} {right}"
    
    def generate_assignment(self):
        """Genera una asignación aleatoria"""
        var = random.choice(self.variables)
        expr = self.generate_expression()
        return f"{var} = {expr}"
    
    def generate_if_statement(self):
        """Genera una estructura IF aleatoria"""
        condition_var = random.choice(self.variables)
        condition_op = random.choice(self.comparisons)
        condition_val = random.randint(0, 50)
        condition = f"{condition_var} {condition_op} {condition_val}"
        
        # 1-3 statements en el cuerpo
        num_statements = random.randint(1, 3)
        body = "\n".join("    " + self.generate_assignment() 
                        for _ in range(num_statements))
        
        return f"IF ({condition}) THEN\n{body}\nENDIF"
    
    def generate_do_loop(self):
        """Genera un bucle DO aleatorio"""
        loop_var = random.choice(['I', 'J', 'K'])
        start = random.randint(1, 5)
        end = random.randint(6, 15)
        
        # 1-3 statements en el cuerpo
        num_statements = random.randint(1, 3)
        body = "\n".join("    " + self.generate_assignment() 
                        for _ in range(num_statements))
        
        return f"DO {loop_var} = {start}, {end}\n{body}\nENDDO"
    
    def generate_valid_test(self, complexity=1):
        """Genera un test case válido"""
        components = []
        
        # Siempre incluir al menos una asignación
        components.append(self.generate_assignment())
        
        if complexity >= 1:
            if random.random() < 0.7:
                components.append(self.generate_if_statement())
        
        if complexity >= 2:
            if random.random() < 0.5:
                components.append(self.generate_do_loop())
        
        # Mezclar componentes
        random.shuffle(components)
        return "\n".join(components)
    
    def generate_invalid_test(self, error_type):
        """Genera test cases inválidos"""
        errors = {
            'missing_endif': """
                IF (X > 5) THEN
                    Y = Y + 1
                """,
            
            'missing_enddo': """
                DO I = 1, 10
                    X = X + I
                """,
            
            'invalid_syntax': """
                DO I = 1, 10
                    X = X + 
                ENDDO
                """,
            
            'unclosed_parenthesis': """
                Y = (A + B * C
                """,
            
            'unknown_operator': """
                Z = X @ Y
                """
        }
        
        return errors.get(error_type, "INVALID CODE")
    
    def generate_test_suite(self, num_valid=10, num_invalid=5):
        """Genera un conjunto completo de pruebas"""
        print("=== SUITE DE PRUEBAS FORTRAN77 ===\n")
        
        print("--- CASOS VÁLIDOS ---")
        valid_tests = []
        for i in range(num_valid):
            test = self.generate_valid_test(complexity=random.randint(1, 3))
            valid_tests.append(test)
            print(f"Test {i+1}:\n{test}\n")
        
        print("\n--- CASOS INVÁLIDOS ---")
        invalid_types = ['missing_endif', 'missing_enddo', 'invalid_syntax', 
                        'unclosed_parenthesis', 'unknown_operator']
        
        invalid_tests = []
        for i in range(num_invalid):
            error_type = random.choice(invalid_types)
            test = self.generate_invalid_test(error_type)
            invalid_tests.append((error_type, test))
            print(f"Test {i+1} ({error_type}):\n{test}\n")
        
        return valid_tests, invalid_tests

# Ejemplo de uso
if __name__ == "__main__":
    generator = FortranTestGenerator()
    
    # Generar suite de pruebas
    valid, invalid = generator.generate_test_suite(5, 3)
    
    # Ejemplo de prueba específica
    print("\n--- EJEMPLOS ESPECÍFICOS ---")
    
    print("1. Asignación simple:")
    print(generator.generate_assignment())
    
    print("\n2. IF complejo:")
    print(generator.generate_if_statement())
    
    print("\n3. DO loop con expresiones:")
    print(generator.generate_do_loop())
    
    print("\n4. Programa completo:")
    complex_program = f"""
{generator.generate_assignment()}
{generator.generate_do_loop()}
{generator.generate_if_statement()}
{generator.generate_assignment()}
"""
    print(complex_program)