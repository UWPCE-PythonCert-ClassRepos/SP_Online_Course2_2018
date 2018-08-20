import hashlib

text_from_iliad = """
The armies approach each other, but before they meet, Paris offers to end the war by fighting a duel with Menelaus, 
urged by his brother and head of the Trojan army, Hector. 
While Helen tells Priam about the Greek commanders from the walls of Troy, 
both sides swear a truce and promise to abide by the outcome of the duel. Paris is beaten, 
but Aphrodite rescues him and leads him to bed with Helen before Menelaus can kill him.
"""

for i in range(10000000):
    x = hashlib.sha224(text_from_iliad.encode()).hexdigest()

