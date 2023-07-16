create database tripsdb;

drop table if exists tripsdb.TbLoadControl;

CREATE TABLE IF NOT EXISTS tripsdb.TbLoadControl (
  IdLoadControl serial4 PRIMARY key NOT NULL,
  NmFile VARCHAR(45) NOT NULL,
  TsLoadStart TIMESTAMP NOT NULL,
  TsLoadFinish TIMESTAMP NULL,
  NmLoadStatus VARCHAR(45) NOT NULL,
  TsLoadUpdate TIMESTAMP NULL
  );

drop table if exists tripsdb.tbtrips;

CREATE TABLE tripsdb.tbtrips (
	idtrips serial4 PRIMARY key NOT NULL,
	nmregion varchar(45) NULL,
	vloriginlat numeric(15, 13) NULL,
	vloriginlon numeric(15, 13) NULL,
	vldestinationlat numeric(15, 13) NULL,
	vldestinationlon numeric(15, 13) NULL,
	tstrip timestamp NULL,
	nmdatasource varchar(45) NULL,
	nboriginclustering int4 NULL,
	nbdestinationclustering int4 NULL,
	idloadcontrol int8
);
ALTER TABLE tripsdb.tbtrips ADD CONSTRAINT tbtrips_idloadcontrol_fkey FOREIGN KEY (idloadcontrol) REFERENCES tripsdb.tbloadcontrol(idloadcontrol);

