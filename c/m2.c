#include <stdio.h>
#include <stdlib.h>
#include "libm2.c"

int main(int argc, char *argv[]) {
	int itermax = atoi(argv[2]);		/* how many iterations to do	*/
	double magnify=atof(argv[3]);		/* no magnification		*/
	int res = atoi(argv[1]);
	char *out = (char*) malloc(255 + res * res);

	mandel(out, res, itermax, magnify);
	free(out);

	printf("%s", out);
}