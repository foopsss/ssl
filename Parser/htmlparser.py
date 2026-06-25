#====================================================================#
#============================== HTML ================================#
#====================================================================#

    def generar_html(self):
        """Genera el HTML del programa"""
        texto = self.editor.get(1.0, tk.END).strip()
        if not texto:
            messagebox.showwarning("Advertencia", "No hay código para generar HTML")
            return
        
        try:
            # Realizar análisis léxico si no se ha hecho
            if not self.tokens_encontrados:
                cargar_datos(texto)
                self.tokens_encontrados = obtener_tokens()
            
            # Generar HTML
            html = self.crear_html(texto, self.tokens_encontrados)
            
            # Mostrar en pestaña HTML
            self.notebook.select(self.tab_html)
            self.tab_html.delete(1.0, tk.END)
            self.tab_html.insert(1.0, html)
            
            # Habilitar botón de guardar
            self.btn_guardar.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar HTML:\n{str(e)}")
    
    def crear_html(self, codigo, tokens):
        """Crea el documento HTML"""
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Escapar HTML en el código
        codigo_escapado = self.escapar_html(codigo)
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Programa SmartHome - BinaryBuilders</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .info {{
            background: #f8f9fa;
            padding: 15px 30px;
            border-bottom: 2px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }}
        
        .info-item {{
            margin: 5px 15px 5px 0;
        }}
        
        .info-label {{
            font-weight: bold;
            color: #555;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 30px;
        }}
        
        @media (max-width: 968px) {{
            .content {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .panel {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .panel h2 {{
            color: #1e3c72;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #1e3c72;
        }}
        
        .code-container {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 5px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
            overflow-x: auto;
            white-space: pre;
        }}
        
        .tokens-container {{
            max-height: 500px;
            overflow-y: auto;
        }}
        
        .token-item {{
            background: white;
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 4px;
            border-left: 3px solid #667eea;
            font-family: 'Consolas', monospace;
            font-size: 13px;
            display: flex;
            justify-content: space-between;
        }}
        
        .token-value {{
            font-weight: bold;
            color: #333;
        }}
        
        .token-type {{
            color: #667eea;
            font-size: 11px;
        }}
        
        .token-pos {{
            color: #999;
            font-size: 11px;
        }}
        
        .stats {{
            background: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin-top: 15px;
        }}
        
        .stats h3 {{
            color: #2e7d32;
            margin-bottom: 10px;
        }}
        
        .stats-item {{
            margin: 5px 0;
            color: #555;
        }}
        
        .footer {{
            background: #1e3c72;
            color: white;
            text-align: center;
            padding: 15px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 Programa SmartHome</h1>
            <p>Analizador Léxico y Sintáctico - BinaryBuilders</p>
        </div>
        
        <div class="info">
            <div class="info-item">
                <span class="info-label">Fecha:</span> {fecha}
            </div>
            <div class="info-item">
                <span class="info-label">Tokens:</span> {len(tokens)}
            </div>
            <div class="info-item">
                <span class="info-label">Líneas:</span> {len(codigo.splitlines())}
            </div>
            <div class="info-item">
                <span class="info-label">Estado:</span> ✓ Válido
            </div>
        </div>
        
        <div class="content">
            <div class="panel">
                <h2>📄 Código Fuente</h2>
                <div class="code-container">{codigo_escapado}</div>
            </div>
            
            <div class="panel">
                <h2>🔍 Tokens Identificados</h2>
                <div class="tokens-container">
"""
        
        # Agregar cada token
        for token in tokens:
            html += f"""                    <div class="token-item">
                        <span class="token-value">'{token['valor']}'</span>
                        <span class="token-type">{token['tipo']}</span>
                        <span class="token-pos">L{token['linea']}:C{token['columna']}</span>
                    </div>
"""
        
        html += """                </div>
                
                <div class="stats">
                    <h3>📊 Estadísticas</h3>
                    <div class="stats-item">Total de tokens: """ + str(len(tokens)) + """</div>
"""
        
        # Contar tipos de tokens
        tipos = {}
        for token in tokens:
            tipo = token['tipo']
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        for tipo, cantidad in sorted(tipos.items()):
            html += f"""                    <div class="stats-item">{tipo}: {cantidad}</div>
"""
        
        html += """                </div>
            </div>
        </div>
        
        <div class="footer">
            BinaryBuilders - UTN FRRe - 2026 | Analizador Léxico y Sintáctico para SmartHome
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def escapar_html(self, texto):
        """Escapa caracteres especiales para HTML"""
        escapes = {
            '&': '&',
            '<': '<',
            '>': '>',
            '"': '"',
            "'": '&#39;'
        }
        for char, escape in escapes.items():
            texto = texto.replace(char, escape)
        return texto
    
    def guardar_html(self):
        """Guarda el HTML generado en un archivo"""
        if not self.tab_html.get(1.0, tk.END).strip():
            messagebox.showwarning("Advertencia", "No hay HTML para guardar")
            return
        
        ruta = filedialog.asksaveasfilename(
            title="Guardar HTML",
            defaultextension=".html",
            filetypes=[("Archivos HTML", "*.html"), ("Todos los archivos", "*.*")]
        )
        
        if ruta:
            try:
                contenido = self.tab_html.get(1.0, tk.END)
                with open(ruta, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                messagebox.showinfo("Éxito", f"HTML guardado en:\n{ruta}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
 