/* 
01. Cancellation Rates.

From the following table of user IDs,
actions, and dates, write a query to
return the publication and cancellation
rate for each user. */

-- PostgreSQL.
/********************************************************************/
with
    "TOTALS" as (
        select
            "USER_ID",
            sum(
                case 
                    when "ACTION" = 'start' 
                    then 1 
                    else 0 
                end
            )::numeric as "TOTAL_STARTS",
            sum(
                case 
                    when "ACTION" = 'cancel' 
                    then 1 
                    else 0 
                end
            )::numeric as "TOTAL_CANCELS",
            sum(
                case 
                    when "ACTION" = 'publish' 
                    then 1 
                    else 0 
                end
            )::numeric as "TOTAL_PUBLISHES"
        from
            "USERS_01"
        group by
            "USER_ID"
    )
select
    "USER_ID",
    round("TOTAL_PUBLISHES" / case 
              when "TOTAL_STARTS" = 0 then null 
              else "TOTAL_STARTS" 
          end, 
          3
    ) as "PUBLISH_RATE",
    round("TOTAL_CANCELS" / case 
              when "TOTAL_STARTS" = 0 then null 
              else "TOTAL_STARTS" 
          end, 
          3
    ) as "CANCEL_RATE"
FROM
    "TOTALS"
ORDER BY 
    1;
