package require tcltest

source ../csv/hashdeep-csv.tcl

::tcltest::test parseCsv_createsDictionary {
} -setup {
} -body {
	set file1Md5 f441b34188a3a5e8ad0fcfa18eb81298
	set file1Sha1 fake-sha1
	set csvOutput "%%%% HASHDEEP-1.0
%%%% size,md5,sha1,filename
## Invoked from: /media/moo
## $ hashdeep -r -c md5 .
##
2761139,$file1Md5,$file1Sha1,/media/moo/file.txt
4034402,d3bd60842b030b94c168c2e730bb26e6,fake-sha1,/media/moo/file2.txt"
	
	set result [::hashdeepCsv::parseCsv $csvOutput]
	set file1 [dict get $result $file1Md5]
	return [expr {
		[dict get $file1 filename] == {/media/moo/file.txt}
		&& [dict get $file1 md5] == $file1Md5
		&& [dict get $file1 sha1] == $file1Sha1
	}]
} -cleanup {
} -result 1

::tcltest::test parseCsv_arbitraryColumns {
} -setup {
} -body {
	set file1Md5 f441b34188a3a5e8ad0fcfa18eb81298
	set csvOutput "%%%% HASHDEEP-1.0
%%%% md5,size,filename
## Invoked from: /media/moo
## $ hashdeep -r -c md5 .
##
$file1Md5,1234,/media/moo/file.txt
d3bd60842b030b94c168c2e730bb26e6,4567,/media/moo/file2.txt"
	
	set result [::hashdeepCsv::parseCsv $csvOutput]
	set file1 [dict get $result $file1Md5]
	return [expr {
		[dict get $file1 filename] == {/media/moo/file.txt}
		&& [dict get $file1 md5] == $file1Md5
	}]
} -cleanup {
} -result 1

::tcltest::test parseCsv_returnsErrorForInvalidOutput {
} -setup {
} -body {
	set file1Md5 f441b34188a3a5e8ad0fcfa18eb81298
	set csvOutput "%%%% BLAH
%%%% size,md5,sha1,filename"
	
	catch {::hashdeepCsv::parseCsv $csvOutput} result options
	return [dict get $options -code]
} -cleanup {
} -result 1

::tcltest::test parseCsv_outputMustContainMd5 {
} -setup {
} -body {
	set file1Md5 f441b34188a3a5e8ad0fcfa18eb81298
	set csvOutput "%%%% HASHDEEP-1.0
%%%% size,sha1,filename"
	
	catch {::hashdeepCsv::parseCsv $csvOutput} result options
	return [expr {
		[dict get $options -code] == 1
		&& [string match "*Arbitrary limitation*" [dict get $options -errorinfo]]
	}]
} -cleanup {
} -result 1

::tcltest::cleanupTests
