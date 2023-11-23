$fn = 50;
use <C:/gh/oomlout_opsc_version_3/pulley_gt2.scad>


difference() {
	union() {
		pulley_gt2(depth = 10, number_of_teeth = 20);
	}
	union();
}