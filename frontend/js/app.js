
const API = "/api/v1";

let carritoId = "web_" + Date.now();
let carritoActual = null;
let vehiculoSeleccionado = null;

// ========================================
// AUTENTICACIÓN DE CLIENTES - CLERK
// ========================================

let usuarioAutenticado = null;

function abrirAcceso() {
    if (window.Clerk && !window.Clerk.isSignedIn) {
        window.Clerk.openSignIn();
    }
}

async function configurarAutenticacion() {

    const clerk = await window.clerkReady;

    if (!clerk) {
        console.error("No se pudo inicializar Clerk");
        return;
    }

    const contenedor = document.getElementById("clerk-auth");

    function actualizarUsuario() {

        if (clerk.isSignedIn && clerk.user) {

            usuarioAutenticado = clerk.user;

            contenedor.innerHTML = '<div id="clerk-user-button"></div>';

            clerk.mountUserButton(document.getElementById("clerk-user-button"), {
    afterSignOutUrl: "/tienda/"
});

            console.log(
                "Cliente autenticado:",
                usuarioAutenticado.primaryEmailAddress?.emailAddress
            );

        } else {

            usuarioAutenticado = null;

            contenedor.innerHTML = `
                <button class="btn-login" onclick="abrirAcceso()">
                    Iniciar sesión
                </button>
            `;
        }
    }

    actualizarUsuario();

    clerk.addListener(() => {
        actualizarUsuario();
    });
}

configurarAutenticacion();

// ========================================
// FUNCIONES GENERALES
// ========================================


async function solicitar(url, opciones = {}) {

    const headers = {
        "Content-Type": "application/json",
        ...(opciones.headers || {})
    };

    // Obtener el token de autenticación de Clerk
    if (window.Clerk && window.Clerk.session) {
        const token = await window.Clerk.session.getToken();

        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }
    }

    const respuesta = await fetch(url, {
        ...opciones,
        headers
    });

    const datos = await respuesta.json();

    if (!respuesta.ok) {
        throw new Error(datos.detail || "Error en la solicitud");
    }

    return datos;
}


function mostrarError(error) {
    alert(error.message || "Ocurrió un error");
}

// ========================================
// CARGAR TIPOS Y MARCAS
// ========================================

document.getElementById("tipo").addEventListener("change", async e => {

    const tipo = e.target.value;

    const marca = document.getElementById("marca");
    const modelo = document.getElementById("modelo");
    const anio = document.getElementById("anio");

    marca.innerHTML = '<option value="">Seleccionar marca</option>';
    modelo.innerHTML = '<option value="">Seleccionar modelo</option>';
    anio.innerHTML = '<option value="">Seleccionar año</option>';

    marca.disabled = true;
    modelo.disabled = true;
    anio.disabled = true;

    document.getElementById("buscar").disabled = true;

    if (!tipo) return;

    try {

        const datos = await solicitar(
            `${API}/vehiculos/marcas?tipo=${tipo}`
        );

        datos.marcas.forEach(nombre => {

            marca.innerHTML +=
                `<option value="${nombre}">${nombre}</option>`;

        });

        marca.disabled = false;

    } catch (error) {
        mostrarError(error);
    }
});


// ========================================
// CARGAR MODELOS
// ========================================

document.getElementById("marca").addEventListener("change", async e => {

    const tipo = document.getElementById("tipo").value;
    const marca = e.target.value;

    const modelo = document.getElementById("modelo");
    const anio = document.getElementById("anio");

    modelo.innerHTML = '<option value="">Seleccionar modelo</option>';
    anio.innerHTML = '<option value="">Seleccionar año</option>';

    modelo.disabled = true;
    anio.disabled = true;

    document.getElementById("buscar").disabled = true;

    if (!marca) return;

    try {

        const datos = await solicitar(
            `${API}/vehiculos/modelos?tipo=${tipo}&marca=${encodeURIComponent(marca)}`
        );

        datos.modelos.forEach(nombre => {

            modelo.innerHTML +=
                `<option value="${nombre}">${nombre}</option>`;

        });

        modelo.disabled = false;

    } catch (error) {
        mostrarError(error);
    }
});


// ========================================
// CARGAR AÑOS
// ========================================

document.getElementById("modelo").addEventListener("change", async e => {

    const tipo = document.getElementById("tipo").value;
    const marca = document.getElementById("marca").value;
    const modelo = e.target.value;

    const anio = document.getElementById("anio");

    anio.innerHTML = '<option value="">Seleccionar año</option>';
    anio.disabled = true;

    document.getElementById("buscar").disabled = true;

    if (!modelo) return;

    try {

        const url = `${API}/vehiculos/anios?tipo=${tipo}&marca=${encodeURIComponent(marca)}&modelo=${encodeURIComponent(modelo)}`;

        const datos = await solicitar(url);

        datos.anios.forEach(valor => {

            anio.innerHTML +=
                `<option value="${valor}">${valor}</option>`;

        });

        anio.disabled = false;

    } catch (error) {
        mostrarError(error);
    }
});


// ========================================
// SELECCIONAR VEHICULO
// ========================================

document.getElementById("anio").addEventListener("change", e => {

    document.getElementById("buscar").disabled = !e.target.value;

});

document.getElementById("buscar").addEventListener("click", () => {

    vehiculoSeleccionado = {
        tipo: document.getElementById("tipo").value,
        marca: document.getElementById("marca").value,
        modelo: document.getElementById("modelo").value,
        anio: document.getElementById("anio").value
    };

    cargarRepuestos();
});

document.getElementById("limpiar").addEventListener("click", () => {

    ["tipo", "marca", "modelo", "anio"].forEach(id => {
        document.getElementById(id).value = "";
    });

    document.getElementById("marca").disabled = true;
    document.getElementById("modelo").disabled = true;
    document.getElementById("anio").disabled = true;
    document.getElementById("buscar").disabled = true;

    vehiculoSeleccionado = null;

    cargarRepuestos();
});


// ========================================
// CARGAR CATEGORIAS
// ========================================

async function cargarCategorias() {

    try {

        const datos = await solicitar(
            `${API}/repuestos/categorias`
        );

        const select = document.getElementById("categoria");

        datos.forEach(categoria => {

            const opcion = document.createElement("option");

            opcion.value = categoria.codigo;
            opcion.textContent = categoria.nombre;

            select.appendChild(opcion);

        });

    } catch (error) {
        mostrarError(error);
    }
}


// ========================================
// MOSTRAR REPUESTOS
// ========================================

async function cargarRepuestos() {

    const contenedor = document.getElementById("productos");

    contenedor.innerHTML = "<p>Buscando repuestos...</p>";

    const parametros = new URLSearchParams();

    if (vehiculoSeleccionado) {

        parametros.append("tipo", vehiculoSeleccionado.tipo);
        parametros.append("marca", vehiculoSeleccionado.marca);
        parametros.append("modelo", vehiculoSeleccionado.modelo);
        parametros.append("anio", vehiculoSeleccionado.anio);

    }

    const categoria = document.getElementById("categoria").value;
    const condicion = document.getElementById("condicion").value;

    if (categoria) parametros.append("categoria", categoria);
    if (condicion) parametros.append("condicion", condicion);

    try {

        const datos = await solicitar(
            `${API}/repuestos/?${parametros.toString()}`
        );

        contenedor.innerHTML = "";

        if (datos.length === 0) {
            contenedor.innerHTML =
                "<p>No encontramos repuestos para los filtros seleccionados.</p>";
            return;
        }

        datos.forEach(repuesto => {

            const tarjeta = document.createElement("article");

            tarjeta.className = "product-card";

            const imagen = document.createElement("img");
            imagen.src = repuesto.imagen;
            imagen.alt = repuesto.nombre;

            imagen.onerror = () => {
                imagen.src = "https://placehold.co/400x250?text=Express+Repuestos";
            };

            const informacion = document.createElement("div");
            informacion.className = "product-info";

            const titulo = document.createElement("h3");
            titulo.textContent = repuesto.nombre;

            const descripcion = document.createElement("p");
            descripcion.textContent = repuesto.descripcion;

            const compatibilidad = document.createElement("p");
            compatibilidad.textContent =
                `${repuesto.marca_vehiculo} ${repuesto.modelo_vehiculo} | ${repuesto.anio_desde}-${repuesto.anio_hasta}`;

            const condicionProducto = document.createElement("span");
            condicionProducto.className =
                repuesto.condicion === "usado" ? "condition used" : "condition";

            condicionProducto.textContent = repuesto.condicion.toUpperCase();

            const precio = document.createElement("div");
            precio.className = "price";
            precio.textContent = `$${Number(repuesto.precio).toFixed(2)}`;

            const boton = document.createElement("button");
            boton.className = "btn-primary";
            boton.textContent = "Agregar al carrito";

            boton.disabled = repuesto.existencia <= 0;

            boton.addEventListener("click", () => {
                agregarAlCarrito(repuesto.id);
            });

            informacion.append(
                titulo,
                descripcion,
                compatibilidad,
                condicionProducto,
                precio,
                boton
            );

            tarjeta.append(imagen, informacion);

            contenedor.appendChild(tarjeta);

        });

    } catch (error) {

        contenedor.innerHTML = `<p>${error.message}</p>`;

    }
}


// ========================================
// FILTROS
// ========================================

document.getElementById("categoria").addEventListener(
    "change",
    cargarRepuestos
);

document.getElementById("condicion").addEventListener(
    "change",
    cargarRepuestos
);


// ========================================
// CARRITO DE COMPRAS
// ========================================

async function agregarAlCarrito(repuestoId) {

    try {

        carritoActual = await solicitar(
            `${API}/carrito/${carritoId}/items`,
            {
                method: "POST",
                body: JSON.stringify({
                    repuesto_id: repuestoId,
                    cantidad: 1
                })
            }
        );

        actualizarVistaCarrito();

        alert("Producto agregado al carrito");

    } catch (error) {
        mostrarError(error);
    }
}


async function consultarCarrito() {

    carritoActual = await solicitar(
        `${API}/carrito/${carritoId}`
    );

    actualizarVistaCarrito();
}


function actualizarVistaCarrito() {

    const productos = carritoActual?.productos || [];

    document.getElementById("contador").textContent =
        carritoActual?.cantidad_total || 0;

    document.getElementById("totalCarrito").textContent =
        Number(carritoActual?.total || 0).toFixed(2);

    const contenido = document.getElementById("contenidoCarrito");

    contenido.innerHTML = "";

    productos.forEach(producto => {

        const fila = document.createElement("div");
        fila.className = "cart-item";

        const informacion = document.createElement("div");

        const nombre = document.createElement("strong");
        nombre.textContent = producto.nombre;

        const detalle = document.createElement("p");
        detalle.textContent =
            `${producto.cantidad} × $${Number(producto.precio_unitario).toFixed(2)}`;

        const subtotal = document.createElement("p");
        subtotal.textContent =
            `Subtotal: $${Number(producto.subtotal).toFixed(2)}`;

        informacion.append(nombre, detalle, subtotal);

        const eliminar = document.createElement("button");
        eliminar.textContent = "Eliminar";

        eliminar.addEventListener("click", () => {
            quitarDelCarrito(producto.repuesto_id);
        });

        fila.append(informacion, eliminar);

        contenido.appendChild(fila);

    });
}


async function abrirCarrito() {

    try {

        await consultarCarrito();

        document.getElementById("modalCarrito").style.display = "flex";

    } catch (error) {
        mostrarError(error);
    }
}


function cerrarCarrito() {

    document.getElementById("modalCarrito").style.display = "none";

}


async function quitarDelCarrito(repuestoId) {

    try {

        carritoActual = await solicitar(
            `${API}/carrito/${carritoId}/items/${repuestoId}`,
            { method: "DELETE" }
        );

        actualizarVistaCarrito();

    } catch (error) {
        mostrarError(error);
    }
}


// ========================================
// FINALIZAR COMPRA
// ========================================

async function mostrarCheckout() {

    try {

        await consultarCarrito();

        if (!carritoActual.productos.length) {
            alert("El carrito está vacío");
            return;
        }

        // Verificar que el cliente haya iniciado sesión
        if (!window.Clerk || !window.Clerk.isSignedIn) {

            alert("Para continuar con tu compra debes iniciar sesión.");

            window.Clerk?.openSignIn();

            return;
        }

        // El cliente está autenticado
        cerrarCarrito();

        document.getElementById("modalCheckout").style.display = "flex";

    } catch (error) {
        mostrarError(error);
    }
}


function cerrarCheckout() {

    document.getElementById("modalCheckout").style.display = "none";

}


// Mostrar u ocultar dirección


// Mostrar información según el método de pago
document.getElementById("metodoPago").addEventListener("change", e => {

    const metodo = e.target.value;
    const mensaje = document.getElementById("mensajePago");
    const contenedorPayPal = document.getElementById("paypal-container");
    const botonesPayPal = document.getElementById("paypal-button-container");

    if (metodo === "efectivo") {

        mensaje.textContent =
            "Pagarás en efectivo al momento de retirar o recibir tu pedido.";

        // Ocultar PayPal cuando se selecciona efectivo
        contenedorPayPal.hidden = true;
        botonesPayPal.innerHTML = "";

        window.pedidoPayPal = null;

    } else {

        mensaje.textContent =
            "Completa tu pago de forma segura mediante PayPal Sandbox.";

    }

});


document.getElementById("modalidad").addEventListener("change", e => {

    const campo = document.getElementById("campoDireccion");
    const direccion = document.getElementById("direccion");

    const domicilio = e.target.value === "domicilio";

    campo.hidden = !domicilio;
    direccion.required = domicilio;

});



 
// Registrar pedido
document.getElementById("formPedido").addEventListener("submit", async e => {

    e.preventDefault();

    const botonEnviar = e.submitter;
    if (botonEnviar) botonEnviar.disabled = true;

    
const datos = {
    carrito_id: carritoId,
    nombre_cliente: document.getElementById("nombreCliente").value,
    celular: document.getElementById("celular").value,
    documento: document.getElementById("documento").value,
    modalidad_entrega: document.getElementById("modalidad").value,
    metodo_pago: document.getElementById("metodoPago").value,
    direccion: document.getElementById("direccion").value || null,

    referencia: document.getElementById("referencia").value || null,

    latitud: document.getElementById("latitud").value
        ? Number(document.getElementById("latitud").value)
        : null,

    longitud: document.getElementById("longitud").value
        ? Number(document.getElementById("longitud").value)
        : null
};


    try {


        // Validar información de entrega a domicilio
        if (datos.modalidad_entrega === "domicilio") {

            if (!datos.direccion || !datos.direccion.trim()) {
                throw new Error(
                    "Debe ingresar la dirección de entrega."
                );
            }

            if (datos.latitud === null || datos.longitud === null) {
                throw new Error(
                    "Debe seleccionar la ubicación de entrega en el mapa."
                );
            }
        }

        // Si el cliente seleccionó tarjeta, iniciar PayPal
        if (datos.metodo_pago === "tarjeta") {

            const resultado = await solicitar(
                `${API}/pedidos/crear-pago`,
                {
                    method: "POST",
                    body: JSON.stringify(datos)
                }
            );

            // Guardar los datos necesarios para continuar el pago
            window.pedidoPayPal = {
    pedidoId: resultado.pedido_id,
    paypalOrderId: resultado.paypal_order_id,
    total: resultado.total
};

            // Mostrar el botón de PayPal
            document.getElementById("paypal-container").hidden = false;

            document.getElementById("resultadoCompra").innerHTML = `
                <div class="tracking-result">
                    <h3>Pedido preparado</h3>
                    <p>Número de pedido:
                        <strong>${resultado.pedido_id}</strong>
                    </p>
                    <p>Total: $${Number(resultado.total).toFixed(2)}</p>
                    <p>Completa el pago utilizando PayPal.</p>
                </div>
            `;

            // Evitar que el cliente vuelva a enviar el formulario
            if (botonEnviar) botonEnviar.disabled = false;

            // Dibujar los botones de PayPal
            mostrarBotonesPayPal();

            return;
        }

        // Pago en efectivo: conservar el proceso actual
        const pedido = await solicitar(
            `${API}/pedidos/`,
            {
                method: "POST",
                body: JSON.stringify(datos)
            }
        );

        document.getElementById("resultadoCompra").innerHTML = `
            <div class="tracking-result">
                <h3>¡Pedido registrado correctamente!</h3>
                <p>Número de seguimiento:
                    <strong>${pedido.pedido_id}</strong>
                </p>
                <p>Total: $${Number(pedido.total).toFixed(2)}</p>
                <p>Estado: ${pedido.estado}</p>
            </div>
        `;

        document.getElementById("pedidoConsulta").value = pedido.pedido_id;

        document.getElementById("contador").textContent = "0";
        carritoActual = null;

        document.getElementById("formPedido").reset();

        alert(
            "¡Compra realizada correctamente!\n\n" +
            "Número de seguimiento: " + pedido.pedido_id +
            "\nTotal: $" + Number(pedido.total).toFixed(2) +
            "\n\nEl número ya está colocado en el formulario de seguimiento."
        );

        cerrarCheckout();

    } catch (error) {

        mostrarError(error);

    } finally {

        if (botonEnviar) botonEnviar.disabled = false;

    }

});


// Mostrar botones de PayPal
function mostrarBotonesPayPal() {

    const contenedor = document.getElementById("paypal-button-container");

    // Evitar dibujar los botones varias veces
    contenedor.innerHTML = "";

    if (!window.paypal || !window.pedidoPayPal) {
        mostrarError(new Error("PayPal todavía no está disponible."));
        return;
    }

    paypal.Buttons({

        createOrder: function () {
            return window.pedidoPayPal.paypalOrderId;
        },

        onApprove: async function (data) {

            try {

                const pedido = await solicitar(
                    `${API}/pedidos/${window.pedidoPayPal.pedidoId}/capturar-pago`,
                    {
                        method: "POST",
                        body: JSON.stringify({})
                    }
                );

                document.getElementById("resultadoCompra").innerHTML = `
                    <div class="tracking-result">
                        <h3>¡Pago realizado correctamente!</h3>
                        <p>Número de pedido:
                            <strong>${pedido.pedido_id}</strong>
                        </p>
                        <p>Total pagado: $${Number(pedido.total).toFixed(2)}</p>
                        <p>Estado del pago: ${pedido.estado_pago}</p>
                    </div>
                `;

                document.getElementById("pedidoConsulta").value = pedido.pedido_id;
                document.getElementById("contador").textContent = "0";

                carritoActual = null;
                window.pedidoPayPal = null;

                document.getElementById("paypal-container").hidden = true;

                alert(
                    "¡Pago confirmado!\nNúmero de pedido: " +
                    pedido.pedido_id
                );

                cerrarCheckout();

            } catch (error) {

                mostrarError(error);

            }
        },

        onCancel: function () {
            alert(
                "El pago fue cancelado. Tu pedido permanece pendiente de pago."
            );
        },

        onError: function (error) {
            console.error("Error de PayPal:", error);
            mostrarError(new Error("Ocurrió un problema con PayPal."));
        }

    }).render("#paypal-button-container");
}


// ========================================
// SEGUIMIENTO DE PEDIDOS
// ========================================

async function consultarPedido() {

    const pedidoId = document.getElementById("pedidoConsulta").value.trim();

    if (!pedidoId) {
        alert("Ingresa el número de pedido");
        return;
    }

    const resultado = document.getElementById("resultadoPedido");

    try {

        const pedido = await solicitar(
            `${API}/pedidos/${encodeURIComponent(pedidoId)}`
        );

        
resultado.innerHTML = `
    <div class="tracking-result">
        <h3>Pedido ${pedido.pedido_id}</h3>
        <p>Cliente: ${pedido.cliente.nombre}</p>
        <p>Estado actual: <strong>${pedido.estado}</strong></p>
        <p>Modalidad: ${pedido.modalidad_entrega}</p>
        <p>Método de pago: <strong>${
            pedido.metodo_pago === "efectivo" ? "Efectivo" : "Tarjeta"
        }</strong></p>
        <p>Estado del pago: <strong>${
            pedido.estado_pago === "pendiente" ? "Pendiente de pago" :
            pedido.estado_pago === "aprobado" ? "Pagado" :
            "Pago rechazado"
        }</strong></p>
        <p>Total: $${Number(pedido.total).toFixed(2)}</p>

        <h4>Historial del pedido</h4>
        <ul>
            ${pedido.historial.map(item => `
                <li>
                    <strong>${item.estado}</strong>
                    <br>${new Date(item.fecha).toLocaleString("es-SV")}
                    <br>${item.observacion}
                </li>
            `).join("")}
        </ul>
    </div>
`;

    } catch (error) {

        resultado.textContent = error.message;

    }
}


// ========================================
// INICIAR TIENDA
// ========================================

async function iniciarTienda() {

    await cargarCategorias();

    await cargarRepuestos();

}

iniciarTienda();


// ==========================================
// MAPA DE UBICACIÓN PARA ENTREGA A DOMICILIO
// ==========================================

let mapaEntrega = null;
let marcadorEntrega = null;

// Mostrar mapa y permitir seleccionar ubicación
function inicializarMapaEntrega() {

    const contenedor = document.getElementById("mapaEntrega");

    if (!contenedor || !window.L) {
        console.error("No se pudo cargar Leaflet.");
        return;
    }

    // Evitar crear el mapa varias veces
    if (mapaEntrega) {
        mapaEntrega.invalidateSize();
        return;
    }

    // Coordenadas iniciales: San Salvador
    const ubicacionInicial = [13.6929, -89.2182];

    mapaEntrega = L.map("mapaEntrega").setView(
        ubicacionInicial,
        13
    );

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(mapaEntrega);

    // Seleccionar ubicación haciendo clic
    mapaEntrega.on("click", function(e) {
        seleccionarUbicacion(e.latlng.lat, e.latlng.lng);
    });

}

// Guardar coordenadas y colocar marcador
function seleccionarUbicacion(latitud, longitud) {

    const posicion = [latitud, longitud];

    if (marcadorEntrega) {
        marcadorEntrega.setLatLng(posicion);
    } else {
        marcadorEntrega = L.marker(posicion, {
            draggable: true
        }).addTo(mapaEntrega);

        // Permitir mover el marcador
        marcadorEntrega.on("dragend", function(e) {
            const nuevaPosicion = e.target.getLatLng();

            guardarCoordenadas(
                nuevaPosicion.lat,
                nuevaPosicion.lng
            );
        });
    }

    guardarCoordenadas(latitud, longitud);
}

// Actualizar campos del formulario
function guardarCoordenadas(latitud, longitud) {

    document.getElementById("latitud").value = latitud;
    document.getElementById("longitud").value = longitud;

    document.getElementById("coordenadasSeleccionadas").textContent =
        "Ubicación seleccionada: " +
        latitud.toFixed(6) + ", " +
        longitud.toFixed(6);
}

// Detectar cuando se selecciona entrega a domicilio
document.getElementById("modalidad").addEventListener("change", function(e) {

    const campoDireccion = document.getElementById("campoDireccion");

    if (e.target.value === "domicilio") {

        campoDireccion.hidden = false;

        setTimeout(function() {
            inicializarMapaEntrega();
            if (mapaEntrega) {
                mapaEntrega.invalidateSize();
            }
        }, 200);

    } else {

        campoDireccion.hidden = true;

    }

});
