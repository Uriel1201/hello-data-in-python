select 
    "DATES"::date as dates,
    nullif(trim("ITEM"), '') as items
from
    "ITEMS_03"
