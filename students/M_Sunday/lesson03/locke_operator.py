
class Locke:

    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def operator():
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    with small_locke as locke:
        locke.move_boats_through(boats)

    with large_locke as locke:
        locke.move_boats_through(boats)


if __name__ == "__main__":
    operator()
