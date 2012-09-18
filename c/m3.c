void mandelbrot(int WIDTH, int HEIGHT, int maxIterations, double startX, double startY, double zoom) {
	// Divide the screen into N equal sections and
	// have N cores calculate each respective portion
	#pragma omp parallel for private(complexReal, complexImaginary) schedule(dynamic)
		for (x=0;x<WIDTH;x++) {
			// Step through each pixel on the x axis
			// Calculate the real part of the complex number represented 
			// by all of the pixles with this x value
			complexReal = startX + x*zoom;
			int y;
			for (y=0;y<HEIGHT;y++) {
				// Calculate the imaginary part of the complex number
				complexImaginary = startY - y*zoom;
				// Setup initial Z value based on the complex number chosen
				double realZ = complexReal;
				double imaginaryZ = complexImaginary;
				int neverDiverges = 1; // bool
				unsigned n;
				// Calculate Zn for 1<n<maxIterations
				for (n=0; n<maxIterations; ++n)
				{
					double imaginarySquared = imaginaryZ*imaginaryZ;
					double realSquared = realZ*realZ;
					// simplified sqrt(realZ*realZ + imaginaryZ*imaginary) > 2
					if (realSquared + imaginarySquared > 4) {
						// Must diverge to infinity
						neverDiverges = 0;
						break;
					}
					imaginaryZ = 2*realZ*imaginaryZ + complexImaginary;
					realZ = realSquared - imaginarySquared + complexReal;
				}
				if ( neverDiverges ) {
					// Complex number associated with pixel (x,y) 
					// does not diverge to Infinity for set
					// Draw it black
					putpixel(x, y, black);
				} else {
					// Diverges... pick a color for it based on how 
					// quickly it diverges, ie n iterations
					putpixel(x, y, colors[n]);
				}
			}
		}
}