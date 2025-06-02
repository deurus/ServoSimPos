import re
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import Tk, filedialog
from sklearn.linear_model import LinearRegression

def corregir_salto_angular(th):
    th_corr = th.copy()
    for i in range(1, len(th_corr)):
        if th_corr[i] - th_corr[i - 1] < -300:
            th_corr[i:] += 360
    return th_corr

# --- Selección de archivo ---
Tk().withdraw()
ruta_archivo = filedialog.askopenfilename(
    title="Selecciona el archivo .m con datos",
    filetypes=[("Archivos MATLAB", "*.m")]
)

if not ruta_archivo:
    raise FileNotFoundError("No se seleccionó ningún archivo.")

base_name = os.path.splitext(os.path.basename(ruta_archivo))[0]
nombre_txt = f"{base_name}_modelo.txt"

with open(ruta_archivo, "r", encoding="utf-8") as f:
    contenido = f.read()

coincidencias = re.findall(r"data\s*=\s*\[([\s\S]+?)\];", contenido)
if not coincidencias:
    raise ValueError("No se encontró el bloque 'data = [...]' en el archivo.")

filas = coincidencias[0].strip().split("\n")
datos = np.array([[float(val) for val in fila.strip().split()] for fila in filas])

# Asignar columnas
t, th, w, u, ref = datos.T
th = corregir_salto_angular(th)

# --- Análisis de tramos ---
eps = 1e-3
cambios = np.where(np.abs(np.diff(u)) > eps)[0] + 1
segmentos = [(0, cambios[0])] + [(cambios[i], cambios[i + 1]) for i in range(len(cambios) - 1)] + [(cambios[-1], len(u))]
segmentos = segmentos[1:]  # Eliminar arranque

ganancias = []

plt.figure(figsize=(10, 6))
for i, (ini, fin) in enumerate(segmentos, start=1):
    t_seg = t[ini:fin]
    th_seg = th[ini:fin]
    u_val = u[ini]

    if len(t_seg) < 5:
        continue

    model = LinearRegression()
    model.fit(t_seg.reshape(-1, 1), th_seg)
    pendiente = model.coef_[0]
    th_fit = model.predict(t_seg.reshape(-1, 1))

    ganancias.append((i, u_val, pendiente))

    # Graficar
    plt.plot(t_seg, th_seg, label=f'U={u_val:.2f} V')
    plt.plot(t_seg, th_fit, linestyle='--', linewidth=1, color='black')

plt.title("Tramos de posición (th) y regresiones lineales")
plt.xlabel("Tiempo (s)")
plt.ylabel("Ángulo (°)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(f"{base_name}_tramos.png", dpi=300)
plt.show()

# --- Modelo global ---
if ganancias:
    U_vals, vel = zip(*[(u, p) for _, u, p in ganancias])
    modelo = LinearRegression().fit(np.array(U_vals).reshape(-1, 1), np.array(vel))
    K = modelo.coef_[0]

    with open(nombre_txt, "w", encoding="utf-8") as ftxt:
        ftxt.write("MODELO IDENTIFICADO\n")
        ftxt.write("-------------------\n")
        ftxt.write(f"G(s) = {K:.4f} / s\n\n")

        ftxt.write("GANANCIAS POR TRAMO\n")
        ftxt.write("-------------------\n")
        for tramo, u_val, pend in ganancias:
            ftxt.write(f"Tramo {tramo}: U = {u_val:.2f} V → Velocidad ≈ {pend:.2f} °/s\n")
        
        ftxt.write("\nSINTONÍAS RECOMENDADAS\n")
        ftxt.write("-----------------------\n")

        # Sintonía LAMBDA (PI)
        ftxt.write("Método LAMBDA (PI puro)\n")
        for lam in [1, 2, 3, 5]:
            Kc = lam / K
            Ti = lam
            ftxt.write(f"λ = {lam:.1f} → Kc = {Kc:.4f}, Ti = {Ti:.4f}, Td = 0\n")

        # Sintonía tipo SERVO PI
        Kc_servo_PI = 0.8 / K
        Ti_servo_PI = 1.5
        ftxt.write("\nTipo SERVO (PI)\n")
        ftxt.write(f"Kc = {Kc_servo_PI:.4f}, Ti = {Ti_servo_PI:.4f}, Td = 0\n")

        # Sintonía tipo SERVO PID
        Kc_servo_PID = 1.2 / K
        Ti_servo_PID = 2
        Td_servo_PID = 0.5
        ftxt.write("\nTipo SERVO (PID)\n")
        ftxt.write(f"Kc = {Kc_servo_PID:.4f}, Ti = {Ti_servo_PID:.4f}, Td = {Td_servo_PID:.4f}\n")

    print(f"\nModelo estimado: G(s) = {K:.2f} / s")
    print(f"Archivo generado: {nombre_txt} + gráfico PNG")
else:
    print("No se obtuvieron tramos válidos.")
