__author__ = 'Pablo Ramos Criado'
__students__ = 'Santiago Martín Bardera y Quanwg Wang'


from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from typing import Generator, Any, Self
from geojson import Point
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import yaml

def getLocationPoint(address: str) -> Point:
    location = None
    intentos = 0
    maxIntentos = 5

    geolocator = Nominatim(user_agent="abd-practica1")

    while location is None and intentos < maxIntentos:
        intentos += 1

        try:
            time.sleep(1)
            location = geolocator.geocode(address)

        except GeocoderTimedOut:
            continue

    if location is None:
        raise ValueError("No se pudieron obtener coordenadas")

    return Point((location.longitude, location.latitude))

class Model:
    """ 
    Clase de modelo abstracta
    Crear tantas clases que hereden de esta clase como  
    colecciones/modelos se deseen tener en la base de datos.

    Attributes
    ----------
        required_vars : set[str]
            conjunto de atributos requeridos por el modelo
        admissible_vars : set[str]
            conjunto de atributos admitidos por el modelo
        db : pymongo.collection.Collection
            conexion a la coleccion de la base de datos
    
    Methods
    -------
        __setattr__(name: str, value: str | dict) -> None
            Sobreescribe el metodo de asignacion de valores a los 
            atributos del objeto con el fin de controlar qué atributos 
            son modificados y cuando son modificados.
        __getattr__(name: str) -> Any
            Sobreescribe el metodo de acceso a atributos del objeto 
        save()  -> None
            Guarda el modelo en la base de datos
        delete() -> None
            Elimina el modelo de la base de datos
        find(filter: dict[str, str | dict]) -> ModelCursor
            Realiza una consulta de lectura en la BBDD.
            Devuelve un cursor de modelos ModelCursor
        aggregate(pipeline: list[dict]) -> pymongo.command_cursor.CommandCursor
            Devuelve el resultado de una consulta aggregate.
        find_by_id(id: str) -> dict | None
            Busca un documento por su id utilizando la cache y lo devuelve.
            Si no se encuentra el documento, devuelve None.
        init_class(db_collection: pymongo.collection.Collection, required_vars: set[str], admissible_vars: set[str]) -> None
            Inicializa las variables de clase en la inicializacion del sistema.

    """
    _required_vars: set[str]
    _admissible_vars: set[str]
    _location_var: str | None = None
    _db: pymongo.collection.Collection
    _internal_vars: set[str] = frozenset(('_modified_vars', '_required_vars', '_admissible_vars', '_db', '_data', '_location_var'))

    def __init__(self, **kwargs: dict[str, str | dict | list]) -> None:
        """
        Inicializa el modelo con los valores proporcionados en kwargs
        Comprueba que los valores proporcionados en kwargs son admitidos
        por el modelo y que las atributos requeridos son proporcionadas.

        Parameters
        ----------
            kwargs : dict[str, str | dict]
                diccionario con los valores de las atributos del modelo
        """
        self._data: dict[str, str | dict | list] = {}
        #TODO
        # Realizar las comprabociones y gestiones necesarias
        # antes de la asignacion.
        self._modified_vars = set()

        received_vars = set(kwargs.keys())

        allowed_vars = self._required_vars | self._admissible_vars | {"_id"}

        if self._location_var is not None:
            allowed_vars.add(f"{self._location_var}_loc")

        missing_vars = self._required_vars - received_vars

        if missing_vars:
            raise ValueError(
                f"Faltan atributos requeridos: {', '.join(sorted(missing_vars))}"
            )

        invalid_vars = received_vars - allowed_vars

        if invalid_vars:
            raise ValueError(
                f"Atributos no admitidos: {', '.join(sorted(invalid_vars))}"
            )
        # Asigna todos los valores en kwargs a las atributos con 
        # nombre las claves en kwargs
        # Utilizamos el atributo data para guardar los variables 
        # almacenadas en la base de datos en una solo atributo
        # Encapsular los datos en una sola variable facilita la 
        # gestion en metodos como save.
        self._data.update(kwargs)

    def __setattr__(self, name: str, value: str | dict) -> None:
        """ Sobreescribe el metodo de asignacion de valores a los 
        atributos del objeto con el fin de controlar que atributos 
        son modificados y cuando son modificados.
        """
        if name in self._internal_vars:
            super().__setattr__(name, value)
            return
        #TODO
        allowed_vars = self._required_vars | self._admissible_vars

        if name not in allowed_vars:
            raise ValueError(f"Atributo no admitido: {name}")

        self._modified_vars.add(name)
        # Realizar las comprabociones y gestiones necesarias
        # antes de la asignacion.

        # Asigna el valor value a la variable name
        self._data[name] = value

    def __getattr__(self, name: str) -> Any:
        """ Sobreescribe el metodo de acceso a atributos del objeto
        __getattr__ solo es llamado cuando no encuentra el atributo
        en el objeto 
        """
        if name in self._internal_vars:
            return super().__getattribute__(name)
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError
        
    def save(self) -> None:

        # Documento nuevo
        if "_id" not in self._data:

            document = self._data.copy()

            if (
                self._location_var is not None
                and self._location_var in document
            ):
                location_field = f"{self._location_var}_loc"
                document[location_field] = getLocationPoint(
                    document[self._location_var]
                )

            result = self._db.insert_one(document)

            self._data.update(document)
            self._data["_id"] = result.inserted_id

            self._modified_vars.clear()
            return

        # Documento ya existente
        if not self._modified_vars:
            return

        modified_data = {
            field: self._data[field]
            for field in self._modified_vars
        }

        if (
            self._location_var is not None
            and self._location_var in self._modified_vars
        ):
            location_field = f"{self._location_var}_loc"

            location_point = getLocationPoint(
                self._data[self._location_var]
            )

            modified_data[location_field] = location_point
            self._data[location_field] = location_point

        self._db.update_one(
            {"_id": self._data["_id"]},
            {"$set": modified_data}
        )

        self._modified_vars.clear()

    def delete(self) -> None:

        if "_id" not in self._data:
            return

        self._db.delete_one(
            {"_id": self._data["_id"]}
        )

        del self._data["_id"]
        self._modified_vars.clear()
    
    @classmethod
    def find(cls, filter: dict[str, str | dict]) -> Any:
        cursor = cls._db.find(filter)
        return ModelCursor(cls, cursor)

    @classmethod
    def aggregate(cls, pipeline: list[dict]) -> pymongo.command_cursor.CommandCursor:
        """ 
        Devuelve el resultado de una consulta aggregate. 
        No hay nada que hacer en esta funcion.
        Se utilizara para las consultas solicitadas
        en el segundo proyecto de la practica.

        Parameters
        ----------
            pipeline : list[dict]
                lista de etapas de la consulta aggregate 
        Returns
        -------
            pymongo.command_cursor.CommandCursor
                cursor de pymongo con el resultado de la consulta
        """ 
        return cls._db.aggregate(pipeline)
    
    @classmethod
    def find_by_id(cls, id: str) -> Self | None:
        """ 
        NO IMPLEMENTAR HASTA EL TERCER PROYECTO
        Busca un documento por su id utilizando la cache y lo devuelve.
        Si no se encuentra el documento, devuelve None.

        Parameters
        ----------
            id : str
                id del documento a buscar
        Returns
        -------
            Self | None
                Modelo del documento encontrado o None si no se encuentra
        """ 
        #TODO
        pass

    @classmethod
    def init_class(cls, db_collection: pymongo.collection.Collection, indexes:dict[str,str], required_vars: set[str], admissible_vars: set[str]) -> None:
        """ 
        Inicializa los atributos de clase en la inicializacion del sistema.
        Aqui se deben inicializar o asegurar los indices. Tambien se puede
        alguna otra inicialización/comprobaciones o cambios adicionales
        que estime el alumno.

        Parameters
        ----------
            db_collection : pymongo.collection.Collection
                Conexion a la collecion de la base de datos.
            indexes: Dict[str,str]
                Set de indices y tipo de indices para la coleccion
            required_vars : set[str]
                Set de atributos requeridos por el modelo
            admissible_vars : set[str] 
                Set de atributos admitidos por el modelo
        """
        cls._db = db_collection
        cls._required_vars = required_vars
        cls._admissible_vars = admissible_vars
        cls._location_var = None

        for field, index_type in indexes.items():

            if index_type == "unique":
                cls._db.create_index(
                    [(field, pymongo.ASCENDING)],
                    unique=True
                )

            elif index_type == "asc":
                cls._db.create_index(
                    [(field, pymongo.ASCENDING)]
                )

            elif index_type == "geosphere":
                cls._location_var = field

                cls._db.create_index(
                    [(f"{field}_loc", pymongo.GEOSPHERE)]
                )
        # TODO
        # Recorrer indexes y crear cada índice segun su tipo: 'unique', 'asc'
        # y 'geosphere'. Comparar el tipo por igualdad, no con el operador 'in'.
        # Ojo con el índice geoespacial: save() guarda el GeoJSON Point en
        # <campo>_loc, luego el índice 2dsphere va sobre <campo>_loc, mientras
        # que _location_var debe guardar el nombre del campo base.


class ModelCursor:
    """ 
    Cursor para iterar sobre los documentos del resultado de una
    consulta. Los documentos deben ser devueltos en forma de objetos
    modelo.

    Attributes
    ----------
        model_class : Model
            Clase para crear los modelos de los documentos que se iteran.
        cursor : pymongo.cursor.Cursor
            Cursor de pymongo a iterar

    Methods
    -------
        __iter__() -> Generator
            Devuelve un iterador que recorre los elementos del cursor
            y devuelve los documentos en forma de objetos modelo.
    """

    def __init__(self, model_class: Model, cursor: pymongo.cursor.Cursor):
        """
        Inicializa el cursor con la clase de modelo y el cursor de pymongo

        Parameters
        ----------
            model_class : Model
                Clase para crear los modelos de los documentos que se iteran.
            cursor: pymongo.cursor.Cursor
                Cursor de pymongo a iterar
        """
        self.model = model_class
        self.cursor = cursor
    
    def __iter__(self) -> Generator:
        while self.cursor.alive:
            try:
                document = next(self.cursor)
            except StopIteration:
                break

            yield self.model(**document)


def initApp(definitions_path: str = "./models.yml",mongodb_uri="mongodb://localhost:27017/",db_name="abd",scope=globals()) -> None:

    # Conexión a MongoDB
    client = MongoClient(mongodb_uri)
    db = client[db_name]

    # Leer las definiciones del YAML
    with open(definitions_path, "r", encoding="utf-8") as file:
        definitions = yaml.safe_load(file)

    # Crear dinámicamente una clase por cada modelo del YAML
    for model_name, definition in definitions.items():

        required_vars = set(definition.get("required_vars", []))
        admissible_vars = set(definition.get("admissible_vars", []))

        indexes = {}

        for field in definition.get("unique_indexes", []):
            indexes[field] = "unique"

        for field in definition.get("regular_indexes", []):
            indexes[field] = "asc"

        location = definition.get("location_index")

        if location is not None:
            indexes[location] = "geosphere"

        # Crear clase dinámicamente
        scope[model_name] = type(model_name, (Model,), {})

        # Inicializarla
        scope[model_name].init_class(db_collection=db[model_name],indexes=indexes,required_vars=required_vars,admissible_vars=admissible_vars)

if __name__ == '__main__':
    
    # Inicializar base de datos y modelos con initApp
    #TODO
    initApp()

    #Ejemplo
    m = MiModelo(nombre="Pablo", apellido="Ramos", edad=18)
    m.save()
    m.nombre="Pedro"
    print(m.nombre)

    # Hacer pruebas para comprobar que funciona correctamente el modelo
    #TODO
    # Crear modelo

    # Asignar nuevo valor a variable admitida del objeto 

    # Asignar nuevo valor a variable no admitida del objeto 

    # Guardar

    # Asignar nuevo valor a variable admitida del objeto

    # Guardar

    # Buscar nuevo documento con find

    # Obtener primer documento

    # Modificar valor de variable admitida

    # Guardar