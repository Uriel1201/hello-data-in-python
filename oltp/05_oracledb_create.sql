/* 
05. Super Users.

A company defines its super users as
those who have made at least two
transactions. 
Writing a query to return, for each user, the
date when they become a super user, ordered by oldest super users first.
Users who are not super users should
also be present in the table. */

/* ORACLE. */

/********************************************************************/
CREATE TABLE USERS_P5 (
    USER_ID          INTEGER,
    PRODUCT_ID       INTEGER,
    TRANSACTION_DATE DATE
);

INSERT INTO USERS_P5
    WITH NAMES AS (
        SELECT
            1,
            101,
            '12-feb-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            2,
            105,
            '13-feb-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            1,
            111,
            '14-feb-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            3,
            121,
            '15-feb-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            1,
            101,
            '16-feb-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            2,
            105,
            '17-feb-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            4,
            101,
            '16-feb-20'
        FROM
            DUAL
        UNION ALL
        SELECT
            3,
            105,
            '15-feb-20'
        FROM
            DUAL
    )
    SELECT
        *
    FROM
        NAMES;
