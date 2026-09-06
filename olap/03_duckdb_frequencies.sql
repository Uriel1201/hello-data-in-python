WITH FREQUENCIES AS (
    FROM
        '{table}'
    SELECT
        ITEM,
        COUNT(*) AS FREQUENCY,
        DATES
    GROUP BY
        DATES,
        ITEM
), RANKED_ITEMS AS (
    FROM
        FREQUENCIES
    SELECT
        ITEM,
        DENSE_RANK() OVER (
            PARTITION BY
                DATES
            ORDER BY
                FREQUENCY DESC
        ) AS POSITION,
        DATES
)
SELECT
    ITEM,
    DATES
FROM
    RANKED_ITEMS
WHERE
    POSITION = 1
