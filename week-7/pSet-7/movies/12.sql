SELECT movies.title FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
    AND people.name = 'Johnny Depp'
    AND movies.id IN (
        SELECT movie_id FROM stars
        JOIN people ON people.id = stars.person_id
            AND people.name = 'Helena Bonham Carter'
    );