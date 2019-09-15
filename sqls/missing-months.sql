SELECT
	substr(date, 1, 7) dt,
	count(m.date) total
FROM missing m
WHERE
	m.deleted=0
    AND date >= ?
GROUP BY
	dt
;
