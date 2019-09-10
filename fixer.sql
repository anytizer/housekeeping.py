-- Pre-import
update missing set  `Associates Name`=trim(`Associates Name`)
update missing set  `Room Number `=trim(`Room Number `) 
update missing set  `Missing Stuff`=trim(`Missing Stuff`)
update missing set  `Area Not Cleaned`=trim(`Area Not Cleaned`)
update missing set  `Remarks`=trim(`Remarks`)

-- Delete erraneous entries
DELETE FROM missing WHERE missingstuffs='' AND anc='' AND remarks='';

UPDATE missing SET missingstuffs=UPPER(missingstuffs);

UPDATE missing SET missingstuffs='Pens' WHERE UPPER(missingstuffs)='pen';
UPDATE missing SET missingstuffs='Pens' WHERE UPPER(missingstuffs)='pens';
UPDATE missing SET missingstuffs='Bath Mat' WHERE UPPER(missingstuffs)='bath mat';
UPDATE missing SET missingstuffs='Ice Bag' WHERE UPPER(missingstuffs)='ice bag';
UPDATE missing SET missingstuffs='Garbage Bag' WHERE UPPER(missingstuffs)='garbage bag';
UPDATE missing SET missingstuffs='Memo Pad (Note Book)' WHERE UPPER(missingstuffs)='memo pad';
UPDATE missing SET missingstuffs='Toilet Paper' WHERE UPPER(missingstuffs)='toilet paper';
UPDATE missing SET missingstuffs='Face Clothes (Towel)' WHERE UPPER(missingstuffs)='face clothes';

UPDATE missing SET missingstuffs=UPPER(missingstuffs);

DELETE FROM amenities;
-- Now, import amenities from web interface, that copies, creates IDs

UPDATE amenities SET amenity_name='Pens' WHERE UPPER(amenity_name)='pen';
UPDATE amenities SET amenity_name='Pens' WHERE UPPER(amenity_name)='pens';
UPDATE amenities SET amenity_name='Bath Mat' WHERE UPPER(amenity_name)='bath mat';
UPDATE amenities SET amenity_name='Ice Bag' WHERE UPPER(amenity_name)='ice bag';
UPDATE amenities SET amenity_name='Garbage Bag' WHERE UPPER(amenity_name)='garbage bag';
UPDATE amenities SET amenity_name='Memo Pad (Note Book)' WHERE UPPER(amenity_name)='memo pad';
UPDATE amenities SET amenity_name='Toilet Paper' WHERE UPPER(amenity_name)='toilet paper';
UPDATE amenities SET amenity_name='Face Clothes (Towel)' WHERE UPPER(amenity_name)='face clothes';
