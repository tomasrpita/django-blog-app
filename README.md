# Django Blog Application

Este es el primer proyecto del libro *Django 5 By Example: Build powerful and reliable Python web applications from scratch (English Edition)*. Este proyecto abarca los siguientes capítulos y alcances:

## Capítulo 1: Construyendo una Aplicación de Blog
Este capítulo te introducirá al framework a través de una aplicación de blog. Crearás los modelos básicos del blog, vistas, plantillas y URLs para mostrar las publicaciones del blog. Aprenderás a construir QuerySets con el mapeador objeto-relacional (ORM) de Django, y configurarás el sitio de administración de Django.

## Capítulo 2: Mejorando tu Blog con Funciones Avanzadas
Este capítulo te enseñará cómo agregar paginación a tu blog, y cómo implementar vistas basadas en clases de Django. Aprenderás a enviar correos electrónicos con Django, y a manejar formularios y formularios basados en modelos. También implementarás un sistema de comentarios para las publicaciones del blog.

## Capítulo 3: Ampliando tu Aplicación de Blog
Este capítulo explora cómo integrar aplicaciones de terceros. Te guiará a través del proceso de crear un sistema de etiquetado, y aprenderás a construir QuerySets complejos para recomendar publicaciones similares. El capítulo te enseñará cómo crear etiquetas y filtros de plantillas personalizados. También aprenderás a utilizar el framework de mapas de sitio y a crear un feed RSS para tus publicaciones. Completarás tu aplicación de blog construyendo un motor de búsqueda utilizando las capacidades de búsqueda de texto completo de PostgreSQL.


```bash
docker run --name=blog_db -e POSRGRES_DB=blog -e POSTGRES_USER=blog -e POSTGRES_PASSWORD=xxxxx -p 5432:5432 -d postgres:16.2
```

