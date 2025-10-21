# 🚀 INICIO RÁPIDO - Analizador Fortran77

## ⚡ Instalación en 3 Pasos

### 1. Instalar Dependencias Python
```powershell
pip install ply graphviz pillow
```

### 2. Instalar Graphviz
Descargar de: https://graphviz.org/download/  
**Windows**: Instalar y añadir `C:\Program Files\Graphviz\bin` al PATH

Verificar:
```powershell
dot -V
```

### 3. Ejecutar la Aplicación
```powershell
python gui.py
```

---

## 📝 Uso Básico

1. **Escribir/pegar código** en el editor
2. **Seleccionar parser** (LALR o LL1)
3. **Clic en "▶ Analizar"**
4. **Ver resultados** en las pestañas

---

## 💡 Ejemplo Rápido

Copia este código en la GUI:

```fortran
! Ejemplo de bucle
DO I = 1, 10
    X = X + I * 2
    IF (X > 50) THEN
        Y = Y + 1
    ENDIF
ENDDO
RESULT = X / 2
```

Haz clic en **▶ Analizar** y explora las pestañas:
- **📋 Mensajes**: Ver análisis exitoso
- **🔤 Tokens**: Ver tokens identificados
- **🌳 AST**: Generar y ver árbol sintáctico

---

## 📚 Documentación Completa

- **README.md**: Descripción completa del proyecto
- **docs/manual_usuario.md**: Manual detallado
- **docs/casos_de_prueba.md**: 22 casos de prueba
- **docs/CHECKLIST_FINAL.md**: Cumplimiento de requisitos
- **docs/RESUMEN_EJECUTIVO.md**: Resumen de mejoras

---

## 🎯 Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `gui.py` | **Interfaz gráfica** (RECOMENDADO) |
| `fortran_analyzer.py` | Parser LALR por línea de comandos |
| `ll1_parser.py` | Parser LL(1) por línea de comandos |
| `test_generator.py` | Generador de pruebas automático |

---

## ❓ Solución Rápida de Problemas

### Error: "No module named 'ply'"
```powershell
pip install ply
```

### Error: "Graphviz not found"
1. Instalar Graphviz: https://graphviz.org/download/
2. Añadir al PATH: `C:\Program Files\Graphviz\bin`
3. Reiniciar terminal
4. Verificar: `dot -V`

### La GUI no abre
```powershell
# Verificar Python
python --version

# Verificar Tkinter
python -c "import tkinter; print('OK')"
```

---

## 🎓 Características Implementadas

✅ **Análisis Léxico**: Tokenización completa  
✅ **Análisis Sintáctico**: LALR y LL(1)  
✅ **Detección de Errores**: Con línea y columna  
✅ **AST Visual**: Generación y visualización  
✅ **GUI Tkinter**: Interfaz completa  
✅ **Comentarios**: Soporte para `!`  
✅ **Archivos**: Abrir/guardar `.f77`  

---

## 📞 Soporte

**Repositorio**: https://github.com/blosttt/Tarea3Info1148  
**Documentación**: Ver carpeta `docs/`

---

**¡Listo para usar! Ejecuta `python gui.py` y empieza a analizar código Fortran77.** 🎉
