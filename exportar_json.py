from pathlib import Path

from bson.json_util import dumps
from pymongo import MongoClient


# Conectar con la base de datos de EnVivo.
client = MongoClient("mongodb://localhost:27017/")
db = client["abd"]

colecciones = [
    "recinto",
    "artista",
    "evento",
    "asistente",
]

try:
    for nombre in colecciones:
        documentos = list(db[nombre].find({}))

        # Guardar el volcado en un JSON en la raíz del proyecto.
        archivo = Path(f"{nombre}.json")

        contenido = dumps(
            documentos,
            indent=2,
            ensure_ascii=False,
        )

        archivo.write_text(contenido, encoding="utf-8")

        print(
            f"OK: {archivo.name} "
            f"({len(documentos)} documentos)"
        )

    print("\nExportación terminada.")

finally:
    client.close()