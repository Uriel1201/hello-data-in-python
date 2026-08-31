/* ORACLE 23ai. */
/********************************************************************/
CREATE TABLE USERS_01 (
    USER_ID INTEGER NOT NULL,
    ACTION  VARCHAR(9),
    DATES   DATE
);

INSERT INTO USERS_01
    WITH NAMES AS (
        SELECT
            1,
            'start',
            '01-jan-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            1,
            'cancel',
            '02-jan-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            2,
            'start',
            '03-jan-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            2,
            'publish',
            '04-jan-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            3,
            'start',
            '05-jan-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            3,
            'cancel',
            '06-jan-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            1,
            'start',
            '07-jan-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            1,
            'publish',
            '08-jan-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            3,
            'start',
            '09-jan-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            3,
            'cancel',
            '10-jan-20'
        FROM
            DUAL
    )
    SELECT
        *
    FROM
        NAMES;
