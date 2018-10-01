
class Locke():
    
    def __init__(self, max_boats):
        self.max_boats = max_boats
        
    def move_boats_through(self, boats):
        if self.max_boats < boats:
            raise ValueError("Too many boats for this locke!  Maximum boats: {}".format(boats))
        else:    
            print("Front Door Operation: Closing the doors.")
            print("Front Door Operation: Restarting the pumps.")
    
    def __enter__(self):
        print("Front Door Operation: Stopping the pumps.")
        print("Front Door Operation: Opening the doors.")
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handle_error = False
        
        if exc_type == ValueError:
            print('({}, {}, {})'.format(exc_type, exc_val, exc_tb))
            
            self.handle_error = True
            
            return self.handle_error
        
        print("Back Door Operation: Stopping the pumps.")
        print("Back Door Operation: Opening the doors.")
        print("Back Door Operation: Closing the doors.")
        print("Back Door Operation: Restarting the pumps.")
        
        return self.handle_error

if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8
    
    print('Too many boats through a small locke will raise an exception')
    with small_locke as locke:
        locke.move_boats_through(boats=boats)

    print('\nA lock with sufficient capacity can move boats without incident.')
    with large_locke as locke:
        locke.move_boats_through(boats=boats)