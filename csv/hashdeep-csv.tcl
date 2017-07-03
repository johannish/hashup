namespace eval ::hashdeepCsv {}

proc ::hashdeepCsv::parseCsv {hashdeepOutputCsv} {
	set i 0
	set hashmap {}
	foreach line [split $hashdeepOutputCsv \n] {
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

