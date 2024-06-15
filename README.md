![Logo](_src/assets/logo_steam.jpg)

 # **PROYECTO INDIVIDUAL - Machine Learning Operations (MLOps)**

 ##  `Tabla de Contenido`
1. [Información General](#Información-General)
2. [Tecnologías Utilizadas](#tecnologías-Utilizadas)
3. [ETL](#etl)
4. [EDA](#eda)
5. [API](#api)
6. [Modelo de Machine Learning](#modelo-ml)
7. [Visualización](#visualización)

## `Informacion General`

#### El objetivo principal de este proyecto es hacer un "Producto Minimo Viable (MVP) de un Modelo de Remomendaciones de juegos tomando datos de la plataforma de juegos "STEAM". Para esto se desarrollo una API con FastAPI y se publicó en la plataforma RENDER. Se aplicaron todos los procesos de ETL, EDA y se utilizaron librerias de Machine Learning para dicho modelo

## `Tecnologias Utilizadas`

#### Se utilizó Python version 3.11 y varias librerias como: *`Pandas, gzip, json, AST, FastAPI, Sklearn, Matplotlib, Seaborn, numpy`*. Se utilizó el entornos en cuadernos de *'jupyter'* para codificar y editar. Tambien se uso uvicorn como servidor web para correr la API

## `ETL`

#### En esta fase se extrajeron los datos desde archivos comprimidos y en formato json, luego se hicieron transformaciones eliminando valores nulos y columnas innecesarias, se imputaron valores faltantes o nulos y se cambiaron tipos de datos para realizar los calculos necesarios. Por ultimo, todos los dataframe tranformados se exportaron en archivos .csv y .parquet para ser cargados desde la API. 

#### El código realizado se puede visualizar en el archivo [ETL.ipynb](ETL.ipynb)

#### En el archivo [funciones.ipynb](funciones.ipynb) se utilizó para cargar los datos limpios y transformados para hacer las funciones y probarlas antes de colocarlas en el main de la API. Tambien se exportaron algunos dataset con datos filtrados para optimizar el rendimiento de las funciones con los recursos limitados de la cuenta gratis de 'render'

## `EDA`

#### Se hicieron graficos para ver la cantidad de juegos por generos y las generos mas recomedados. En base a estas visualizaciones, se redujeron los generos a trabajar en el modelo de recomendacion para optimizar la cantidad de datos. Tambien se filtraron los datos tomando solo los juegos con mas de 10 mil horas jugadas con los cual se dejo el dataset con 2158 juegos

#### Se puede ver el codigo en el archivo [EDA.py](EDA.ipynb)

## `API`

#### Se realizó con el framework FastAPI. Este consta de las siguientes funciones
- #### *`PlayTimeGenre(genero)`*: Retorna el año del genero de juego con mas horas jugadas
- #### *`UserForGenre(genero)`*:  Retorna el usuario con mas horas jugadas para el genero ingresado y una lista con las horas jugadas de ese usuario por año
- #### *`UsersRecommend(año)`*: Retorna los 3 juegos mas recomendados por los usuarios para el año ingresado
- #### *`UsersNotRecommend(año)`*: Retorna los 3 juegos menos recomedados por los usuarios para el año ingresado
- #### *`sentiment_analysis(año)`*: Retorna la cantidad de reseñas (negativas, neutrales y positivas) de la categoria de analisis de sentimiento
- #### *`recomendacion_juego(id_game)`*: Retorna los 5 juegos mas recomendados en base a un id de juego ingresado

### Se puede ver el codigo en el archivo [main.py](main.py)

## `Modelo de Machine Learning`

### El modelo de recomendacion elegido fue item-item. Para este se utilizó la "Similitud del Coseno" para encontrar los juegos mas similares al ingresado como parametro.


## `Visualización`

#### - Se puede ver la API deployada en Render en este link: [https://henry-pi-mlops-nelvin.onrender.com/docs](https://henry-pi-mlops-nelvin.onrender.com/docs)
#### - Tambien se grabó un video corto explicando un poco el proyecto y haciendo una demostracion: [video](https://drive.google.com/file/d/1vaLuodePxqWefO9zbajXydNxqyfQb12E/view)
