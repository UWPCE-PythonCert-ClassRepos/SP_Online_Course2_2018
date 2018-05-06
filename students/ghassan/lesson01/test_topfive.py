from list_comp import top_5ive


def test_top_five():
    x = top_5ive()
    assert [
        ('21 Savage', 'Bank Account', 0.884, -8.228), 
        ('Bruno Mars', '24K Magic', 0.818, -4.282), 
        ('Bruno Mars', "That's What I Like", 0.853, -4.961), 
        ('Calvin Harris', 'Feels', 0.893, -3.105), 
        ('Drake', 'Fake Love', 0.927, -9.433)
        ] == x
