# Delete erraneous entries
DELETE FROM missing WHERE missingstuffs='' AND anc='' AND remarks='';

UPDATE missing SET missingstuffs=UPPER(missingstuffs);

UPDATE missing SET missingstuffs='Pens' WHERE LOWER(missingstuffs)='pen';
UPDATE missing SET missingstuffs='Pens' WHERE LOWER(missingstuffs)='pens';
UPDATE missing SET missingstuffs='Bath Mat' WHERE LOWER(missingstuffs)='bath mat';
UPDATE missing SET missingstuffs='Ice Bag' WHERE LOWER(missingstuffs)='ice bag';
UPDATE missing SET missingstuffs='Garbage Bag' WHERE LOWER(missingstuffs)='garbage bag';
UPDATE missing SET missingstuffs='Memo Pad (Note Book)' WHERE LOWER(missingstuffs)='memo pad';
UPDATE missing SET missingstuffs='Toilet Paper' WHERE LOWER(missingstuffs)='toilet paper';
UPDATE missing SET missingstuffs='Face Clothes (Towel)' WHERE LOWER(missingstuffs)='face clothes';

DELETE FROM amenities;
# Import amenities from web interface

UPDATE amenities SET amenity_name='Pens' WHERE LOWER(amenity_name)='pen';
UPDATE amenities SET amenity_name='Pens' WHERE LOWER(amenity_name)='pens';
UPDATE amenities SET amenity_name='Bath Mat' WHERE LOWER(amenity_name)='bath mat';
UPDATE amenities SET amenity_name='Ice Bag' WHERE LOWER(amenity_name)='ice bag';
UPDATE amenities SET amenity_name='Garbage Bag' WHERE LOWER(amenity_name)='garbage bag';
UPDATE amenities SET amenity_name='Memo Pad (Note Book)' WHERE LOWER(amenity_name)='memo pad';
UPDATE amenities SET amenity_name='Toilet Paper' WHERE LOWER(amenity_name)='toilet paper';
UPDATE amenities SET amenity_name='Face Clothes (Towel)' WHERE LOWER(amenity_name)='face clothes';
