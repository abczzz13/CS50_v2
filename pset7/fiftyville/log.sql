-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Location: took place on Humphrey Street.
-- Date: took place on July 28, 2021

-- 001: Search the crime scene reports
SELECT  *
FROM    crime_scene_reports
WHERE   year = 2021
AND     month = 7
AND     day = 28
AND     street = 'Humphrey Street';
/*
| 295 | 2021 | 7     | 28  | Humphrey Street | Theft of the CS50 duck took place at 10:15am at the
Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the
time – each of their interview transcripts mentions the bakery. |
*/

-- 002: Search for interview transcripts
SELECT  *
FROM    interviews
WHERE   year = 2021
AND     month = 7
AND     day = 28;
/*
| 162 | Eugene  | 2021 | 7     | 28  | I don't know the thief's name, but it was someone I recognized.
Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street
and saw the thief there withdrawing some money.
| 163 | Raymond | 2021 | 7     | 28  | As the thief was leaving the bakery, they called someone who
talked to them for less than a minute. In the call, I heard the thief say that they were planning to
take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end
of the phone to purchase the flight ticket. |
| 193 | Emma    | 2021 | 7     | 28  | I'm the bakery owner, and someone came in, suspiciously
whispering into a phone for about half an hour. They never bought anything.
*/

-- 003: Checking the ATM logs
SELECT  *
FROM    atm_transactions
WHERE   year = 2021
AND     month = 7
AND     day = 28
AND     atm_location = 'Leggett Street'
AND     transaction_type = 'withdraw';

-- 004: Checking the bankaccounts of the above query
SELECT  *
FROM    bank_accounts
    JOIN    .sch
    ON      people.id = bank_accounts.person_id
    WHERE   account_number IN
        (SELECT account_number
        FROM    atm_transactions
        WHERE   year = 2021
        AND     month = 7
        AND     day = 28
        AND     atm_location = 'Leggett Street'
        AND     transaction_type = 'withdraw');

-- 005: Checking for the earliest flight from Fiftyville tomorrow
SELECT  *
FROM    flights
    JOIN    airports
    ON      airports.id = flights.origin_airport_id
    WHERE   airports.city = 'Fiftyville'
    AND     flights.year = 2021
    AND     flights.month = 7
    AND     flights.day = 29
    AND     flights.hour < 12;
/* flight.id = 36 -> Thief escaped to destination_airport_id: 4 */


-- 006: Getting passengerlist for earliest flight from Fiftyville tomorrow
SELECT  *
FROM    passengers
WHERE   flight_id = 36
AND     passport_number IN
    (SELECT people.passport_number
    FROM    people
        JOIN    bank_accounts
        ON      people.id = bank_accounts.person_id
        WHERE   account_number IN
            (SELECT account_number
            FROM    atm_transactions
            WHERE   year = 2021
            AND     month = 7
            AND     day = 28
            AND     atm_location = 'Leggett Street'
            AND     transaction_type = 'withdraw'));

-- 007: Checking phone_calls
SELECT *
FROM phone_calls
WHERE   year = 2021
AND     month = 7
AND     day = 28
AND     duration < 60;

-- 008: Query to connect some dots: phonecalls <60s, atm transactions on Leggett Street, and passenger on the earliest flight tomorrow
SELECT *
FROM people
WHERE   passport_number IN
    (SELECT passport_number
    FROM    passengers
    WHERE   flight_id = 36
    AND     passport_number IN
        (SELECT people.passport_number
        FROM    people
            JOIN    bank_accounts
            ON      people.id = bank_accounts.person_id
            WHERE   account_number IN
                (SELECT account_number
                FROM    atm_transactions
                WHERE   year = 2021
                AND     month = 7
                AND     day = 28
                AND     atm_location = 'Leggett Street'
                AND     transaction_type = 'withdraw')))
AND     phone_number IN
    (SELECT caller
    FROM phone_calls
    WHERE   year = 2021
    AND     month = 7
    AND     day = 28
    AND     duration < 60);

-- 009: Check the bakery_security_logs
SELECT  *
FROM    bakery_security_logs
WHERE   year = 2021
AND     month = 7
AND     day = 28
AND     hour > 8
AND     hour < 11;

-- 010: Connecting some dots: phonecalls <60s, atm transactions on Leggett Street, passenger on the earliest flight tomorrow,
-- and license plate exiting the bakery shortly after the theft
SELECT *
FROM people
WHERE   passport_number IN
    (SELECT passport_number
    FROM    passengers
    WHERE   flight_id = 36
    AND     passport_number IN
        (SELECT people.passport_number
        FROM    people
        JOIN    bank_accounts
        ON      people.id = bank_accounts.person_id
        WHERE   account_number IN
            (SELECT account_number
            FROM    atm_transactions
            WHERE   year = 2021
            AND     month = 7
            AND     day = 28
            AND     atm_location = 'Leggett Street'
            AND     transaction_type = 'withdraw')))
AND phone_number IN
    (SELECT caller
    FROM phone_calls
    WHERE   year = 2021
    AND     month = 7
    AND     day = 28
    AND     duration < 60)
AND license_plate IN
    (SELECT  license_plate
    FROM    bakery_security_logs
    WHERE   year = 2021
    AND     month = 7
    AND     day = 28
    AND     hour > 9
    AND     hour < 11
    AND     minute < 25
    AND     activity = 'exit');
/*
+--------+-------+----------------+-----------------+---------------+
|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+-------+----------------+-----------------+---------------+
*/

-- 011:  Query to find where the thief escaped too
-- Thief escaped to destination_airport_id: 4
SELECT  *
FROM    airports
WHERE   id = 4;
/*
+----+--------------+-------------------+---------------+
| id | abbreviation |     full_name     |     city      |
+----+--------------+-------------------+---------------+
| 4  | LGA          | LaGuardia Airport | New York City |
+----+--------------+-------------------+---------------+
*/

-- 012: Find the accomplice
SELECT *
FROM people
WHERE phone_number IN
    (SELECT  receiver
    FROM    phone_calls
    WHERE   caller = '(367) 555-5533'
    AND     year = 2021
    AND     month = 7
    AND     day = 28
    AND     duration < 60);
