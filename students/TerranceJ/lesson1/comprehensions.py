import pandas as pd 
"""Conprehension Assignment
	written by Terrance J
"""

#COMPREHENSION ASSIGNMENT
def top_five():
	"""
	Returns the name and title of the top 5 tracks meeting loudness scores less than -5-0 and danceability scores greater than 0.8.

	"""
	music = pd.read_csv("featuresdf.csv")

	results = [(d,l,n,a) for d,l,n,a in zip(music.danceability,music.loudness, music.name,music.artists)]  

	new_results = []

	for i in results:
		if i[0] > 0.8:
			if i[1] < -5.0:
				new_results.append(i)

	new_results = sorted(new_results, reverse = True)

	top_five =  new_results[:5]

	return top_five


if __name__ == '__main__':
	print(top_five())

