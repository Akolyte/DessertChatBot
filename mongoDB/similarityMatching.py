import difflib
words = ["coffeepie", "coffeeicecream", "banoffeepie", "bananaicecream", "bananacreampie", "coffeecreamcake"]
print(difflib.get_close_matches("banana",words))

from difflib import SequenceMatcher
s = SequenceMatcher(None, "abcd", "bcde")
print(s.ratio())

#for each of the close matches compare the ratio score for each of the matched words to the input, and return highest match?