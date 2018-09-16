# ----------------------------------------------------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: Lesson_01
# DATE CREATED: 08/13/2018
# UPDATED:
# PURPOSE: Using Iterators and Generators
# DESCRIPTION:  Program accesses .csv file with music data and performs sorts for specific data based on assignment
# criteria. Uses nested comprehensions and the Pandas library to access .csv file.
# ----------------------------------------------------------------------------------------------------------------------


#  =============================================    SET UP    =======================================================
import pandas as pd  												# Import pandas library
from operator import itemgetter										# Function used for sorting list

music = pd.read_csv("featuresdf.csv")  								# Access .csv file in current directory
pd.set_option('display.expand_frame_repr', False)  					# Expand current display frame for viewing columns

print(music.head())  												# Display columns
print(music.describe(include='all'))  								# Analysis of .csv data via .describe function

#  ==================================================================================================================


#  ============================================    PROCESSING    ====================================================
print('\n' * 4)

# container of filtered values (zip list of only associated col/rows that met criteria)
top_five = [filter_val for filter_val in zip(music.name, music.artists, music.danceability, music.loudness) \
			if filter_val[2] > 0.8 and filter_val[3] < -5.0]


#  ==================================================================================================================


#  ==============================================    OUT-PUT    =====================================================
# sort container vals in descending order for print-out
final = sorted(top_five, key=itemgetter(2), reverse=True)[:5]

count = 1
print('{:^75}'.format('DANCEABLE SONGS\n'))
for i in final:
	print(count, '.)  ', end='')
	print('{:<40s} {:^10s} {:<10s} '.format(i[0], '  :::  ', i[1]))
	count += 1
#  ==================================================================================================================
