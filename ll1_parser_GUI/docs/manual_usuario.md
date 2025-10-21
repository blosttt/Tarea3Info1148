# Manual de Usuario - Analizador Fortran77

## 🎯 Introducción

Bienvenido al **Analizador Léxico y Sintáctico para Fortran77**. Este manual le guiará en el uso de la aplicación para analizar código Fortran77, detectar errores y visualizar árboles sintácticos.

---

## 📖 Contenido

1. [Inicio Rápido](#inicio-rápido)
2. [Interfaz Gráfica](#interfaz-gráfica)
3. [Funcionalidades](#funcionalidades)
4. [Ejemplos de Uso](#ejemplos-de-uso)
5. [Solución de Problemas](#solución-de-problemas)
6. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🚀 Inicio Rápido

### Instalación

1. **Instalar Python 3.8+**
   - Descargar de: https://www.python.org/downloads/

2. **Instalar dependencias**
   ```powershell
   pip install ply graphviz pillow
   ```

3. **Instalar Graphviz**
   - Descargar de: https://graphviz.org/download/
   - Añadir al PATH: `C:\Program Files\Graphviz\bin`

4. **Verificar instalación**
   ```powershell
   python --version
   dot -V
   ```

### Ejecutar la Aplicación

```powershell
cd ruta\al\proyecto
python gui.py
```

---

## 🖥️ Interfaz Gráfica

### Componentes Principales

```
┌─────────────────────────────────────────────────────────────┐
│ 🔘 Parser: ⚪ LALR  ⚪ LL(1)                               │
├─────────────────────┬───────────────────────────────────────┤
│  Código Fuente      │  Resultados                           │
│                     │                                       │
│  [Editor de texto]  │  📋 Mensajes  🔤 Tokens  🌳 AST      │
│                     │                                       │
│  ▶ Analizar         │  [Panel de resultados]                │
│  🗑 Limpiar         │                                       │
│  📂 Abrir           │  🖼 Generar Imagen AST               │
│  💾 Guardar         │  🔄 Actualizar Vista                 │
└─────────────────────┴───────────────────────────────────────┘
│ Estado: Listo                                               │
└─────────────────────────────────────────────────────────────┘
```

### Descripción de Elementos

1. **Selector de Parser**: Elige entre LALR (PLY) o LL(1) (Recursivo)
2. **Editor de Código**: Área para escribir/pegar código Fortran77
3. **Botones de Acción**:
   - **▶ Analizar**: Ejecuta análisis léxico y sintáctico
   - **🗑 Limpiar**: Borra el contenido del editor
   - **📂 Abrir**: Carga archivo `.f77` o `.txt`
   - **💾 Guardar**: Guarda código actual
4. **Panel de Resultados**:
   - **📋 Mensajes**: Muestra resultados del análisis y errores
   - **🔤 Tokens**: Lista todos los tokens identificados
   - **🌳 AST**: Visualiza el árbol sintáctico
5. **Barra de Estado**: Muestra estado actual de la aplicación

---

## ⚙️ Funcionalidades

### 1. Análisis Léxico

**¿Qué hace?**  
Descompone el código en tokens (palabras clave, identificadores, números, operadores).

**Cómo usar:**
1. Escribir código en el editor
2. Hacer clic en **▶ Analizar**
3. Ver tokens en pestaña **🔤 Tokens**

**Ejemplo de salida**:
```
  1. DO             = do
  2. ID             = I
  3. ASSIGN         = =
  4. NUMBER         = 1
  5. COMMA          = ,
  6. NUMBER         = 10
  7. ID             = X
  8. ASSIGN         = =
  9. ID             = X
 10. PLUS           = +
 11. ID             = I
 12. ENDDO          = enddo
```

### 2. Análisis Sintáctico

**¿Qué hace?**  
Valida que la estructura del código siga las reglas gramaticales de Fortran77.

**Cómo usar:**
1. Elegir tipo de parser (LALR o LL1)
2. Hacer clic en **▶ Analizar**
3. Ver resultados en pestaña **📋 Mensajes**

**Resultado exitoso**:
```
=== ANÁLISIS LÉXICO ===
✅ Tokens identificados: 12

=== ANÁLISIS SINTÁCTICO ===
✅ Análisis exitoso (Parser LALR)
Estructura sintáctica válida.
```

**Resultado con error**:
```
=== ANÁLISIS SINTÁCTICO ===
❌ Error sintáctico: token inesperado 'X' en línea 2, columna 5
  Tip: Verifica que IF tenga ENDIF, DO tenga ENDDO...
```

### 3. Visualización del AST

**¿Qué hace?**  
Genera una representación gráfica del árbol sintáctico abstracto.

**Cómo usar:**
1. Analizar código válido primero
2. Ir a pestaña **🌳 Árbol Sintáctico**
3. Hacer clic en **🖼 Generar Imagen AST**
4. Ver imagen en el canvas

**Estructura del AST**:
```
Program
  └─ StatementList
      └─ DoLoop
          ├─ ID(I)
          ├─ Number(1)
          ├─ Number(10)
          └─ StatementList
              └─ Assignment
                  ├─ ID(X)
                  └─ BinOp(+)
                      ├─ ID(X)
                      └─ ID(I)
```

### 4. Abrir y Guardar Archivos

**Formatos soportados**: `.f`, `.for`, `.f77`, `.txt`

**Abrir archivo**:
1. Clic en **📂 Abrir**
2. Seleccionar archivo
3. El contenido se carga en el editor

**Guardar archivo**:
1. Clic en **💾 Guardar**
2. Elegir ubicación y nombre
3. El código actual se guarda

---

## 📝 Ejemplos de Uso

### Ejemplo 1: Analizar Asignación Simple

**Código**:
```fortran
X = A + B * C
```

**Pasos**:
1. Copiar código en el editor
2. Seleccionar parser LALR
3. Clic en **▶ Analizar**

**Resultado**:
- ✅ 7 tokens identificados
- ✅ Análisis sintáctico exitoso
- AST generado

### Ejemplo 2: Detectar Error en IF

**Código** (con error):
```fortran
IF (X > 5) THEN
    Y = Y + 1
! Falta ENDIF
```

**Resultado**:
```
❌ Error sintáctico: el archivo terminó inesperadamente
  Tip: ¿Olvidaste cerrar un bloque IF o DO?
```

### Ejemplo 3: Comparar Parsers

**Código**:
```fortran
DO I = 1, 10
    X = X + I
ENDDO
```

**Probar con ambos parsers**:
1. Seleccionar **LALR**, analizar → ✅ Exitoso
2. Seleccionar **LL(1)**, analizar → ✅ Exitoso

Ambos parsers producen el mismo resultado para código válido.

### Ejemplo 4: Programa Completo

**Código**:
```fortran
! Cálculo de factorial iterativo
FACT = 1
DO I = 1, N
    FACT = FACT * I
    IF (FACT > 1000) THEN
        STOP = 1
    ENDIF
ENDDO
RESULT = FACT
```

**Análisis**:
- ✅ Comentarios ignorados correctamente
- ✅ Estructura DO con IF anidado válida
- ✅ AST con múltiples niveles

---

## 🔧 Solución de Problemas

### Problema 1: "ModuleNotFoundError: No module named 'ply'"

**Solución**:
```powershell
pip install ply
```

### Problema 2: "Graphviz not found"

**Causas**:
- Graphviz no instalado
- No está en el PATH

**Solución**:
1. Instalar Graphviz: https://graphviz.org/download/
2. Añadir al PATH: `C:\Program Files\Graphviz\bin`
3. Reiniciar terminal/IDE
4. Verificar: `dot -V`

### Problema 3: "No se puede cargar imagen del AST"

**Solución**:
1. Verificar que Graphviz funciona: `dot -V`
2. Generar imagen primero (botón **🖼 Generar Imagen AST**)
3. Hacer clic en **🔄 Actualizar Vista**
4. Si persiste, verificar que existe `ast_lalr.png` o `ast_ll1.png`

### Problema 4: "Error: PIL not installed"

**Solución**:
```powershell
pip install pillow
```

### Problema 5: La GUI no abre

**Pasos de diagnóstico**:
```powershell
# Verificar Python
python --version

# Probar importación Tkinter
python -c "import tkinter; print('Tkinter OK')"

# Si falla, instalar Tkinter (Ubuntu/Debian)
sudo apt-get install python3-tk

# Windows: Tkinter viene incluido con Python
```

---

## ❓ Preguntas Frecuentes

### ¿Qué diferencia hay entre LALR y LL(1)?

| Característica | LALR | LL(1) |
|---------------|------|-------|
| Implementación | Automática (PLY) | Manual (recursiva) |
| Velocidad | Más rápido | Medio |
| Gramáticas | Más flexible | Más restrictivo |
| Mensajes de error | Genéricos | Personalizables |

**Recomendación**: Usar LALR para análisis general, LL(1) para entender el proceso.

### ¿Soporta todo Fortran77?

**No**. Solo un subconjunto:
- ✅ Asignaciones
- ✅ IF-THEN-ENDIF
- ✅ DO-ENDDO
- ✅ Expresiones aritméticas
- ✅ Comparaciones
- ❌ GOTO, CALL, FUNCTION
- ❌ Declaraciones de tipo
- ❌ WRITE, READ completos

### ¿Puedo usar comentarios?

**Sí**. Formatos soportados:
```fortran
! Comentario estilo moderno
C Comentario estilo clásico (columna 1)
```

### ¿Cómo exporto el AST?

**Opción 1**: Copiar imagen PNG generada  
**Opción 2**: Guardar desde el canvas (clic derecho → Guardar)  
**Archivos generados**: `ast_lalr.png`, `ast_ll1.png`

### ¿Funciona en Linux/Mac?

**Sí**, con ajustes menores:
- Instalar Graphviz: `sudo apt install graphviz` (Ubuntu)
- Tkinter incluido en Python estándar
- Rutas de archivo usan `/` en lugar de `\`

---

## 📞 Soporte

**Repositorio**: https://github.com/blosttt/Tarea3Info1148  
**Issues**: Reportar problemas en GitHub Issues  
**Documentación adicional**: Ver `README.md` y `docs/`

---

## 📚 Recursos Adicionales

- **Casos de prueba**: `docs/casos_de_prueba.md`
- **Gramática formal**: Ver `README.md` sección Arquitectura
- **Código fuente**: Todos los `.py` tienen comentarios explicativos

---

**¡Gracias por usar el Analizador Fortran77!** 🎉
