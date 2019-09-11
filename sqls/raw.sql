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
    deleted = ?
    AND SUBSTR(date, 1, 7)=?
ORDER BY `date` DESC, associate ASC, room_number ASC
LIMIT ?;
