from fastapi import FastAPI
import pandas as pd

# Se cargan los dataset transformados
df_games= pd.read_csv('DataSet_tranformados/games.csv',delimiter = ',',encoding = "utf-8")
df_reviews= pd.read_csv('DataSet_tranformados/reviews.csv',delimiter = ',',encoding = "utf-8")
df_items= pd.read_parquet('DataSet_tranformados/items.parquet')

app = FastAPI()

@app.get("/PlayTimeGenre/{genero}")
def PlayTimeGenre(genero: str = None)-> dict:
    df_filtro_genero= df_games[df_games['genres'] == genero]    # Se filtra el Dataset de Games con el genero del parametro
    # Se hace un Join con el df donde se cargo el filtro  y el Data set de Items
    df_union = pd.merge(df_filtro_genero, df_items, on='game_name', how= 'inner')   
    # Se agrupa por genero y año y se suman los tiempos de juego. Luego se ordena
    df_grupo_por_genero_y_año = df_union.groupby(by=['genres','release_year'], as_index=False)['playtime_forever'].sum().sort_values(by='playtime_forever', ascending=False)
    year_max_horas= int(df_grupo_por_genero_y_año.iloc[0,1])    #Se toma el primer año de el dataset Ordenado
    result= {'Año de lanzamiento con más horas jugadas para Género {}'.format(genero): year_max_horas}  
    return result

@app.get("/UserForGenre/{genero}")
def UserForGenre(genero: str = None)-> dict:
    # Se agrupa el dataset "df_Items" por Usuario y juegos y se sumo el tiempo de juef
    df_items_por_user = df_items.groupby(by=['user_id','game_name'], as_index=False)['playtime_forever'].sum() 
    # Se filtra el dataset "df_games" por el genero requerido
    df_filtro_genero= df_games[df_games['genres'] == genero]
    # Se hace una union de los juegos fltrados por el genero requerido y el dataset de items ya filtrado
    df_union = pd.merge(df_filtro_genero, df_items_por_user, on='game_name', how= 'inner')
    # se suman las horas jugadas de cada usuario por año
    df_grupo_por_user_y_año = df_union.groupby(by=['user_id','release_year'], as_index=False)['playtime_forever'].sum().sort_values(by='playtime_forever', ascending=False)
    # Se suman las horas jugadas de todos los años por usuario
    df_user_max= df_grupo_por_user_y_año.groupby(by=['user_id'], as_index=False)['playtime_forever'].sum().sort_values(by='playtime_forever', ascending=False)
    user_max_horas= df_user_max.iloc[0,0]   # Se toma el user_id con mas horas jugadas 
    df_horas_jugadas= df_grupo_por_user_y_año[df_grupo_por_user_y_año['user_id']==user_max_horas]   #se realiza un filtro por el usuario con mas horas jugadas
    df_horas_jugadas.sort_values(by='playtime_forever', ascending=False)    #se ordena por tiempo de juego
    
    list_horas_xyear= [{'Año ': year, 'Horas: ': horas} for year, horas in zip(df_horas_jugadas['release_year'], df_horas_jugadas['playtime_forever'])]
    
    result= {'Usuario con mas horas jugadas para el Género {}'.format(genero): user_max_horas,'Horas Jugadas':list_horas_xyear}
    return result


@app.get("/UsersRecommend/{year}")
def UsersRecommend(año: int)-> dict:  
    # Filtra los remomendados positivos, comentarios positivos y neutrales y el año especificado en el parametro de entrada
    df_filtred_rec_sent_year= df_reviews[(df_reviews['recommend']== True) & (df_reviews['sentiment_analysis']> 0) & (df_reviews['year'] == año)]
    # Se agrupan por id de juego y se cuentan las comentarios. Luego se ordenan de mayor a menor
    df_grupo_xgames= df_filtred_rec_sent_year.groupby('game_id', as_index=False).size().sort_values(by='size', ascending=False)
    # Se eliminan los duplicados de columna game_id del dataset de juegos en un df temporal
    df_games_sin_duplicados = df_games.drop_duplicates(subset=['game_id'])  
    # Se hace un Join con del df agrupado por id con el df de juegos temporal para tomar los nombres de los juegos
    df_union_con_items= pd.merge(df_grupo_xgames, df_games_sin_duplicados, on='game_id', how= 'inner')
    # Se muestran los resultados de los 3 juegos mas recomendados
    result= {'Puesto {}'.format(pos +1): game for pos, game in zip(range(3),df_union_con_items['game_name'].iloc[:3])}
    return result