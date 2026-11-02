import pandas as pd
from sqlalchemy import create_engine, text

#coneccion a la base de datos
db_url = 'postgresql://admin:secret@localhost:5432/hibridocafe_db'

def crear_engine():
    return create_engine(
        db_url,
        connect_args={'connect_timeout': 5}
    )


#funcion para generar la consulta de SQL
def consultar_datos_ventas():
    engine = crear_engine()
    
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


def consultar_productos_venta():
    query = text("""
        select id_producto, nombre, precio
        from productos
        order by nombre asc
    """)

    with crear_engine().connect() as connection:
        rows = connection.execute(query).mappings().all()

    return [
        {
            "id_producto": int(row["id_producto"]),
            "nombre": row["nombre"],
            "precio": float(row["precio"]) if row["precio"] is not None else None
        }
        for row in rows
    ]


def registrar_venta(id_producto, fecha, cantidad):
    with crear_engine().begin() as connection:
        producto = connection.execute(
            text("select 1 from productos where id_producto = :id_producto"),
            {"id_producto": id_producto}
        ).first()
        if producto is None:
            raise ValueError("El producto seleccionado no existe.")

        connection.execute(
            text("""
                insert into ventas (id_producto, fecha, cantidad)
                values (:id_producto, :fecha, :cantidad)
            """),
            {
                "id_producto": id_producto,
                "fecha": fecha,
                "cantidad": cantidad
            }
        )