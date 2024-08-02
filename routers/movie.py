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
from schemas.movie import Movie, GetMovie, GetMovieByCategory

movie_router = APIRouter()
db = session()
movie_service = MovieService(db)

@movie_router.post('/movies/get_movies', tags=["Movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    movies = movie_service.get_movies()
    db.close()
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))


@movie_router.post('/movies/get_movie', tags=["Movies"], response_model=Movie, dependencies=[Depends(JWTBearer())])
def get_movie(getMovie: GetMovie):
    movie = movie_service.get_movie(getMovie.id)
    db.close()
    if not movie:
        return JSONResponse(status_code= 404, content=["No encontrado"])
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))


@movie_router.post('/movies/get_movies_by_category', tags=["Movies"], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies_by_category(category: GetMovieByCategory) -> List[Movie]:
    movies = movie_service.get_movies_by_category(category.category)
    db.close()
    if not movies:
        return JSONResponse(status_code= 404, content=["No encontrado"])
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))


@movie_router.post('/movies/create_movie', tags=["Movies"], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie) -> dict:
    movie_service.create_movie(movie)
    db.close()
    response = {
        "message": "Se registro la pelicula"
    }

    return JSONResponse(status_code=201, content=response)


@movie_router.post('/movies/update_movie', tags=["Movies"], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_movie(movie: Movie) -> dict:

    result = movie_service.update_movie(movie)
    if not result:
        db.close()
        return JSONResponse(status_code=404, content={"Error": "No se encontró"})
    db.close()
    response = {
        "message": "Se modificó la pelicula"
    }

    return JSONResponse(status_code=201, content=response)


@movie_router.post('/movies/delete_movie', tags=["Movies"], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_movie(getMovie: GetMovie) -> dict:
    
    result = movie_service.delete_movie(getMovie.id)
    if not result:
        db.close()
        return JSONResponse(status_code=404, content={"Error": "No se encontró"})
    db.close()
    response = {
        "message": "Se eliminó la pelicula"
    }

    return JSONResponse(status_code=200, content=response)
