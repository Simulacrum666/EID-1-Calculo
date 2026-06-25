# interfaz.py

import customtkinter as ctk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from factory import crear_conica_desde_rut
from limites import AnalizadorLimites  # Importación del nuevo módulo de límites
from graficador import dibujar_conica  # Lógica de dibujo de cónicas, separada de la GUI

# =========================================================
# CONFIG
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =========================================================
# VENTANA PRINCIPAL
# =========================================================

app = ctk.CTk()
app.title("Proyecto MAT1186 - Evaluación Integrada")
app.geometry("1200x720")

conica_actual = None

# =========================================================
# LAYOUT PRINCIPAL (Paneles e Interfaz de Pestañas)
# =========================================================

# Panel Izquierdo que contendrá las pestañas de control
frame_izq = ctk.CTkFrame(app, width=380)
frame_izq.pack(side="left", fill="y", padx=10, pady=10)
frame_izq.pack_propagate(False)

# Control de Pestañas
tab_control = ctk.CTkTabview(frame_izq, width=360)
tab_control.pack(expand=True, fill="both", padx=10, pady=10)

tab_conicas = tab_control.add("Secciones Cónicas")
tab_limites = tab_control.add("Funciones por Tramos")

# Panel Derecho para el gráfico (Matplotlib integrado)
frame_der = ctk.CTkFrame(app)
frame_der.pack(side="right", expand=True, fill="both", padx=10, pady=10)

# =========================================================
# COMPONENTES GLOBALES (Entrada de RUT en la parte superior)
# =========================================================

# Para no duplicar la entrada de RUT, la dejamos arriba en el panel izquierdo
frame_rut = ctk.CTkFrame(frame_izq, fg_color="transparent")
frame_rut.pack(side="top", fill="x", padx=10, pady=(10, 0))

label_rut = ctk.CTkLabel(frame_rut, text="Ingrese RUT (con DV):", font=("Consolas", 12))
label_rut.pack(pady=(5, 2))

entry_rut = ctk.CTkEntry(frame_rut, placeholder_text="12345678-9", width=200, justify="center")
entry_rut.pack(pady=2)

# =========================================================
# PESTAÑA 1: SECCIONES CÓNICAS (Tus elementos originales)
# =========================================================

titulo_conicas = ctk.CTkLabel(
    tab_conicas,
    text="Analizador de Cónicas",
    font=("Consolas", 16, "bold")
)
titulo_conicas.pack(pady=10)

textbox = ctk.CTkTextbox(tab_conicas, width=320, height=340, font=("Consolas", 11))
textbox.pack(pady=10, expand=True, fill="both")

# =========================================================
# PESTAÑA 2: FUNCIONES POR TRAMOS (Límites y Continuidad)
# =========================================================

titulo_limites = ctk.CTkLabel(
    tab_limites,
    text="Análisis de Límites",
    font=("Consolas", 16, "bold")
)
titulo_limites.pack(pady=10)

label_caso_rut = ctk.CTkLabel(
    tab_limites, 
    text="Caso generado: (Esperando RUT)", 
    font=("Consolas", 12, "bold"), 
    text_color="orange",
    wraplength=300
)
label_caso_rut.pack(pady=5)

# Tabla visual usando un TextBox para la evidencia computacional
label_tabla = ctk.CTkLabel(tab_limites, text="Evidencia Numérica (Entornos de a):", font=("Consolas", 11, "underline"))
label_tabla.pack(pady=(5, 0))

textbox_tabla = ctk.CTkTextbox(tab_limites, width=320, height=130, font=("Consolas", 11))
textbox_tabla.pack(pady=5)

# CAMPOS COMPLETAMENTE VACÍOS PARA LA DEFENSA ORAL (Requerimiento estricto)
label_defensa = ctk.CTkLabel(tab_limites, text="📋 RESPUESTAS EVALUACIÓN ORAL", font=("Consolas", 12, "bold"), text_color="#1f538d")
label_defensa.pack(pady=(10, 5))

entry_lim_izq = ctk.CTkEntry(tab_limites, placeholder_text="Límite por Izquierda (L⁻)", width=300)
entry_lim_izq.pack(pady=2)

entry_lim_der = ctk.CTkEntry(tab_limites, placeholder_text="Límite por Derecha (L⁺)", width=300)
entry_lim_der.pack(pady=2)

entry_existe = ctk.CTkEntry(tab_limites, placeholder_text="¿Existe el límite en x=a? (Sí/No)", width=300)
entry_existe.pack(pady=2)

entry_f_a = ctk.CTkEntry(tab_limites, placeholder_text="Valor exacto de f(a)", width=300)
entry_f_a.pack(pady=2)

entry_tipo_disc = ctk.CTkEntry(tab_limites, placeholder_text="Tipo de Discontinuidad", width=300)
entry_tipo_disc.pack(pady=2)

# Función interna de validación para la comisión evaluadora
def verificar_respuestas_alumno():
    rut = entry_rut.get().strip()
    if not rut:
        messagebox.showwarning("Aviso", "Primero debe ingresar un RUT y Analizar.")
        return
    try:
        lim_obj = AnalizadorLimites(rut)
        verdades = lim_obj.obtener_analisis_teorico()
        
        messagebox.showinfo(
            "Solucionario Interno (Validación)", 
            f"Resultados esperados para el análisis:\n\n"
            f"• Límite Izquierdo: {verdades['limite_izquierdo']}\n"
            f"• Límite Derecho: {verdades['limite_derecho']}\n"
            f"• ¿Existe Límite?: {verdades['existe_limite']}\n"
            f"• Valor f(a): {verdades['valor_funcion']}\n"
            f"• Tipo de Discontinuidad: {verdades['tipo_discontinuidad']}\n\n"
            f"Justificación:\n{verdades['justificacion']}"
        )
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo validar: {str(e)}")

btn_verificar = ctk.CTkButton(tab_limites, text="Validar Respuestas", fg_color="#2e7d32", hover_color="#1b5e20", command=verificar_respuestas_alumno)
btn_verificar.pack(pady=8)

# =========================================================
# CONFIGURACIÓN DEL LIENZO DE MATPLOTLIB
# =========================================================

fig, ax = plt.subplots(figsize=(6, 5))
canvas = FigureCanvasTkAgg(fig, master=frame_der)
canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

def _ejes(titulo_grafico=""):
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.axvline(0, color="gray", linewidth=0.8)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.set_title(titulo_grafico, fontname="Consolas", fontsize=12, fontweight="bold")
    canvas.draw()

def limpiar_grafico():
    ax.clear()
    _ejes("Gráfico")

# Inicializar ejes limpios
_ejes("Gráfico")

# =========================================================
# GRAFICADO DE CÓNICAS (la lógica de dibujo vive en graficador.py)
# =========================================================

def graficar_conica(conica):
    ax.clear()
    dibujar_conica(ax, conica)
    _ejes(f"{conica.tipo} — RUT: {conica.rut}")

# =========================================================
# FUNCIÓN MODIFICADA: mostrar_info (Punto 1 implementado)
# =========================================================
def mostrar_info(conica):
    textbox.delete("0.0", "end")
    textbox.insert("end", f"RUT: {conica.rut}\n\n")

    textbox.insert("end", "── Validación del RUT (Módulo 11) ──\n")
    for paso in conica.pasos_validacion:
        textbox.insert("end", f" {paso}\n")
    textbox.insert("end", "\n")

    # === NUEVO: Inserción de los Pasos de Construcción de Coeficientes ===
    if hasattr(conica, 'pasos_construccion'):
        for paso in conica.pasos_construccion:
            textbox.insert("end", f"{paso}\n")
        textbox.insert("end", "\n")

    textbox.insert("end", f"Tipo de Cónica: {conica.tipo}\n")
    textbox.insert("end", f"Coeficientes Finales:\n")
    textbox.insert("end", f" A = {conica.A:.2f}, B = {conica.B:.2f}\n")
    textbox.insert("end", f" C = {conica.C:.2f}, D = {conica.D:.2f}, E = {conica.E:.2f}\n\n")

    textbox.insert("end", "Ecuación General:\n")
    try:
        textbox.insert("end", f" {conica.ecuacion_general()}\n\n")
    except AttributeError:
        textbox.insert("end", f" {conica.A:.2f}x² + {conica.B:.2f}y² + {conica.C:.2f}x + {conica.D:.2f}y + {conica.E:.2f} = 0\n\n")

    textbox.insert("end", f"Ecuación Canónica:\n {conica.ecuacion_canonica()}\n")

# =========================================================
# OPERACIONES CENTRALES (Analizar / Limpiar)
# =========================================================

def analizar():
    global conica_actual
    rut = entry_rut.get().strip()
    if not rut:
        messagebox.showwarning("Error", "Ingrese un RUT")
        return
        
    pestana_activa = tab_control.get()
    
    try:
        # CASO A: El usuario está viendo la pestaña de Cónicas
        if pestana_activa == "Secciones Cónicas":
            conica_actual = crear_conica_desde_rut(rut)
            mostrar_info(conica_actual)
            graficar_conica(conica_actual)
            
        # CASO B: El usuario está viendo la pestaña de Límites
        elif pestana_activa == "Funciones por Tramos":
            ax.clear()
            obj_lim = AnalizadorLimites(rut)
            
            # 1. Mostrar la regla del caso detectado en la etiqueta
            label_caso_rut.configure(text=obj_lim.obtener_nombre_caso())
            
            # 2. Población manual de la tabla de aproximación (Evidencia Computacional)
            izq, der = obj_lim.generar_tabla_valores()
            textbox_tabla.delete("0.0", "end")
            textbox_tabla.insert("end", f" x (Izq)  │ f(x)       │ x (Der)  │ f(x)\n")
            textbox_tabla.insert("end", f"──────────┼────────────┼──────────┼────────────\n")
            
            for i in range(len(izq)):
                x_izq, y_izq = izq[i]
                x_der, y_der = der[i]
                
                str_izq = f"{y_izq:.4f}" if y_izq is not None else "Indef."
                str_der = f"{y_der:.4f}" if y_der is not None else "Indef."
                
                textbox_tabla.insert("end", f" {x_izq:<8.3f} │ {str_izq:<10} │ {x_der:<8.3f} │ {str_der:<10}\n")

            # 3. Graficado manual de la función por tramos (Sin NumPy)
            puntos_x = [obj_lim.a - 5 + (i * 10 / 250) for i in range(251)]
            puntos_y = []
            
            for px in puntos_x:
                puntos_y.append(obj_lim.evaluar_funcion(px, aproximacion=True))
                
            ax.plot(puntos_x, puntos_y, color="purple", linewidth=2.5, label="f(x)")
            
            if obj_lim.caso == 3:
                ax.axvline(obj_lim.a, color="red", linestyle="--", alpha=0.7, label=f"Asíntota (x={obj_lim.a})")
            
            ax.axvline(obj_lim.a, color="gray", linestyle=":", alpha=0.4)
            
            _ejes(f"Función por Tramos — (Punto Crítico a = {obj_lim.a})")
            
            # 4. Forzar el blanqueamiento de los campos para la evaluación del alumno
            entry_lim_izq.delete(0, "end")
            entry_lim_der.delete(0, "end")
            entry_existe.delete(0, "end")
            entry_f_a.delete(0, "end")
            entry_tipo_disc.delete(0, "end")

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def limpiar():
    global conica_actual
    conica_actual = None
    entry_rut.delete(0, "end")
    textbox.delete("0.0", "end")
    textbox_tabla.delete("0.0", "end")
    label_caso_rut.configure(text="Caso generado: (Esperando RUT)")
    
    # Limpiar campos de la defensa
    entry_lim_izq.delete(0, "end")
    entry_lim_der.delete(0, "end")
    entry_existe.delete(0, "end")
    entry_f_a.delete(0, "end")
    entry_tipo_disc.delete(0, "end")
    
    limpiar_grafico()

# =========================================================
# BOTONES DE ACCIÓN PRINCIPALES
# =========================================================

frame_botones = ctk.CTkFrame(frame_izq, fg_color="transparent")
frame_botones.pack(side="bottom", fill="x", padx=10, pady=10)

btn_analizar = ctk.CTkButton(frame_botones, text="Analizar RUT", fg_color="#1f538d", command=analizar)
btn_analizar.pack(side="left", expand=True, padx=5, pady=5)

btn_limpiar = ctk.CTkButton(frame_botones, text="Limpiar Todo", fg_color="#555555", command=limpiar)
btn_limpiar.pack(side="right", expand=True, padx=5, pady=5)


def cerrar_aplicacion():
    # Destruye la ventana de manera segura y detiene los hilos/tareas pendientes
    app.quit()
    app.destroy()

# Indicarle a CustomTkinter que use nuestra función al presionar la 'X' de cerrar
app.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

# Lanzar la aplicación
app.mainloop()
