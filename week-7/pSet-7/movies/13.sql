SELECT DISTINCT people.name FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON movies.id = stars.movie_id
    AND movies.id IN (SELECT movie_id FROM stars
            JOIN people ON stars.person_id = people.id
                AND people.name = 'Kevin Bacon' 
                AND people.birth = 1958
            )
AND people.name != 'Kevin Bacon';