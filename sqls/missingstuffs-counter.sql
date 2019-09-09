SELECT
	m.missingstuffs stuff,
	COUNT(m.missingstuffs) total
FROM associates a
INNER JOIN missing m ON m.associate = a.associate_name
WHERE
    a.deleted=0
    AND m.missingstuffs!=""
    AND m.deleted=0
GROUP BY
	m.missingstuffs
ORDER BY total DESC