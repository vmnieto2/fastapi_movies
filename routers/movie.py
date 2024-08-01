from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import session
from Models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()
db = session()
movie_service = MovieService(db)

  
# , dependencies=[Depends(JWTBearer())]
@movie_router.get('/movies', tags=["Movies"], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    movies = movie_service.get_movies()
    db.close()
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))


@movie_router.get('/movies/{id}', tags=["Movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    movie = movie_service.get_movie(id)
    db.close()
    if not movie:
        return JSONResponse(status_code= 404, content=["No encontrado"])
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))


@movie_router.get('/movies/', tags=["Movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=100)) -> List[Movie]:
    movies = movie_service.get_movies_by_category(category)
    db.close()
    if not movies:
        return JSONResponse(status_code= 404, content=["No encontrado"])
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))


@movie_router.post('/movies', tags=["Movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movie_service.create_movie(movie)
    db.close()
    response = {
        "message": "Se registro la pelicula"
    }

    return JSONResponse(status_code=201, content=response)


@movie_router.put('/movies/{id}', tags=["Movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:

    result = movie_service.update_movie(id, movie)
    if not result:
        db.close()
        return JSONResponse(status_code=404, content={"Error": "No se encontró"})
    db.close()
    response = {
        "message": "Se modificó la pelicula"
    }

    return JSONResponse(status_code=201, content=response)


@movie_router.delete('/movies/{id}', tags=["Movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    
    result = movie_service.delete_movie(id)
    if not result:
        db.close()
        return JSONResponse(status_code=404, content={"Error": "No se encontró"})
    db.close()
    response = {
        "message": "Se eliminó la pelicula"
    }

    return JSONResponse(status_code=200, content=response)
