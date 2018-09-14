# ----------------------------------------------------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: Closures.py
# DATE CREATED: 09/13/2018
# UPDATED: N/A
# PURPOSE: PYTHON 220 Lesson 02
# DESCRIPTION: Program exemplifies aspects of Python's closures (a function defined within another function) that has
# 'memory' of variables from the outer function without having the actual variables present in RAM. For this program
# the main() function calls the outer function, closure_part_one(), which takes the .csv variable as an argument
# passed in to it. The function, filters the .csv file for music tracks over 0.8 (tempo) and then falls through
# to the nested function, closure_part_two which 'remembers' the data from the outer scope and formats/prints it.
# ------------------------------------------------------------------------------------------------------------------

#  =============================================    SET UP    =======================================================
import pandas as f
space = '\n' 																	# spacing between prints
decor = "-" * 100																# line separator for printing
#  ============================================    PROCESSING    ====================================================


def closure_part_one(music):													# outer scope with access to .csv data
	print(space)
	print('{:>55}'.format('HYPE SONGS'))													# Header for data
	print(decor)
	over_point_eight = ([(artist, name, energy) for artist, name, energy
						in zip(music.artists, music.name, music.energy) if energy > 0.8])  # filter/generator

	def closure_part_two():																	# nested function
		count_next = 1
		for i in over_point_eight:
			if count_next <= 9:  										# Adjusts spaces based on single/double-digits
				print(count_next, ' .)  ', end='')
				print('{:>20s} {:^25f} {:<5s} '.format(i[0], i[2], i[1]))
				count_next += 1
			else:
				print(count_next, '.)  ', end='')
				print('{:>20s} {:^25f} {:<15s} '.format(i[0], i[2], i[1]))
				count_next += 1
	return closure_part_two()


def main():
	music = f.read_csv("featuresdf.csv")
	closure_part_one(music)
#  ==============================================    OUT-PUT    =====================================================


if __name__ == '__main__':
	main()
