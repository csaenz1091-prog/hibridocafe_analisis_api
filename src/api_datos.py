from datetime import date
import logging

from flask import Flask, jsonify, render_template, request
from sqlalchemy.exc import SQLAlchemyError

from consulta_datos import consultar_productos_venta, registrar_venta
from imprimir_datos import obtener_datos_ventas

app = Flask(__name__)
app.json.sort_keys = False
logger = logging.getLogger(__name__)


def leer_entero_positivo(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, (int, str)):
        raise ValueError(f"El campo {campo} debe ser un número entero positivo.")

    texto = str(valor).strip()
    if not texto.isdecimal() or int(texto) < 1:
        raise ValueError(f"El campo {campo} debe ser un número entero positivo.")
    return int(texto)


@app.route("/", methods=["GET"])
def mensaje_bienvenida():
    return render_template("index.html")


@app.route("/ventas", methods=["GET"])
def pagina_registro_ventas():
    return render_template("ventas.html")


@app.route("/api/productos", methods=["GET"])
def productos_venta():
    try:
        return jsonify({
            "estado": "exitoso",
            "datos": consultar_productos_venta()
        }), 200
    except SQLAlchemyError:
        logger.exception("No fue posible consultar el catálogo de productos.")
        return jsonify({
            "estado": "error",
            "mensaje": "No fue posible cargar los productos. Intenta de nuevo más tarde."
        }), 500


@app.route("/api/ventas", methods=["POST"])
def crear_venta():
    if not request.is_json:
        return jsonify({
            "estado": "error",
            "mensaje": "Envía los datos de la venta en formato JSON."
        }), 415

    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({
            "estado": "error",
            "mensaje": "Los datos de la venta no son válidos."
        }), 400

    fecha_texto = datos.get("fecha")
    if not isinstance(fecha_texto, str):
        return jsonify({
            "estado": "error",
            "mensaje": "Selecciona una fecha válida."
        }), 400

    try:
        fecha_venta = date.fromisoformat(fecha_texto)
        if fecha_venta.isoformat() != fecha_texto:
            raise ValueError
    except ValueError:
        return jsonify({
            "estado": "error",
            "mensaje": "Usa una fecha válida con el formato AAAA-MM-DD."
        }), 400

    try:
        id_producto = leer_entero_positivo(datos.get("id_producto"), "producto")
        cantidad = leer_entero_positivo(datos.get("cantidad"), "cantidad")
    except ValueError as error:
        return jsonify({
            "estado": "error",
            "mensaje": str(error)
        }), 400

    try:
        registrar_venta(id_producto, fecha_venta, cantidad)
        return jsonify({
            "estado": "exitoso",
            "mensaje": "La venta se registró correctamente."
        }), 201
    except ValueError as error:
        return jsonify({
            "estado": "error",
            "mensaje": str(error)
        }), 400
    except SQLAlchemyError:
        logger.exception("No fue posible registrar la venta.")
        return jsonify({
            "estado": "error",
            "mensaje": "No fue posible guardar la venta. Verifica la conexión con la base de datos."
        }), 500


@app.route("/api/resumen", methods=["GET"])
def resumen_ventas():
    fecha_inicio = request.args.get("desde")
    fecha_fin = request.args.get("hasta")

    try:
        desde = date.fromisoformat(fecha_inicio) if fecha_inicio else None
        hasta = date.fromisoformat(fecha_fin) if fecha_fin else None
    except ValueError:
        return jsonify({
            "estado": "error",
            "mensaje": "Usa fechas válidas con el formato AAAA-MM-DD."
        }), 400

    if desde and hasta and desde > hasta:
        return jsonify({
            "estado": "error",
            "mensaje": "La fecha inicial no puede ser posterior a la fecha final."
        }), 400

    try:
        resultado = obtener_datos_ventas(desde, hasta)
        return jsonify({
            "estado": "exitoso",
            "datos": resultado
        }), 200
    except SQLAlchemyError:
        logger.exception("No fue posible consultar el resumen de ventas.")
        return jsonify({
            "estado": "error",
            "mensaje": "No fue posible cargar el reporte. Verifica la conexión con la base de datos."
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    