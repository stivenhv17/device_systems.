# device_systems

API desarrollada con **Python y FastAPI** para la gestión de usuarios mediante diferentes endpoints. El proyecto permite consultar, registrar, actualizar y eliminar usuarios a través de una API REST.

En esta nueva versión se mejoró la estructura del proyecto separando las rutas, esquemas, servicios, dependencias y los datos de los usuarios. También se agregaron validaciones, manejo de errores, actualización completa y parcial de usuarios y eliminación de registros.

La documentación y las pruebas de los endpoints se realizan mediante **Swagger UI** y **ReDoc**, proporcionados automáticamente por FastAPI.

---

## Tecnologías utilizadas

* Python
* FastAPI
* Pydantic
* Uvicorn
* Swagger UI
* ReDoc
* UV
* Entorno virtual de Python

---

## Descripción de la aplicación

`device_systems` es una aplicación backend desarrollada con FastAPI que permite gestionar información de usuarios.

La API cuenta con endpoints para:

* Consultar todos los usuarios.
* Consultar un usuario específico mediante su ID.
* Registrar nuevos usuarios.
* Actualizar completamente un usuario.
* Actualizar parcialmente un usuario.
* Eliminar usuarios.
* Filtrar usuarios por rol y estado.
* Validar correos electrónicos.
* Evitar correos duplicados.
* Validar los roles permitidos.
* Manejar errores mediante códigos de respuesta HTTP.

Los usuarios se almacenan temporalmente en una lista que funciona como una base de datos en memoria.

---

## Instalación de dependencias

El proyecto utiliza un entorno virtual para mantener separadas las dependencias de la aplicación.

### Sincronizar el proyecto con UV

Si se utiliza UV, las dependencias del proyecto pueden instalarse mediante:

```bash
uv sync
```

También se dispone del archivo `requirements.txt` con las dependencias utilizadas.

---

## Ejecución del servidor

Para iniciar el servidor de desarrollo se utiliza Uvicorn.

En Windows, utilizando el entorno virtual del proyecto:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

El servidor estará disponible en:

```text
http://127.0.0.1:8000
```

La aplicación puede comprobarse desde:

```text
http://127.0.0.1:8000/
```

---

## Swagger UI

FastAPI genera automáticamente una interfaz de documentación interactiva mediante Swagger UI.

Se encuentra disponible en:

```text
http://127.0.0.1:8000/docs
```

Desde Swagger UI es posible:

* Visualizar los endpoints.
* Consultar los métodos HTTP disponibles.
* Ejecutar peticiones.
* Enviar parámetros.
* Enviar información en formato JSON.
* Revisar las respuestas de la API.
* Comprobar los códigos de respuesta.

---

## ReDoc

FastAPI también genera automáticamente una documentación mediante ReDoc.

Se encuentra disponible en:

```text
http://127.0.0.1:8000/redoc
```

ReDoc permite consultar la documentación de los endpoints de una forma organizada y facilita la revisión de la API.

---

# Tabla de endpoints

| Método | Endpoint | Descripción | Respuesta |
|---|---|---|---|
| GET | `/users` | Obtiene la lista de usuarios. | 200 |
| GET | `/users/{user_id}` | Obtiene un usuario específico mediante su ID. | 200 / 404 |
| POST | `/users` | Registra un nuevo usuario. | 201 / 400 |
| PUT | `/users/{user_id}` | Actualiza completamente un usuario. | 200 / 400 / 404 |
| PATCH | `/users/{user_id}` | Actualiza parcialmente un usuario. | 200 / 400 / 404 |
| DELETE | `/users/{user_id}` | Elimina un usuario. | 204 / 404 |

---

# Ejemplos de peticiones

## GET `/users`

Permite obtener todos los usuarios registrados.

```http
GET /users
```

Ejemplo de respuesta:

```json
[
    {
        "id": 1,
        "name": "Carlos",
        "email": "carlos@example.com",
        "role": "admin",
        "is_active": true
    },
    {
        "id": 2,
        "name": "Laura",
        "email": "laura@example.com",
        "role": "support",
        "is_active": true
    },
    {
        "id": 3,
        "name": "Miguel",
        "email": "miguel@example.com",
        "role": "user",
        "is_active": false
    }
]
```

También se pueden utilizar filtros:

```text
GET /users?role=admin
```

```text
GET /users?is_active=true
```

---

## GET `/users/{user_id}`

Permite consultar un usuario específico mediante su ID.

```http
GET /users/2
```

Ejemplo de respuesta:

```json
{
    "id": 2,
    "name": "Laura",
    "email": "laura@example.com",
    "role": "support",
    "is_active": true
}
```

Si el usuario no existe, se genera una respuesta `404 Not Found`.

---

## POST `/users`

Permite registrar un nuevo usuario.

```http
POST /users
```

Ejemplo de cuerpo JSON:

```json
{
    "name": "Andres Perez",
    "email": "andresperez@example.com",
    "role": "support",
    "is_active": true
}
```

Los roles permitidos son:

```text
admin
support
user
```

Cuando el usuario se crea correctamente, la API responde con:

```text
201 Created
```

Si el correo ya se encuentra registrado, la API devuelve:

```text
400 Bad Request
```

---

## PUT `/users/{user_id}`

Permite realizar una actualización completa de un usuario.

```http
PUT /users/4
```

Ejemplo de cuerpo JSON:

```json
{
    "name": "Andres Perez",
    "email": "andresperez@example.com",
    "role": "support",
    "is_active": true
}
```

En PUT se deben enviar todos los campos definidos para el usuario.

---

## PATCH `/users/{user_id}`

Permite actualizar solamente algunos campos de un usuario.

```http
PATCH /users/4
```

Ejemplo:

```json
{
    "name": "Andres P"
}
```

En este caso solamente se modifica el nombre.

No se permite realizar un PATCH vacío:

```json
{}
```

Si se intenta realizar esta operación, la API responde con:

```text
400 Bad Request
```

---

## DELETE `/users/{user_id}`

Permite eliminar un usuario existente.

```http
DELETE /users/4
```

Cuando la operación se realiza correctamente, la API responde:

```text
204 No Content
```

Si el usuario no existe, responde:

```text
404 Not Found
```

---

# Validaciones

Para mejorar el funcionamiento de la API se implementaron diferentes validaciones.

## Validación de datos

Los datos recibidos por la API son validados mediante Pydantic.

Por ejemplo, el campo `email` debe tener un formato válido.

Si se envía un correo incorrecto, FastAPI responde:

```text
422 Unprocessable Entity
```

---

## Validación de nombre

El nombre del usuario debe tener como mínimo 3 caracteres.

Esta validación se realiza mediante Pydantic.

---

## Roles permitidos

Los usuarios solamente pueden tener uno de los siguientes roles:

```text
admin
support
user
```

Si se envía un rol diferente, la API genera una excepción HTTP con código:

```text
400 Bad Request
```

---

## Correos duplicados

Antes de crear o actualizar un usuario se comprueba que el correo electrónico no pertenezca a otro usuario.

Si el correo ya existe, se genera:

```text
400 Bad Request
```

---

# Manejo de errores

La aplicación utiliza `HTTPException` de FastAPI para manejar diferentes situaciones de error.

Entre ellas se encuentran:

* Usuario no encontrado.
* Correo electrónico duplicado.
* Rol no permitido.
* PATCH sin campos.
* Eliminación de un usuario inexistente.

Los principales códigos utilizados son:

| Código | Significado |
|---|---|
| 200 | Operación realizada correctamente |
| 201 | Usuario creado correctamente |
| 204 | Usuario eliminado correctamente |
| 400 | Error en los datos o regla de negocio |
| 404 | Usuario no encontrado |
| 422 | Error de validación de Pydantic |

---

# Inyección de dependencias con Depends()

En el proyecto se utilizó la inyección de dependencias de FastAPI mediante `Depends()`.

La dependencia principal se encuentra en:

```text
app/dependencies/user_dependencies.py
```

En este archivo se encuentra la función:

```python
get_user_or_404
```

Esta función permite comprobar si un usuario existe antes de ejecutar determinadas operaciones.

Por ejemplo:

```python
usuario: dict = Depends(get_user_or_404)
```

De esta manera se evita repetir la misma validación en diferentes endpoints.

Cuando el usuario no existe, la dependencia genera automáticamente una respuesta:

```text
404 Not Found
```

---

# Organización del código

El proyecto fue organizado separando las responsabilidades de cada parte de la aplicación.

### Routes

La carpeta:

```text
app/routes/
```

contiene los endpoints de la API.

Archivo principal:

```text
user_routes.py
```

Aquí se encuentran las rutas GET, POST, PUT, PATCH y DELETE.

### Schemas

La carpeta:

```text
app/schemas/
```

contiene los modelos utilizados para validar los datos mediante Pydantic.

Archivo:

```text
user_schema.py
```

### Services

La carpeta:

```text
app/services/
```

contiene la lógica principal de la aplicación.

Archivo:

```text
user_service.py
```

Aquí se realizan operaciones como crear, consultar, actualizar, eliminar y validar usuarios.

### Dependencies

La carpeta:

```text
app/dependencies/
```

contiene las funciones reutilizables utilizadas mediante `Depends()`.

### Data

La carpeta:

```text
app/data/
```

contiene la información de los usuarios almacenada temporalmente en memoria.

---

# Evidencias de Swagger UI

## Evidencia01 — Swagger UI funcionando

Vista general de Swagger UI mostrando los seis endpoints disponibles de la API.

![Evidencia01](evidencias/Evidencia01.png)

---

## Evidencia02 — GET `/users`

Prueba del endpoint GET `/users`, obteniendo correctamente la lista de usuarios.

![Evidencia02](evidencias/Evidencia02.png)

---

## Evidencia03 — GET `/users/{user_id}`

Prueba del endpoint GET `/users/{user_id}`, consultando correctamente el usuario con ID 2.

![Evidencia03](evidencias/Evidencia03.png)

---

## Evidencia04 — POST `/users`

Prueba del endpoint POST `/users`, registrando correctamente un nuevo usuario y obteniendo respuesta `201 Created`.

![Evidencia04](evidencias/Evidencia04.png)

---

## Evidencia05 — PUT `/users/{user_id}`

Prueba de actualización completa de un usuario mediante PUT, obteniendo respuesta `200 OK`.

![Evidencia05](evidencias/Evidencia05.png)

---

## Evidencia06 — PATCH `/users/{user_id}`

Prueba de actualización parcial de un usuario mediante PATCH, modificando únicamente el campo enviado.

![Evidencia06](evidencias/Evidencia06.png)

---

## Evidencia07 — DELETE `/users/{user_id}`

Prueba de eliminación de un usuario existente mediante DELETE, obteniendo respuesta `204 No Content`.

![Evidencia07](evidencias/Evidencia07.png)

---

# Evidencias de manejo de errores

## Evidencia08 — Usuario inexistente

Prueba de consulta de un usuario que no existe, obteniendo correctamente respuesta `404 Not Found`.

![Evidencia08](evidencias/Evidencia08.png)

---

## Evidencia09 — Correo duplicado

Prueba de creación de un usuario utilizando un correo que ya se encuentra registrado. La API responde con `400 Bad Request`.

![Evidencia09](evidencias/Evidencia09.png)

---

## Evidencia10 — Datos inválidos

Prueba de envío de un correo electrónico con formato incorrecto. FastAPI responde con `422 Unprocessable Entity`.

![Evidencia10](evidencias/Evidencia10.png)

---

## Evidencia11 — PATCH vacío

Prueba de PATCH sin campos para actualizar. La API responde correctamente con `400 Bad Request`.

![Evidencia11](evidencias/Evidencia11.png)

---

## Evidencia12 — DELETE de usuario inexistente

Prueba de eliminación de un usuario que no existe. La API responde correctamente con `404 Not Found`.

![Evidencia12](evidencias/Evidencia12.png)

---

# Evidencias de ReDoc

## Evidencia13 — ReDoc

Primera evidencia de la documentación de la API mediante ReDoc.

![Evidencia13](evidencias/Evidencia13.png)

---

## Evidencia14 — ReDoc

Segunda evidencia de la documentación y endpoints disponibles mediante ReDoc.

![Evidencia14](evidencias/Evidencia14.png)

---

# Git Flow

Para organizar el desarrollo del proyecto se utilizaron diferentes ramas mediante Git.

Las ramas utilizadas son:

```text
main
develop
feature/fastapi-intermedio
```

La rama:

```text
feature/fastapi-intermedio
```

se utilizó para desarrollar las funcionalidades correspondientes a esta actividad.

La estructura de trabajo utilizada es:

```text
main
  │
  └── develop
        │
        └── feature/fastapi-intermedio
```

Después de finalizar el desarrollo, los cambios serán integrados a `develop` y posteriormente a `main`.

---

# Estructura del proyecto

```text
device_systems/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── routes/
│   │   └── user_routes.py
│   │
│   ├── schemas/
│   │   └── user_schema.py
│   │
│   ├── services/
│   │   └── user_service.py
│   │
│   ├── dependencies/
│   │   └── user_dependencies.py
│   │
│   └── data/
│       └── users_db.py
│
├── evidencias/
│   ├── Evidencia01.png
│   ├── Evidencia02.png
│   ├── Evidencia03.png
│   ├── Evidencia04.png
│   ├── Evidencia05.png
│   ├── Evidencia06.png
│   ├── Evidencia07.png
│   ├── Evidencia08.png
│   ├── Evidencia09.png
│   ├── Evidencia10.png
│   ├── Evidencia11.png
│   ├── Evidencia12.png
│   ├── Evidencia13.png
│   └── Evidencia14.png
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
├── requirements.txt
└── uv.lock
```

---

# Estado del proyecto

* ✅ Proyecto `device_systems` actualizado.
* ✅ FastAPI configurado.
* ✅ Entorno virtual configurado.
* ✅ Uvicorn funcionando.
* ✅ Swagger UI disponible.
* ✅ ReDoc disponible.
* ✅ Estructura organizada por rutas, esquemas, servicios, dependencias y datos.
* ✅ Endpoint GET implementado.
* ✅ Endpoint POST implementado.
* ✅ Endpoint PUT implementado.
* ✅ Endpoint PATCH implementado.
* ✅ Endpoint DELETE implementado.
* ✅ Validación de datos mediante Pydantic.
* ✅ Validación de roles.
* ✅ Validación de correos duplicados.
* ✅ Manejo de errores mediante `HTTPException`.
* ✅ Inyección de dependencias mediante `Depends()`.
* ✅ Pruebas de funcionamiento realizadas.
* ✅ Evidencias de Swagger y ReDoc realizadas.
* ✅ Git Flow implementado.

---

# Reflexión final

Con esta actividad se pudo mejorar el proyecto `device_systems` que se había desarrollado anteriormente.

Uno de los principales cambios fue organizar mejor el código, separando las rutas, los modelos de validación, la lógica de negocio, las dependencias y los datos. Esto permite que el proyecto sea más fácil de entender y mantener.

También se implementaron nuevos métodos HTTP como PUT, PATCH y DELETE, además de diferentes validaciones para controlar los datos enviados por el usuario.

El uso de `HTTPException` permitió manejar de una mejor manera los errores y devolver códigos HTTP adecuados dependiendo de cada situación.

Finalmente, las pruebas realizadas mediante Swagger UI y ReDoc permitieron comprobar el funcionamiento de los diferentes endpoints y documentar el comportamiento de la API.

El uso de Git Flow también permitió organizar el desarrollo mediante ramas, manteniendo los cambios de la nueva funcionalidad separados antes de integrarlos al proyecto principal.

---

# Autor

**Stiven Hurtado Valencia**

Proyecto desarrollado como parte del proceso de formación en **Análisis y Desarrollo de Software (ADSO) – SENA**.