#!/usr/bin/env tclsh

package require Tcl 8.5
package require tcltest

::tcltest::configure -file {"*.test.tcl"} -notfile {}
::tcltest::runAllTests
