# hashup
Hashdeep Utility Program

## Purpose
Help compare and audit output files from hashdeep. Yes, hashdeep has an audit mode, but it can only compare a working directory against an existing hashdeep output file. I'm insterested in answering questions like, "what files were lost between these two hashdeep runs?" "What duplicate files exist within this single hashdeep output?" "What are the differences between these two directory structures?"

## Interesting queries:
Show me all files from a single hashdeep run that are duplicates over 100MB:
```sql
select o.*, o2.*
from file1 o
	join file1 o2 on o.md5 = o2.md5
where o.filename <> o2.filename
	and cast(o.size as NUMERIC) > 100000000
limit 10;
```

How many new files were added in file2 (a second run):
```
select count(*) as not_in_file1
from file2 f2
	left join file1 f on f.md5 = f2.md5
where f.md5 is null;
```

How many files were deleted in file2 (a second run):
```
select count(*) as not_in_file2
from file1 f
	left join file2 f2 on f.md5 = f2.md5
where f2.md5 is null;
```

Show me all files that moved in-between file1 and file2 scans:
```
select *
from file1 f
	join file2 f2 on f.md5 = f2.md5
where f.filename <> f2.filename
	-- with limit 10 this subquery is acceptable. without it, it's not.
	and not exists (
		select *
		from file2 f3
		where f3.filename = f.filename
	)
limit 10;
```

## developing
### running unit tests
```
python -m unittest discover
```
or
```
python -m unittest test.test_hashdeep_csv
```


## to-do
* prettier output for "only in file 2" mode
* ability to configure ignore patterns
* Use hashdeep header to determine what columns exist in the file
