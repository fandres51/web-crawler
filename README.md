# API de News Crawler con Django

## Descripción del Proyecto

Este proyecto Django es una API que obtiene y procesa las 30 principales entradas de noticias de un sitio web especificado (por ejemplo, Hacker News). La API extrae información como el título, los puntos y el número de comentarios, y proporciona dos operaciones de filtrado:

1. **Títulos Largos**: Títulos con más de cinco palabras, ordenados por el número de comentarios en orden descendente.
2. **Títulos Cortos**: Títulos con cinco o menos palabras, ordenados por puntos en orden descendente.

## Características

- Obtiene las 30 principales entradas de noticias de un sitio web especificado.
- Filtra y ordena las entradas de noticias según la longitud del título y otros criterios.
- Devuelve los resultados filtrados en formato JSON a través de un endpoint de API simple.

## Requisitos Previos

- Python 3.8 o superior
- Django 4.0 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. **Clonar el Repositorio:**

   ```bash
   git clone https://github.com/yourusername/news_crawler.git
   cd news_crawler
   ```

2. **Crear un Entorno Virtual:**

   Es recomendable usar un entorno virtual para gestionar las dependencias.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. **Instalar las Dependencias:**

   ```bash
   pip install django requests beautifulsoup4
   ```

4. **Aplicar Migraciones:**

   Aunque este proyecto no usa una base de datos, es buena práctica ejecutar las migraciones para futuras integraciones.

   ```bash
   python manage.py migrate
   ```

## Ejecutando el Servidor

1. **Iniciar el Servidor de Desarrollo de Django:**

   ```bash
   python manage.py runserver
   ```

2. **Acceder a la API:**

   Abre tu navegador web y navega a:

   ```
   http://127.0.0.1:8000/api/news/
   ```

   La API devolverá una respuesta JSON que contiene las entradas de noticias filtradas.

## Estructura del Proyecto

```plaintext
news_crawler/
│
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│
├── news_crawler/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── manage.py
└── README.md
```

## Endpoints de la API

### `/api/news/`

- **Método**: `GET`
- **Descripción**: Obtiene, filtra y ordena las 30 principales entradas de noticias del sitio web especificado. Devuelve un objeto JSON con dos listas: `long_titles_sorted` y `short_titles_sorted`.

#### Ejemplo de Respuesta JSON:

```json
{
    "long_titles_sorted": [
        {
            "number": "12345",
            "title": "Ejemplo de Título con Más de Cinco Palabras",
            "points": 120,
            "comments": 45
        }
    ],
    "short_titles_sorted": [
        {
            "number": "67890",
            "title": "Título Corto",
            "points": 200,
            "comments": 15
        }
    ]
}
```

## Personalización

- **Fuente de Noticias**: La fuente de noticias predeterminada es Hacker News (`https://news.ycombinator.com/`). Puedes cambiar la URL en la función `fetch_news_entries` en `views.py` para usar un sitio de noticias diferente.
- **Filtros y Ordenación**: La lógica de filtrado y ordenación se puede personalizar modificando la función `filter_entries` en `views.py`.

## Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT. Consulta el archivo `LICENSE` para más información.

## Contribuciones

No dudes en abrir issues o enviar pull requests para mejoras y correcciones de errores.

## Contacto

Para cualquier pregunta o consulta, por favor contacta a [fabio.and1514@gmail.com](mailto:fabio.and1514@gmail.com).

---