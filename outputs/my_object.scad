$fn = 50;
use <c:/Program Files/OpenSCAD/libraries/MCAD/involute_gears.scad>


difference() {
	union() {
		gear(backlash = 0, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 0.2000000000, diametral_pitch = 0.5333330000, flat = false, gear_thickness = 6, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 28, rim_thickness = 6, rim_width = 0, twist = 0);
	}
	union();
}