$fn = 30;


lobe_number = 30;
radius_offset = 1.5;
radius_pin = 6/2;

cycloid(lobe_number, radius_offset, radius_pin);


module cycloid (lobe_number, radius_offset, radius_pin){
	//hypotrochoidBandFast(n, r, thickness, r_off)
	hypotrochoidBandFast(lobe_number, radius_offset, 6, radius_pin);
}


module hypotrochoidBandFast(n, r, thickness, r_off) {
    
    pi = 3.14159265;

	R = r*n;
	d = r;

	// set to 1 for normal size cylinders.  this will leave a tiny cusp in some cases that does
	// not blend in to cylinders.  see below for details.  make hideCuspFactor larger to scale up
	// the cylinders slightly. 1.01 seems to work OK.
	hideCuspFactor = 1.01;

	// dth stands for dtheta - i.e. a small change of the angle "theta"
	// there are 14 intermediate points on the curve, so a wedge is
	// divided into 14 + 1 = 15.  You may be tempted to change this, but it really is 15.
	dth = 360/n/15;

	// X points on base hypotrochoid
	xbStart = (R-r) + d;
	xbEnd =  (R-r)*cos(360/n) + d*cos((R-r)/r*360/n);	

	// Instead of an array and a for-loop we just hard-code these 
	// intermediate points, this if for X coords on the base hypocycloid.
	//
	xb1 = (R-r)*cos(dth*1) + d*cos((R-r)/r*dth*1);
	xb2 = (R-r)*cos(dth*2) + d*cos((R-r)/r*dth*2);
	xb3 = (R-r)*cos(dth*3) + d*cos((R-r)/r*dth*3);
	xb4 = (R-r)*cos(dth*4) + d*cos((R-r)/r*dth*4);
	xb5 = (R-r)*cos(dth*5) + d*cos((R-r)/r*dth*5);
	xb6 = (R-r)*cos(dth*6) + d*cos((R-r)/r*dth*6);
	xb7 = (R-r)*cos(dth*7) + d*cos((R-r)/r*dth*7);	
	xb8 = (R-r)*cos(dth*8) + d*cos((R-r)/r*dth*8);
	xb9 = (R-r)*cos(dth*9) + d*cos((R-r)/r*dth*9);
	xb10 = (R-r)*cos(dth*10) + d*cos((R-r)/r*dth*10);
	xb11 = (R-r)*cos(dth*11) + d*cos((R-r)/r*dth*11);
	xb12 = (R-r)*cos(dth*12) + d*cos((R-r)/r*dth*12);
	xb13 = (R-r)*cos(dth*13) + d*cos((R-r)/r*dth*13);
	xb14 = (R-r)*cos(dth*14) + d*cos((R-r)/r*dth*14);	

	// Y points on base hypotrochoid
	ybStart = 0;
	ybEnd =   (R-r)*sin(360/n) - d*sin((R-r)/r*360/n);

	// Instead of an array and a for-loop we just hard-code these 
	// intermediate points, this if for Y coords on the base hypocycloid.
	//
	yb1 =  (R-r)*sin(dth*1) - d*sin((R-r)/r*dth*1);
	yb2 =  (R-r)*sin(dth*2) - d*sin((R-r)/r*dth*2);
	yb3 =  (R-r)*sin(dth*3) - d*sin((R-r)/r*dth*3);
	yb4 =  (R-r)*sin(dth*4) - d*sin((R-r)/r*dth*4);
	yb5 =  (R-r)*sin(dth*5) - d*sin((R-r)/r*dth*5);
	yb6 =  (R-r)*sin(dth*6) - d*sin((R-r)/r*dth*6);
	yb7 =  (R-r)*sin(dth*7) - d*sin((R-r)/r*dth*7);
	yb8 =  (R-r)*sin(dth*8) - d*sin((R-r)/r*dth*8);
	yb9 =  (R-r)*sin(dth*9) - d*sin((R-r)/r*dth*9);
	yb10 =  (R-r)*sin(dth*10) - d*sin((R-r)/r*dth*10);
	yb11 =  (R-r)*sin(dth*11) - d*sin((R-r)/r*dth*11);
	yb12 =  (R-r)*sin(dth*12) - d*sin((R-r)/r*dth*12);
	yb13 =  (R-r)*sin(dth*13) - d*sin((R-r)/r*dth*13);
	yb14 =  (R-r)*sin(dth*14) - d*sin((R-r)/r*dth*14);

	// Now we do the offset points.  The tangent to the
	// hypotrochoid is [dx/dtheta, dy/dtheta].
	// We take the tangent, normalize it, rotate it, and scale it 
	// to get the offsets in X and Y coords.
	
	// X offset points
	xfStart = 0;
	xfEnd =  r_off*cos(360/n - 90);

	// hard-coded offset points for X
	//
	xf1 = (R-r)*cos(dth*1) - r*cos( (R-r)/r*dth*1) * (R-r)/r ;
	xf2 = (R-r)*cos(dth*2) - r*cos( (R-r)/r*dth*2) * (R-r)/r ;
	xf3 = (R-r)*cos(dth*3) - r*cos( (R-r)/r*dth*3) * (R-r)/r ;
	xf4 = (R-r)*cos(dth*4) - r*cos( (R-r)/r*dth*4) * (R-r)/r ;
	xf5 = (R-r)*cos(dth*5) - r*cos( (R-r)/r*dth*5) * (R-r)/r ;
	xf6 = (R-r)*cos(dth*6) - r*cos( (R-r)/r*dth*6) * (R-r)/r ;
	xf7 = (R-r)*cos(dth*7) - r*cos( (R-r)/r*dth*7) * (R-r)/r ;	
	xf8 = (R-r)*cos(dth*8) - r*cos( (R-r)/r*dth*8) * (R-r)/r ;
	xf9 = (R-r)*cos(dth*9) - r*cos( (R-r)/r*dth*9) * (R-r)/r ;
	xf10 = (R-r)*cos(dth*10) - r*cos( (R-r)/r*dth*10) * (R-r)/r ;
	xf11 = (R-r)*cos(dth*11) - r*cos( (R-r)/r*dth*11) * (R-r)/r ;
	xf12 = (R-r)*cos(dth*12) - r*cos( (R-r)/r*dth*12) * (R-r)/r ;
	xf13 = (R-r)*cos(dth*13) - r*cos( (R-r)/r*dth*13) * (R-r)/r ;
	xf14 = (R-r)*cos(dth*14) - r*cos( (R-r)/r*dth*14) * (R-r)/r ;	

	// Y offset points
	yfStart = r_off;
	yfEnd =  r_off*sin(360/n - 90);

	yf1 =  (R-r)*sin(dth*1) + r*sin( (R-r)/r*dth*1) * (R-r)/r ;
	yf2 =  (R-r)*sin(dth*2) + r*sin( (R-r)/r*dth*2) * (R-r)/r ;
	yf3 =  (R-r)*sin(dth*3) + r*sin( (R-r)/r*dth*3) * (R-r)/r ;
	yf4 =  (R-r)*sin(dth*4) + r*sin( (R-r)/r*dth*4) * (R-r)/r ;
	yf5 =  (R-r)*sin(dth*5) + r*sin( (R-r)/r*dth*5) * (R-r)/r ;
	yf6 =  (R-r)*sin(dth*6) + r*sin( (R-r)/r*dth*6) * (R-r)/r ;
	yf7 =  (R-r)*sin(dth*7) + r*sin( (R-r)/r*dth*7) * (R-r)/r ;
	yf8 =  (R-r)*sin(dth*8) + r*sin( (R-r)/r*dth*8) * (R-r)/r ;
	yf9 =  (R-r)*sin(dth*9) + r*sin( (R-r)/r*dth*9) * (R-r)/r ;
	yf10 =  (R-r)*sin(dth*10) + r*sin( (R-r)/r*dth*10) * (R-r)/r ;
	yf11 =  (R-r)*sin(dth*11) + r*sin( (R-r)/r*dth*11) * (R-r)/r ;
	yf12 =  (R-r)*sin(dth*12) + r*sin( (R-r)/r*dth*12) * (R-r)/r ;
	yf13 =  (R-r)*sin(dth*13) + r*sin( (R-r)/r*dth*13) * (R-r)/r ;
	yf14 =  (R-r)*sin(dth*14) + r*sin( (R-r)/r*dth*14) * (R-r)/r ;

	m1 = sqrt(xf1*xf1 + yf1*yf1)/r_off;
	m2 = sqrt(xf2*xf2 + yf2*yf2)/r_off;
	m3 = sqrt(xf3*xf3 + yf3*yf3)/r_off;
	m4 = sqrt(xf4*xf4 + yf4*yf4)/r_off;
	m5 = sqrt(xf5*xf5 + yf5*yf5)/r_off;
	m6 = sqrt(xf6*xf6 + yf6*yf6)/r_off;
	m7 = sqrt(xf7*xf7 + yf7*yf7)/r_off;
	m8 = sqrt(xf8*xf8 + yf8*yf8)/r_off;
	m9 = sqrt(xf9*xf9 + yf9*yf9)/r_off;
	m10 = sqrt(xf10*xf10 + yf10*yf10)/r_off;
	m11 = sqrt(xf11*xf11 + yf11*yf11)/r_off;
	m12 = sqrt(xf12*xf12 + yf12*yf12)/r_off;
	m13 = sqrt(xf13*xf13 + yf13*yf13)/r_off;
	m14 = sqrt(xf14*xf14 + yf14*yf14)/r_off;

// Now that we have the points, we make a polygon and extrude it.
    union(){}
		for  ( i = [0:n-1] ) {
			rotate([0,0, 360/n*i]) {

					// the first point in the polygon is moved slightly off the origin
					polygon(points= [
						[-R/20 * cos(360/n/2) , -R/20 * sin(360/n/2)],
						[xbStart, ybStart],
						[xbStart + xfStart, ybStart + yfStart], 

						[xb1 + xf1/m1, yb1 + yf1/m1], 
						[xb2 + xf2/m2, yb2 + yf2/m2], 
						[xb3 + xf3/m3, yb3 + yf3/m3], 
						[xb4 + xf4/m4, yb4 + yf4/m4], 
						[xb5 + xf5/m5, yb5 + yf5/m5], 
						[xb6 + xf6/m6, yb6 + yf6/m6], 
						[xb7 + xf7/m7, yb7 + yf7/m7], 
						[xb8 + xf8/m8, yb8 + yf8/m8], 
						[xb9 + xf9/m9, yb9 + yf9/m9], 
						[xb10 + xf10/m10, yb10 + yf10/m10], 
						[xb11 + xf11/m11, yb11 + yf11/m11], 
						[xb12 + xf12/m12, yb12 + yf12/m12], 
						[xb13 + xf13/m13, yb13 + yf13/m13], 
						[xb14 + xf14/m14, yb14 + yf14/m14], 

						[xbEnd + xfEnd, ybEnd + yfEnd],
						[xbEnd, ybEnd]],
						paths = [[0,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]],
						convexity = 10);

			// If you look at just the wedge extruded above, without the cylinders below,
			// you can see a small cusp as the band radius gets larger.  The radius of 
			// the cylinder is manually increased a slight bit so that the cusp is contained 
			// within the cylinder.  With unlimited resolution, the cusp and cylinder would
			// blend together perfectly (I think), but this workaround is needed because
			// we are only using piecewise linear approximations to these curves.
			
			translate([xbStart, ybStart, 0])
				//cylinder(r = hideCuspFactor*r_off, h = thickness, center = true);
				circle(r = hideCuspFactor*r_off);
        
	    } //end rotate

    } //end for




} // end module hypotrochoidBandFast
//=========================================== 

