from ODM import initApp

# Inicializar los cuatro modelos definidos en models.yml.
modelos = {}
initApp(scope=modelos)

Recinto = modelos["recinto"]
Artista = modelos["artista"]
Evento = modelos["evento"]
Asistente = modelos["asistente"]


# --------------------------------------------------
# 1. RECINTOS
# --------------------------------------------------

recintos = [
    {
        "nombre": "Movistar Arena",
        "direccion": "Movistar Arena, Madrid, Spain",
        "aforo": 17453,
        "zonas": {"pista": 5500, "grada": 11953},
        "servicios": ["bar", "accesibilidad", "guardarropa"],
    },
    {
        "nombre": "Palau Sant Jordi",
        "direccion": "Palau Sant Jordi, Barcelona, Spain",
        "aforo": 17960,
        "zonas": {"pista": 6000, "grada": 11960},
        "servicios": ["bar", "accesibilidad", "parking"],
    },
    {
        "nombre": "Bilbao Arena",
        "direccion": "Bilbao Arena, Bilbao, Spain",
        "aforo": 10014,
        "zonas": {"pista": 3000, "grada": 7014},
        "servicios": ["bar", "accesibilidad"],
    },
    {
        "nombre": "Auditorio Alfredo Kraus",
        "direccion": (
            "Auditorio Alfredo Kraus, "
            "Las Palmas de Gran Canaria, Spain"
        ),
        "aforo": 1656,
        "zonas": {"platea": 800, "anfiteatro": 856},
        "servicios": ["accesibilidad", "guardarropa"],
    },
    {
        "nombre": "Estadio Santiago Bernabeu",
        "direccion": "Estadio Santiago Bernabeu, Madrid, Spain",
        "aforo": 83186,
        "zonas": {"pista": 25000, "grada": 58186},
        "servicios": ["bar", "accesibilidad", "parking"],
    },
]


# --------------------------------------------------
# 2. ARTISTAS
# --------------------------------------------------

artistas = [
    {
        "nombre": "Rosalia",
        "pais_origen": "España",
        "anio_inicio": 2013,
        "generos": ["pop", "flamenco"],
    },
    {
        "nombre": "Alejandro Sanz",
        "pais_origen": "España",
        "anio_inicio": 1988,
        "generos": ["pop", "flamenco"],
    },
    {
        "nombre": "Aitana",
        "pais_origen": "España",
        "anio_inicio": 2017,
        "generos": ["pop"],
    },
    {
        "nombre": "Vetusta Morla",
        "pais_origen": "España",
        "anio_inicio": 1998,
        "generos": ["indie rock"],
    },
    {
        "nombre": "Amaral",
        "pais_origen": "España",
        "anio_inicio": 1997,
        "generos": ["pop rock"],
    },
    {
        "nombre": "Bad Gyal",
        "pais_origen": "España",
        "anio_inicio": 2016,
        "generos": ["dancehall", "regueton"],
    },
    {
        "nombre": "Coldplay",
        "pais_origen": "Reino Unido",
        "anio_inicio": 1997,
        "generos": ["pop rock", "alternative rock"],
    },
    {
        "nombre": "Dani Martin",
        "pais_origen": "España",
        "anio_inicio": 2000,
        "generos": ["pop rock"],
    },
]


# --------------------------------------------------
# 3. EVENTOS
# --------------------------------------------------

eventos = [
    {
        "titulo": "Gira de Alejandro Sanz",
        "artistas": ["Alejandro Sanz"],
        "recinto": "Movistar Arena",
        "fecha": "2018-06-14",
        "hora": "21:00",
        "precios_zona": {"pista": 70, "grada": 55},
        "entradas_vendidas": 12000,
    },
    {
        "titulo": "Concierto de Amaral",
        "artistas": ["Amaral"],
        "recinto": "Palau Sant Jordi",
        "fecha": "2019-10-03",
        "hora": "20:30",
        "precios_zona": {"pista": 50, "grada": 35},
        "entradas_vendidas": 8500,
    },
    {
        "titulo": "Invierno Indie",
        "artistas": ["Vetusta Morla", "Dani Martin"],
        "recinto": "Bilbao Arena",
        "fecha": "2020-02-15",
        "hora": "20:00",
        "precios_zona": {"pista": 40, "grada": 30},
        "entradas_vendidas": 8000,
    },
    {
        "titulo": "Pop en Canarias",
        "artistas": ["Aitana"],
        "recinto": "Auditorio Alfredo Kraus",
        "fecha": "2021-09-05",
        "hora": "19:30",
        "precios_zona": {"platea": 45, "anfiteatro": 30},
        "entradas_vendidas": 1200,
    },
    {
        "titulo": "Rosalia en Madrid",
        "artistas": ["Rosalia"],
        "recinto": "Movistar Arena",
        "fecha": "2022-07-18",
        "hora": "21:00",
        "precios_zona": {"pista": 85, "grada": 65},
        "entradas_vendidas": 16000,
    },
    {
        "titulo": "Noches de Barcelona",
        "artistas": ["Bad Gyal"],
        "recinto": "Palau Sant Jordi",
        "fecha": "2023-03-16",
        "hora": "21:30",
        "precios_zona": {"pista": 55, "grada": 40},
        "entradas_vendidas": 14500,
    },
    {
        "titulo": "Coldplay en Madrid",
        "artistas": ["Coldplay"],
        "recinto": "Estadio Santiago Bernabeu",
        "fecha": "2024-06-20",
        "hora": "21:00",
        "precios_zona": {"pista": 110, "grada": 80},
        "entradas_vendidas": 78000,
    },
    {
        "titulo": "Musica en Bilbao",
        "artistas": ["Vetusta Morla", "Amaral"],
        "recinto": "Bilbao Arena",
        "fecha": "2025-05-09",
        "hora": "20:00",
        "precios_zona": {"pista": 45, "grada": 35},
        "entradas_vendidas": 9500,
    },
    {
        "titulo": "EnVivo Summer",
        "artistas": ["Coldplay", "Aitana"],
        "recinto": "Estadio Santiago Bernabeu",
        "fecha": "2026-06-22",
        "hora": "21:00",
        "precios_zona": {"pista": 120, "grada": 90},
        "entradas_vendidas": 72000,
    },
    {
        "titulo": "Cierre de Gira",
        "artistas": ["Alejandro Sanz", "Rosalia"],
        "recinto": "Palau Sant Jordi",
        "fecha": "2026-09-18",
        "hora": "20:30",
        "precios_zona": {"pista": 75, "grada": 55},
        "entradas_vendidas": 17000,
    },
]


# --------------------------------------------------
# 4. ASISTENTES
# --------------------------------------------------

asistentes = [
    {
        "nombre": "Lucia Fernandez",
        "email": "lucia@example.com",
        "fecha_alta": "2020-01-12",
        "direccion": "Puerta del Sol, Madrid, Spain",
        "preferencias_genero": ["pop", "flamenco"],
    },
    {
        "nombre": "Mario Gomez",
        "email": "mario@example.com",
        "fecha_alta": "2021-05-04",
        "direccion": "Placa de Catalunya, Barcelona, Spain",
        "preferencias_genero": ["indie rock"],
    },
    {
        "nombre": "Sara Lopez",
        "email": "sara@example.com",
        "fecha_alta": "2022-08-30",
        "direccion": "Plaza Nueva, Bilbao, Spain",
        "preferencias_genero": ["pop rock"],
    },
    {
        "nombre": "Pablo Ruiz",
        "email": "pablo@example.com",
        "fecha_alta": "2023-02-18",
        "preferencias_genero": ["regueton"],
    },
    {
        "nombre": "Elena Martin",
        "email": "elena@example.com",
        "fecha_alta": "2023-11-09",
        "preferencias_genero": ["pop"],
    },
    {
        "nombre": "Diego Torres",
        "email": "diego@example.com",
        "fecha_alta": "2024-04-22",
        "preferencias_genero": ["indie rock", "pop rock"],
    },
    {
        "nombre": "Carmen Vega",
        "email": "carmen@example.com",
        "fecha_alta": "2025-01-15",
        "preferencias_genero": ["flamenco"],
    },
    {
        "nombre": "Hugo Martin",
        "email": "hugo@example.com",
        "fecha_alta": "2025-09-03",
        "preferencias_genero": ["dancehall"],
    },
]


# --------------------------------------------------
# 5. LIMPIAR SOLO NUESTROS DATOS DE EJEMPLO
# --------------------------------------------------

# Permite volver a ejecutar este script sin duplicar sus documentos.
# No borra documentos ajenos a este conjunto de datos.

Recinto._db.delete_many({
    "nombre": {"$in": [d["nombre"] for d in recintos]}
})

Artista._db.delete_many({
    "nombre": {"$in": [d["nombre"] for d in artistas]}
})

Evento._db.delete_many({
    "titulo": {"$in": [d["titulo"] for d in eventos]}
})

Asistente._db.delete_many({
    "email": {"$in": [d["email"] for d in asistentes]}
})


# --------------------------------------------------
# 6. GUARDAR LOS DOCUMENTOS
# --------------------------------------------------

print("Guardando recintos...")
for datos in recintos:
    Recinto(**datos).save()
print("Recintos guardados:", len(recintos))

print("\nGuardando artistas...")
for datos in artistas:
    Artista(**datos).save()
print("Artistas guardados:", len(artistas))

print("\nGuardando eventos...")
for datos in eventos:
    Evento(**datos).save()
print("Eventos guardados:", len(eventos))

print("\nGuardando asistentes...")
for datos in asistentes:
    Asistente(**datos).save()
print("Asistentes guardados:", len(asistentes))


# --------------------------------------------------
# 7. RESUMEN FINAL
# --------------------------------------------------

print("\nResumen de las colecciones:")

for nombre, modelo in modelos.items():
    total = modelo._db.count_documents({})
    print(f"{nombre}: {total} documentos")

print("\nCarga de datos finalizada.")