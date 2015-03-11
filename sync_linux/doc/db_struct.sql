create table distribution(
	id				integer primary key AUTO_INCREMENT,
	name			varchar(64)，
	store_root		varchar(128)
);

CREATE TABLE t_hashdata (
	id				INTEGER PRIMARY KEY AUTO_INCREMENT,
	pid				integer,
	distribution_id	integer,
	filename		varchar(2048),
	md5				char(32),
	sha1			char(40),
	sha256			char(64),
	filesize		bigint(20),
	filetype		varchar(1024),
	add_time		timestamp
);
