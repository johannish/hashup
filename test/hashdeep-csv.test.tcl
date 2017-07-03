package require tcltest

source ../csv/hashdeep-csv.tcl

::tcltest::test parseCsv_createsDictionary {
} -setup {
} -body {
	set file1Md5 f441b34188a3a5e8ad0fcfa18eb81298
	set csvOutput "%%%% HASHDEEP-1.0
%%%% size,md5,sha1,filename
## Invoked from: /media/moo
## $ hashdeep -r -c md5 .
##
2761139,$file1Md5,fake-sha1,/media/moo/file.txt
4034402,d3bd60842b030b94c168c2e730bb26e6,fake-sha1,/media/moo/file2.txt"
	
	set result [::hashdeepCsv::parseCsv $csvOutput]
	set file1 [dict get $result $file1Md5]
	return [expr {
		[dict get $file1 filename] == {/media/moo/file.txt}
		&& [dict get $file1 md5] == $file1Md5
	}]
} -cleanup {
} -result 1

::tcltest::cleanupTests
