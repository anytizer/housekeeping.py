SELECT
    a.associate_name associate,
    SUM(CASE WHEN m.missingstuffs = "" THEN 0 ELSE 1 END) missingstuffs_total,
    SUM(CASE WHEN m.anc = "" THEN 0 ELSE 1 END) anc_total,
    COUNT(a.associate_name) total
FROM associates a
INNER JOIN missing m ON m.associate = a.associate_name
WHERE
    a.deleted = 0
    AND m.deleted = 0
    AND SUBSTR(m.date, 1, 7)=?
GROUP BY a.associate_name
ORDER BY total DESC
;