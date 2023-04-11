# Librerias a utilizar
from fastapi import FastAPI, Request, HTMLResponse
import pandas as pd

# Creacion de la APP
app = FastAPI()

# Importamos el data set "df_streaming" exportado del archivo (ETL.ipynb)
df_streaming = pd.read_csv("Datasets/df_streaming.csv")

# Creamos un directorio index con mensaje de bienvenida
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    output = """
        <div style="display:flex; flex-direction:row;">
            <img src="https://ejemplo.com/imagen_portada.png" alt="Imagen de portada" style="width:300px; height:auto;">
            <div style="display:flex; flex-direction:column; margin-left:20px;">
                <h1>¡Te damos la bienvenida a nuestra plataforma en línea, donde podrás realizar consultas sobre películas y series de diversas plataformas, como Netflix, Amazon, Hulu y Disney! </h1>
                <p>Aquí encontrarás 6 diferentes tipos de búsquedas disponibles:</p>
                <ol>
                    <li>-> Película con mayor duración según año, plataforma y tipo de duración. Ej :  </li>
                    <li>-> Cantidad de películas según plataforma, con un puntaje mayor a XX en determinado año. Ej : </li>
                    <li>-> Cantidad de películas según plataforma. Ej : </li>
                    <li>-> Actor que más se repite según plataforma y año. Ej : </li>
                    <li>-> La cantidad de contenidos que se publicó por país y año. Ej : </li>
                    <li>-> La cantidad total de contenidos según el rating de audiencia dado. Ej : </li>
                </ol>
                <p>En el archivo README.md del repositorio de GitHub (www.), encontrarás información detallada sobre el formato de búsqueda que debes seguir para cada una de las consultas disponibles</p>
            </div>
            <img src="https://ejemplo.com/imagen_derecha.png" alt="Imagen a la derecha" style="width:300px; height:auto;">
        </div>
    """
    return HTMLResponse(content=output)

# Se desarrollan las consutlas que fueron solicitadas por el cliente:

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
    df_filtrado = df_streaming.query(f"type == '{tipo}' & country == '{pais}' & release_year == {anio}")
    # Contar la cantidad de filas del contenido
    count = df_filtrado["id"].count()
    # Crear un diccionario con los resultados
    resultado = {   "pais": pais,
                    "anio": anio,
                    "pelicula": count  }
    return {'pais': pais, 'anio': anio, 'peliculas': count}


# Consulta 6: La cantidad total de contenidos/productos (todo lo disponible en streaming, series, documentales, peliculas, etc),
# según el rating de audiencia dado (para que publico fue clasificada la pelicula). 
# La función debe llamarse get_contents(rating) y debe devolver el numero total de contenido con ese rating de audiencias.

@app.get('/get_contents/{rating}')
def get_contents(rating: str):
    # Filtramos
    df_filtrado = df_streaming[df_streaming["rating"] == rating]
    # Contamos la cantidad de contenido
    count = df_filtrado["id"].count()
    # Mostramos resultado en un diccionario
    return {'rating': rating, 'contenido': count}








""""
@app.get('/get_recomendation/{title}')
def get_recomendation(title,):
    
    return {'recomendacion':respuesta}
"""