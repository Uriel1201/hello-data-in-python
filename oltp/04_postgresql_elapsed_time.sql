with positions (
    user_id,
    dates,
    position 
) as (
    select 
        "ID",
        "ACTION_DATE",
        row_number() over(
            partition by
                "ID"
            order by "ACTION_DATE" desc
        )
    from
        "USERS_04"
), last (
    user_id,
    dates
) as (
    select 
        positions.user_id,
        positions.dates
    feom
        positions 
    where
        positions.position = 1
), second_last (
    user_id,
    dates
) as (
    select 
        positions.user_id,
        positions.dates
    from
        positions 
    where
        positions.position = 2
)
select 
    last_user_id,
    (last.dates - second_last.dates) as days_elapsed
from 
    last
     SECOND_LAST ON LAST.ID = SECOND_LAST.ID
