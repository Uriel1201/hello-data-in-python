WITH FREQUENCIES (
    ITEM,
    FREQUENCY,
    DATES
) AS (
    SELECT
        ITEM,
        COUNT(*) AS FREQUENCY,
        DATES
    FROM
        ITEMS_03
    GROUP BY
        DATES,
        ITEM
), RANKED_ITEMS (
    ITEM,
    POSITION,
    DATES
) AS (
    SELECT 
        FREQUENCIES.ITEM,
        RANK() OVER (
            PARTITION BY
                FREQUENCIES.DATES
            ORDER BY
                FREQUENCIES.FREQUENCY DESC
        ),
        DATES
    FROM
        FREQUENCIES 
)
SELECT 
    *
FROM
    RANKED_ITEMS
WHERE 
    RANKED_ITEMS.POSITION = 1
