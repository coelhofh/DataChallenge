-- ordering the region by number of rows 
-- to answer the top 2 regions just uncomment the where clause =)
select * from (
	select 
		nmregion,
		nbRows,
		row_number() over(order by nbrows desc) as rn
	from (
		select 
			nmregion,
			count(*) as NbRows
		from tripsdb.tbtrips
		group by 1
	) t0
) t1
--where rn < 3


-- ordering the datasource by number of rows 
-- to answer the last datasource just uncomment the where clause =)
select * from (
	select 
		nmdatasource,
		nbRows,
		row_number() over(order by nbrows asc) as rn
	from (
		select 
			nmdatasource,
			count(*) as NbRows
		from tripsdb.tbtrips
		group by 1
	) t0
) t1
--where rn = 1