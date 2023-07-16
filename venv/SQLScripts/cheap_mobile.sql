-- looks like all regions =)
select 
	nmregion,
	count(*) as NbRows
from tripsdb.tbtrips
where nmdatasource = 'cheap_mobile'
group by 1