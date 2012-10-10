#include <iostream>
#include <CL/cl.hpp>

using namespace cl;


void die(STRING_CLASS msg) {
	std::cerr << std::endl << msg << std::endl;
	exit(1);
}


int main(int argc, char* argv[]) {
	cl_int retCode;

	// get platforms
	const cl_platform_info PLATFORM_INFOS[] = {
		CL_PLATFORM_NAME,
		CL_PLATFORM_VENDOR,
		CL_PLATFORM_PROFILE,
		CL_PLATFORM_VERSION
	};
	VECTOR_CLASS<Platform> platforms;

	retCode = Platform::get(&platforms);
	if (retCode != CL_SUCCESS)
		die("failed to get platforms");

	std::cout << "platforms found: " << platforms.size() << std::endl;
	for (uint i = 0; i < platforms.size(); i++) {
		std::cout << "platform " << i+1 << ": ";
		for (uint j = 0; j < (sizeof(PLATFORM_INFOS) / sizeof(cl_platform_info)); j++) {
			STRING_CLASS info;
			retCode = platforms[i].getInfo(PLATFORM_INFOS[j], &info);
			if (retCode != CL_SUCCESS)
				die("failed to get platform info");
			std::cout << info << " ";
		}
		std::cout << std::endl;

		// get devices
		const cl_device_info DEVICE_INFOS[] = {
			CL_DEVICE_NAME,
			CL_DEVICE_VENDOR,
			CL_DEVICE_PROFILE,
			CL_DEVICE_VERSION,
			CL_DRIVER_VERSION,
			CL_DEVICE_OPENCL_C_VERSION
		};
		VECTOR_CLASS<Device> devices;

		retCode = platforms[i].getDevices(CL_DEVICE_TYPE_ALL, &devices);
		if (retCode != CL_SUCCESS)
			die("  failed to get devices");

		std::cout << "  devices found: " << devices.size() << std::endl;
		for (uint j = 0; j < devices.size(); j++) {
			std::cout << "  device " << j+1 << ": ";
			for (uint k = 0; k < (sizeof(DEVICE_INFOS) / sizeof(cl_device_info)); k++) {
				STRING_CLASS info;
				retCode = devices[j].getInfo(DEVICE_INFOS[k], &info);
				if (retCode != CL_SUCCESS)
					die("  failed to get device info");
				std::cout << info << " ";
			}

			cl_ulong memSize;
			retCode = devices[j].getInfo(CL_DEVICE_GLOBAL_MEM_SIZE, &memSize);
			if (retCode != CL_SUCCESS)
				die("  failed to get device info");
			std::cout << "GlobalMemSize:" << memSize / 1024 / 1024 << "MB ";

			retCode = devices[j].getInfo(CL_DEVICE_LOCAL_MEM_SIZE, &memSize);
			if (retCode != CL_SUCCESS)
				die("  failed to get device info");
			std::cout << "LocalMemSize:" << memSize / 1024 << "KB ";

			std::cout << std::endl;
		}
	}
}