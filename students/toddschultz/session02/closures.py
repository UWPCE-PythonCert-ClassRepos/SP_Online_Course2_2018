import pandas as pd
music = pd.read_csv("featuresdf.csv")

def energy_closure():
    ''' Using the same data set, write a closure to capture high energy tracks. We will define high energy tracks as anything over 0.8. 
    Submit your code and the tracks it finds, artist name, track name and energy value.'''
    songs = [x for x in zip(music.energy, music.artists, music.name) if x[0] > 0.8]
    #sorted_songs = songs.sorted(reverse=True)
    def print_energy_tracks():
        for x in songs:
            print(f"{x[0]:4.2}\t{x[1]:16}\t{x[2]:35}")

    print_energy_tracks()

print("The following are HIGH ENERGY tracks!!!")
energy_closure()


'''
HIGH ENERGY TRACKS
0.81    Luis Fonsi          Despacito - Remix                  
0.81    Post Malone         Congratulations                    
0.82    Jason Derulo        Swalla (feat. Nicki Minaj & Ty Dolla $ign)
0.83    Ed Sheeran          Castle on the Hill                 
0.81    Imagine Dragons     Thunder                            
 0.8    Danny Ocean         Me Rehúso                          
0.88    Ed Sheeran          Galway Girl                        
0.81    The Weeknd          I Feel It Coming                   
0.84    Starley             Call On Me - Ryan Riback Extended Remix
0.84    Martin Jensen       Solo Dance                         
0.82    Enrique Iglesias    SUBEME LA RADIO                    
0.87    Maggie Lindemann    Pretty Girl - Cheat Codes X CADE Remix
 0.8    Bruno Mars          24K Magic                          
 0.8    Katy Perry          Chained To The Rhythm              
0.86    Wisin               Escápate Conmigo                   
0.93    Steve Aoki          Just Hold On                       
0.84    CNCO                Reggaetón Lento (Bailemos)         
0.81    The Vamps           All Night                          
0.86    The Chainsmokers    Don't Let Me Down 
'''