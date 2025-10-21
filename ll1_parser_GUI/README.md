# Analizador Léxico y Sintáctico - Fortran77

## 📋 Descripción del Proyecto

Implementación de un **analizador léxico y sintáctico** para un subconjunto de Fortran77, desarrollado como proyecto académico de la asignatura de Compiladores. El sistema permite analizar código fuente, detectar errores léxicos y sintácticos, y generar un árbol sintáctico abstracto (AST) visualizable.

### Características Principales

✅ **Análisis Léxico**: Tokenización completa con detección de errores y ubicación (línea y columna)  
✅ **Análisis Sintáctico**: Dos implementaciones disponibles (LALR y LL(1))  
✅ **Generación de AST**: Árbol sintáctico abstracto con visualización gráfica  
✅ **Interfaz Gráfica**: Aplicación Tkinter completa y funcional  
✅ **Generador de Pruebas**: Sistema automatizado para crear casos de prueba  
✅ **Manejo de Errores**: Reportes detallados con línea y columna  

---

## 🏗️ Arquitectura del Sistema

### Componentes

1. **`fortran_analyzer.py`**: Analizador principal con parser LALR (PLY/Yacc)
2. **`ll1_parser.py`**: Parser LL(1) descendente recursivo
3. **`test_generator.py`**: Generador automático de casos de prueba
4. **`gui.py`**: Interfaz gráfica de usuario (Tkinter)

### Gramática Implementada

```
program → statement_list
statement_list → statement statement_list'
statement_list' → statement statement_list' | ε
statement → assignment | if_statement | do_loop
assignment → ID = expression
if_statement → IF ( expression ) THEN statement_list ENDIF
do_loop → DO ID = expression , expression statement_list ENDDO
expression → term expression'
expression' → (+ | - | == | != | < | > | <= | >=) term expression' | ε
term → factor term'
term' → (* | /) factor term' | ε
factor → ID | NUMBER | ( expression )
```

**Nota**: La gramática está libre de recursividad izquierda para el parser LL(1).

---

## 🔧 Instalación y Requisitos

### Requisitos del Sistema

- Python 3.8 o superior
- Windows 10/11 (o Linux/macOS con ajustes menores)

### Dependencias Python

```powershell
pip install ply graphviz pillow
```

### Graphviz Binario

Descarga e instala Graphviz desde: https://graphviz.org/download/

**Windows**: Añade `C:\Program Files\Graphviz\bin` al PATH.

Verifica la instalación:
```powershell
dot -V
```

---

## 🚀 Uso del Sistema

### Opción 1: Interfaz Gráfica (Recomendado)

```powershell
python gui.py
```

**Funcionalidades de la GUI**:
- Editor de código con syntax highlighting
- Selector de tipo de parser (LALR/LL(1))
- Visualización de tokens
- Mensajes de error detallados
- Visualización del AST integrada
- Abrir/Guardar archivos `.f77`

### Opción 2: Línea de Comandos

**Analizador LALR**:
```powershell
python fortran_analyzer.py
```

**Parser LL(1)**:
```powershell
python ll1_parser.py
```

**Generador de pruebas**:
```powershell
python test_generator.py
```

---

## 📊 Metodología de Desarrollo

### Metodología Aplicada: **Desarrollo Ágil (Scrum)**

Se aplicó una metodología ágil con sprints de 1 semana para permitir iteraciones rápidas y mejora continua.

### Sprint 1: Análisis y Diseño (Semana 1)

**Objetivos**:
- Definir requisitos funcionales y no funcionales
- Diseñar gramática libre de contexto
- Especificar tokens y estructura del AST
- Crear arquitectura del sistema

**Entregables**:
- Gramática formalizada
- Definición de tokens
- Diagrama de arquitectura

### Sprint 2: Implementación del Core (Semana 2)

**Objetivos**:
- Implementar analizador léxico (PLY)
- Implementar parser LALR
- Crear estructura del AST
- Desarrollar visualización con Graphviz

**Entregables**:
- `fortran_analyzer.py` funcional
- Casos de prueba básicos
- Generación de AST

### Sprint 3: Parser LL(1) y Testing (Semana 3)

**Objetivos**:
- Eliminar recursividad izquierda de gramática
- Implementar parser descendente recursivo LL(1)
- Crear generador automático de pruebas
- Mejorar detección de errores

**Entregables**:
- `ll1_parser.py` completo
- `test_generator.py` con casos válidos e inválidos
- Reporte de columna en errores

### Sprint 4: Interfaz Gráfica y Documentación (Semana 4)

**Objetivos**:
- Desarrollar interfaz Tkinter
- Integrar ambos parsers en GUI
- Completar documentación
- Preparar entrega final

**Entregables**:
- `gui.py` completo y funcional
- README.md con metodología
- Manual de usuario
- Presentación final

---

## 🧪 Casos de Prueba

### Ejemplos de Código Válido

**Ejemplo 1: Asignación simple**
```fortran
X = A + B * C
```

**Ejemplo 2: Estructura IF**
```fortran
IF (X > 5) THEN
    Y = Y * 2
    Z = Z + 1
ENDIF
```

**Ejemplo 3: Bucle DO**
```fortran
DO I = 1, 10
    X = X + I
    Y = Y * 2
ENDDO
```

**Ejemplo 4: Programa completo**
```fortran
! Programa de ejemplo
DO I = 1, 10
    X = X + I * 2
    IF (X > 50) THEN
        Y = Y + 1
    ENDIF
ENDDO
RESULT = (A + B) * C / D
```

### Ejemplos de Errores Detectados

**Error Léxico**:
```fortran
Z = X @ Y
```
```
Error léxico: Carácter ilegal '@' en línea 1, columna 7
```

**Error Sintáctico**:
```fortran
IF (X > 5) THEN
    Y = Y + 1
! Falta ENDIF
```
```
Error sintáctico: el archivo terminó inesperadamente
  Tip: ¿Olvidaste cerrar un bloque IF o DO?
```

---

## 📈 Resultados y Análisis

### Comparación de Parsers

| Característica | LALR (PLY/Yacc) | LL(1) Recursivo |
|---------------|-----------------|-----------------|
| **Complejidad de Implementación** | Baja (automática) | Media (manual) |
| **Velocidad** | Rápido | Medio |
| **Mensajes de Error** | Genéricos | Personalizables |
| **Gramáticas Aceptadas** | Más amplio | Más restrictivo |
| **Lookahead** | 1 token | 1 token |
| **Recursividad Izquierda** | ✅ Soportada | ❌ No soportada |

### Métricas del Proyecto

- **Líneas de código**: ~1,200
- **Tokens reconocidos**: 23 tipos
- **Producciones gramaticales**: 15
- **Casos de prueba**: 50+ (automáticos)
- **Cobertura de errores**: Léxicos y sintácticos

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal
- **PLY (Python Lex-Yacc)**: Generador de parsers LALR
- **Graphviz**: Visualización de AST
- **Tkinter**: Interfaz gráfica
- **Pillow (PIL)**: Procesamiento de imágenes
- **Git/GitHub**: Control de versiones

---

## 📚 Referencias

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.).
2. Documentación oficial de PLY: https://www.dabeaz.com/ply/
3. Fortran 77 Language Reference: https://docs.oracle.com/cd/E19957-01/805-4939/

---

## 👥 Autor

**Repositorio**: [blosttt/Tarea3Info1148](https://github.com/blosttt/Tarea3Info1148)  
**Curso**: Compiladores - Info1148  
**Fecha**: Octubre 2025

---

## 📝 Licencia

Este proyecto es de uso académico y educativo.

---

## 🔍 Estructura de Archivos

```
Tarea3Info1148/
│
├── fortran_analyzer.py     # Analizador LALR principal
├── ll1_parser.py            # Parser LL(1) descendente recursivo
├── test_generator.py        # Generador de casos de prueba
├── gui.py                   # Interfaz gráfica Tkinter
├── README.md                # Este archivo
├── parser.out               # Tablas del parser (generado)
├── parsetab.py              # Cache del parser (generado)
├── test_*.png               # Imágenes AST (generadas)
└── ast_*.png                # Imágenes AST de GUI (generadas)
```

---

## ⚠️ Limitaciones Conocidas

1. **Subconjunto de Fortran77**: Solo soporta asignaciones, IF y DO (no incluye GOTO, WRITE, READ completos, etc.)
2. **Sin análisis semántico**: No valida tipos ni uso de variables
3. **Comentarios**: Solo `!` y `C` al inicio de línea
4. **Números**: Solo enteros y flotantes simples (sin notación científica)

---

## 🚧 Trabajo Futuro

- [ ] Análisis semántico básico (tabla de símbolos)
- [ ] Soporte para más estructuras Fortran77 (GOTO, CALL, FUNCTION)
- [ ] Generación de código intermedio
- [ ] Optimizaciones básicas
- [ ] Tests unitarios con pytest
- [ ] Cobertura de código automatizada