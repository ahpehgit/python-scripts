import json
from difflib import get_close_matches

def getKey():
	return input("Enter a word: ")

def camelCase(w):
	return w[0].upper() + w[1:len(w)]

def translate(word):
	orgWord = word
	word = word.lower()
	if word in data:
		return data[word]
	elif camelCase(word) in data: 
		return data[camelCase(word)]
	elif word.upper() in data:
		return data[word.upper()]
	else:
		matches = get_close_matches(word, data.keys(), n=3, cutoff=0.7)
		if len(matches) > 0:
			res = input("Do you mean %s? Y for Yes, N for No: " %(matches[0]))
			if res.upper() == 'Y':
				return translate(matches[0])
			else:
				for idx in range(1, len(matches)):
					res = input("Or do you mean %s? Y for Yes, N for No: " %(matches[idx]))
					if res.upper() == 'Y':
						return translate(matches[idx])

				return "The word \"%s\" doesn't exists." %(orgWord)
		else:
			return "The word \"%s\" doesn't exists." %(orgWord)
	
data = json.load(open("data.json", "r"))

output = translate(getKey())

if type(output) == list:
	for definition in output:
		print(definition)
else:
	print(output)
	