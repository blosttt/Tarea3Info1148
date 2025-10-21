# gui.py
# Interfaz Gráfica para el Analizador Fortran77
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, filedialog
from fortran_analyzer import FortranAnalyzer
from ll1_parser import FortranLL1Analyzer
import os
from PIL import Image, ImageTk

class CompilerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Analizador Léxico y Sintáctico - Fortran77")
        self.window.geometry("1000x700")
        
        # Analizadores
        self.lalr_analyzer = FortranAnalyzer()
        self.ll1_analyzer = FortranLL1Analyzer()
        self.current_analyzer = self.lalr_analyzer
        
        self.setup_ui()
    
    def setup_ui(self):
        # === FRAME SUPERIOR: Selector de parser ===
        top_frame = tk.Frame(self.window)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(top_frame, text="Tipo de Parser:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        self.parser_var = tk.StringVar(value="LALR")
        
        lalr_radio = tk.Radiobutton(top_frame, text="LALR (PLY/Yacc)", 
                                    variable=self.parser_var, value="LALR",
                                    command=self.switch_parser)
        lalr_radio.pack(side=tk.LEFT, padx=10)
        
        ll1_radio = tk.Radiobutton(top_frame, text="LL(1) (Descendente Recursivo)", 
                                   variable=self.parser_var, value="LL1",
                                   command=self.switch_parser)
        ll1_radio.pack(side=tk.LEFT, padx=10)
        
        # === FRAME PRINCIPAL: Dividido en dos columnas ===
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Columna izquierda: Editor de código
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(left_frame, text="Código Fuente Fortran77:", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.code_text = scrolledtext.ScrolledText(left_frame, 
                                                    width=50, height=20,
                                                    font=('Courier New', 10))
        self.code_text.pack(fill=tk.BOTH, expand=True)
        
        # Código de ejemplo
        example_code = """! Programa de ejemplo Fortran77
DO I = 1, 10
    X = X + I * 2
    IF (X > 50) THEN
        Y = Y + 1
    ENDIF
ENDDO
RESULT = (A + B) * C / D"""
        self.code_text.insert('1.0', example_code)
        
        # Botones de acción
        button_frame = tk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(button_frame, text="▶ Analizar", 
                 command=self.analyze_code,
                 bg='#4CAF50', fg='white', 
                 font=('Arial', 10, 'bold'),
                 padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="🗑 Limpiar", 
                 command=self.clear_code).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="📂 Abrir", 
                 command=self.load_file).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="💾 Guardar", 
                 command=self.save_file).pack(side=tk.LEFT, padx=5)
        
        # Columna derecha: Resultados y visualización
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(right_frame, text="Resultados del Análisis:", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # Panel de resultados con pestañas
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña 1: Mensajes
        messages_frame = tk.Frame(self.notebook)
        self.notebook.add(messages_frame, text="📋 Mensajes")
        
        self.result_text = scrolledtext.ScrolledText(messages_frame, 
                                                      width=50, height=20,
                                                      font=('Courier New', 9),
                                                      bg='#f0f0f0')
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña 2: Tokens
        tokens_frame = tk.Frame(self.notebook)
        self.notebook.add(tokens_frame, text="🔤 Tokens")
        
        self.tokens_text = scrolledtext.ScrolledText(tokens_frame, 
                                                      width=50, height=20,
                                                      font=('Courier New', 9))
        self.tokens_text.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña 3: AST (imagen)
        ast_frame = tk.Frame(self.notebook)
        self.notebook.add(ast_frame, text="🌳 Árbol Sintáctico")
        
        self.ast_canvas = tk.Canvas(ast_frame, bg='white')
        self.ast_canvas.pack(fill=tk.BOTH, expand=True)
        
        ast_buttons = tk.Frame(ast_frame)
        ast_buttons.pack(fill=tk.X)
        
        tk.Button(ast_buttons, text="🖼 Generar Imagen AST", 
                 command=self.generate_ast_image).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(ast_buttons, text="🔄 Actualizar Vista", 
                 command=self.refresh_ast_view).pack(side=tk.LEFT, padx=5, pady=5)
        
        # === BARRA DE ESTADO ===
        self.status_bar = tk.Label(self.window, text="Listo", 
                                   bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def switch_parser(self):
        """Cambia entre parser LALR y LL(1)"""
        if self.parser_var.get() == "LALR":
            self.current_analyzer = self.lalr_analyzer
            self.status_bar.config(text="Parser LALR seleccionado")
        else:
            self.current_analyzer = self.ll1_analyzer
            self.status_bar.config(text="Parser LL(1) seleccionado")
    
    def analyze_code(self):
        """Analiza el código ingresado"""
        code = self.code_text.get('1.0', tk.END)
        
        if not code.strip():
            messagebox.showwarning("Advertencia", "Por favor ingrese código a analizar")
            return
        
        self.status_bar.config(text="Analizando...")
        self.window.update()
        
        # Limpiar resultados anteriores
        self.result_text.delete('1.0', tk.END)
        self.tokens_text.delete('1.0', tk.END)
        
        # Análisis léxico (tokens)
        self.result_text.insert(tk.END, "=== ANÁLISIS LÉXICO ===\n\n")
        try:
            lexer = lex.lex(module=__import__('fortran_analyzer'))
            lexer.input(code)
            
            token_count = 0
            for token in lexer:
                token_count += 1
                self.tokens_text.insert(tk.END, 
                    f"{token_count:3d}. {token.type:15s} = {token.value}\n")
            
            self.result_text.insert(tk.END, f"✅ Tokens identificados: {token_count}\n\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"❌ Error léxico: {e}\n\n")
        
        # Análisis sintáctico
        self.result_text.insert(tk.END, "=== ANÁLISIS SINTÁCTICO ===\n\n")
        
        if self.parser_var.get() == "LL1":
            success, message = self.ll1_analyzer.analyze(code)
        else:
            success, message = self.lalr_analyzer.analyze(code)
        
        if success:
            self.result_text.insert(tk.END, f"✅ {message}\n")
            self.result_text.insert(tk.END, "\nEstructura sintáctica válida.\n")
            self.result_text.insert(tk.END, "Puede visualizar el AST en la pestaña 'Árbol Sintáctico'.\n")
            self.status_bar.config(text="✅ Análisis completado exitosamente")
        else:
            self.result_text.insert(tk.END, f"❌ {message}\n")
            self.status_bar.config(text="❌ Errores encontrados")
        
        # Configurar colores
        self.result_text.tag_config('success', foreground='green')
        self.result_text.tag_config('error', foreground='red')
    
    def generate_ast_image(self):
        """Genera imagen del AST"""
        if self.parser_var.get() == "LL1" and self.ll1_analyzer.ast:
            # Para LL1, usar visualización del AST
            from fortran_analyzer import visualize_ast
            graph = visualize_ast(self.ll1_analyzer.ast)
            graph.render('ast_ll1', format='png', cleanup=True)
            self.status_bar.config(text="✅ Imagen AST generada: ast_ll1.png")
            self.refresh_ast_view('ast_ll1.png')
        elif self.lalr_analyzer.ast:
            msg = self.lalr_analyzer.generate_ast_image('ast_lalr')
            self.status_bar.config(text=f"✅ {msg}")
            self.refresh_ast_view('ast_lalr.png')
        else:
            messagebox.showinfo("Info", "Primero debe analizar código válido")
    
    def refresh_ast_view(self, filename=None):
        """Muestra la imagen del AST en el canvas"""
        if filename is None:
            filename = 'ast_lalr.png' if self.parser_var.get() == "LALR" else 'ast_ll1.png'
        
        if not os.path.exists(filename):
            self.ast_canvas.delete('all')
            self.ast_canvas.create_text(250, 150, 
                text="No hay imagen AST disponible.\nGenere el AST primero.",
                font=('Arial', 12))
            return
        
        try:
            img = Image.open(filename)
            # Redimensionar si es muy grande
            max_size = (600, 500)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            self.ast_photo = ImageTk.PhotoImage(img)
            self.ast_canvas.delete('all')
            self.ast_canvas.create_image(10, 10, anchor=tk.NW, image=self.ast_photo)
            self.ast_canvas.config(scrollregion=self.ast_canvas.bbox('all'))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
    
    def clear_code(self):
        """Limpia el editor de código"""
        self.code_text.delete('1.0', tk.END)
        self.result_text.delete('1.0', tk.END)
        self.tokens_text.delete('1.0', tk.END)
        self.status_bar.config(text="Editor limpiado")
    
    def load_file(self):
        """Carga un archivo de código"""
        filename = filedialog.askopenfilename(
            title="Abrir archivo",
            filetypes=[("Fortran", "*.f *.for *.f77"), ("Texto", "*.txt"), ("Todos", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    code = f.read()
                    self.code_text.delete('1.0', tk.END)
                    self.code_text.insert('1.0', code)
                    self.status_bar.config(text=f"Archivo cargado: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")
    
    def save_file(self):
        """Guarda el código actual"""
        filename = filedialog.asksaveasfilename(
            title="Guardar archivo",
            defaultextension=".f77",
            filetypes=[("Fortran", "*.f *.for *.f77"), ("Texto", "*.txt"), ("Todos", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    code = self.code_text.get('1.0', tk.END)
                    f.write(code)
                    self.status_bar.config(text=f"Archivo guardado: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
    
    def run(self):
        """Inicia la aplicación"""
        self.window.mainloop()

# === PUNTO DE ENTRADA ===
if __name__ == "__main__":
    import ply.lex as lex  # Importar aquí para el análisis léxico en la GUI
    app = CompilerGUI()
    app.run()
