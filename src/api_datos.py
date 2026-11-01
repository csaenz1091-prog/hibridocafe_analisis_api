from flask import Flask, jsonify
from imprimir_datos import obtener_datos_ventas

app = Flask (__name__)
app.json.sort_keys = False

@app.route("/", methods=["GET"])
def mensaje_bienvenida():
        
    try:
        return jsonify({
            "mensaje": "Bienvenido al análisis de ventas de Híbrido Café!",
            "detalle": {
                "ingreso_total": "Ingreso total.",
                "top_cinco": "Productos estrella."
                }   
        }), 200
        
    except Exception as e:
        return jsonify({
            "estado": "error",
            "mensaje": str(e)
        }), 500


@app.route("/api/resumen", methods=["GET"])
def resumen_ventas():
    
    try:
        resultado = obtener_datos_ventas()
        
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