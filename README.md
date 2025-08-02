# RETO TECNICO/ EDGAR NAJAR/ AEROMEXICO/ Alimentos y Bebidas

## Español
### Proyecto
Se debe ccrear una API REST desde cero para un sistema de inventarios de Alimentos y Bebidas, que implemente un CRUD usando Python.

#### Requisitos
1.- Crear un proyecto backend con cualquier tecnología como (FastAPI).

2.-.- Base de datos:

2.1.- Conectar a una base de datos H2 en memoria

2.2.- Crear las tablas automáticamente desde entidades o con scripts.

3.- Implementar un CRUD de alimentos y bebidas, con una tabla con los siguientes campos:

3.1.- id: identificador único.

3.2.- nombre: string obligatorio.

3.3.- descripción: texto opcional.

3.4.- estatus: activo/inactivo (boolean o enum).

4.- Escribir al menos una prueba unitaria de un método del CRUD.

5.- Opcional pero valorado:

5.1.- Validaciones en los endpoints.

5.2.- Logs básicos.

5.3.- Manejo de errores.

#### Desarrollo
Se desarrollo con la siguiente estructura:

food_inventory/

├── tests/

│   └── test_main.py

├── crud.py

├── database.py

├── main.py

├── models.py

├── requirements.txt

└── schemas.py

##### test/test_main.py
Este módulo contiene pruebas unitarias para los endpoints de la API mediante pytest y TestClient. Configura una base de datos aislada en memoria para cada prueba, garantizando así su independencia.
##### crud.py
Este módulo contiene la lógica principal de creación, lectura, actualización y eliminación (CRUD) para interactuar con la base de datos.
##### database.py
Este módulo configura la conexión a la base de datos. Utilizamos SQLite en memoria para simplificar y garantizar la compatibilidad directa con Python, ya que H2 es una base de datos Java y requeriría una configuración más compleja (por ejemplo, mediante JPype) para la interacción directa con Python.
##### main.py
Este es el archivo principal de la aplicación FastAPI, que define los puntos finales de la API.
##### models.py
Este módulo define el modelo ORM de SQLAlchemy para nuestros artículos de inventario.
##### requirements.txt
Este archivo enumera todos los paquetes de Python necesarios.
##### schemas.py
Este módulo define modelos de Pydantic para la validación y serialización de datos de solicitud y respuesta.

#### Ejecución
Instalar dependencias:

pip install -r food_inventory/requirements.txt

Si ocurre algún problema o error, simplemente:

pip install fastapi uvicorn sqlalchemy pydantic pytest httpx

Ejecutar la aplicación FastAPI:

uvicorn food_inventory.main:app --reload

El parámetro --reload reiniciará automáticamente el servidor al realizar cambios en el código.
Acceder a la API:

Documentación interactiva (Swagger UI): Abra su navegador y vaya a http://127.0.0.1:8000/docs

Documentación alternativa (ReDoc): Abra su navegador y vaya a http://127.0.0.1:8000/redoc

Puede usar herramientas como curl, Postman, Insomnia o la documentación interactiva para probar los endpoints.

#### Cómo ejecutar las pruebas
Vaya a la raíz de su proyecto (el directorio que contiene food_inventory).

Ejecute pytest:

pytest food_inventory/tests/

## English
### Project
A REST API must be created from scratch for a Food and Beverage inventory system that implements CRUD using Python.

#### Requirements
1.- Create a backend project using any technology such as (FastAPI).

2.- Database:

2.1.- Connect to an in-memory H2 database.

2.2.- Create tables automatically from entities or with scripts.

3.- Implement a CRUD for food and beverages, with a table containing the following fields:

3.1.- id: unique identifier

3.2.- name: required string

3.3.- description: optional text

3.4.- status: active/inactive (boolean or enum).

4.- Write at least one unit test for a CRUD method.

5.- Optional but highly valued:

5.1.- Endpoint validations

5.2.- Basic logs

5.3.- Error handling

#### Development
Development was carried out with the following structure:

food_inventory/

├── tests/

│ └── test_main.py

├── crud.py

├── database.py

├── main.py

├── models.py

├── requirements.txt

└── schemas.py

##### test/test_main.py
This module contains unit tests for the API endpoints using pytest and TestClient. It sets up an isolated in-memory database for each test to ensure test independence.
##### crud.py
This module contains the core Create, Read, Update, Delete (CRUD) logic for interacting with the database.
#### database.py
This module sets up the database connection. We use SQLite in-memory for simplicity and direct Python compatibility, as H2 is a Java database and would require more complex setup (e.g., via JPype) for direct Python interaction.
##### main.py
This is the main FastAPI application file, defining the API endpoints.
##### models.py
This module defines the SQLAlchemy ORM model for our inventory items.
##### requirements.txt
This file lists all the necessary Python packages.
##### schemas.py
This module defines Pydantic models for request and response data validation and serialization.

#### Ejecution
Install dependencies:

pip install -r food_inventory/requirements.txt

If some issue or error acurres, just:

pip install fastapi uvicorn sqlalchemy pydantic pytest httpx

Run the FastAPI application:
uvicorn food_inventory.main:app --reload

The --reload flag will automatically restart the server on code changes.
Access the API:

Interactive Docs (Swagger UI): Open your browser and go to http://127.0.0.1:8000/docs

Alternative Docs (ReDoc): Open your browser and go to http://127.0.0.1:8000/redoc

You can use tools like curl, Postman, Insomnia, or the interactive docs to test the endpoints.

#### How to Run the Tests
Navigate to the root of your project (the directory containing food_inventory).
Run pytest:
pytest food_inventory/tests/

