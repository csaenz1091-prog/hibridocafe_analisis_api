# Dashboard de ventas de Híbrido Café

La aplicación Flask muestra un dashboard con ingresos, unidades vendidas, precio
promedio, productos más vendidos y ventas agrupadas por fecha. El filtro permite
consultar un periodo inclusivo.

## Ejecutar

Desde la raíz del proyecto:

```bash
python src/api_datos.py
```

Abre `http://localhost:5000`. La base de datos PostgreSQL debe estar disponible
con la configuración utilizada por `src/consulta_datos.py`.

El endpoint JSON está disponible en `/api/resumen`. Puede filtrarse con
`?desde=AAAA-MM-DD&hasta=AAAA-MM-DD`, por ejemplo:
`/api/resumen?desde=2026-10-01&hasta=2026-10-31`.
