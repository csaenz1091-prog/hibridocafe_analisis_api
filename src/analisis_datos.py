

def calcular_ingreso_total(datos):
    ingreso_total = (datos['precio'] * datos['cantidad']).sum()
    return round(ingreso_total, 2)

def calcular_promedio_precio(datos):
    promedio_precio = datos['precio'].mean()
    return round(promedio_precio, 2)

def calcular_top_productos(datos):
    por_unidades_vendidas = datos.groupby('nombre')['cantidad'].sum().reset_index()
    top_productos = por_unidades_vendidas.sort_values(by='cantidad', ascending=False)
    return top_productos.head(5)


