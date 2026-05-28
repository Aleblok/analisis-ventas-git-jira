import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Definimos rutas relativas para que el proyecto sea reproducible en Google Colab
RUTA_DATOS = Path("datos/ventas.csv")
RUTA_RESULTADOS = Path("resultados")
RUTA_RESULTADOS.mkdir(exist_ok=True)

# Lectura del dataset de ventas
ventas = pd.read_csv(RUTA_DATOS)

# Conversión de la columna fecha a formato datetime para poder agrupar por mes
ventas["fecha"] = pd.to_datetime(ventas["fecha"])

# Cálculo del importe total de cada venta
ventas["total_venta"] = ventas["cantidad"] * ventas["precio_unitario"]

# Indicador 1: ventas totales del período analizado
ventas_totales = ventas["total_venta"].sum()

# Indicador 2: producto más vendido según cantidad total
ventas_por_producto = ventas.groupby("producto")["cantidad"].sum().sort_values(ascending=False)
producto_mas_vendido = ventas_por_producto.idxmax()
cantidad_producto_mas_vendido = ventas_por_producto.max()

# Indicador 3: ventas mensuales
ventas["mes"] = ventas["fecha"].dt.to_period("M").astype(str)
ventas_por_mes = ventas.groupby("mes")["total_venta"].sum().reset_index()

# Guardado de resumen general en archivo CSV
resumen = pd.DataFrame({
    "indicador": [
        "Ventas totales",
        "Producto más vendido",
        "Cantidad vendida del producto más vendido"
    ],
    "valor": [
        ventas_totales,
        producto_mas_vendido,
        cantidad_producto_mas_vendido
    ]
})

resumen.to_csv(RUTA_RESULTADOS / "resumen_ventas.csv", index=False)
ventas_por_mes.to_csv(RUTA_RESULTADOS / "ventas_por_mes.csv", index=False)

# Generación de gráfico de evolución mensual de ventas
plt.figure(figsize=(8, 5))
plt.plot(ventas_por_mes["mes"], ventas_por_mes["total_venta"], marker="o")
plt.title("Evolución mensual de ventas")
plt.xlabel("Mes")
plt.ylabel("Total de ventas")
plt.grid(True)
plt.tight_layout()
plt.savefig(RUTA_RESULTADOS / "grafico_ventas_mensuales.png")
plt.close()

# Salida por consola para verificar la ejecución del análisis
print("Análisis de ventas finalizado correctamente.")
print(f"Ventas totales: {ventas_totales}")
print(f"Producto más vendido: {producto_mas_vendido}")
print(f"Cantidad vendida del producto más vendido: {cantidad_producto_mas_vendido}")
print("Archivos generados en la carpeta resultados.")
