import pandas as pd

from analisis_datos import calcular_promedio_precio, calcular_ingreso_total, calcular_top_productos, calcular_fecha_ventas
from consulta_datos import consultar_datos_ventas


#funcion para imprimir en consola y retornar un diccionario para la API
def obtener_datos_ventas(fecha_inicio=None, fecha_fin=None):
    
    datos = consultar_datos_ventas()
    
    if fecha_inicio or fecha_fin:
        fechas = pd.to_datetime(datos["fecha"], errors="coerce").dt.date
        if fecha_inicio:
            datos = datos.loc[fechas >= fecha_inicio]
        if fecha_fin:
            datos = datos.loc[fechas <= fecha_fin]

    #INGRESO TOTAL
    ingreso_total = calcular_ingreso_total(datos)

    #PROMEDIO DE PRECIO
    promedio_precio = calcular_promedio_precio(datos)

    #TOP 5 PRODUCTOS
    top_cinco = calcular_top_productos(datos).head(5)

    #MEJOR FECHA DE VENTAS
    ventas_por_fecha = calcular_fecha_ventas(datos).sort_values(by="fecha")
    top_fecha = ventas_por_fecha.sort_values(by="cantidad", ascending=False).head(1)

    #RETURN PARA LA API
    return {
        "ingreso total": float(ingreso_total),
        "promedio_precio": float(promedio_precio) if pd.notna(promedio_precio) else None,
        "unidades_vendidas": int(datos["cantidad"].sum()),
        "top_productos": top_cinco.to_dict(orient="records"),
        "top_fecha": top_fecha.to_dict(orient="records"),
        "ventas_por_fecha": ventas_por_fecha.to_dict(orient="records")
    }


if __name__ == "__main__":
    analisis = obtener_datos_ventas()
