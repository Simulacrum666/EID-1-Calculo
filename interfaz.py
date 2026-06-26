# interfaz.py

import customtkinter as ctk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from factory import crear_conica_desde_rut
from utils import sin_manual, cos_manual, PI
from limites import AnalizadorLimites

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
app.geometry("1200x750")

conica_actual = None

# =========================================================
# LAYOUT PRINCIPAL (Paneles e Interfaz de Pestañas)
# =========================================================

frame_izq = ctk.CTkFrame(app, width=380)
frame_izq.pack(side="left", fill="y", padx=10, pady=10)
frame_izq.pack_propagate(False)

tab_control = ctk.CTkTabview(frame_izq, width=360)
tab_control.pack(expand=True, fill="both", padx=10, pady=10)

tab_conicas = tab_control.add("Secciones Cónicas")
tab_limites = tab_control.add("Funciones por Tramos")

frame_der = ctk.CTkFrame(app)
frame_der.pack(side="right", expand=True, fill="both", padx=10, pady=10)

# =========================================================
# COMPONENTES GLOBALES (Entrada de RUT)
# =========================================================

frame_rut = ctk.CTkFrame(frame_izq, fg_color="transparent")
frame_rut.pack(side="top", fill="x", padx=10, pady=(10, 0))

label_rut = ctk.CTkLabel(frame_rut, text="Ingrese RUT (con DV):", font=("Consolas", 12))
label_rut.pack(pady=(5, 2))

entry_rut = ctk.CTkEntry(frame_rut, placeholder_text="12345678-9", width=200, justify="center")
entry_rut.pack(pady=2)

# =========================================================
# PESTAÑA 1: SECCIONES CÓNICAS (Campos vacíos para la defensa)
# =========================================================

titulo_conicas = ctk.CTkLabel(
    tab_conicas,
    text="Analizador de Cónicas",
    font=("Consolas", 16, "bold")
)
titulo_conicas.pack(pady=5)

# Bloque automatizado obligatorio para las ecuaciones
label_ecuaciones = ctk.CTkLabel(tab_conicas, text="Ecuaciones de la Cónica:", font=("Consolas", 11, "underline"))
label_ecuaciones.pack(pady=(5, 0))

textbox = ctk.CTkTextbox(tab_conicas, width=320, height=110, font=("Consolas", 11))
textbox.pack(pady=5)

# CAMPOS COMPLETAMENTE VACÍOS PARA LA DEFENSA DE CÓNICAS (Requerimiento PDF)
label_defensa_conicas = ctk.CTkLabel(tab_conicas, text="📋 RESPUESTAS EVALUACIÓN ORAL", font=("Consolas", 12, "bold"), text_color="#1f538d")
label_defensa_conicas.pack(pady=(10, 5))

entry_centro = ctk.CTkEntry(tab_conicas, placeholder_text="Centro / Vértice (h, k)", width=300)
entry_centro.pack(pady=2)

entry_vertices = ctk.CTkEntry(tab_conicas, placeholder_text="Vértices (Coordenadas)", width=300)
entry_vertices.pack(pady=2)

entry_focos = ctk.CTkEntry(tab_conicas, placeholder_text="Focos (Coordenadas)", width=300)
entry_focos.pack(pady=2)

entry_eje_mayor = ctk.CTkEntry(tab_conicas, placeholder_text="Eje Mayor / Transverso / Lado Recto", width=300)
entry_eje_mayor.pack(pady=2)

entry_eje_menor = ctk.CTkEntry(tab_conicas, placeholder_text="Eje Menor / Conjugado / Directriz", width=300)
entry_eje_menor.pack(pady=2)

# Función de validación interna de cónicas para el docente
def verificar_respuestas_conica():
    global conica_actual
    if not conica_actual:
        messagebox.showwarning("Aviso", "Primero debe ingresar un RUT y Analizar.")
        return
    
    tipo = conica_actual.tipo
    info = f"Resultados esperados para la {tipo}:\n\n"
    
    if tipo == "Circunferencia":
        norte, sur, este, oeste = conica_actual.obtener_puntos_cardinales()
        info += f"• Centro (h, k): ({conica_actual.h}, {conica_actual.k})\n"
        info += f"• Radio (r): {conica_actual.r:.4f} (r² = {conica_actual.r2})\n"
        info += f"• Puntos Cardinales: N:{norte}, S:{sur}, E:{este}, O:{oeste}\n"
        info += f"• Área: {conica_actual.calcular_area():.4f}\n"
        info += f"• Perímetro: {conica_actual.calcular_perimetro():.4f}\n"
    elif tipo == "Elipse":
        princ, secun = conica_actual.obtener_vertices()
        info += f"• Centro (h, k): ({conica_actual.h}, {conica_actual.k})\n"
        info += f"• Orientación: {conica_actual.orientacion}\n"
        info += f"• Vértices Principales: {princ}\n"
        info += f"• Vértices Secundarios: {secun}\n"
        info += f"• Focos: {conica_actual.focos}\n"
        info += f"• Semiejes: a = {conica_actual.a:.4f}, b = {conica_actual.b:.4f}, c = {conica_actual.c:.4f}\n"
    elif tipo == "Parabola":
        info += f"• Vértice (h, k): {conica_actual.vertice}\n"
        info += f"• Orientación: {conica_actual.orientacion}\n"
        info += f"• Foco: {conica_actual.foco}\n"
        info += f"• Directriz: {conica_actual.obtener_directriz()}\n"
        info += f"• Parámetro p: {conica_actual.p:.4f} (4p = {conica_actual.cuatro_p:.4f})\n"
        info += f"• Lado Recto: {conica_actual.lado_recto:.4f}\n"
    elif tipo == "Hiperbola":
        p1, p2 = conica_actual.obtener_asintotas()
        info += f"• Centro (h, k): ({conica_actual.h}, {conica_actual.k})\n"
        info += f"• Orientación: {conica_actual.orientacion}\n"
        info += f"• Vértices: {conica_actual.vertices}\n"
        info += f"• Focos: {conica_actual.focos}\n"
        info += f"• Semiejes: a = {conica_actual.a:.4f}, b = {conica_actual.b:.4f}, c = {conica_actual.c:.4f}\n"
        info += f"• Pendientes Asíntotas: {p1:.4f} y {p2:.4f}\n"

    messagebox.showinfo("Solucionario Cónicas (Validación)", info)

btn_verificar_conica = ctk.CTkButton(tab_conicas, text="Validar Cónica", fg_color="#2e7d32", hover_color="#1b5e20", command=verificar_respuestas_conica)
btn_verificar_conica.pack(pady=8)

# =========================================================
# PESTAÑA 2: FUNCIONES POR TRAMOS (Límites y Continuidad)
# =========================================================

titulo_limites = ctk.CTkLabel(tab_limites, text="Análisis de Límites", font=("Consolas", 16, "bold"))
titulo_limites.pack(pady=5)

label_caso_rut = ctk.CTkLabel(tab_limites, text="Caso generado: (Esperando RUT)", font=("Consolas", 12, "bold"), text_color="orange", wraplength=300)
label_caso_rut.pack(pady=5)

label_tabla = ctk.CTkLabel(tab_limites, text="Evidencia Numérica (Entornos de a):", font=("Consolas", 11, "underline"))
label_tabla.pack(pady=(5, 0))

textbox_tabla = ctk.CTkTextbox(tab_limites, width=320, height=120, font=("Consolas", 11))
textbox_tabla.pack(pady=5)

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

def verificar_respuestas_alumno():
    rut = entry_rut.get().strip()
    if not rut:
        messagebox.showwarning("Aviso", "Primero debe ingresar un RUT y Analizar.")
        return
    try:
        lim_obj = AnalizadorLimites(rut)
        verdades = lim_obj.obtener_analisis_teorico()
        
        messagebox.showinfo(
            "Solucionario Límites (Validación)", 
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

btn_verificar = ctk.CTkButton(tab_limites, text="Validar Límites", fg_color="#2e7d32", hover_color="#1b5e20", command=verificar_respuestas_alumno)
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
# LÓGICA DE RE-DIBUJO DE CÓNICAS
# =========================================================

def graficar_conica(conica):
    ax.clear()
    tipo = conica.tipo
    pasos = 400

    if tipo == "Circunferencia":
        puntos_x, puntos_y = [], []
        for i in range(pasos + 1):
            t = 2 * PI * i / pasos
            puntos_x.append(conica.h + conica.r * cos_manual(t))
            puntos_y.append(conica.k + conica.r * sin_manual(t))
        ax.plot(puntos_x, puntos_y, color="royalblue", linewidth=2, label="Circunferencia")
        ax.scatter([conica.h], [conica.k], color="red", zorder=5, label="Centro")

    elif tipo == "Elipse":
        puntos_x, puntos_y = [], []
        for i in range(pasos + 1):
            t = 2 * PI * i / pasos
            if conica.orientacion == "Horizontal":
                puntos_x.append(conica.h + conica.a * cos_manual(t))
                puntos_y.append(conica.k + conica.b * sin_manual(t))
            else:
                puntos_x.append(conica.h + conica.b * cos_manual(t))
                puntos_y.append(conica.k + conica.a * sin_manual(t))
        ax.plot(puntos_x, puntos_y, color="seagreen", linewidth=2, label="Elipse")
        ax.scatter([conica.h], [conica.k], color="black", zorder=5, label="Centro")

    elif tipo == "Parabola":
        if conica.orientacion == "Vertical":
            xs = [conica.h - 10 + (i * 20 / pasos) for i in range(pasos + 1)]
            ys = [((x - conica.h)**2 / (4 * conica.p)) + conica.k for x in xs]
        else:
            ys = [conica.k - 10 + (i * 20 / pasos) for i in range(pasos + 1)]
            xs = [((y - conica.k)**2 / (4 * conica.p)) + conica.h for y in ys]
        ax.plot(xs, ys, color="darkorange", linewidth=2, label="Parábola")
        ax.scatter([conica.vertice[0]], [conica.vertice[1]], color="red", zorder=5, label="Vértice")

    elif tipo == "Hiperbola":
        t_vals = [-2.5 + (i * 5 / pasos) for i in range(pasos + 1) if i != pasos//2]
        for signo in [-1, 1]:
            xs, ys = [], []
            for t in t_vals:
                import math
                try:
                    cosh_t = math.cosh(t)
                    sinh_t = math.sinh(t)
                    if conica.orientacion == "Horizontal":
                        xs.append(conica.h + conica.a * cosh_t * signo)
                        ys.append(conica.k + conica.b * sinh_t)
                    else:
                        xs.append(conica.h + conica.b * sinh_t)
                        ys.append(conica.k + conica.a * cosh_t * signo)
                except:
                    continue
            ax.plot(xs, ys, color="crimson", linewidth=2)
        ax.scatter([conica.h], [conica.k], color="black", zorder=5, label="Centro")

    _ejes(f"{tipo} — RUT: {conica.rut}")

def mostrar_info(conica):
    """Muestra exclusivamente los datos iniciales y ecuaciones requeridas."""
    textbox.delete("0.0", "end")
    textbox.insert("end", f"Tipo de Cónica: {conica.tipo}\n")
    textbox.insert("end", f"Ecuación General:\n {conica.ecuacion_general()}\n\n")
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
        if pestana_activa == "Secciones Cónicas":
            conica_actual = crear_conica_desde_rut(rut)
            mostrar_info(conica_actual)
            graficar_conica(conica_actual)
            
            # Forzar el blanqueamiento de los campos para la evaluación de cónicas
            entry_centro.delete(0, "end")
            entry_vertices.delete(0, "end")
            entry_focos.delete(0, "end")
            entry_eje_mayor.delete(0, "end")
            entry_eje_menor.delete(0, "end")
            
        elif pestana_activa == "Funciones por Tramos":
            ax.clear()
            obj_lim = AnalizadorLimites(rut)
            label_caso_rut.configure(text=obj_lim.obtener_nombre_caso())
            
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

            puntos_x = [obj_lim.a - 5 + (i * 10 / 250) for i in range(251)]
            puntos_y = []
            for px in puntos_x:
                puntos_y.append(obj_lim.evaluar_funcion(px, aproximacion=True))
                
            ax.plot(puntos_x, puntos_y, color="purple", linewidth=2.5, label="f(x)")
            
            if obj_lim.caso == 3:
                ax.axvline(obj_lim.a, color="red", linestyle="--", alpha=0.7, label=f"Asíntota (x={obj_lim.a})")
            
            ax.axvline(obj_lim.a, color="gray", linestyle=":", alpha=0.4)
            _ejes(f"Función por Tramos — (Punto Crítico a = {obj_lim.a})")
            
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
    
    # Limpiar campos de cónicas
    entry_centro.delete(0, "end")
    entry_vertices.delete(0, "end")
    entry_focos.delete(0, "end")
    entry_eje_mayor.delete(0, "end")
    entry_eje_menor.delete(0, "end")
    
    # Limpiar campos de límites
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

app.mainloop()