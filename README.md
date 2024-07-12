# Django Blog Application

Este es el primer proyecto del libro *Django 5 By Example: Build powerful and reliable Python web applications from scratch (English Edition)*. Este proyecto abarca los siguientes capítulos y alcances:

## Capítulos del Libro

### Capítulo 1: Construyendo una Aplicación de Blog
Este capítulo te introducirá al framework a través de una aplicación de blog. Crearás los modelos básicos del blog, vistas, plantillas y URLs para mostrar las publicaciones del blog. Aprenderás a construir QuerySets con el mapeador objeto-relacional (ORM) de Django, y configurarás el sitio de administración de Django.

### Capítulo 2: Mejorando tu Blog con Funciones Avanzadas
Este capítulo te enseñará cómo agregar paginación a tu blog, y cómo implementar vistas basadas en clases de Django. Aprenderás a enviar correos electrónicos con Django, y a manejar formularios y formularios basados en modelos. También implementarás un sistema de comentarios para las publicaciones del blog.

### Capítulo 3: Ampliando tu Aplicación de Blog
Este capítulo explora cómo integrar aplicaciones de terceros. Te guiará a través del proceso de crear un sistema de etiquetado, y aprenderás a construir QuerySets complejos para recomendar publicaciones similares. El capítulo te enseñará cómo crear etiquetas y filtros de plantillas personalizados. También aprenderás a utilizar el framework de mapas de sitio y a crear un feed RSS para tus publicaciones. Completarás tu aplicación de blog construyendo un motor de búsqueda utilizando las capacidades de búsqueda de texto completo de PostgreSQL.

## Puesta en Marcha

### Prerrequisitos

Asegúrate de tener Docker y Docker Compose instalados en tu sistema.

### Instalación de Dependencias

1. **Clonar el repositorio:**

    ```sh
    git clone https://github.com/tomasrpita/django-blog-app.git
    cd tu-repositorio
    ```

2. **Crear un entorno virtual e instalar las dependencias de Python:**

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Crear el archivo `.env` a partir del archivo de plantilla `env.template`:**

    ```sh
    cp .env.template .env
    ```

4. **Rellenar las variables de entorno en el archivo `.env`:**

    ```plaintext
    # Email
    EMAIL_HOST=smtp.example.com
    EMAIL_HOST_USER=your-email@example.com
    EMAIL_HOST_PASSWORD=your-email-password
    EMAIL_PORT=587
    DEFAULT_FROM_EMAIL=your-email@example.com

    # Database
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=db
    DB_PORT=5432
    ```

### Configuración de Docker

1. **Iniciar los servicios con Docker Compose:**

    ```sh
    docker-compose up -d
    ```

### Configuración de la Aplicación Django

1. **Ejecutar las migraciones de la base de datos:**

    ```sh
    python ./mysite/manage.py migrate
    ```

2. **Crear un superusuario:**

    ```sh
    python ./mysite/manage.py createsuperuser
    ```

3. **Cargar datos iniciales (si aplica):**

    ```sh
    python ./mysite/manage.py loaddata initial_data.json
    ```

### Iniciar el Servidor de Desarrollo

1. **Iniciar el servidor de desarrollo de Django:**

    ```sh
    python ./mysite/manage.py runserver 0.0.0.0:8000
    ```

### Acceso a la Aplicación

- La aplicación estará disponible en `http://localhost:8000/blog`.
- La interfaz de administración de Django estará en `http://localhost:8000/admin`.

