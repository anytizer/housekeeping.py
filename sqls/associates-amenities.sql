SELECT COUNT(*) total
FROM missing m
         INNER JOIN amenities a ON a.amenity_name = m.missingstuffs
WHERE a.amenity_name = ?
;