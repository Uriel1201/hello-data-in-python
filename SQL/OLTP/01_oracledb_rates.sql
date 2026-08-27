/* 
01. Cancellation Rates.

Write a query to return the publication and cancellation
rate for each user. */

/* ORACLE 23ai. */
/********************************************************************/
        -- Returning rates for each user.
WITH TOTALS ( -- Totals for each action 
    USER_ID,
    TOTAL_STARTS,
    TOTAL_CANCELS,
    TOTAL_PUBLISHES
) AS (
    SELECT
        USER_ID,
        SUM(
            CASE
                WHEN ACTION = 'start' THEN
                    1
                ELSE
                    0
            END
        ),
        SUM(
            CASE
                WHEN ACTION = 'cancel' THEN
                    1
                ELSE
                    0
            END
        ),
        SUM(
            CASE
                WHEN ACTION = 'publish' THEN
                    1
                ELSE
                    0
            END
        )
    FROM
        USERS_01
    GROUP BY
        USER_ID
)
SELECT
    USER_ID,
    ROUND(TOTAL_PUBLISHES / NULLIF(TOTAL_STARTS, 0),
          2) AS PUBLISH_RATE,
    ROUND(TOTAL_CANCELS / NULLIF(TOTAL_STARTS, 0),
          2) AS CANCEL_RATE
FROM
    TOTALS;
