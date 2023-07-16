select 
	nmregion,
	nboriginclustering,
	nbdestinationclustering,
	extract(hour from tstrip) as nbhour,
	count(*) as nbtotaltrips
FROM tripsdb.tbtrips
where idloadcontrol = 79 --1.2M rows loaded 
group by 1,2,3,4
order by nmregion, nbhour asc
