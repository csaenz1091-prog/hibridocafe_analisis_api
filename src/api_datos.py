from flask import Flask, jsonify
from analisis_datos import obtener_datos_ventas, analizar_datos_ventas

app = Flask (__name__)

@app.route("/api/resumen", methods=["GET"])
def resumen_ventas():
    
    try:
        analisis = obtener_datos_ventas()
        resultado = analizar_datos_ventas(analisis)
        
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