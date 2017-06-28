#!/usr/bin/env tclsh

proc parseCsv {csvLines} {
	set i 0
	set hashmap {}
	foreach line $csvLines {
		set firstchar [string index $line 0]
		if {$firstchar == "%" || $firstchar == "#"} {
			continue
		}

		#if { $i > 100 } {
		#	break
		#}

		set parts [split $line ,]
		#TODO: get these names dynamically from the hashdeep header
		set size [lindex $parts 0]
		set md5 [lindex $parts 1]
		set sha1 [lindex $parts 2]
		set filename [lindex $parts 3]

		# The point is to compare two files, not a single one. Given that goal,
		# a dict key of one of the file's hashes is ideal. This will not be ideal for finding
		# duplicates within a single file.
		# although...
		#if {[dict exists $hashmap $md5] && $md5 != "45b47db11f92bf5fd98d41034e74c9eb"} {
		#	puts stderr "duplicate: $md5"
		#}
	
		#TODO: find a better way to create this dict
		#dict set hashmap $md5 "size $size md5 $md5 sha1 $sha1 filename $filename"
		dict set hashmap $md5 size $size
		dict set hashmap $md5 md5 $md5
		dict set hashmap $md5 sha1 $sha1
		dict set hashmap $md5 size $size
		dict set hashmap $md5 filename "$filename"

		incr i
	}

	return $hashmap
}

if {[llength $argv] != 2} {
	puts "usage: hashdeep-compare <file-one> <file-two>"
}
puts stderr "comparing: $argv"

set firstFile [lindex $argv 0]
set secondFile [lindex $argv 1]

set fp [open $firstFile r]
set firstLines [split [read $fp] \n]
close $fp

set fp [open $secondFile r]
set secondLines [split [read $fp] \n]
close $fp

set indexOne [parseCsv $firstLines] 
set indexTwo [parseCsv $secondLines] 

#puts "Name of hash (file1) is: [dict get [dict get $indexOne 89b337fd82777c2efdaabb11594d4dd5] filename]"

foreach hash [dict keys $indexTwo] {
	#puts "looking for $hash"
	set fileMetadata [dict get $indexTwo $hash]
	#puts "metadata| $fileMetadata"
	set filename [dict get $fileMetadata filename]
	if {[dict exists $indexOne $hash]} {
		#puts "in both files: $hash"
	} else {
		puts "only in file 2: $hash ($filename)"
	}
}
