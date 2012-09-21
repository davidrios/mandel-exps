#include <stdio.h>

#define WIDTH 800
#define HEIGHT WIDTH

__global__ void kernel(uchar4 * pbo, double centerX, double centerY,
					   double zoom, unsigned maxIterations) {
	// Calculate the relative thread identifiers
	int x = blockIdx.x * blockDim.x + threadIdx.x;
	int y = blockIdx.y * blockDim.y + threadIdx.y;
	// Calculate the pixel index for this thread
	unsigned index = y * WIDTH + x;
	// Find the top left C value based on the center
	double startX = centerX - WIDTH/2/zoom;
	double startY = centerY - HEIGHT/2/zoom;
	// Calculate the C value for this thread
	double cReal = startX + x/zoom;
	double cImaginary = startY + y/zoom;
	// Begin Mandelbrot
	// Much of this code is the same as openMP
	double realZ = cReal;
	double imaginaryZ = cImaginary;
	double imaginarySquared;
	double realSquared;
	if(index < WIDTH*HEIGHT) {  
		unsigned n;
		for(n=0; n<maxIterations; n++) {
			realSquared = realZ*realZ;
			imaginarySquared = imaginaryZ*imaginaryZ;
			// Determine distance of Z from the origin of the complex plane'
			//simplified from sqrt(realZ*realZ + imaginaryZ*imaginary) > 2
			if (realSquared + imaginarySquared > 4)
				break;
			// Calculate z= z^2 + C
			// See: http:warp.povusers.org/Mandelbrot/ for simplification of function
			imaginaryZ = 2*realZ*imaginaryZ + cImaginary;
			realZ = realSquared - imaginarySquared + cReal;
		}
		if (n == maxIterations)
			1;
			// sprintf(&pbo[index], "%c", 0);
		else
			2;
			// pbo[index] = 255 - (n * 10 % 255);
	}
}

// Chop up the screen into 8x8 pixel sections
// Spawn a thread for each pixel
extern const int blockWidth = 8;
extern const int blockHeight = 8;
extern const int numBlocksWidth = WIDTH/blockWidth;
extern const int numBlocksHeight = HEIGHT/blockHeight;
// Declare the cuda dimension parameters
extern dim3 blockSize(blockWidth, blockHeight);
extern dim3 numBlocks(numBlocksWidth, numBlocksHeight);
extern "C" void runCuda(uchar4* pos, unsigned maxIterations, double zoom,
						double startX, double startY) {
	// Allocate memory to store the color palette
	uchar4 * d_palette;
	cudaMalloc(&d_palette, sizeof(uchar4)*(maxIterations+1));
	// cudaMemcpy(d_palette, palette, sizeof(uchar4)*(maxIterations+1), 
	// cudaMemcpyHostToDevice);
	// Call the kernel
	kernel<<<numBlocks,blockSize>>>(pos, startX, startY, zoom, maxIterations);
	// Deallocate the palette memory
	// cudaFree(d_palette);
}

int main(int argc, char *argv[]) {
	uchar4* pos = NULL;
	int itermax = atoi(argv[1]);
	runCuda(pos, itermax, 3, -1, 0);
}