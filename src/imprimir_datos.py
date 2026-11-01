from analisis_datos import calcular_promedio_precio, calcular_ingreso_total, calcular_top_productos, calcular_fecha_ventas
from consulta_datos import consultar_datos_ventas


#funcion para imprimir en consola y retornar un diccionario para la API
def obtener_datos_ventas():
    datos = consultar_datos_ventas()

    #INGRESO TOTAL
    ingreso_total = calcular_ingreso_total(datos)
    print(f"Ingreso total: ${ingreso_total} MXN")
        
    #PROMEDIO DE PRECIO
    promedio_precio = calcular_promedio_precio(datos)
    print(f"Promedio de precio: ${promedio_precio} MXN")
    
    #TOP 5 PRODUCTOS
    top_cinco = calcular_top_productos(datos).head(5)
    print(f"Top 5: {top_cinco}") 
    
    #MEJOR FECHA DE VENTAS
    top_fecha = calcular_fecha_ventas(datos).head(1)
    print(f"Mejor fecha de ventas: {top_fecha}")
    
    #RETURN PARA LA API
    return {
        "ingreso total": float(ingreso_total),
        "promedio_precio": float(promedio_precio),
        "top_productos": top_cinco.to_dict(orient="records"),
        "top_fecha": top_fecha.to_dict(orient="records")
    }
    

if __name__ == "__main__":
    analisis = obtener_datos_ventas()
    
