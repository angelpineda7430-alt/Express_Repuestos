# Express Repuestos

## 1. Descripción del proyecto

**Express Repuestos** es una aplicación web diseñada para facilitar la búsqueda, consulta y compra de repuestos nuevos y usados para automóviles y motocicletas.

El sistema permite seleccionar el tipo de vehículo, marca, modelo y año para consultar repuestos disponibles según su compatibilidad. También incorpora un carrito de compras, registro de pedidos y seguimiento del estado de las compras.

El proyecto incluye una API desarrollada con FastAPI y un Agent Skill denominado `asesor-repuestos`, que permite a un agente de inteligencia artificial consultar el catálogo y recomendar productos según las necesidades del cliente.

## 2. Objetivos

### Objetivo general

Desarrollar una plataforma web para la búsqueda y adquisición de repuestos vehiculares, integrando una API modular y un agente inteligente que facilite la selección de productos compatibles.

### Objetivos específicos

- Permitir la búsqueda de repuestos para automóviles y motocicletas.
- Consultar marcas, modelos y años disponibles.
- Diferenciar productos nuevos y usados.
- Mostrar precios, descripciones y existencias.
- Administrar un carrito de compras.
- Registrar pedidos con modalidad de entrega en sucursal o domicilio.
- Consultar el seguimiento de los pedidos.
- Integrar un Agent Skill que consulte la API y recomiende repuestos compatibles.

## 3. Tecnologías utilizadas

| Tecnología | Utilización |
|---|---|
| Python | Lenguaje del backend |
| FastAPI | Desarrollo de la API REST |
| Uvicorn | Servidor de desarrollo |
| Pydantic | Validación de datos |
| HTML5 | Estructura de la tienda |
| CSS3 | Diseño y estilos |
| JavaScript | Interacción con la API |
| Git y GitHub | Control de versiones |
| GitHub Copilot Agent | Integración y prueba del agente inteligente |

## 4. Arquitectura del proyecto

El proyecto utiliza una estructura modular para separar las responsabilidades del sistema.

```text
Express_Repuestos/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   │
│   │   ├── routes/
│   │   │   ├── vehiculos.py
│   │   │   ├── repuestos.py
│   │   │   ├── carrito.py
│   │   │   └── pedidos.py
│   │   │
│   │   ├── services/
│   │   │   ├── catalogo_service.py
│   │   │   ├── repuestos_service.py
│   │   │   ├── carrito_service.py
│   │   │   └── pedido_service.py
│   │   │
│   │   ├── models/
│   │   │   ├── vehiculo.py
│   │   │   ├── repuesto.py
│   │   │   ├── carrito.py
│   │   │   └── pedido.py
│   │   │
│   │   └── data/
│   │       ├── catalogo.py
│   │       └── catalogo_repuestos.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── estilos.css
│   ├── js/
│   │   └── app.js
│   └── images/
│
├── .github/
│   └── skills/
│       └── asesor-repuestos/
│           └── SKILL.md
│
└── README.md
```

## 5. Funcionalidades de la aplicación

### 5.1. Catálogo de vehículos

Permite seleccionar:

- Tipo de vehículo: automóvil o motocicleta.
- Marca.
- Modelo.
- Año.

Las marcas y modelos se consultan dinámicamente desde la API.

### 5.2. Catálogo de repuestos

Permite consultar repuestos utilizando filtros como:

- Tipo de vehículo.
- Marca.
- Modelo.
- Año.
- Categoría.
- Condición: nuevo o usado.

Cada producto contiene información como código, nombre, descripción, precio, existencia y compatibilidad.

### 5.3. Carrito de compras

Permite:

- Agregar productos.
- Modificar cantidades.
- Eliminar productos.
- Consultar subtotales.
- Calcular el total de la compra.

### 5.4. Registro de pedidos

El sistema permite registrar pedidos solicitando:

- Nombre del cliente.
- Número de celular.
- Documento de identificación.
- Modalidad de entrega.
- Dirección cuando se selecciona entrega a domicilio.

### 5.5. Seguimiento de pedidos

Cada pedido recibe un identificador único que permite consultar:

- Número de pedido.
- Cliente.
- Estado actual.
- Modalidad de entrega.
- Total.
- Historial de cambios de estado.

## 6. API REST con FastAPI

La API utiliza como dirección base:

`http://127.0.0.1:8000/api/v1`

### Principales endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/estado` | Verificar el estado de la API |
| GET | `/vehiculos/tipos` | Consultar tipos de vehículos |
| GET | `/vehiculos/marcas` | Consultar marcas |
| GET | `/vehiculos/modelos` | Consultar modelos |
| GET | `/vehiculos/anios` | Consultar años disponibles |
| GET | `/repuestos/categorias` | Consultar categorías |
| GET | `/repuestos/` | Buscar repuestos |
| GET | `/repuestos/{id}` | Consultar un repuesto |
| GET | `/carrito/{id}` | Consultar carrito |
| POST | `/carrito/{id}/items` | Agregar productos |
| PATCH | `/carrito/{id}/items/{repuesto_id}` | Actualizar cantidad |
| DELETE | `/carrito/{id}/items/{repuesto_id}` | Eliminar producto |
| POST | `/pedidos/` | Registrar pedido |
| GET | `/pedidos/{id}` | Consultar pedido |
| PATCH | `/pedidos/{id}/estado` | Actualizar estado |

La documentación interactiva de FastAPI está disponible en:

`http://127.0.0.1:8000/docs`

## 7. Agent Skill: asesor-repuestos

El proyecto incorpora un Skill personalizado siguiendo la estructura de Agent Skills.

**Nombre:** `asesor-repuestos`

**Ubicación:**

`.github/skills/asesor-repuestos/SKILL.md`

### Objetivo del Skill

Actuar como un asesor especializado que ayuda a los clientes a encontrar repuestos compatibles para automóviles y motocicletas.

### Reglas principales

El agente debe:

1. Identificar el tipo de vehículo, marca, modelo y año.
2. Consultar las categorías disponibles en la API.
3. Utilizar los códigos exactos de las categorías.
4. Consultar el catálogo de repuestos.
5. Verificar compatibilidad.
6. Comprobar condición y existencia.
7. Mostrar los precios recibidos de la API sin asumir una moneda no especificada.
8. Evitar inventar productos, precios o características.

### Integración y prueba del agente

Se utilizó GitHub Copilot en modo Agent para comprobar el reconocimiento y funcionamiento del Skill.

Durante las pruebas se verificó que:

- Copilot reconoció automáticamente el Skill desde la carpeta `.github/skills/`.
- Consultó el estado de la API.
- Consultó las categorías disponibles.
- Identificó el código `FRENOS`.
- Buscó repuestos en el catálogo.
- Recomendó productos según la información devuelta por FastAPI.

### Ejemplo de prueba realizada

Solicitud:

Pastillas de freno nuevas para una motocicleta Honda CB125F del año 2022.

Resultado obtenido:

| Campo | Resultado |
|---|---|
| Código | REP-006 |
| Producto | Pastillas de freno Honda |
| Condición | Nuevo |
| Precio | 12.00 |
| Existencia | 10 |
| Compatibilidad | Honda CB125F |
| Rango de años | 2018–2025 |

La moneda no está especificada por la API.

## 8. Instalación y ejecución

### Requisitos previos

- Python instalado.
- Visual Studio Code.
- Git.
- Navegador web.

### Paso 1. Abrir el proyecto

Abrir la carpeta `Express_Repuestos` en Visual Studio Code.

### Paso 2. Crear el entorno virtual

Desde la terminal de VS Code, ubicarse en la carpeta `backend` y ejecutar:

```powershell
python -m venv venv
```

Activar el entorno virtual:

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución del script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Después ejecutar nuevamente:

```powershell
.\venv\Scripts\Activate.ps1
```

### Paso 3. Instalar dependencias

Desde la carpeta `backend`:

```powershell
pip install -r requirements.txt
```

### Paso 4. Iniciar FastAPI

Desde la carpeta `backend`:

```powershell
uvicorn app.main:app --reload
```

### Paso 5. Abrir la tienda

En el navegador ingresar:

`http://127.0.0.1:8000/tienda/`

Para consultar la documentación de la API:

`http://127.0.0.1:8000/docs`

## 9. Pruebas realizadas

Se realizaron pruebas funcionales de los siguientes componentes:

| Prueba | Resultado |
|---|---|
| Inicio de la tienda web | Correcto |
| Selección de tipo de vehículo | Correcto |
| Carga de marcas y modelos | Correcto |
| Consulta de repuestos | Correcto |
| Filtros por condición y categoría | Correcto |
| Agregar productos al carrito | Correcto |
| Modificar cantidades | Correcto |
| Eliminar productos | Correcto |
| Finalizar compra | Correcto |
| Generar número de seguimiento | Correcto |
| Consultar seguimiento del pedido | Correcto |
| Reconocimiento del Agent Skill | Correcto |
| Consulta de categorías mediante el agente | Correcto |
| Recomendación de repuestos mediante el agente | Correcto |

## 10. Limitaciones actuales

Esta versión es un prototipo funcional con datos de demostración.

- El catálogo utiliza registros de prueba.
- Los carritos, pedidos y existencias se mantienen en memoria; no existe persistencia en una base de datos.
- Los datos pueden perderse al reiniciar el servidor.
- No se integra una pasarela de pago real.
- No se implementa autenticación de usuarios ni un sistema de administración.
- La compatibilidad depende de los datos registrados en el catálogo.

Para un entorno de producción será necesario incorporar una base de datos, autenticación, controles de seguridad, persistencia de pedidos y un proceso de validación comercial de los repuestos.

## 11. Mejoras futuras

- Integración con Oracle o MySQL.
- Registro e inicio de sesión de clientes.
- Panel administrativo.
- Gestión de inventario.
- Carga de fotografías reales de productos.
- Integración de pagos electrónicos.
- Notificaciones por correo o WhatsApp.
- Seguimiento de entregas.
- Ampliación del catálogo de vehículos y repuestos.

## 12. Conclusión

Express Repuestos integra una tienda web, una API REST modular y un agente inteligente especializado.

El proyecto demuestra cómo un Agent Skill personalizado puede orientar a un agente para consultar una API, verificar información del catálogo y ofrecer recomendaciones de repuestos basadas en datos disponibles.

El resultado es un prototipo funcional que establece una base para desarrollar una plataforma comercial de compra y cotización de repuestos para automóviles y motocicletas.