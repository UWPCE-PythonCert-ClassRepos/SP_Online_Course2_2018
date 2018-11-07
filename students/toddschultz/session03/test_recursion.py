from recursion import rec

def test_rec():
	assert rec(0) == 1
	assert rec(1) == 1
	assert rec(5) == 120
	assert rec(7) == 5040
	assert rec(10) == 3628800