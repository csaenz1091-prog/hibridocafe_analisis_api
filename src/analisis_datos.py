import pandas as pd
from sqlalchemy import create_engine


#coneccion a la base de datos
db_url = 'postgresql://admin:secret@localhost:5432/hibridocafe_db'


#funcion para generar la consulta de SQL
def obtener_datos_ventas():
    engine = create_engine(
        db_url,
        connect_args={'connect_timeout': 5}
    )
    
    query = """
        select *
        from ventas v 
            full join productos p 
            on v.id_producto = p.id_producto
            where p.nombre != 'jarabe' and p.nombre != 'leche deslac'
        order by v.fecha, p.id_producto asc
    """
    
    datos = pd.read_sql(query, engine)
    
    return datos


#funcion para analizar los datos
def analizar_datos_ventas(datos):

    ingreso_total = (datos['precio'] * datos['cantidad']).sum()
    print(f"Ingreso total: {ingreso_total}")
    
    por_unidades_vendidas = datos.groupby('nombre')['cantidad'].sum().reset_index()
    top_productos = por_unidades_vendidas.sort_values(by='cantidad', ascending=False)
    top_cinco = top_productos.head(5)
    print(f"Top 5: {top_cinco}")
    
    return {
        "ingreso total": float(ingreso_total),
        "top_productos": top_cinco.to_dict(orient="records")
    }
    
    

if __name__ == "__main__":
    analisis = obtener_datos_ventas()
    analizar_datos_ventas(analisis)