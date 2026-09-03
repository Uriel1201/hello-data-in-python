select 
  "USER_ID", 
  "ACTION", 
  ("DATES"::timestamptz)::date as "DATES"
from 
  "USERS_01"
