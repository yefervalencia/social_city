# social_city

DESARROLLADORES
Yeferson Valencia Aristizabal
Fabian Hernandez Castaño

Desarrollo de un proyecto de backend completo elaborado en fastapi como framework y python como lenguaje oficial del proyecto
consiste en una api que almacenara informacion sobre los lugares,reuniones o llamados urbanamente como parches donde se manejaran ususarios, parches, categorias, comentarios calificacion desarrollarlo de forma escalable para que aplique en varias ciudades.

Diagrama de Clases para la estructura del API:
![Diagrama sin título drawio](https://github.com/yefervalencia/social_city/assets/123003082/df5b3edf-d7ea-40c4-b4e4-52ca9654a0a0)


## Requisitos

- Python 3.10+
- FastAPI
- SQLAlchemy
- Uvicorn
- Pydantic

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/yefervalencia/social_city.git
    cd social_city
    ```

2. Crea y activa un entorno virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Configura la base de datos en el archivo `src/config/database.py` con tus propias credenciales.

5. Realiza las migraciones de la base de datos (si estás usando Alembic):
    ```sh
    alembic upgrade head
    ```

## Ejecución

Para ejecutar la aplicación en modo desarrollo, usa:

```sh
uvicorn main:app --reload

La aplicación estará disponible en http://127.0.0.1:8000.


Este archivo README incluye una descripción general del proyecto, los requisitos, las instrucciones de instalación y ejecución, una descripción detallada de cada endpoint disponible en la API, la estructura del proyecto y la información sobre la licencia del proyecto. Puedes ajustarlo según las necesidades específicas de tu proyecto.
