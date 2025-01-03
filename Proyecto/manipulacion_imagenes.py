import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def cargar_imagen(ruta):
    """Carga una imagen desde la ruta especificada y la convierte a escala de grises."""
    imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        raise FileNotFoundError("No se pudo cargar la imagen. Verifica la ruta.")
    return imagen

def rotar_imagen(imagen, angulo):
    """Aplica una rotación a la imagen."""
    filas, columnas = imagen.shape
    matriz_rotacion = cv2.getRotationMatrix2D((columnas / 2, filas / 2), angulo, 1)
    return cv2.warpAffine(imagen, matriz_rotacion, (columnas, filas))

def escalar_imagen(imagen, factor_x, factor_y):
    """Escala la imagen por los factores especificados."""
    return cv2.resize(imagen, None, fx=factor_x, fy=factor_y, interpolation=cv2.INTER_LINEAR)

def reflejar_imagen(imagen, eje):
    """Refleja la imagen sobre el eje especificado."""
    if eje == 'horizontal':
        return cv2.flip(imagen, 0)
    elif eje == 'vertical':
        return cv2.flip(imagen, 1)
    else:
        raise ValueError("El eje debe ser 'horizontal' o 'vertical'.")

def trasladar_imagen(imagen, desplazamiento_x, desplazamiento_y):
    """Aplica una traslación a la imagen."""
    filas, columnas = imagen.shape
    matriz_traslacion = np.float32([[1, 0, desplazamiento_x], [0, 1, desplazamiento_y]])
    return cv2.warpAffine(imagen, matriz_traslacion, (columnas, filas))

def mostrar_imagen(imagen_cv):
    """Convierte la imagen de OpenCV a un formato compatible con Tkinter y la muestra."""
    imagen_pil = Image.fromarray(imagen_cv)
    return ImageTk.PhotoImage(imagen_pil)

def cargar_archivo():
    """Abre un cuadro de diálogo para seleccionar una imagen y cargarla."""
    global imagen_original, imagen_transformada, tk_imagen_original
    ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg;*.png")])
    if ruta:
        try:
            imagen_original = cargar_imagen(ruta)
            tk_imagen_original = mostrar_imagen(imagen_original)
            etiqueta_imagen_original.config(image=tk_imagen_original)
            etiqueta_imagen_original.image = tk_imagen_original
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))

def aplicar_transformacion():
    """Aplica la transformación seleccionada a la imagen."""
    global imagen_transformada, tk_imagen_transformada
    if imagen_original is None:
        messagebox.showerror("Error", "Primero carga una imagen.")
        return

    try:
        if opcion_transformacion.get() == "Rotar":
            angulo = float(entrada_parametro_1.get())
            imagen_transformada = rotar_imagen(imagen_original, angulo)
        elif opcion_transformacion.get() == "Escalar":
            factor_x = float(entrada_parametro_1.get())
            factor_y = float(entrada_parametro_2.get())
            imagen_transformada = escalar_imagen(imagen_original, factor_x, factor_y)
        elif opcion_transformacion.get() == "Reflejar":
            eje = entrada_parametro_1.get().strip().lower()
            imagen_transformada = reflejar_imagen(imagen_original, eje)
        elif opcion_transformacion.get() == "Trasladar":
            desplazamiento_x = int(entrada_parametro_1.get())
            desplazamiento_y = int(entrada_parametro_2.get())
            imagen_transformada = trasladar_imagen(imagen_original, desplazamiento_x, desplazamiento_y)
        else:
            messagebox.showerror("Error", "Selecciona una transformación válida.")
            return

        tk_imagen_transformada = mostrar_imagen(imagen_transformada)
        etiqueta_imagen_transformada.config(image=tk_imagen_transformada)
        etiqueta_imagen_transformada.image = tk_imagen_transformada
    except Exception as e:
        messagebox.showerror("Error", str(e))

def guardar_imagen():
    """Guarda la imagen transformada en un archivo."""
    if imagen_transformada is None:
        messagebox.showerror("Error", "No hay una imagen transformada para guardar.")
        return

    ruta = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Imágenes", "*.jpg;*.png")])
    if ruta:
        cv2.imwrite(ruta, imagen_transformada)
        messagebox.showinfo("Éxito", "Imagen guardada correctamente.")

def actualizar_campos(*args):
    """Actualiza los campos de entrada según la opción seleccionada."""
    for widget in [etiqueta_parametro_1, entrada_parametro_1, etiqueta_parametro_2, entrada_parametro_2]:
        widget.pack_forget()

    if opcion_transformacion.get() == "Rotar":
        etiqueta_parametro_1.config(text="Ángulo:")
        etiqueta_parametro_1.pack(pady=5)
        entrada_parametro_1.pack(pady=5, ipadx=5, ipady=5)
    elif opcion_transformacion.get() == "Escalar":
        etiqueta_parametro_1.config(text="Factor X:")
        etiqueta_parametro_1.pack(pady=5)
        entrada_parametro_1.pack(pady=5, ipadx=5, ipady=5)
        etiqueta_parametro_2.config(text="Factor Y:")
        etiqueta_parametro_2.pack(pady=5)
        entrada_parametro_2.pack(pady=5, ipadx=5, ipady=5)
    elif opcion_transformacion.get() == "Reflejar":
        etiqueta_parametro_1.config(text="Eje ('horizontal' o 'vertical'):")
        etiqueta_parametro_1.pack(pady=5)
        entrada_parametro_1.pack(pady=5, ipadx=5, ipady=5)
    elif opcion_transformacion.get() == "Trasladar":
        etiqueta_parametro_1.config(text="Desplazamiento X:")
        etiqueta_parametro_1.pack(pady=5)
        entrada_parametro_1.pack(pady=5, ipadx=5, ipady=5)
        etiqueta_parametro_2.config(text="Desplazamiento Y:")
        etiqueta_parametro_2.pack(pady=5)
        entrada_parametro_2.pack(pady=5, ipadx=5, ipady=5)

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Manipulación de Imágenes")
ventana.geometry("1000x700")
ventana.configure(bg="#2b2b2b")

# Variables globales
imagen_original = None
imagen_transformada = None
tk_imagen_original = None
tk_imagen_transformada = None

# Configuración de estilos
estilo_label = {"bg": "#2b2b2b", "fg": "#ffffff", "font": ("Arial", 14)}
estilo_button = {"bg": "#444444", "fg": "#ffffff", "font": ("Arial", 12), "relief": "flat", "activebackground": "#555555"}

# Marco de controles
marco_controles = tk.Frame(ventana, bg="#2b2b2b")
marco_controles.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

boton_cargar = tk.Button(marco_controles, text="Cargar Imagen", command=cargar_archivo, **estilo_button)
boton_cargar.pack(pady=10, ipadx=5, ipady=5)

opcion_transformacion = tk.StringVar(value="Rotar")
opcion_transformacion.trace("w", actualizar_campos)
menu_transformaciones = tk.OptionMenu(marco_controles, opcion_transformacion, "Rotar", "Escalar", "Reflejar", "Trasladar")
menu_transformaciones.config(bg="#444444", fg="#ffffff", font=("Arial", 12), activebackground="#555555", relief="flat")
menu_transformaciones.pack(pady=10, ipadx=5, ipady=5)

etiqueta_parametro_1 = tk.Label(marco_controles, text="Ángulo:", **estilo_label)
entrada_parametro_1 = tk.Entry(marco_controles, font=("Arial", 12))
etiqueta_parametro_2 = tk.Label(marco_controles, text="Factor Y:", **estilo_label)
entrada_parametro_2 = tk.Entry(marco_controles, font=("Arial", 12))

boton_aplicar = tk.Button(marco_controles, text="Aplicar Transformación", command=aplicar_transformacion, **estilo_button)
boton_aplicar.pack(pady=10, ipadx=5, ipady=5)

boton_guardar = tk.Button(marco_controles, text="Guardar Imagen", command=guardar_imagen, **estilo_button)
boton_guardar.pack(pady=10, ipadx=5, ipady=5)

# Marcos para mostrar imágenes
marco_imagenes = tk.Frame(ventana, bg="#2b2b2b")
marco_imagenes.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

etiqueta_imagen_original = tk.Label(marco_imagenes, text="Imagen Original", **estilo_label)
etiqueta_imagen_original.pack(side=tk.LEFT, padx=10, pady=10)

etiqueta_imagen_transformada = tk.Label(marco_imagenes, text="Imagen Transformada", **estilo_label)
etiqueta_imagen_transformada.pack(side=tk.RIGHT, padx=10, pady=10)

# Inicia con los campos actualizados
actualizar_campos()

ventana.mainloop()
