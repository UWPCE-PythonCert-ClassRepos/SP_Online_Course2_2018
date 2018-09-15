# ----------------------------------------------------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: Lesson_02.py
# DATE CREATED: 08/31/2018
# UPDATED: 09/07/2018
# PURPOSE: Utilizing generators in data manipulation
# DESCRIPTION: Program utilizes .csv spreadsheet to obtain data-sets to be evaluated a generator object to
# evaluate if certain criteria are met within the data, and then displays the desired data if it is found.
# ------------------------------------------------------------------------------------------------------------------

#  =============================================    SET UP    =======================================================
import pandas as f															# import pandas to manage tabular data

music = f.read_csv("featuresdf.csv")										# assign .csv file to 'music'
f.set_option('display.expand_frame_repr', False)							# pandas option for displaying results
spaces = '\n' * 2															# spacing between prints
decor = "----------------------------------------------------------"		# decorator for printing
header = ' ' * 20 + 'FAVORITE ARTIST\n'										# header display
count = 1																	# display incremental numbering

#  ============================================    PROCESSING    ====================================================


def csv_data_generator(data):								# generator yields iterables from generator obj fave_trx,
	for found in data:
		yield found


fave_trx = (filter_val for filter_val in zip(music.name, music.artists, music.danceability)
				if filter_val[1] == 'Ed Sheeran')

#  ==============================================    OUT-PUT    =====================================================
print(spaces, header, decor)												# spacing and header decorations
data_set = csv_data_generator(fave_trx)										# create variable for looping
for i in data_set:															# for row in data
	print(count, '.)  ', end='')											# print number (no newline)
	print('{:<20s} {:^15s} {:>15s} '.format(i[0], '  :::   ', i[1]))		# print name/artist and space correctly
	count += 1																# increment count
print(decor)																# print lines
