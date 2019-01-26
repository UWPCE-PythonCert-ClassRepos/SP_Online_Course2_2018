"""test to make sure generators have the right behavior"""

import generator_assignment as gm


def test_generate_increasing_ints():
    """tests generator works for 5 iterations and doubles results"""
    count = 0
    gen = gm.generate_increasing_ints(start=0, step=1)

    assert next(gen) == 0
    assert next(gen) == 1
    assert next(gen) == 3
    assert next(gen) == 6
    assert next(gen) == 10
    assert next(gen) == 15
    


 
