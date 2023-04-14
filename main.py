# Librerias a utilizar
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import pandas as pd
import pickle

# Creacion de la APP
app = FastAPI(title = "Proyecto MLOps")

# Importamos el data set "df_streaming" exportado del archivo (ETL.ipynb)
df_streaming = pd.read_csv("Datasets/df_streaming.csv")

# Cargamos el modelo desde el archivo pickle
with open('modelo_recomendacion.pkl', 'rb') as f:
    cosine_sim = pickle.load(f)

# Creamos la página de inicio de la api
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    output = """
        <div style="display:flex; flex-direction:row;">
        <div style="display:flex; flex-direction:row; background-color:#f2f2f2;">
            <img src="https://raw.githubusercontent.com/MatyTrova/PI-MLOps/main/imgs/streaming.jpg" width="420" height="700">
            <div style="display:flex; flex-direction:column; margin-left:20px;">
                <h1>¡Te damos la bienvenida a nuestra plataforma en línea, donde podrás realizar consultas sobre películas y series de diversas plataformas, como Netflix, Amazon, Hulu y Disney! </h1>
                <p style="font-size: 26px;">Aquí encontrarás 7 diferentes tipos de búsquedas disponibles:</p>
                <ol>
                    <li style="font-size: 22px;">Película con mayor duración según año, plataforma y tipo de duración.  </li>
                     EJ -> ...  /get_max_duration/{anio}/{plataforma}/{dtype} <br>
                    <br><li style="font-size: 24px;">Cantidad de películas según plataforma, con un puntaje mayor a XX en determinado año. </li>
                     EJ -> ...  /get_score_count/{plataforma}/{scored}/{anio}  <br>
                    <br><li style="font-size: 24px;">Cantidad de películas según plataforma. </li>
                     EJ -> ...  /get_count_platform/{plataforma}<br> 
                    <br><li style="font-size: 24px;">Actor que más se repite según plataforma y año.</li>
                     EJ -> ...  /get_actor/{plataforma}/{anio}<br> 
                    <br><li style="font-size: 24px;">La cantidad de contenidos que se publicó por país y año.</li>
                     EJ -> ...  /prod_per_country/{tipo}/{pais}/{anio} <br>
                   <br> <li style="font-size: 24px;">La cantidad total de contenidos según el rating de audiencia dado.</li>
                     EJ -> ...  /get_contents/{rating}<br> 
                    <br> <li style="font-size: 26px;">Modelo de recomendación de películas.</li>
                     EJ -> ...  /get_recomendation/{title}<br> 
                </ol>
                <p>En el archivo README.md del repositorio de GitHub ( https://github.com/MatyTrova/PI-MLOps ), <br> encontrarás información detallada sobre el formato de búsqueda que debes seguir para cada una de las consultas disponibles</p>
            </div>
            <img src="https://raw.githubusercontent.com/MatyTrova/PI-MLOps/main/imgs/plataformas.jpg" width="420" height="700">
        </div>
    """
    return HTMLResponse(content=output)

# Se desarrollan las consultas que fueron solicitadas por el cliente:

# Consulta 1: Película (sólo película, no serie, ni documentales, etc) con mayor duración según año, plataforma y tipo de duración. 
# La función debe llamarse get_max_duration(year, platform, duration_type) y debe devolver sólo el string del nombre de la película.

@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}')
def get_max_duration(anio: int, plataforma: str, dtype: str):
    # Filtramos plataforma por letra del id, por ejemplo el id de disney es "dsXX"
    if plataforma == "amazon":
        df = df_streaming[df_streaming['id'].str.contains("a")]
    elif plataforma == "disney":
        df = df_streaming[df_streaming['id'].str.contains("d")]
    elif plataforma == "hulu":
        df = df_streaming[df_streaming['id'].str.contains("h")]
    elif plataforma == "netflix":
        df = df_streaming[df_streaming['id'].str.contains("n")]
    else:
        return print("error al introducir plataforma")
    # Filtramos el dataframe con los parametros solicitados
    df_filtrado = df.query("release_year == @anio & duration_type == @dtype")
    # Obtener el nombre de la película con mayor duración
    max_duration_movie = df_filtrado.loc[df_filtrado.duration_int.idxmax()]["title"]
    # Devolver el nombre de la película en un diccionario, como un string
    return {'pelicula': max_duration_movie}   




# Consulta 2: Cantidad de películas (sólo películas, no series, ni documentales, etc) según plataforma, con un puntaje mayor a XX en determinado año. 
# La función debe llamarse get_score_count(platform, scored, year) y debe devolver un int, con el total de películas que cumplen lo solicitado.

@app.get('/get_score_count/{plataforma}/{scored}/{anio}')
def get_score_count(plataforma: str, scored: float, anio: int):
    # Filtramos plataforma por letra del id, por ejemplo el id de disney es "dsXX"
    if plataforma == "amazon":
        df = df_streaming[df_streaming['id'].str.contains("a")]
    elif plataforma == "disney":
        df = df_streaming[df_streaming['id'].str.contains("d")]
    elif plataforma == "hulu":
        df = df_streaming[df_streaming['id'].str.contains("h")]
    elif plataforma == "netflix":
        df = df_streaming[df_streaming['id'].str.contains("n")]
    else:
        return print("error al introducir plataforma")
    # Definimos que solo sea película
    type = "movie"
    # Filtramos
    df_filtrado = df.query("release_year == @anio & score > @scored  & type == @type")
    # Contamos la cantidad total de registros que cumplen estos parametros
    cantidad_total = len(df_filtrado)
    # Retornamos un diccionario con las respuestas
    return {
        'plataforma': plataforma,
        'cantidad': cantidad_total,
        'anio': anio,
        'score': scored
    }



# Consulta 3: Cantidad de películas (sólo películas, no series, ni documentales, etc) según plataforma. 
# La función debe llamarse get_count_platform(platform) y debe devolver un int, con el número total de películas de esa plataforma. 
# Las plataformas deben llamarse amazon, netflix, hulu, disney.

@app.get('/get_count_platform/{plataforma}')
def get_count_platform(plataforma: str):
    # Filtramos plataforma por letra del id, por ejemplo el id de disney es "dsXX y agregamos variable con el nombre de la plataforma" 
    if plataforma == "amazon":
        df = df_streaming[df_streaming['id'].str.contains("a")]
    elif plataforma == "disney":
        df = df_streaming[df_streaming['id'].str.contains("d")]
    elif plataforma == "hulu":
        df = df_streaming[df_streaming['id'].str.contains("h")]
    elif plataforma == "netflix":
        df = df_streaming[df_streaming['id'].str.contains("n")]
    else:
        return print("error al introducir plataforma")
    # Filtramos
    df_filtrado = df.query("type == 'movie'")
    # Contamos cantidad de registros del df filtrado por plataforma
    cantidad_total = len(df_filtrado)
    # Retornamos un diccionario con el nombre de la plataforma y la cantidad de películas
    return {'plataforma': plataforma, 'peliculas': cantidad_total}




# Consulta 4: Actor que más se repite según plataforma y año. 
# La función debe llamarse get_actor(platform, year) y debe devolver sólo el string con el nombre del actor que más se repite según la plataforma y el año dado.

@app.get('/get_actor/{plataforma}/{anio}')
def get_actor(plataforma: str, anio: int):
    # Filtramos plataforma por letra del id, por ejemplo el id de disney es "dsXX"
    if plataforma == "amazon":
        df = df_streaming[df_streaming['id'].str.contains("a")]
    elif plataforma == "disney":
        df = df_streaming[df_streaming['id'].str.contains("d")]
    elif plataforma == "hulu":
        df = df_streaming[df_streaming['id'].str.contains("h")]
    elif plataforma == "netflix":
        df = df_streaming[df_streaming['id'].str.contains("n")]
    else:
        return print("error al introducir plataforma")
    # Filtramos
    df_filtrado = df.query("release_year == @anio")
    # Iteramos para saber que actor se repite mas y lo guardamos en un diccionario
    name_counts = {}
    for index, row in df_filtrado.iterrows():
        # Comprueba que sea de tipo de dato str
        if isinstance(row["cast"], str):
            # Separamos por la coma, ya que el "cast" cuenta con varios nombres separados por coma
            names = row["cast"].split(", ")
            for name in names:
                if name in name_counts:
                    name_counts[name] += 1
                else:
                    name_counts[name] = 1
    most_common_name = max(name_counts, key=name_counts.get)
    # Devuelve el actor que mas se repite en un diccionario
    return {
            'plataforma': plataforma,
            'anio': anio,
            'actor': most_common_name,
            'apariciones': name_counts[most_common_name]
        }



# Consulta 5: La cantidad de contenidos/productos (todo lo disponible en streaming) que se publicó por país y año. 
# La función debe llamarse prod_per_county(tipo,pais,anio) deberia devolver el tipo de contenido (pelicula,serie,documental) por pais,
# y año en un diccionario con las variables llamadas 'pais' (nombre del pais), 'anio' (año), 'pelicula' (tipo de contenido).

@app.get('/prod_per_country/{tipo}/{pais}/{anio}')
def prod_per_country(tipo: str, pais: str, anio: int):
    # Filtrar los datos para el país, año y tipo especificados
    df_filtrado = df_streaming.query("type ==  @tipo & country == @pais & release_year == @anio")
    # Contar la cantidad de filas del contenido
    count = len(df_filtrado["id"])
    # Crear un diccionario con los resultados
    return {'pais': pais, 'anio': anio, 'peliculas': count}


# Consulta 6: La cantidad total de contenidos/productos (todo lo disponible en streaming, series, documentales, peliculas, etc),
# según el rating de audiencia dado (para que publico fue clasificada la pelicula). 
# La función debe llamarse get_contents(rating) y debe devolver el numero total de contenido con ese rating de audiencias.

@app.get('/get_contents/{rating}')
def get_contents(rating: str):
    # Filtramos
    df_filtrado = df_streaming[df_streaming["rating"] == rating]
    # Contamos la cantidad de contenido
    count = len(df_filtrado["id"])
    # Mostramos resultado en un diccionario
    return {'rating': rating, 'contenido': count}






# Modelo de recomendación: Creamos el modelo de recomendación, que éste consiste en recomendar películas a los usuarios basándose en películas similares, 
# se ordenarán según el score y devolverá una lista con 5 valores, cada uno siendo el string del nombre de las películas con mayor puntaje, en orden descendente.

@app.get('/get_recomendation/{title}')
def get_recommendations(title, cosine_sim=cosine_sim, df=df_streaming):
    # Obtener el índice del elemento que coincide con el título
    idx = df[df['title'] == title].index[0]
    # Obtener las puntuaciones de similitud de coseno del elemento con todos los elementos
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Ordenar los elementos según su puntuación de similitud de coseno
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Obtener los índices de los elementos más similares
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    # Devolver los títulos de los elementos más similares
    peliculas = df[['title',"score"]].iloc[movie_indices]
    # Ordenamos según "score" descendente
    peliculas = peliculas.sort_values(by="score",ascending = False)
    # Convertimos a lista y solo tomamos el titulo
    peliculas = list(peliculas["title"])
    # Retornamos un diccionario con una lista de las 5 películas ordenadas de forma descendente según el score
    return {'recomendacion': peliculas[:5]}
  
