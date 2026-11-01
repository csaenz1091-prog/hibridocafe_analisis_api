import pandas as pd
from sqlalchemy import create_engine

#coneccion a la base de datos
db_url = 'postgresql://admin:secret@localhost:5432/hibridocafe_db'


#funcion para generar la consulta de SQL
def consultar_datos_ventas():
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