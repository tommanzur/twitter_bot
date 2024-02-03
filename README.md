# Bot de Tweets de Noticias

## Resumen del Proyecto

Este repositorio contiene el código para un Bot de Tweets de Noticias, diseñado para raspar automáticamente, resumir y tuitear artículos de noticias de diversas fuentes. Utiliza bibliotecas de Python como Tweepy, BeautifulSoup, Requests y la IA Generativa de Google (API de Gemini) para realizar tareas como raspado web, gestión de bases de datos, síntesis de texto y tuiteo.

## Características

- Scraping de Noticias: Extrae artículos de 'La Política Online', 'Ámbito' y 'Página 12'.
- Gestión de Bases de Datos: Almacena y gestiona los artículos de noticias raspados en una base de datos SQLite.
- Síntesis de Texto: Resume artículos de noticias utilizando la API de Gemini de Google.
- Tuitear: Publica tuits de resúmenes de noticias con enlaces a los artículos originales.
- Tuiteo Automatizado: Tuitea un resumen de noticias aleatorio cada minuto.

## Instalación

Para ejecutar este proyecto, necesitas instalar el archivo requirements.txt

```bash
pip install -p requirements.txt
```

## Configuración

Antes de ejecutar el script, necesitas configurar las siguientes claves API:

- Credenciales de la API de Twitter: API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN
- Clave de la IA Generativa de Google (API de Gemini): GOOGLE_API_KEY
Estas claves deben introducirse en las respectivas variables dentro del script.

## Uso
- Una vez configuradas las credenciales debes correr el script: ```python bot.py```
- Inicialización de la Base de Datos: El script creará automáticamente una base de datos SQLite (news.db) para almacenar artículos de noticias.
- Scraping de Noticias: El script raspa los últimos artículos de noticias de las fuentes especificadas.
- Resumen de Artículos: El contenido de cada artículo se resume utilizando la API de Gemini.
- Publicación de Tweets: El script publica tuits con resúmenes y enlaces a los artículos completos.
- Operación Continua: El script se ejecuta en un bucle, publicando un tuit aleatorio cada minuto.

## Contribuciones

Se bienvenidas las contribuciones, problemas y solicitudes de características. No dudes en consultar la página de problemas para problemas abiertos o abrir un nuevo problema para discutir cambios o características que te gustaría agregar.