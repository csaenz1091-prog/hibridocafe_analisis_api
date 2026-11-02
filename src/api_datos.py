from datetime import date
from flask import Flask, jsonify, render_template, request
from imprimir_datos import obtener_datos_ventas

app = Flask(__name__)
app.json.sort_keys = False


@app.route("/", methods=["GET"])
def mensaje_bienvenida():
    return render_template("index.html")


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
    except Exception as e:
        return jsonify({
            "estado": "error",
            "mensaje": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)