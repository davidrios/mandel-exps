.PHONY: all
all: m2 m3 m3p m5 ocl_info

OPTS = -O2 -Wfatal-errors

.PHONY: m2
m2:
	gcc $(OPTS) m2.c -o ../bin/m2

.PHONY: m3
m3:
	gcc $(OPTS) m3.c -o ../bin/m3

.PHONY: m3p
m3p:
	gcc $(OPTS) -fopenmp m3.c -o ../bin/m3p

.PHONY: m5
m5:
	g++ $(OPTS) -lOpenCL m5.cpp -o ../bin/m5

.PHONY: ocl_info
ocl_info:
	g++ $(OPTS) -lOpenCL ocl_info.cpp -o ../bin/ocl_info