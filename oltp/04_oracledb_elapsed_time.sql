WITH POSITIONS (
    ID,
    ACTION_DATE,
    POSITION 
) AS (
    SELECT 
        ID,
        ACTION_DATE,
        RANK() OVER(
            PARTITION BY 
                ID
            ORDER BY ACTION_DATE DESC
        )
    FROM
        USERS_04
), LAST (
    ID,
    ACTION_DATE
) AS (
    SELECT 
        POSITIONS.ID,
        POSITIONS.ACTION_DATE
    FROM
        POSITIONS
    WHERE
        POSITION = 1
), SECOND_LAST (
    ID,
    ACTION_DATE
) AS (
    SELECT
        POSITIONS.ID,
        POSITIONS.ACTION_DATE
    FROM
        POSITIONS
    WHERE
        POSITION = 2
)
SELECT 
    *
FROM
    SECOND_LAST
