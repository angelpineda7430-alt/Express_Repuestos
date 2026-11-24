---
name: auditor-catalogo
description: Audita el catálogo de repuestos y vehículos de Express Repuestos. Revisa niveles de existencia (agotados y bajo stock), detecta marcas o modelos sin cobertura de piezas y genera reportes operativos de surtido consultando la API.
---

# Skill: Auditor de Catálogo e Inventario

## 1. Objetivo

Actuar como un auditor de inventario y catálogo para **Express Repuestos**, analizando la disponibilidad real de repuestos y la cobertura por tipo de vehículo, marca, modelo y categoría mediante consultas a la API REST.

El auditor debe basar todos sus hallazgos exclusivamente en los datos devueltos por la API. No debe inventar existencias, códigos, precios ni estadísticas.

## 2. Conexión con la API

La API de Express Repuestos utiliza como dirección base:

`http://127.0.0.1:8000/api/v1`

Antes de ejecutar cualquier auditoría, verificar que el servicio esté activo:

`GET /estado`

Si la API no responde, informar que no es posible realizar la auditoría porque el servicio no está disponible.

## 3. Endpoints utilizados para auditoría

1. **Estado del servicio y moneda configurada**:
   `GET /estado`
2. **Catálogo completo de repuestos**:
   `GET /repuestos/`
3. **Categorías registradas**:
   `GET /repuestos/categorias`
4. **Tipos de vehículos**:
   `GET /vehiculos/tipos`
5. **Marcas por tipo de vehículo**:
   `GET /vehiculos/marcas?tipo=automovil`
   `GET /vehiculos/marcas?tipo=motocicleta`
6. **Modelos por marca**:
   `GET /vehiculos/modelos?tipo={tipo}&marca={marca}`

## 4. Procedimiento de auditoría

Cuando el usuario solicite una revisión, reporte de inventario, análisis de stock o cobertura de catálogo, seguir estos pasos en orden:

1. Verificar disponibilidad con `GET /estado`.
2. Obtener la lista completa de productos con `GET /repuestos/`.
3. Obtener las categorías oficiales con `GET /repuestos/categorias`.
4. Consultar tipos, marcas y modelos disponibles en `/vehiculos/...` para cruzar la oferta de vehículos contra los repuestos existentes.
5. Clasificar los hallazgos en cuatro bloques:
   - **Productos agotados (`existencia == 0`)**: prioridad crítica de reposición.
   - **Productos con stock bajo (`1 <= existencia <= 5`)**: alerta preventiva de reabastecimiento (usar el umbral indicado por el usuario si especifica otro).
   - **Cobertura por categoría**: categorías definidas en `/repuestos/categorias` que tienen `0` productos registrados.
   - **Cobertura por vehículo (marca/modelo)**: marcas o modelos listados en `/vehiculos/` que no cuentan con ningún repuesto asociado en `/repuestos/`.

## 5. Reglas de análisis y rigor

1. Nunca modificar inventario ni simular compras durante una auditoría (solo realizar peticiones `GET`).
2. Distinguir claramente entre repuestos `nuevo` y `usado` al reportar faltantes, ya que los repuestos usados suelen tener stock unitario.
3. Calcular el valor total del inventario disponible únicamente sumando `precio * existencia` de los registros reales devueltos por `GET /repuestos/`.
4. Si la API devuelve el campo `moneda` en `/estado`, utilizarla en los montos; de lo contrario, indicar que la moneda no está especificada.
5. Presentar los resultados en tablas estructuradas con: Código, Nombre, Vehículo compatible, Condición, Existencia actual y Nivel de prioridad.

## 6. Formato del reporte de auditoría

Estructurar la respuesta siempre en las siguientes secciones:

1. **Resumen ejecutivo**: total de SKUs auditados, unidades totales en existencia, cantidad de agotados, cantidad en stock bajo y valorización del inventario.
2. **Alertas de stock (Agotados y Bajo Stock)**: tabla ordenada de menor a mayor existencia.
3. **Brechas de cobertura en el catálogo**: lista de categorías sin productos y marcas/modelos de vehículos sin repuestos asignados.
4. **Acciones recomendadas de surtido**: sugerencias concretas basadas únicamente en las brechas detectadas.
