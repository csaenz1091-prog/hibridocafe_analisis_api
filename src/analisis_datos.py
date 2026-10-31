import pandas as pd
from sqlalchemy import create_engine

#coneccion a la base de datos
db_url = 'postgresql://admin:secret@localhost:5432/hibridocafe_db'

#funcion para generar la consulta de SQL
def obtener_datos_ventas():
    engine = create_engine(db_url)
    
    query = """
        select *
        from ventas v 
            full join productos p 
            on v.id_producto = p.id_producto
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
    print(f"Top 3: {top_productos.head(3)}")
    
    


if __name__ == "__main__":
    analisis = obtener_datos_ventas()
    analizar_datos_ventas(analisis)