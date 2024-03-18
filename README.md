![HenryLogo](https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png)

# **PROYECTO INDIVIDUAL - Machine Learning Operations (MLOps)**

 ##  ```Tabla de Contenido```
1. [Información General](#Información-General)
2. [Tecnologías Utilizadas](#tecnologías-Utilizadas)
3. [ETL](#etl)
4. [API](#api)
5. [EDA](#eda)
6. [Modelo de Machine Learning](#modelo-ml)

## ```Informacion General```

### El objetivo principal de este proyecto es poner en practico lo aprendido duarante el curso. Se nos proporciono una data de la plataforma de juegos "STEAM" con la cual debemos aplicar los procesos de ETL y crear una API donde se podrar extraer unformacion requerida. Luego se tendra que hacer un "Modelo de recomendaciones" utilizando librerias de Machine Learning.

## ```Tecnologias Utilizadas```

### Se utilizo Python version 3.11 y varias librerias como: Pandas, gzip, json, AST, FastAPI, Sklearn, Matplotlib, Seaborn, numpy. Tambien se uso uvicorn como servidor web para correr la API

## ```ETL```

### En esta fase se extrajeron los datos desde archivos comprimidos y en formato json, luego se hicieron transformaciones eliminando valores nulos y columnas innecesarias, se imputaron valores faltantes o nulos, se cambiaron tipos de datos. Por ultimo, todos los dataframe tranformados cargados en archivos .csv y .parquet para reducir espacio de almacenamiento. 

### El codigo realizado se puede visualizar en el archivo [ETL.ipynb](ETL.ipynb)

## ```API```

### La api se realizo en FastAPI. Este consta de las sieguientes funciones
- #### PlayTimeGenre(genero)
- #### UserForGenre(genero)
- #### UsersRecommend(año)
- #### UsersNotRecommend(año)
- #### sentiment_analysis(año)
- #### recomendacion_juego(idproducto)

### Se puede ver el codigo en el archivo [main.py](main.py)

## ```EDA```

### Se hicieron graficos para ver la cantidad de juegos por generos y las generos mas recomedados. En base a estas visualizaciones, se redujeron los generos a trabajar en el modelo de recomendacion para optimizar la cantidad de datos. Tambien se filtraron los datos por los juegos con mas de 10 mil horas jugadas con los cual se dejo el dataset con 2158 juegos

### Se puede ver el codigo en el archivo [EDA.py](EDA.ipynb)

## ```Modelo de Machine Learning```

### El modelo de remomendacion elegido fue item-item. Para este se utilizó la "similitud del coseno" para encontras los juegos mas similares al dado como parametro de entrada.