
# Catálogo inicial de vehículos de Express Repuestos

# Los modelos y años son datos de demostración.
# La compatibilidad real deberá verificarse con el catálogo
# de cada fabricante antes de vender una pieza.

CATALOGO_VEHICULOS = {

    "automovil": {
        "Toyota": [
            "Corolla", "Yaris", "Hilux", "RAV4", "Prado"
        ],
        "Nissan": [
            "Sentra", "Versa", "Frontier", "X-Trail", "Altima"
        ],
        "Hyundai": [
            "Accent", "Elantra", "Tucson", "Santa Fe", "Creta"
        ],
        "Kia": [
            "Rio", "Sportage", "Cerato", "Sorento", "Picanto"
        ],
        "Mitsubishi": [
            "Lancer", "L200", "Outlander", "Montero", "ASX"
        ],
        "Mazda": [
            "Mazda 2", "Mazda 3", "CX-3", "CX-5", "BT-50"
        ],
        "Chevrolet": [
            "Spark", "Aveo", "Cruze", "Colorado", "Tracker"
        ],
        "Ford": [
            "Focus", "Ranger", "Escape", "Explorer", "Fiesta"
        ],
        "Honda": [
            "Civic", "Accord", "CR-V", "Fit", "HR-V"
        ],
        "Volkswagen": [
            "Jetta", "Golf", "Tiguan", "Polo", "Passat"
        ]
    },

    "motocicleta": {
        "Honda": [
            "CB125F", "CB190R", "XR150L", "Navi", "CBR250R"
        ],
        "Yamaha": [
            "FZ", "FZ-S", "Crypton", "R15", "NMAX"
        ],
        "Suzuki": [
            "GN125", "Gixxer", "AX100", "V-Strom", "EN125"
        ],
        "Bajaj": [
            "Boxer", "Pulsar 150", "Pulsar NS200",
            "Discover", "Dominar 400"
        ],
        "TVS": [
            "Apache", "HLX", "Sport", "Ntorq", "Raider"
        ],
        "Hero": [
            "Hunk", "Eco Deluxe", "Splendor", "XPulse", "Ignitor"
        ],
        "AKT": [
            "NKD 125", "TT 125", "CR4", "Dynamic", "TTR"
        ],
        "Kawasaki": [
            "Ninja 400", "Z400", "Versys", "KLX", "Ninja 650"
        ],
        "BMW": [
            "G 310 R", "G 310 GS", "F 800 GS", "R 1250 GS"
        ],
        "KTM": [
            "Duke 200", "Duke 390", "Adventure 390",
            "RC 200", "Adventure 250"
        ]
    }
}

# Años disponibles inicialmente para pruebas
ANIOS_DISPONIBLES = list(range(2000, 2027))
