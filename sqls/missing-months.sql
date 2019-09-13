SELECT
	substr(date, 1, 7) dt,
	count(m.date) total
FROM missing m
where
	m.deleted=0
group by
	dt
;