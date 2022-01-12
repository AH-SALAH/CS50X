SELECT title, rating FROM movies, ratings
WHERE movies.year = 2010 
AND movies.id = ratings.movie_id 
AND ratings.rating > 0
ORDER BY
(CASE WHEN ratings.rating THEN ratings.rating END) DESC,
(CASE WHEN ratings.rating = ratings.rating THEN movies.title END);