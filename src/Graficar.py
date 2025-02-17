import matplotlib.pyplot as plt
import numpy as np

# Ruta del archivo
file_path = "src/RESULTS/results.txt"

# Listas para almacenar los datos
similitud_generada = []
similitud_mejorada = []

# Leer el archivo y extraer los datos
with open(file_path, "r") as file:
    for line in file:
        if "|" in line:  # Asegurar que la línea tiene datos válidos
            izquierda, derecha = map(float, line.strip().split("|"))
            similitud_generada.append(izquierda)
            similitud_mejorada.append(derecha)

# Crear el gráfico
mejor_generada = 0
mejor_mejorada = 0
total_datos = len(similitud_mejorada)
for i in range(total_datos):
    if similitud_mejorada[i] >= similitud_generada[i]:
        mejor_mejorada += 1
    else:
        mejor_generada += 1

# Determinar posiciones para los ticks del eje X (cada 10%)
num_ticks = 10  # Para 10%, 20%, ..., 100%
tick_positions = np.linspace(0, total_datos - 1, num_ticks + 1, dtype=int)
tick_labels = [f"{int(p)}%" for p in np.linspace(0, 100, num_ticks + 1)]

print(f"Mejor mejorada: {mejor_mejorada}/{total_datos}")
print(f"Mejor generada: {mejor_generada}/{total_datos}")

similitud_generada.sort()
similitud_mejorada.sort()
plt.figure(figsize=(10, 5))
plt.plot(similitud_mejorada, label="Similitud de la descripción mejorada", marker="s")
plt.plot(similitud_generada, label="Similitud de la descripción generada", marker="o")
plt.xlabel("Porcentaje de datos graficados")
plt.ylabel("Similitud")
plt.title("Similitud frente a descripción original")
plt.legend()
plt.grid(True)
plt.xticks(ticks=tick_positions, labels=tick_labels)
plt.axhline(y=0.5, color='red', linestyle='--')

# Mostrar el gráfico
plt.show()
