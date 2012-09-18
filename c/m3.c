#include <stdio.h>
#include <stdlib.h>

#define WIDTH 500
#define HEIGHT 500

void mandel(char* out, int width, int height, int maxIterations, double centerX, double centerY, double zoom) {
	int xi, yi;
	double x, y, a, b, oa;

    for (xi=0;xi<width;xi++) {
    	x = centerX + zoom * (xi - width / 2.0) / width;

		for (yi=0;yi<height;yi++) {
			unsigned n;
			int idx;

			y = centerY + zoom * (yi - height / 2.0) / height;

	        a = oa = 0;
	        b = 0;

	        for (n=0; n<maxIterations; n++) {
	        	double aS = a * a;
				double bS = b * b;

				if (aS + bS > 4) {
					break;
				}

	        	a = aS - bS + x;
	        	b = 2 * oa * b + y;
	        	oa = a;
	        }

	        idx = yi * height + xi;
	        if (n == maxIterations) {
	        	out[idx] = 0;
	        }
	        else {
	            out[idx] = 255 - (n * 10 % 255);
	        }
	    }
    }
}

int main(int argc, char *argv[]) {
	int itermax = atoi(argv[1]);		/* how many iterations to do	*/
	// double magnify=atof(argv[3]);		/* no magnification		*/
	// int res = atoi(argv[1]);
	char* out = (char*) malloc(WIDTH * HEIGHT);
	// mandelbrot(out, WIDTH, HEIGHT, itermax, -3, -2, 3.0);
	mandel(out, WIDTH, HEIGHT, itermax, -1.0, 0, 4.0);

	printf("P5\n%d %d\n255\n", WIDTH, HEIGHT);
	int i;
	for (i=0;i<WIDTH*HEIGHT;i++) {
		printf("%c", out[i]);
    }

	free(out);
}