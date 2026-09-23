# device_systems

API REST desarrollada con **Python, FastAPI y SQLAlchemy** para la gestión de usuarios, dispositivos y préstamos. El proyecto utiliza una base de datos SQLite para almacenar la información de forma persistente y Alembic para administrar las migraciones de la base de datos.

El proyecto hace parte del proceso de formación del programa **Análisis y Desarrollo de Software (ADSO) – SENA**.

---

## Tecnologías utilizadas

* Python 3.14
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic v2
* Uvicorn
* Swagger UI
* ReDoc
* Alembic
* UV
* tzdata
* Git y Git Flow

---

## Descripción del proyecto

`device_systems` es una API REST desarrollada para administrar usuarios, dispositivos y préstamos dentro de un sistema de gestión.

El proyecto comenzó utilizando almacenamiento temporal en memoria y posteriormente evolucionó hacia una solución con persistencia mediante **SQLAlchemy y SQLite**.

En la versión actual se incorporó **Alembic** para controlar las migraciones de la base de datos y se agregaron nuevos modelos relacionados con dispositivos y préstamos.

La aplicación permite:

* Registrar usuarios.
* Consultar todos los usuarios.
* Consultar un usuario por su ID.
* Actualizar completamente un usuario.
* Actualizar parcialmente un usuario.
* Eliminar usuarios.
* Filtrar usuarios por rol.
* Filtrar usuarios por estado.
* Ordenar usuarios por nombre o fecha de creación.
* Registrar dispositivos.
* Consultar dispositivos.
* Actualizar dispositivos.
* Eliminar dispositivos.
* Filtrar dispositivos por tipo.
* Filtrar dispositivos por disponibilidad.
* Filtrar dispositivos por marca.
* Buscar dispositivos mediante texto.
* Registrar préstamos.
* Consultar préstamos.
* Consultar préstamos por usuario.
* Consultar historial de préstamos de dispositivos.
* Filtrar préstamos por estado.
* Filtrar préstamos por correo del usuario.
* Filtrar préstamos por tipo de dispositivo.
* Consultar información relacionada mediante consultas `JOIN`.
* Registrar devoluciones.
* Actualizar automáticamente la disponibilidad de los dispositivos.
* Validar los datos mediante Pydantic.
* Manejar errores mediante códigos de respuesta HTTP.
* Mantener los registros almacenados en SQLite.
* Administrar cambios de estructura de la base de datos mediante Alembic.

---

## Estructura del proyecto

```text
device_systems/
│
├── app/
│   ├── main.py
│   ├── __init__.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── __init__.py
│   │
│   ├── dependencies/
│   │   ├── database_dependency.py
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   ├── device_model.py
│   │   ├── loan_model.py
│   │   └── __init__.py
│   │
│   ├── routes/
│   │   ├── user_routes.py
│   │   ├── device_routes.py
│   │   ├── loan_routes.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── device_schema.py
│   │   ├── loan_schema.py
│   │   └── __init__.py
│   │
│   └── services/
│       ├── user_service.py
│       ├── device_service.py
│       ├── loan_service.py
│       └── __init__.py
│
├── alembic/
│   ├── versions/
│   │   └── 226c24a90b7c_crear_dispositivos_y_prestamos.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── evidencias/
│   ├── anteriores/
│   │   ├── Evidencia01.png
│   │   ├── Evidencia02.png
│   │   ├── ...
│   │   └── Evidencia17.png
│   │
│   └── ev10/
│       ├── 01_historial_alembic.png
│       ├── 02_upgrade_headV2.png
│       ├── 03_tablas_bd.png
│       ├── 04_modelos_relaciones.png
│       ├── 05_schemas_pydantic.png
│       ├── 06_swagger_completo.png
│       ├── 07_filtro_device_type.png
│       ├── 08_crear_prestamo.png
│       ├── 09_dispositivo_no_disponible.png
│       ├── 10_loan_details.png
│       ├── 11_filtros_prestamos.png
│       ├── 12_prestamos_usuario.png
│       ├── 13_prestamos_dispositivo.png
│       ├── 14_devolver_prestamo.png
│       ├── 15_dispositivo_disponible.png
│       ├── 16_usuario_no_existe.png
│       ├── 17_prestamo_ya_devuelto.png
│       └── 18_redoc.png
│
├── device_systems.db
├── .env
├── .env.example
├── .gitignore
├── .python-version
├── alembic.ini
├── README.md
├── pyproject.toml
├── requirements.txt
└── uv.lock
```

---

## Organización del código

### `app/main.py`

Es el archivo principal de la aplicación. Configura FastAPI, registra los routers de usuarios, dispositivos y préstamos y configura la documentación de la API.

La estructura actual utiliza **Alembic para administrar el esquema de la base de datos**, por lo que la aplicación no crea las tablas mediante `Base.metadata.create_all()`.

### `app/database/connection.py`

Configura la conexión con SQLite mediante SQLAlchemy.

La base de datos utilizada es:

```text
sqlite:///./device_systems.db
```

También define el motor de conexión, las sesiones y la clase base `Base` utilizada por los modelos.

### `app/models/`

Contiene los modelos de SQLAlchemy que representan las tablas de la base de datos:

* `user_model.py`: modelo `User`.
* `device_model.py`: modelo `Device`.
* `loan_model.py`: modelo `Loan`.

Los modelos también contienen las relaciones entre usuarios, dispositivos y préstamos.

### `app/schemas/`

Contiene los esquemas de Pydantic utilizados para validar los datos recibidos por la API y estructurar las respuestas.

Se encuentran:

* `user_schema.py`
* `device_schema.py`
* `loan_schema.py`

### `app/routes/`

Contiene los endpoints de la API:

* `user_routes.py`: endpoints de usuarios.
* `device_routes.py`: endpoints de dispositivos.
* `loan_routes.py`: endpoints de préstamos.

### `app/services/`

Contiene la lógica de negocio y las consultas realizadas sobre la base de datos:

* `user_service.py`
* `device_service.py`
* `loan_service.py`

Esta separación permite mantener las rutas más organizadas y separar la recepción de solicitudes de la lógica de negocio.

### `app/dependencies/database_dependency.py`

Contiene la dependencia `get_db`, utilizada mediante `Depends()` para proporcionar una sesión de SQLAlchemy a los endpoints y cerrarla al finalizar la solicitud.

---

# Modelos y relaciones

## Modelo `User`

El modelo `User` representa la tabla `users`.

Sus principales campos son:

* `id`
* `name`
* `email`
* `role`
* `is_active`
* `created_at`

Un usuario puede tener varios préstamos mediante la relación:

```text
User → Loan
```

La relación se configura utilizando:

```python
loans = relationship("Loan", back_populates="user")
```

---

## Modelo `Device`

El modelo `Device` representa la tabla `devices`.

Sus campos principales son:

* `id`
* `name`
* `serial_number`
* `device_type`
* `brand`
* `is_available`
* `created_at`

Un dispositivo puede tener varios registros históricos de préstamos:

```text
Device → Loan
```

La relación se configura utilizando:

```python
loans = relationship("Loan", back_populates="device")
```

---

## Modelo `Loan`

El modelo `Loan` representa la tabla `loans`.

Sus campos principales son:

* `id`
* `user_id`
* `device_id`
* `loan_date`
* `return_date`
* `status`

El préstamo establece las relaciones entre un usuario y un dispositivo:

```text
User 1 ──────── N Loan N ──────── 1 Device
```

Las relaciones utilizan:

```python
user = relationship("User", back_populates="loans")
device = relationship("Device", back_populates="loans")
```

De esta forma, un usuario puede tener varios préstamos y un dispositivo puede tener un historial de varios préstamos.

---

# SQLAlchemy y Pydantic

En el proyecto se utilizan SQLAlchemy y Pydantic para responsabilidades diferentes.

## SQLAlchemy

SQLAlchemy se encarga de representar los modelos, establecer relaciones y realizar operaciones sobre la base de datos.

Los modelos principales son:

```text
User
Device
Loan
```

SQLAlchemy permite realizar consultas, inserciones, actualizaciones, eliminaciones y consultas relacionadas mediante `JOIN`.

## Pydantic

Pydantic se utiliza para validar los datos recibidos por la API y establecer la estructura de las respuestas.

Los esquemas principales son:

```text
UserCreate
UserUpdate
UserPatch
UserResponse

DeviceCreate
DeviceUpdate
DevicePatch
DeviceResponse

LoanCreate
LoanResponse
LoanDetailResponse
```

De esta manera:

* **SQLAlchemy** se encarga de la interacción con la base de datos.
* **Pydantic** se encarga de validar y estructurar los datos de la API.

---

# Alembic y migraciones

Para administrar los cambios de estructura de la base de datos se incorporó **Alembic**.

La configuración principal se encuentra en:

```text
alembic.ini
alembic/env.py
alembic/versions/
```

Alembic utiliza los modelos de SQLAlchemy mediante:

```python
target_metadata = Base.metadata
```

y reconoce los modelos:

```python
from app.models import User, Device, Loan
```

## Inicialización

El proyecto fue configurado utilizando:

```bash
uv run alembic init alembic
```

## Creación de la migración

Se generó una migración para crear las tablas relacionadas con dispositivos y préstamos.

Archivo generado:

```text
alembic/versions/226c24a90b7c_crear_dispositivos_y_prestamos.py
```

La migración crea:

```text
devices
loans
```

y establece las claves foráneas correspondientes:

```text
loans.user_id   → users.id
loans.device_id → devices.id
```

## Aplicación de la migración

La migración se aplica mediante:

```bash
uv run alembic upgrade head
```

## Consulta del historial

Para consultar las migraciones:

```bash
uv run alembic history
```

Para consultar la revisión actual:

```bash
uv run alembic current
```

La revisión aplicada actualmente corresponde a:

```text
226c24a90b7c (head)
```

También se verificó el estado de las migraciones mediante:

```bash
uv run alembic check
```

Resultado:

```text
No new upgrade operations detected.
```

Esto indica que no existen cambios pendientes de generar en las migraciones.

---

# Base de datos SQLite

El proyecto utiliza SQLite como sistema de almacenamiento relacional.

El archivo de la base de datos es:

```text
device_systems.db
```

Actualmente contiene las tablas principales:

```text
users
devices
loans
```

Además, Alembic utiliza la tabla:

```text
alembic_version
```

para registrar la revisión de migración aplicada.

La estructura de la base de datos es administrada mediante Alembic y los modelos de SQLAlchemy.

---

# CRUD de usuarios

Los usuarios mantienen las operaciones CRUD implementadas durante las etapas anteriores del proyecto.

| Método | Endpoint           | Descripción                                              | Respuestas principales |
| ------ | ------------------ | -------------------------------------------------------- | ---------------------- |
| GET    | `/users`           | Lista usuarios y permite aplicar filtros y ordenamiento. | 200                    |
| GET    | `/users/{user_id}` | Consulta un usuario por ID.                              | 200 / 404              |
| POST   | `/users`           | Registra un usuario.                                     | 201 / 400 / 422        |
| PUT    | `/users/{user_id}` | Actualiza completamente un usuario.                      | 200 / 400 / 404 / 422  |
| PATCH  | `/users/{user_id}` | Actualiza parcialmente un usuario.                       | 200 / 400 / 404 / 422  |
| DELETE | `/users/{user_id}` | Elimina un usuario.                                      | 204 / 404              |

---

# CRUD de dispositivos

Se incorporó el modelo `Device` y sus operaciones de gestión.

| Método | Endpoint               | Descripción                                   | Respuestas principales |
| ------ | ---------------------- | --------------------------------------------- | ---------------------- |
| GET    | `/devices`             | Lista dispositivos y permite aplicar filtros. | 200                    |
| GET    | `/devices/{device_id}` | Consulta un dispositivo por ID.               | 200 / 404              |
| POST   | `/devices`             | Registra un dispositivo.                      | 201 / 400 / 422        |
| PUT    | `/devices/{device_id}` | Actualiza completamente un dispositivo.       | 200 / 400 / 404 / 422  |
| PATCH  | `/devices/{device_id}` | Actualiza parcialmente un dispositivo.        | 200 / 400 / 404 / 422  |
| DELETE | `/devices/{device_id}` | Elimina un dispositivo.                       | 204 / 404              |

---

# Filtros de dispositivos

El endpoint:

```text
GET /devices
```

permite realizar diferentes consultas.

### Filtrar por tipo

```text
GET /devices?device_type=laptop
```

### Filtrar por disponibilidad

```text
GET /devices?is_available=true
```

### Filtrar por marca

```text
GET /devices?brand=Lenovo
```

### Buscar mediante texto

```text
GET /devices?search=ThinkPad
```

La búsqueda permite encontrar coincidencias utilizando diferentes campos del dispositivo.

---

# Gestión de préstamos

Los préstamos permiten relacionar usuarios y dispositivos.

## Consultar préstamos

```text
GET /loans
```

Obtiene los préstamos registrados y permite aplicar filtros.

## Consultar préstamo por ID

```text
GET /loans/{loan_id}
```

Permite consultar un préstamo específico.

## Crear préstamo

```text
POST /loans
```

Ejemplo:

```json
{
  "user_id": 1,
  "device_id": 1
}
```

Al crear un préstamo se verifica:

1. Que el usuario exista.
2. Que el dispositivo exista.
3. Que el dispositivo esté disponible.

Cuando el préstamo se crea correctamente:

* Se registra la fecha del préstamo.
* El estado inicial es `active`.
* El dispositivo pasa a `is_available = false`.

## Devolver un dispositivo

```text
PATCH /loans/{loan_id}/return
```

Al registrar una devolución:

* El estado del préstamo cambia a `returned`.
* Se registra `return_date`.
* El dispositivo vuelve a estar disponible.

---

# Consultas con JOIN

Para obtener información relacionada de usuarios, dispositivos y préstamos se utilizan consultas SQLAlchemy con `join()`.

El endpoint:

```text
GET /loans/details
```

permite consultar los préstamos incluyendo información relacionada.

La consulta relaciona:

```text
Loan → User
Loan → Device
```

y permite obtener información como:

* ID del préstamo.
* Nombre del usuario.
* Correo del usuario.
* Nombre del dispositivo.
* Número de serie.
* Tipo de dispositivo.
* Marca.
* Fecha del préstamo.
* Fecha de devolución.
* Estado.

Esto permite consultar información de varias tablas en una sola operación.

---

# Filtros avanzados de préstamos

El endpoint:

```text
GET /loans
```

permite aplicar diferentes filtros.

## Filtrar por estado

```text
GET /loans?status=active
```

Los estados permitidos son:

```text
active
returned
overdue
```

## Filtrar por correo del usuario

```text
GET /loans?user_email=aprendiz@sena.edu.co
```

También permite realizar búsquedas parciales mediante `ilike`.

## Filtrar por tipo de dispositivo

```text
GET /loans?device_type=laptop
```

## Filtrar por rango de fechas

También se pueden utilizar:

```text
loan_date_from
loan_date_to
```

para limitar los resultados a un rango de fechas.

Las consultas combinan condiciones mediante herramientas de SQLAlchemy como:

```python
join()
where()
and_()
or_()
ilike()
```

---

# Historial de préstamos

## Historial de un usuario

```text
GET /users/{user_id}/loans
```

Permite consultar los préstamos asociados a un usuario.

Antes de realizar la consulta se verifica que el usuario exista.

## Historial de un dispositivo

```text
GET /devices/{device_id}/loans
```

Permite consultar los préstamos asociados a un dispositivo.

Antes de realizar la consulta se verifica que el dispositivo exista.

---

# Validaciones y manejo de errores

La aplicación utiliza Pydantic y `HTTPException` para validar los datos y manejar diferentes situaciones.

| Código | Significado                                                 |
| ------ | ----------------------------------------------------------- |
| 200    | Operación realizada correctamente.                          |
| 201    | Recurso creado correctamente.                               |
| 204    | Recurso eliminado correctamente sin contenido de respuesta. |
| 400    | Error en una regla de negocio.                              |
| 404    | Recurso solicitado no encontrado.                           |
| 409    | Conflicto con el estado actual del recurso.                 |
| 422    | Error de validación de los datos recibidos.                 |

## Usuario inexistente

Cuando se consulta, actualiza o elimina un usuario que no existe, la API responde:

```text
404 Not Found
```

## Dispositivo inexistente

Cuando se intenta trabajar con un dispositivo que no existe:

```text
404 Not Found
```

## Dispositivo no disponible

Si se intenta crear un préstamo utilizando un dispositivo que ya se encuentra prestado:

```text
409 Conflict
```

## Préstamo inexistente

Si se consulta o intenta devolver un préstamo que no existe:

```text
404 Not Found
```

## Préstamo ya devuelto

Si se intenta devolver nuevamente un préstamo cuyo estado ya es `returned`:

```text
409 Conflict
```

## Correo duplicado

La API valida que no exista otro usuario con el mismo correo electrónico.

## Serial duplicado

La API valida que el número de serie de un dispositivo no esté registrado previamente.

## Validaciones de Pydantic

Los datos enviados a los endpoints son validados mediante los esquemas definidos en `app/schemas/`.

Los errores de validación generan:

```text
422 Unprocessable Entity
```

---

# Inyección de dependencias

Se utiliza la inyección de dependencias de FastAPI mediante `Depends()`.

La dependencia de base de datos se encuentra en:

```text
app/dependencies/database_dependency.py
```

La función `get_db` proporciona una sesión de SQLAlchemy a cada solicitud y se encarga de cerrarla al finalizar.

Esto permite que los endpoints trabajen con la base de datos sin crear y cerrar manualmente una sesión en cada operación.

---

# Persistencia de datos

Los usuarios, dispositivos y préstamos se almacenan en SQLite mediante SQLAlchemy.

La información permanece almacenada en:

```text
device_systems.db
```

La persistencia permite que los registros continúen disponibles después de detener y volver a iniciar el servidor.

La estructura de las tablas es administrada mediante las migraciones de Alembic.

---

# Manejo de zona horaria

Los campos de fecha y hora utilizan la zona horaria:

```text
America/Bogota
```

Para permitir el funcionamiento de esta zona horaria en el entorno de Python se utiliza:

```text
tzdata
```

Esto permite registrar las fechas utilizando la zona horaria correspondiente a Colombia.

---

# Documentación de la API

## Swagger UI

Disponible en:

```text
http://127.0.0.1:8000/docs
```

Swagger permite consultar y probar los endpoints, enviar parámetros y cuerpos JSON y revisar las respuestas HTTP.

La documentación utiliza etiquetas para organizar los recursos:

```text
Users
Devices
Loans
```

Los endpoints también cuentan con:

* `summary`
* `description`
* `response_description`
* códigos de respuesta esperados
* ejemplos de datos en los esquemas Pydantic

## ReDoc

Disponible en:

```text
http://127.0.0.1:8000/redoc
```

ReDoc permite consultar de manera organizada la documentación generada por FastAPI.

---

# Instalación y ejecución

## Requisitos

* Python instalado.
* UV instalado.
* Git instalado.
* Proyecto descargado o clonado.

## Instalar dependencias

Desde la carpeta del proyecto:

```bash
uv sync
```

También se dispone del archivo:

```text
requirements.txt
```

con las dependencias utilizadas por el proyecto.

## Ejecutar migraciones

Para aplicar las migraciones:

```bash
uv run alembic upgrade head
```

Para comprobar el estado:

```bash
uv run alembic current
```

Para revisar el historial:

```bash
uv run alembic history
```

## Iniciar el servidor

En Windows:

```bash
uv run uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Evidencias

Las evidencias se organizan en dos grupos para conservar la evolución completa del proyecto.

## Evidencias de etapas anteriores

Estas evidencias corresponden a las primeras etapas del desarrollo de `device_systems`, donde se implementaron el CRUD de usuarios, validaciones, persistencia, Swagger, ReDoc y organización inicial del proyecto.

### Evidencia 01 — Swagger UI

Captura de la documentación interactiva de la API mediante Swagger UI.

![Evidencia 01](evidencias/Anteriores/Evidencia01.png)

---

### Evidencia 02 — GET `/users`

Consulta de la lista de usuarios registrados.

![Evidencia 02](evidencias/Anteriores/Evidencia02.png)

---

### Evidencia 03 — GET `/users/{user_id}`

Consulta de un usuario específico mediante su ID.

![Evidencia 03](evidencias/Anteriores/Evidencia03.png)

---

### Evidencia 04 — POST `/users`

Registro de un usuario mediante el endpoint POST.

![Evidencia 04](evidencias/Anteriores/Evidencia04.png)

---

### Evidencia 05 — PUT `/users/{user_id}`

Actualización completa de un usuario.

![Evidencia 05](evidencias/Anteriores/Evidencia05.png)

---

### Evidencia 06 — PATCH `/users/{user_id}`

Actualización parcial de un usuario.

![Evidencia 06](evidencias/Anteriores/Evidencia06.png)

---

### Evidencia 07 — DELETE `/users/{user_id}`

Eliminación de un usuario.

![Evidencia 07](evidencias/Anteriores/Evidencia07.png)

---

### Evidencia 08 — Usuario inexistente

Prueba de consulta de un usuario que no existe y manejo de respuesta `404 Not Found`.

![Evidencia 08](evidencias/Anteriores/Evidencia08.png)

---

### Evidencia 09 — Correo duplicado

Prueba de registro utilizando un correo electrónico que ya existe y manejo de respuesta `400 Bad Request`.

![Evidencia 09](evidencias/Anteriores/Evidencia09.png)

---

### Evidencia 10 — Validación de datos

Prueba de datos que no cumplen las validaciones de Pydantic y respuesta `422 Unprocessable Entity`.

![Evidencia 10](evidencias/Anteriores/Evidencia10.png)

---

### Evidencia 11 — PATCH vacío

Prueba de actualización parcial sin enviar campos y manejo del error `400 Bad Request`.

![Evidencia 11](evidencias/Anteriores/Evidencia11.png)

---

### Evidencia 12 — DELETE de usuario inexistente

Prueba de eliminación de un usuario que no existe y respuesta `404 Not Found`.

![Evidencia 12](evidencias/Anteriores/Evidencia12.png)

---

### Evidencia 13 — ReDoc

Captura de la documentación de la API mediante ReDoc.

![Evidencia 13](evidencias/Anteriores/Evidencia13.png)

---

### Evidencia 14 — ReDoc y endpoints

Segunda captura de la documentación de la API mostrando los endpoints disponibles.

![Evidencia 14](evidencias/Anteriores/Evidencia14.png)

---

### Evidencia 15 — Estructura del proyecto

Captura de la estructura del proyecto y organización de sus módulos.

![Evidencia 15](evidencias/Anteriores/Evidencia15.png)

---

### Evidencia 16 — Base de datos SQLite

Captura de la base de datos `device_systems.db` mostrando los registros almacenados.

![Evidencia 16](evidencias/Anteriores/Evidencia16.png)

---

### Evidencia 17 — Persistencia después de reiniciar

Evidencia de la persistencia de los datos después de detener y volver a iniciar el servidor.

![Evidencia 17](evidencias/Anteriores/Evidencia17.png)

---

# Evidencias GA1-220501096-01-AA1-EV10

Las siguientes evidencias corresponden a la implementación de **Alembic, modelos relacionados, dispositivos, préstamos, consultas JOIN, filtros avanzados y documentación actualizada**.

### Evidencia EV10-01 — Historial de Alembic

Captura del historial de migraciones mediante `alembic history`.

![Historial de Alembic](evidencias/EV10/01_historial_alembic.png)

---

### Evidencia EV10-02 — Aplicación de la migración

Captura del proceso de aplicación de la migración mediante `alembic upgrade head`.

![Upgrade head](evidencias/EV10/02_upgrade_headV2.png)

---

### Evidencia EV10-03 — Tablas de la base de datos

Captura de las tablas generadas en SQLite, incluyendo `users`, `devices`, `loans` y `alembic_version`.

![Tablas de la base de datos](evidencias/EV10/03_tablas_bd.png)

---

### Evidencia EV10-04 — Modelos y relaciones

Captura de los modelos `User`, `Device` y `Loan`, incluyendo las relaciones entre ellos.

![Modelos y relaciones](evidencias/EV10/04_modelos_relaciones.png)

---

### Evidencia EV10-05 — Schemas Pydantic

Captura de los esquemas Pydantic utilizados para dispositivos y préstamos.

![Schemas Pydantic](evidencias/EV10/05_schemas_pydantic.png)

---

### Evidencia EV10-06 — Swagger completo

Captura de la documentación actualizada de la API mediante Swagger UI, incluyendo los recursos de usuarios, dispositivos y préstamos.

![Swagger completo](evidencias/EV10/06_swagger_completo.png)

---

### Evidencia EV10-07 — Filtro de dispositivos

Prueba del filtro:

```text
GET /devices?device_type=laptop
```

![Filtro de dispositivos](evidencias/EV10/07_filtro_device_type.png)

---

### Evidencia EV10-08 — Crear préstamo

Prueba de creación de un préstamo mediante:

```text
POST /loans
```

La respuesta muestra la creación correcta del préstamo.

![Crear préstamo](evidencias/EV10/08_crear_prestamo.png)

---

### Evidencia EV10-09 — Dispositivo no disponible

Prueba de creación de un préstamo utilizando un dispositivo que ya se encuentra ocupado.

La API responde con:

```text
409 Conflict
```

![Dispositivo no disponible](evidencias/EV10/09_dispositivo_no_disponible.png)

---

### Evidencia EV10-10 — Consulta de detalles con JOIN

Prueba del endpoint:

```text
GET /loans/details
```

La respuesta incluye información del usuario y del dispositivo relacionado con cada préstamo.

![Detalles de préstamos](evidencias/EV10/10_loan_details.png)

---

### Evidencia EV10-11 — Filtros de préstamos

Pruebas de los filtros disponibles para el endpoint `GET /loans`, incluyendo el estado del préstamo y filtros relacionados con el usuario y el dispositivo.

![Filtros de préstamos](evidencias/EV10/11_filtros_prestamos.png)

---

### Evidencia EV10-12 — Préstamos de un usuario

Prueba del endpoint:

```text
GET /users/{user_id}/loans
```

La respuesta muestra el historial de préstamos asociados al usuario.

![Préstamos del usuario](evidencias/EV10/12_prestamos_usuario.png)

---

### Evidencia EV10-13 — Historial de un dispositivo

Prueba del endpoint:

```text
GET /devices/{device_id}/loans
```

La respuesta muestra el historial de préstamos asociados al dispositivo.

![Historial del dispositivo](evidencias/EV10/13_prestamos_dispositivo.png)

---

### Evidencia EV10-14 — Devolución de préstamo

Prueba de devolución mediante:

```text
PATCH /loans/{loan_id}/return
```

La respuesta muestra el cambio del estado del préstamo y el registro de la devolución.

![Devolución de préstamo](evidencias/EV10/14_devolver_prestamo.png)

---

### Evidencia EV10-15 — Disponibilidad del dispositivo

Después de realizar la devolución, se verifica que el dispositivo vuelve a estar disponible.

![Dispositivo disponible](evidencias/EV10/15_dispositivo_disponible.png)

---

### Evidencia EV10-16 — Usuario inexistente

Prueba de creación de un préstamo utilizando un usuario que no existe.

La API responde con:

```text
404 Not Found
```

![Usuario inexistente](evidencias/EV10/16_usuario_no_existe.png)

---

### Evidencia EV10-17 — Préstamo ya devuelto

Prueba de devolución de un préstamo que ya había sido devuelto.

La API responde con:

```text
409 Conflict
```

![Préstamo ya devuelto](evidencias/EV10/17_prestamo_ya_devuelto.png)

---

### Evidencia EV10-18 — ReDoc

Captura de la documentación actualizada mediante ReDoc.

![ReDoc](evidencias/EV10/18_redoc.png)

---

# Git Flow

Para organizar el desarrollo se utilizaron ramas de Git.

Las etapas anteriores utilizaron las ramas correspondientes al desarrollo inicial del proyecto, incluyendo:

```text
main
develop
feature/fastapi-intermedio
feature/sqlalchemy-crud
```

Para la implementación de esta actividad se creó la rama:

```text
device_systems_alembic_relaciones
```

Esta rama contiene la implementación de:

* Alembic.
* Migraciones.
* Modelo `Device`.
* Modelo `Loan`.
* Relaciones entre modelos.
* CRUD de dispositivos.
* Gestión de préstamos.
* Consultas con `JOIN`.
* Filtros avanzados.
* Documentación actualizada.
* Evidencias de la actividad.

La integración final con `main` se realizará después de completar las pruebas y verificar el funcionamiento del proyecto.

---

# Verificaciones finales

Durante la implementación se realizaron diferentes verificaciones.

## Carga de la API

```bash
uv run python -c "from app.main import app; print('API completa cargada correctamente')"
```

Resultado:

```text
API completa cargada correctamente
```

## Verificación de modelos

```bash
uv run python -c "from app.models import User, Device, Loan; print('Modelos y relaciones cargados correctamente')"
```

Resultado:

```text
Modelos y relaciones cargados correctamente
```

## Verificación de migraciones

```bash
uv run alembic check
```

Resultado:

```text
No new upgrade operations detected.
```

Esto confirma que los modelos actuales no presentan cambios pendientes de generar en una nueva migración.

---

# Estado final del proyecto

* [x] FastAPI configurado.
* [x] SQLAlchemy implementado.
* [x] SQLite configurado.
* [x] Pydantic v2 implementado.
* [x] Modelo `User`.
* [x] Modelo `Device`.
* [x] Modelo `Loan`.
* [x] Relaciones entre usuarios y préstamos.
* [x] Relaciones entre dispositivos y préstamos.
* [x] Schemas de usuarios.
* [x] Schemas de dispositivos.
* [x] Schemas de préstamos.
* [x] CRUD de usuarios.
* [x] CRUD de dispositivos.
* [x] Gestión de préstamos.
* [x] Devolución de dispositivos.
* [x] Control de disponibilidad.
* [x] Filtros de dispositivos.
* [x] Filtros de préstamos.
* [x] Consultas mediante `JOIN`.
* [x] Historial de préstamos por usuario.
* [x] Historial de préstamos por dispositivo.
* [x] Validaciones Pydantic.
* [x] Manejo de errores HTTP.
* [x] Swagger UI.
* [x] ReDoc.
* [x] Alembic configurado.
* [x] Migración creada.
* [x] Migración aplicada.
* [x] Verificación mediante `alembic check`.
* [x] Persistencia mediante SQLite.
* [x] Manejo de zona horaria `America/Bogota`.
* [x] Dependencia `tzdata`.
* [x] Evidencias de las etapas anteriores.
* [x] Evidencias correspondientes a EV10.
* [x] README actualizado.

---

# Reflexión final

Con esta actividad se continuó la evolución del proyecto `device_systems`, pasando de una API enfocada principalmente en la gestión de usuarios a una solución con diferentes entidades relacionadas.

La incorporación de **Alembic** permitió administrar de una manera más organizada los cambios realizados en la estructura de la base de datos. Las migraciones permiten registrar y aplicar las modificaciones necesarias sin depender de la creación automática de tablas al iniciar la aplicación.

También se implementaron los modelos `Device` y `Loan`, estableciendo relaciones entre usuarios, dispositivos y préstamos mediante SQLAlchemy.

El manejo de relaciones permitió realizar consultas más completas utilizando `JOIN`, obteniendo información de diferentes tablas en una misma operación.

Además, se implementaron filtros para consultar préstamos según su estado, el correo del usuario, el tipo de dispositivo y rangos de fechas. También se agregaron consultas para consultar el historial de préstamos de usuarios y dispositivos.

La gestión de préstamos permitió aplicar reglas de negocio como verificar que el usuario y el dispositivo existan, comprobar la disponibilidad del dispositivo, cambiar su estado al realizar un préstamo y devolverlo a disponibilidad cuando se registra la devolución.

Finalmente, se actualizaron Swagger y ReDoc para documentar los nuevos endpoints, se realizaron pruebas de funcionamiento y se organizaron las evidencias de las diferentes etapas del proyecto.

Esta actividad permitió reforzar el uso de **FastAPI, SQLAlchemy, Pydantic, SQLite, Alembic, relaciones entre modelos y consultas avanzadas**, manteniendo una estructura modular y organizada.

---

# Autor

**Stiven Hurtado Valencia**

**Programa:** Análisis y Desarrollo de Software (ADSO)

**SENA**
