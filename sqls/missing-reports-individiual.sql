SELECT
       id,
       SUBSTR(`date`, 0, 11) `date`,
       associate,
       room_number,
       missingstuffs,
       anc,
       remarks
FROM missing
WHERE
    deleted=0
    AND associate=?
    -- AND date >= date('2010-01-01') -- 6 months old as of now
ORDER BY DATE DESC
LIMIT ?;
