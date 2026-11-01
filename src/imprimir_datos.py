from analisis_datos import calcular_promedio_precio, calcular_ingreso_total, calcular_top_productos
from consulta_datos import consultar_datos_ventas


#funcion para generar la consulta de SQL
def obtener_datos_ventas():
    datos = consultar_datos_ventas()
    return datos

############################################

#funcion para analizar los datos
def analizar_datos_ventas(datos):

    ingreso_total = calcular_ingreso_total(datos)
    print(f"Ingreso total: ${ingreso_total} MXN")
        
    promedio_precio = calcular_promedio_precio(datos)
    print(f"Promedio de precio: ${promedio_precio} MXN")
    
    top_cinco = calcular_top_productos(datos)
    print(f"Top 5: {top_cinco}") 
    
    return {
        "ingreso total": float(ingreso_total),
        "promedio_precio": float(promedio_precio),
        "top_productos": top_cinco.to_dict(orient="records")
    }
    

if __name__ == "__main__":
    analisis = consultar_datos_ventas()
    analizar_datos_ventas(analisis)
    
