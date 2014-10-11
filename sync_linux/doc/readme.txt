CREATE TABLE hash (
	id	INTEGER PRIMARY KEY AUTOINCREMENT,
	distribution_id	integer,
	filename	varchar(256),
	md5	char(32),
	sha1	char(40),
	sha256	char(64)
);

create table distribution(id integer primary key autoincrement, name varchar(64));