all: great_circle_v1.c great_circle_v2.c

great_circle_v1.c: great_circle_v1.pyx great_circle_v1_setup.py
	python3 great_circle_v1_setup.py build_ext --inplace

great_circle_v2.c: great_circle_v2.pyx great_circle_v2_setup.py
	python3 great_circle_v2_setup.py build_ext --inplace
