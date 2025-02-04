import re, os

def match_letters(word, target):
  """
  Searches for matching letters between the search word and target. Returns a list of the indexes of the
  matching letters.
  """
  matches = []
  if (sum(1 for (c, t) in zip(word, target) if c == t)) > 0:
    matches = [i for i, x in enumerate(zip(word, target)) if all(y == x[0] for y in x)]
  return matches

def same(item, target):
  """
  Returns the number of matching letters in the item and target
  """
  return len([c for (c, t) in zip(item, target) if c == t])

def build(pattern, words, seen, list):
  """
  Returns a list of words from the read file that match the pattern against the target word and are not
  in the seen dict
  """
  return [word for word in words if re.search(pattern, word) and word not in seen.keys() and word not in list]

def find(word, words, seen, target, path):
  """
  Creates a list of possible words and loops over until target word is reached
  """
  list = []
  matching_letters = match_letters(word, target)

  for i in range(len(word)):
    if i not in matching_letters:
      list += build(word[:i] + "." + word[i + 1:], words, seen, list) #calls build with a list of patterns e.g. .ead, l.ad, le.d, lead. and feeds to build function
  
  if len(list) == 0:
    return False

  list = sorted([(same(w, target), w) for w in list], reverse=True) # updates list to include number of matching letters and sorts by number of matches
  
  for (match, item) in list:
    if match >= len(target) - 1:
      if match == len(target) - 1:
        path.append(item)
      return True
    seen[item] = True

  for (match, item) in list:
    path.append(item)
    if find(item, words, seen, target, path):
      return True
    path.pop()

def legal_word(word):
  """
  Returns true is all chars in provided word are alpha. Returns false if letters are numeric.
  """
  clean_word = word.strip().upper()
  for i in clean_word:
    if not i.isalpha():
      return legal_word(input('Invalid entry, try again: '))
  return word

def legal_dictionary(f_name):
  """
  Validates the input of the dictionary file name. Triggers retry if file name is invalid or if
  the file doesnt exist in the path'
  """
  f_name_parts = f_name.split('.')
  if len(f_name_parts) != 2 or f_name_parts[1] != 'txt':
    return(legal_dictionary(input('Invalid file, try again: ')))
  elif not os.path.exists(f_name):
    return(legal_dictionary(input('Invalid file, try again: ')))
  return f_name

def excluded_words(words_string):
  return words_string.split()

def existsAlongPath(pitStop):
  """
   Forces the input word to appear along the path.
   start -> pitStop -> target
  """
  if find(start, words, seen, pitStop, path):     #start -> pitStop
    path.append(pitStop)
  else:
    print("No path found")
  if find(pitStop, words, seen, target, path):    #pitStop -> target
    path.append(target)
    print(len(path), path)                        #path-1 is incorrect count
  else:
    print("No path found")


fname = legal_dictionary(input("Enter dictionary name: "))

file = open(fname)
lines = file.readlines()
while True:
  start = legal_word(input("Enter start word: "))
  target = legal_word(input("Enter target word: "))
  exclusions = input('Enter words you wish to exclude separated by a space: ')
  pitStop = legal_word(input("Enter a word that must be exist along the start and target path: "))
  words = []
  for line in lines:
    word = line.rstrip()
    if len(word) == len(start) and word not in exclusions:
      words.append(word)
  break

count = 0
path = [start]
seen = {start : True}
if not pitStop:
  if find(start, words, seen, target, path):
    path.append(target)
    print(len(path) - 1, path)
  else:
    print("No path found")
else:
  existsAlongPath(pitStop)

