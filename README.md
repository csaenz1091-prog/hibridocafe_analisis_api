# Dashboard de ventas de Híbrido Café

La aplicación Flask incluye un dashboard con ingresos, unidades vendidas, precio
promedio, ingreso promedio diario, proyección de ingresos a 30 días, productos
más vendidos, ventas agrupadas por fecha y un gráfico de ingresos por día de la
semana en porcentajes, además de un formulario para registrar ventas en
PostgreSQL. El promedio diario se calcula únicamente con fechas que tienen
ventas y respeta el periodo seleccionado.

## Ejecutar

Desde la raíz del proyecto:

```bash
python src/api_datos.py
```

Abre `http://localhost:5000`. La base de datos PostgreSQL debe estar disponible
con la configuración utilizada por `src/consulta_datos.py`.

Usa **Registrar una venta** para elegir un producto del catálogo, indicar fecha
y cantidad y guardar el movimiento en la tabla `ventas`. La tabla `ventas` debe
tener las columnas `id_producto`, `fecha` y `cantidad`; la llave primaria debe
generarse automáticamente. El precio se consulta del catálogo `productos`.

El endpoint JSON está disponible en `/api/resumen`. Puede filtrarse con
`?desde=AAAA-MM-DD&hasta=AAAA-MM-DD`, por ejemplo:
`/api/resumen?desde=2026-10-01&hasta=2026-10-31`.

El catálogo de productos se sirve desde `/api/productos` y las ventas se guardan
mediante `POST /api/ventas`.
