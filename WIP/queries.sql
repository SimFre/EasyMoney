
select * from autoinfo --where aiPattern='LOUGHBOROUGH PREMIER INN'

select * from imports

select * from cleanup

select * from categories -- where caParent=4 -- c where c.caName='Prylar'

select * from transactions where trId=3409

CREATE TABLE transactions (
	trId INTEGER,
	trDate TEXT(2000000000),
	trAccount INTEGER,
	trDescription TEXT(2000000000),
	trAmount REAL,
	trCategory INTEGER,
	trDestination TEXT(2000000000),
	trComment TEXT(2000000000),
	trMatch INTEGER,
	trIgnore TEXT(2000000000),
	trImport INTEGER,
	trDummy TEXT(2000000000),
	trOriginalCategory INTEGER,
	trOriginalDescription TEXT(2000000000),
	CONSTRAINT TRANSACTIONS_PK PRIMARY KEY (trId)
);

select
    trId,
    trDate,
    trAccount,
    trDescription,
    trAmount,
    trCategory,
    c.caName
from transactions
left join categories c on caId=trCategory
where
    trImport=?
order by trDate


CREATE TABLE imports (
	imId INTEGER,
	imTimestamp TEXT(2000000000),
	imAccount INTEGER,
	imComment TEXT(2000000000),
	imLines INTEGER,
	CONSTRAINT IMPORTS_PK PRIMARY KEY (imId)
);

select
    imId,
    imTimestamp,
    imAccount,
    imComment,
    imLines
from imports
order by imTimestamp asc



insert into autoinfo (aiType, aiPattern, aiCategory, aiDestination) values
('string', 'LOUGHBOROUGH PREMIER INN', 49, 'Tärande')


select
   i.*,
   (select count(*) as c from transactions t where t.trImport=i.imId) as c
from imports i

insert into cleanup (clFrom, clTo) values ('HAIR I HOV$S/ SARA', 'HAIR I HOVÅS/ SARA')



update transactions set trDestination=null, trCategory=null where trImport=38

-- Cleanup descriptions
update transactions
set
   trOriginalDescription=trDescription,
   trDescription=(select clTo from cleanup where clFrom=trDescription)
where
   trOriginalDescription is null
   and trDescription in(select clFrom from cleanup)

   
-- Auto categories #1
with 
update transactions	
set
   trCategory=(
      select coalesce(a1.aiCategory, a2.aiCategory)
      from transactions z
      left join autoinfo a1 on a1.aiType='string' and z.trDescription = a1.aiPattern
      left join autoinfo a2 on a2.aiType='regexp' and z.trDescription REGEXP a2.aiPattern
      where z.trImport=?
      limit 1
   )
where
   trCategory is null
   and trImport=39
   
   
-- Auto set categories
update transactions	
set
   trCategory=(
      select coalesce(a1.aiCategory, a2.aiCategory)
      from transactions z
      left join autoinfo a1 on a1.aiType='string' and z.trDescription = a1.aiPattern
      left join autoinfo a2 on a2.aiType='regexp' and z.trDescription REGEXP a2.aiPattern
      where z.trImport=?
      limit 1
   )
where
   trCategory is null
   and trImport=39

select
   trId, trImport, trAccount, trDate, trAmount, trDescription,		
   coalesce(a1.aiPattern, a2.aiPattern) as pattern,
   coalesce(a1.aiCategory, a2.aiCategory) as category
from transactions
left join autoinfo a1 on a1.aiType='string' and trDescription = a1.aiPattern
left join autoinfo a2 on a2.aiType='regexp' and trDescription REGEXP a2.aiPattern
where
   trImport=?

select trId, trDescription, trIgnore from transactions --- where trId=3408 or trIgnore='Y'

update Transactions set
	trOriginalDescription=case when trOriginalDescription is null then trDescription else trOriginalDescription end,
	"trDescription"='meep'
where trId = 1

update transactions set trCategory=null, trOriginalCategory=null, trOriginalDescription=null, trDescription='STACKSOCIAL' where trId=3408

select * from imports

insert into accounts(acId, acName, acCard, acService) values(0,'Bulk Import','Bulk Import','DefaultBulk')

-- delete from transactions where trImport > 27;
-- delete from imports where imId > 27;

select trId, trDate, trAccount, trDescription, trAmount, aiPattern, aiCategory
from transactions
join autoinfo on aiType='regex' and trDescription REGEXP '^ICA'
where trImport=4
order by trId desc

insert into cleanup (clFrom, clTo) values
('HARD ROCK CAF\', 'HARD ROCK CAFE')

select distinct trDescription, trDescription from transactions where
   trDescription like '%$%' or
   trDescription like '%#%' or
   trDescription like '%{%' or
   trDescription like '%}%' or
   trDescription like '%@%' or
   trDescription like '%''%'



INSERT INTO rawImport
(Datum, Tjänst, Beskrivning, Belopp, Kategori, Överkategori, Skuld, InUt, Period, CC, Kommentar)
VALUES('', '', '', '', '', '', '', '', '', '', '');
select * from rawImport
