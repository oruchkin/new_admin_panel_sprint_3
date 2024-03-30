
class Movie:
    def __init__(self, movie_id, title, description, rating, genres, directors=None, actors=None, writers=None):
        self.id = movie_id
        self.title = title
        self.description = description
        self.imdb_rating = rating
        self.genres = genres
        self.directors = directors if directors is not None else []
        self.actors = actors if actors is not None else []
        self.writers = writers if writers is not None else []
        self.directors_names = [director['name'] for director in self.directors]
        self.actors_names = [actor['name'] for actor in self.actors]
        self.writers_names = [writer['name'] for writer in self.writers]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "imdb_rating": self.imdb_rating,
            "genres": self.genres,
            "directors": self.directors,
            "actors": self.actors,
            "writers": self.writers,
            "directors_names": self.directors_names,
            "actors_names": self.actors_names,
            "writers_names": self.writers_names
        }



def transform_data(results) -> list:
    """Преобразование результатов запроса в список экземпляров класса Movie."""
    movies = []
    for row in results:
        movie = Movie(
            movie_id=row['id'],
            title=row['title'],
            description=row['description'],
            rating=row['rating'],
            genres=row['genres'],
            directors=row['directors'],
            actors=row['actors'],
            writers=row['writers']
        )
        movies.append(movie.to_dict())  # Преобразование экземпляра класса Movie в словарь
    return movies
