create table distribution(
	id				integer primary key AUTO_INCREMENT,
	name			varchar(64)
);

CREATE TABLE hash_origin (
	id				INTEGER PRIMARY KEY AUTO_INCREMENT,
	distribution_id	integer,
	filename		varchar(2048),
	md5				char(32),
	sha1			char(40),
	sha256			char(64)
);

create table hash_derive(
	id				INTEGER PRIMARY KEY AUTO_INCREMENT,
    pid				integer,
	distribution_id	integer,
	filename		varchar(2048),
	md5				char(32),
	sha1			char(40),
	sha256			char(64)
);