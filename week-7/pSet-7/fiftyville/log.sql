-- Keep a log of any SQL queries you execute as you solve the mystery.

-- see crime reports that day in this city which related to cs50 duck robbery
SELECT * FROM crime_scene_reports
WHERE day = 28 AND month = 7 AND year = 2020 AND street = 'Chamberlin Street';

-- see what interviews say for this day
SELECT * FROM interviews
WHERE day = 28 AND month = 7 AND year = 2020 AND transcript LIKE '%courthouse%';

-- start seek upon
SELECT name as Thief, 
    (SELECT people.name FROM people WHERE people.phone_number = receiver) as accomplice, 
    city as Escaped_Place FROM (
    SELECT * FROM courthouse_security_logs
    -- Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away.
    JOIN people ON people.license_plate IN (courthouse_security_logs.license_plate)
    -- Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money
    JOIN atm_transactions ON atm_transactions.atm_location = 'Fifer Street'
        AND atm_transactions.day = 28 AND atm_transactions.month = 7 AND atm_transactions.year = 2020 
        AND atm_transactions.transaction_type = 'withdraw'
    JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number AND bank_accounts.person_id = people.id
    -- they called someone who talked to them for less than a minute.
    JOIN phone_calls ON phone_calls.day = 28 AND phone_calls.month = 7 AND phone_calls.year = 2020 
        AND phone_calls.duration < 60
        -- AND phone_calls.caller IN (people.phone_number)
        AND (phone_calls.receiver IN (people.phone_number) OR phone_calls.caller IN (people.phone_number))
        -- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. 
        -- The thief then asked the person on the other end of the phone to purchase the flight ticket.
        JOIN flights ON flights.origin_airport_id = (
            SELECT airports.id FROM airports WHERE airports.city = 'Fiftyville'
        ) 
            -- tomorrow flight [day 29]
            AND flights.day = 29 AND flights.month = 7 AND flights.year = 2020 
            -- earliest flight
            AND flights.hour = (
                SELECT MIN(flights.hour) FROM flights 
                    WHERE flights.day = 29 AND flights.month = 7 AND flights.year = 2020
                )
        -- get passenger passport at this flight among filtered people we have so far till now
        JOIN passengers ON passengers.flight_id = flights.id 
            AND passengers.passport_number = people.passport_number
        -- get dist city
        JOIN airports ON airports.id = flights.destination_airport_id

    WHERE courthouse_security_logs.day = 28 
    AND courthouse_security_logs.month = 7 
    AND courthouse_security_logs.year = 2020
    AND courthouse_security_logs.hour BETWEEN (SELECT MIN(courthouse_security_logs.hour) FROM courthouse_security_logs) AND 10
    AND courthouse_security_logs.minute > 15
    AND courthouse_security_logs.minute <= 25
    AND activity = 'exit'
);