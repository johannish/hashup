namespace eval ::hashdeepCsv {}

proc ::hashdeepCsv::parseCsv {hashdeepOutputCsv} {
	set hashmap {}
	set lines [split $hashdeepOutputCsv \n]

	if {![string match "%%%% HASHDEEP*" [lindex $lines 0]]} {
		error "Invalid input file: found [lindex $lines 0] at line 1, expected '%%%% HASHDEEP...'";
	}

	set columnInfo [regsub {^%%%% } [lindex $lines 1] {}]
	set columns [split $columnInfo ,]
	if {[lsearch $columns "md5"] < 0} {
		error "Arbitrary limitation of this program: each csv line must contain an md5 hash"
	}

	set runPath [regsub {^## Invoked from: } [lindex $lines 2] {}]

	foreach line $lines {
		set firstchar [string index $line 0]
		if {$firstchar == "%" || $firstchar == "#"} {
			continue
		}

		set parts [split $line ,]
		set keyValPairs {}

		set columnCountExceptLast [expr {[llength $columns] -1}]
		for {set i 0} {$i < $columnCountExceptLast} {incr i} {
			dict append keyValPairs [lindex $columns $i] [lindex $parts $i]
		}

		# Hackish way to handle filenames with commas in them (reconstructing filename)
		set filepath [join [lrange $parts $columnCountExceptLast end] ","]

		set filenameStartIndex [expr {[string last [file separator] $filepath]} + 1]
		set filename [string range $filepath $filenameStartIndex end]
		set relativeFilepath [regsub "^$runPath[file separator]" $filepath {}]
		set relativeFileDir [string replace $relativeFilepath [string last "$filename" $relativeFilepath] end]

		dict append keyValPairs filepath $filepath
		dict append keyValPairs filename $filename
		dict append keyValPairs relativeDir $relativeFileDir

		dict set hashmap [dict get $keyValPairs md5] $keyValPairs
	}

	return $hashmap
}

