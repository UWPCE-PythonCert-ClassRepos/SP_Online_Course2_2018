from iterator_2 import iterator_2

def test_iterator_2():
	qwerty = list(iterator_2(10, 30, 3))
	assert qwerty[-1] is 28