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
    AND created_on LIKE DATE('NOW', 'LOCALTIME')||'%'
ORDER BY created_on DESC
LIMIT ?
;