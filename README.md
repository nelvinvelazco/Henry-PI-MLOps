![HenryLogo](https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png)

# **PROYECTO INDIVIDUAL - Machine Learning Operations (MLOps)**

 ##  `Tabla de Contenido`
1. [Información General](#Información-General)
2. [Tecnologías Utilizadas](#tecnologías-Utilizadas)
3. [ETL](#etl)
4. [API](#api)
5. [EDA](#eda)
6. [Modelo de Machine Learning](#modelo-ml)

## `Informacion General`

### El objetivo principal de este proyecto es hacer un "Producto Minimo Viable (MVP) de un Modelo de Remomendaciones de juegos tomando datos de la plataforma de juegos "STEAM". Para esto se desarrollo una API con FastAPI y se publicó en la plataforma RENDER. Se aplicaron todos los procesos de ETL, EDA y se utilizaron librerias de Machine Learning para dicho modelo

## `Tecnologias Utilizadas`

### Se utilizo Python version 3.11 y varias librerias como: Pandas, gzip, json, AST, FastAPI, Sklearn, Matplotlib, Seaborn, numpy. Tambien se uso uvicorn como servidor web para correr la API

## `ETL`

### En esta fase se extrajeron los datos desde archivos comprimidos y en formato json, luego se hicieron transformaciones eliminando valores nulos y columnas innecesarias, se imputaron valores faltantes o nulos y se cambiaron tipos de datos para realizar los calculos necesarios. Por ultimo, todos los dataframe tranformados se cargaron en archivos .csv y .parquet para ser cargados desde la API. 

### El codigo realizado se puede visualizar en el archivo [ETL.ipynb](ETL.ipynb)

## `API`

### Se realizo con el framework FastAPI. Este consta de las siguientes funciones
- #### `PlayTimeGenre(genero)`: Retorna el año del genero de juego con mas horas jugadas
- #### `UserForGenre(genero)`:  Retorna el usuario con mas horas jugadas para el genero ingresado y una lista con las horas jugadas de ese usuario por año
- #### `UsersRecommend(año)`: Retorna los 3 juegos mas recomendados por los usuarios para el año ingresado
- #### `UsersNotRecommend(año)`: Retorna los 3 juegos menos recomedados por los usuarios para el año ingresado
- #### `sentiment_analysis(año)`: Retorna la cantidad de reseñas (negativas, neutrales y positivas) de la categoria de analisis de sentimiento
- #### `recomendacion_juego(id_game)`: Retorna los 5 juegos mas recomendados en base a un id de juego ingresado

### Se puede ver el codigo en el archivo [main.py](main.py)

## `EDA`

### Se hicieron graficos para ver la cantidad de juegos por generos y las generos mas recomedados. En base a estas visualizaciones, se redujeron los generos a trabajar en el modelo de recomendacion para optimizar la cantidad de datos. Tambien se filtraron los datos tomando solo los juegos con mas de 10 mil horas jugadas con los cual se dejo el dataset con 2158 juegos

### Se puede ver el codigo en el archivo [EDA.py](EDA.ipynb)

## `Modelo de Machine Learning`

### El modelo de remomendacion elegido fue item-item. Para este se utilizó la "Similitud del Coseno" para encontrar los juegos mas similares al ingresado como parametro.