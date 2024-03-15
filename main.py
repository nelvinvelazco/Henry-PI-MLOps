from fastapi import FastAPI
import pandas as pd

# Se cargan los dataset transformados
df_games= pd.read_csv('DataSet_tranformados/games.csv',delimiter = ',',encoding = "utf-8")
df_reviews= pd.read_csv('DataSet_tranformados/reviews.csv',delimiter = ',',encoding = "utf-8")

# Se carga el dataFrame para la funcion PlayTimeGenre()
df_PlayTimeGenre= pd.read_csv('DataSet_tranformados/funcion1.csv')
# Se carga el dataFrame para la funcion UserForGenre
df_UserForGenre = pd.read_parquet('DataSet_tranformados/funcion2.parquet')


# Funcion para culcular los juegos recomendados y no recomendados
def userRecomended_or_Not(año: int, tipo: bytes):
    if tipo == 1:
        # Filtra los remomendados positivos, comentarios positivos y neutrales en el año especificado en el parametro de entrada
        df_filtred_rec_sent_year= df_reviews[(df_reviews['recommend']== True) & (df_reviews['sentiment_analysis']> 0) & (df_reviews['year'] == año)]
    else:
        # Filtra los No remomendados, comentarios negativos en el año especificado en el parametro de entrada
        df_filtred_rec_sent_year= df_reviews[(df_reviews['recommend']== False) & (df_reviews['sentiment_analysis']== 0) & (df_reviews['year'] == año)]    
    # Se agrupan por id de juego y se cuentan las comentarios. Luego se ordenan de mayor a menor
    df_grupo_xgames= df_filtred_rec_sent_year.groupby('game_id', as_index=False).size().sort_values(by='size', ascending=False)
    # Se eliminan los duplicados de columna game_id del dataset de juegos en un df temporal
    df_games_sin_duplicados = df_games.drop_duplicates(subset=['game_id'])  
    # Se hace un Join con del df agrupado por id con el df de juegos temporal para tomar los nombres de los juegos
    df_union_con_items= pd.merge(df_grupo_xgames, df_games_sin_duplicados, on='game_id', how= 'inner')
    # Se muestran los resultados de los 3 juegos mas recomendados
    result= {'Puesto {}'.format(pos +1): game for pos, game in zip(range(3),df_union_con_items['game_name'].iloc[:3])}
    return result

app = FastAPI()

@app.get("/PlayTimeGenre/{genero}")
def PlayTimeGenre(genero: str):
    """Retorna el año del genero de juego con mas horas jugadas

    Args: genero (str): Genero de Juego

    Returns: json
    """    
    df_Filtro_X_genero= df_PlayTimeGenre.copy()                 # Copia el df cargado para procesar en esta funcion    
    df_Filtro_X_genero['genres']= df_Filtro_X_genero['genres'].str.lower()      #Convierte la columan Genero a minusculas
    # Se filtra por el genero de parametro en minusculas
    df_Filtro_X_genero= df_Filtro_X_genero[df_Filtro_X_genero['genres'] == genero.lower()]
    indice_genero= df_Filtro_X_genero.index[0]                  # Se toma el indice de la primera fila del df filtrado
    strGenero= df_PlayTimeGenre.loc[indice_genero]['genres']    # Guarda el Genero como esta en el df_game original para visualizarlo en el resultado
    year_max_horas= int(df_Filtro_X_genero.iloc[0,1])           #Se toma el primer año de el dataset Ordenado
    result= [{'Año de lanzamiento con más horas jugadas para Género {}'.format(strGenero): year_max_horas}] 
    return result

@app.get("/UserForGenre/{genero}")
def UserForGenre(genero: str):  
    """Retorna el usuario con mas horas jugara para el genero  ingresado y 
        una lista con las horas jugadas de ese usuario por año

    Args: genero (str): Genero de Juego

    Returns: json
    """
    df_filtro_genero= df_UserForGenre.copy()                    # Copia el df cargado para procesar en esta funcion   
    df_filtro_genero['genres']= df_filtro_genero['genres'].str.lower()      #Convierte la columan Genero a minusculas
    # Se filtra por el genero de entrada en minusculas
    df_filtro_genero= df_filtro_genero[df_filtro_genero['genres'] == genero.lower()]        
    indice_genero= df_filtro_genero.index[0]                    # Se toma el indice de la primera fila del df filtrado
    strGenero= df_UserForGenre.loc[indice_genero]['genres']     # Guarda el Genero como esta en el df_game original para visualizarlo en el resultado
    # Se agrupa por id y año de lanzamiento y se suman las horas jugadas
    df_user_max= df_filtro_genero.groupby(by=['user_id','release_year'], as_index=False)['playtime_forever'].sum().sort_values(by='playtime_forever', ascending=False)    
    user_max_horas= df_user_max.iloc[0,0]   # Se toma el user_id con mas horas jugadas 
    df_horas_jugadas= df_user_max[df_user_max['user_id']==user_max_horas]   #se realiza un filtro por el usuario con mas horas jugadas
    df_horas_jugadas.sort_values(by='playtime_forever', ascending=False)    #se ordena por tiempo de juego
    # Se itera sobre el df donde se estan los años y hora jugadas por año y se guardan en una lista
    list_horas_xyear= [{'Año ': year, 'Horas: ': horas} for year, horas in zip(df_horas_jugadas['release_year'], df_horas_jugadas['playtime_forever'])]
    # Se guardan los resultado en la variable result y se retorna
    result= {'Usuario con mas horas jugadas para el Genero {}'.format(strGenero): user_max_horas,
            'Horas Jugadas':list_horas_xyear}
    return result


@app.get("/UsersRecommend/{year}")
def UsersRecommend(año: int):
    """Retorna los 3 juegos mas recomedados por los usuarios para el año ingresado

    Args: año (int): Año

    Returns: json
    """ 
    return userRecomended_or_Not(año, 1)    # Retorna el resultado de la funcion


@app.get("/UsersNotRecommend/{year}")
def UsersNotRecommend(año: int): 
    """Retorna los 3 juegos menos recomedados por los usuarios para el año ingresado

    Args: año (int): Año

    Returns: json
    """ 
    return userRecomended_or_Not(año, 2)    # Retorna el resultado de la funcion

@app.get("/sentiment_analysis/{year}")
def sentiment_analysis(año: int):
    """Retorna la cantidad de reseñas (negrativas, neutrales y positivas) de la categoria de analisis de sentimiento

    Args: año (int): Año

    Returns: json
    """
    # se crea un df temporal con los valores unicos de juegos para hacer el join con reviews
    df_games_sin_duplicados = df_games.drop_duplicates(subset=['game_id'])
    # Se filtran los juegos por el año de lanzamiento del parametro de entrada    
    df_games_sin_duplicados = df_games_sin_duplicados[df_games_sin_duplicados['release_year'] == año]
    # Hace una union(join) de los juegos resutrados del filtro con los reviews
    df_union_games_rev = pd.merge(df_games_sin_duplicados, df_reviews, on='game_id', how= 'inner')
    # Se agrupan por analisis de sentimiento y se cuentan
    df_grupo_xSententiment= df_union_games_rev.groupby('sentiment_analysis', as_index=False).size().sort_values(by='sentiment_analysis', ascending=True)
    # Se formatean los datos para el resultado y se retornan
    result= {'Negative': int(df_grupo_xSententiment.iloc[0,1]), 'Neutral': int(df_grupo_xSententiment.iloc[1,1]), 'Positive': int(df_grupo_xSententiment.iloc[2,1])}
    return result


#########################################################################

