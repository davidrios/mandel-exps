#include <iostream>
#include <sstream>
#include <CL/cl.hpp>

using namespace cl;


void die(STRING_CLASS msg, cl_int errCode) {
	std::cerr << std::endl << msg << errCode << std::endl;
	exit(errCode);
}


int main(int argc, char* argv[]) {
	cl_int retCode;

	// get platforms
	VECTOR_CLASS<Platform> platforms;

	retCode = Platform::get(&platforms);
	if (retCode != CL_SUCCESS)
		die("failed to get platforms: ", retCode);

	if (platforms.size() > 1)
		std::cerr << "more than one platform found, using first: ";
	else
		std::cerr << "using platform: ";

	Platform & platform = platforms[0];

	STRING_CLASS info;
	retCode = platform.getInfo(CL_PLATFORM_NAME, &info);
	if (retCode != CL_SUCCESS)
		die("failed to get platform info: ", retCode);
	std::cerr << info << std::endl;

	// get devices
	VECTOR_CLASS<Device> devices;
	retCode = platform.getDevices(CL_DEVICE_TYPE_ALL, &devices);
	if (retCode != CL_SUCCESS)
		die("failed to get devices: ", retCode);

	// create context
	Context context = Context(devices, NULL, NULL, NULL, &retCode);
	if (retCode != CL_SUCCESS)
		die("unable to create context: ", retCode);
}