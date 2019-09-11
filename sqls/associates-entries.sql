SELECT a.associate_id,
       a.associate_name,
       COUNT(*) entries
FROM missing m
         INNER JOIN associates a ON a.associate_name = m.associate
WHERE m.deleted = ?
  AND a.associate_id = ?
GROUP BY a.associate_name
ORDER BY a.associate_name ASC
;