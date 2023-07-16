-- give values to draw the rectangles for origin and destination
select
	nmregion,
	NbMonthWeek,
	-- Origin box drawing coordinates
	minOriLat::text || ' | ' || minOriLon as boxOriPoint1,
	minOriLat::text || ' | ' || maxOriLon as boxOriPoint2,
	maxOriLat::text || ' | ' || minOriLon as boxOriPoint3,
	maxOriLat::text || ' | ' || maxOriLon as boxOriPoint4,
	-- Destination drawing box coordinates
	minDesLat::text || ' | ' || minDesLon as boxDesPoint1,
	minDesLat::text || ' | ' || maxDesLon as boxDesPoint2,
	maxDesLat::text || ' | ' || minDesLon as boxDesPoint3,
	maxDesLat::text || ' | ' || maxDesLon as boxDesPoint4
from 
(
	select 
		nmregion,
		TO_CHAR( tstrip, 'W' )::integer as NbMonthWeek,
		max(vloriginlat) as maxOriLat,
		max(vloriginLon) as maxOriLon,
		min(vloriginlat) as minOriLat,
		min(vloriginLon) as minOriLon,
		max(vldestinationlat) as maxDesLat,
		max(vldestinationLon) as maxDesLon,
		min(vldestinationlat) as minDesLat,
		min(vldestinationLon) as minDesLon
	FROM tripsdb.tbtrips tt
	where idloadcontrol = 79 --1.2M rows loaded
	group by 1,2
) as t0