# Casos de Prueba Documentados

## Categoría 1: Asignaciones Simples

### Test 1.1: Asignación con constante
**Entrada**:
```fortran
X = 5
```
**Resultado Esperado**: ✅ Análisis exitoso  
**AST**:
```
Program
  └─ StatementList
      └─ Assignment
          ├─ ID(X)
          └─ Number(5)
```

### Test 1.2: Asignación con expresión aritmética
**Entrada**:
```fortran
RESULT = (A + B) * C / D
```
**Resultado Esperado**: ✅ Análisis exitoso  
**Tokens**: ID, ASSIGN, LPAREN, ID, PLUS, ID, RPAREN, TIMES, ID, DIVIDE, ID

---

## Categoría 2: Estructuras IF-THEN-ENDIF

### Test 2.1: IF simple
**Entrada**:
```fortran
IF (X > 5) THEN
    Y = Y + 1
ENDIF
```
**Resultado Esperado**: ✅ Análisis exitoso

### Test 2.2: IF con múltiples sentencias
**Entrada**:
```fortran
IF (A == B) THEN
    X = X + 1
    Y = Y * 2
    Z = X + Y
ENDIF
```
**Resultado Esperado**: ✅ Análisis exitoso

### Test 2.3: IF con operador relacional complejo
**Entrada**:
```fortran
IF (X <= 100) THEN
    COUNT = COUNT + 1
ENDIF
```
**Resultado Esperado**: ✅ Análisis exitoso

---

## Categoría 3: Bucles DO

### Test 3.1: DO básico
**Entrada**:
```fortran
DO I = 1, 10
    X = X + I
ENDDO
```
**Resultado Esperado**: ✅ Análisis exitoso

### Test 3.2: DO con cuerpo complejo
**Entrada**:
```fortran
DO J = 5, 20
    A = A + J
    B = B * 2
    C = (A + B) / J
ENDDO
```
**Resultado Esperado**: ✅ Análisis exitoso

---

## Categoría 4: Programas Combinados

### Test 4.1: DO con IF anidado
**Entrada**:
```fortran
DO I = 1, 10
    X = X + I
    IF (X > 50) THEN
        Y = Y + 1
    ENDIF
ENDDO
```
**Resultado Esperado**: ✅ Análisis exitoso

### Test 4.2: Programa completo con comentarios
**Entrada**:
```fortran
! Programa de ejemplo
X = 0
DO I = 1, 5
    X = X + I * 2
ENDDO
RESULT = X / 2
```
**Resultado Esperado**: ✅ Análisis exitoso

---

## Categoría 5: Errores Léxicos

### Test 5.1: Carácter ilegal
**Entrada**:
```fortran
Z = X @ Y
```
**Resultado Esperado**: ❌ Error léxico  
**Mensaje**: `Error léxico: Carácter ilegal '@' en línea 1, columna 7`

### Test 5.2: Identificador inválido
**Entrada**:
```fortran
123ABC = 5
```
**Resultado Esperado**: ❌ Error léxico  
**Mensaje**: `Error léxico: Carácter ilegal '1' en línea 1, columna 1`

---

## Categoría 6: Errores Sintácticos

### Test 6.1: IF sin ENDIF
**Entrada**:
```fortran
IF (X > 5) THEN
    Y = Y + 1
```
**Resultado Esperado**: ❌ Error sintáctico  
**Mensaje**: `Error sintáctico: el archivo terminó inesperadamente. Tip: ¿Olvidaste cerrar un bloque IF o DO?`

### Test 6.2: DO sin ENDDO
**Entrada**:
```fortran
DO I = 1, 10
    X = X + I
```
**Resultado Esperado**: ❌ Error sintáctico  
**Mensaje**: `Error sintáctico: el archivo terminó inesperadamente`

### Test 6.3: Paréntesis sin cerrar
**Entrada**:
```fortran
Y = (A + B * C
```
**Resultado Esperado**: ❌ Error sintáctico  
**Mensaje**: `Error sintáctico: el archivo terminó inesperadamente`

### Test 6.4: Expresión incompleta
**Entrada**:
```fortran
X = A + 
```
**Resultado Esperado**: ❌ Error sintáctico  
**Mensaje**: `Error sintáctico: el archivo terminó inesperadamente`

### Test 6.5: Falta operador de asignación
**Entrada**:
```fortran
X 5
```
**Resultado Esperado**: ❌ Error sintáctico  
**Mensaje**: `Error sintáctico: token inesperado '5' en línea 1, columna 3, se esperaba ASSIGN`

---

## Categoría 7: Casos Límite

### Test 7.1: Programa vacío
**Entrada**:
```fortran

```
**Resultado Esperado**: ❌ Error sintáctico

### Test 7.2: Solo comentarios
**Entrada**:
```fortran
! Esto es un comentario
! Otra línea de comentario
```
**Resultado Esperado**: ❌ Error sintáctico (no hay código ejecutable)

### Test 7.3: Expresión con múltiples paréntesis
**Entrada**:
```fortran
X = ((A + B) * (C + D)) / ((E - F) + (G * H))
```
**Resultado Esperado**: ✅ Análisis exitoso

### Test 7.4: Números flotantes
**Entrada**:
```fortran
PI = 3.14159
AREA = PI * R * R
```
**Resultado Esperado**: ✅ Análisis exitoso

---

## Categoría 8: Comparación LALR vs LL(1)

### Test 8.1: Recursividad izquierda implícita
**Entrada**:
```fortran
X = A + B + C + D
```
**LALR**: ✅ Análisis exitoso  
**LL(1)**: ✅ Análisis exitoso (mediante recursividad derecha transformada)

### Test 8.2: Expresión compleja
**Entrada**:
```fortran
RESULT = A * B + C / D - E
```
**LALR**: ✅ Análisis exitoso  
**LL(1)**: ✅ Análisis exitoso

---

## Resumen de Cobertura

| Categoría | Total | Válidos | Inválidos |
|-----------|-------|---------|-----------|
| Asignaciones | 2 | 2 | 0 |
| IF-THEN | 3 | 3 | 0 |
| Bucles DO | 2 | 2 | 0 |
| Combinados | 2 | 2 | 0 |
| Errores Léxicos | 2 | 0 | 2 |
| Errores Sintácticos | 5 | 0 | 5 |
| Casos Límite | 4 | 2 | 2 |
| Comparación | 2 | 2 | 0 |
| **TOTAL** | **22** | **13** | **9** |

---

## Instrucciones para Ejecutar Pruebas

### Pruebas Automáticas
```powershell
python test_generator.py
```

### Prueba Manual (GUI)
1. Ejecutar `python gui.py`
2. Copiar código de prueba en el editor
3. Seleccionar parser (LALR o LL1)
4. Hacer clic en "Analizar"
5. Revisar resultados en pestañas

### Prueba por Línea de Comandos
```powershell
# LALR
python fortran_analyzer.py

# LL(1)
python ll1_parser.py
```
