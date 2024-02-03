# Bot de Tweets de Noticias

## Resumen del Proyecto

Este repositorio contiene el código para un Bot de Tweets de Noticias, diseñado para scrapear automáticamente, resumir y tuitear artículos de noticias argentinas de diversas fuentes. Utiliza bibliotecas de Python como Tweepy, BeautifulSoup, Requests y la IA Generativa de Google (API de Gemini) para realizar tareas como raspado web, gestión de bases de datos, síntesis de texto y tuiteo.

## Características

- Scraping de Noticias: El bot puede extraer artículos de periódicos online como 'La Política Online', 'Ámbito Financiero' y 'Página 12'.
- Gestión de Bases de Datos: Utiliza SQLite para almacenar y gestionar los artículos extraídos.
- Síntesis de Texto: Emplea la API de GenerativeAI de Google para resumir los artículos de noticias.
- Publicación Automatizada en Twitter: Publica tweets con resúmenes y enlaces a los artículos originales.
Operación Continua: Configurado para publicar tweets de manera automática en intervalos regulares.

## Instalación

1. Instalación de Dependencias:

```bash
pip install -p requirements.txt
```
Las dependencias incluyen requests, bs4, tweepy y google-generativeai.

2. Configuración de Credenciales:
- Completar el archivo utils.credentials.py con las claves API necesarias:
    - Credenciales de Twitter (API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN).
    - Clave de la API de GenerativeAI de Google (GOOGLE_API_KEY).


## Uso
- Una vez configuradas las credenciales debes correr el script: ```python twitter_bot.py```
- Inicialización de la Base de Datos: El script creará automáticamente una base de datos SQLite (news.db) para almacenar artículos de noticias.
- Scraping de Noticias: El script raspa los últimos artículos de noticias de las fuentes especificadas.
- Resumen de Artículos: El contenido de cada artículo se resume utilizando la API de Gemini.
- Publicación de Tweets: El script publica tuits con resúmenes y enlaces a los artículos completos.
- Operación Continua: El script se ejecuta en un bucle, publicando un tuit aleatorio cada cierto tiempo definido por el usuario.

## Contribuciones

Se bienvenidas las contribuciones, problemas y solicitudes de características. No dudes en consultar la página de problemas para problemas abiertos o abrir un nuevo problema para discutir cambios o características que te gustaría agregar.
