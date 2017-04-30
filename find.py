# -*- coding: utf-8 -*-
from features_matrix import *

fm = FeaturesMatrix()


# main function
def find_natural_class(phonemes=[]):
  manner_features = assess_manner(phonemes)
  if manner_features == ["+syllabic", "-consonantal"]:
    print "CONSONANT"
  else:
    print "VOWEL"

  return True


# extracts necessary manner features
def assess_manner(phonemes=[]):
  # Use Feature class
  shared_features = [Feature(f) for f in fm.get_shared_manner_features(phonemes)]

  all_manner_features = [Feature(f) for f in fm.manner_features]

  efficient_features = []

  if len(shared_features) >= 5:  # all major manner features same, vowel/glide/liquid/nasal/fricative/affricate/stop
    shared_features[1].value = not shared_features[1].value  # have to flip consonantal feature momentarily :P

    if shared_features[0].is_positive():  # +syllabic
      efficient_features.append(shared_features[0])
      return [f.full_string for f in efficient_features]
    else:
      negative_counter = 0  # marks where overlap is
      for i, x in enumerate(shared_features):
        negative_counter = 5  # set default
        if x.is_positive():
          negative_counter = i
          break

      if negative_counter == 5:  # reached end of chart, nothing +, stop
        efficient_features.append(Feature("-delayed_release"))
        return [f.full_string for f in efficient_features]

      feature1 = all_manner_features[negative_counter - 1].make_negative()
      feature2 = all_manner_features[negative_counter].make_positive()

      efficient_features.append(feature1)
      efficient_features.append(feature2)

  for i, x in enumerate(efficient_features):
    if x.name == "consonantal":  # swapping back consonantal values bs
      if x.is_positive():
        efficient_features[i] = "-" + x.value
      else:
        efficient_features[i] = "+" + x.value

  return [f.full_string for f in efficient_features]


"""

    syllabic  consonantal   approximant   sonorant    continuant    delayed release     Expected output

a, e, i   +     -       +       +       +       0         +syllabic
w, j    -     - (+)     +       +       +       0         -syllabic, -consonantal
l, r    -     + (-)     +       +       +       0         +consonantal, +approximant
m, n    -     +   (-)     -       +       -       0         -approximant, +sonorant
f, s    -     + (-)     -       -       +       +         -sonorant, +continuant
affricate                                                 -continuant, +delayed release
t, k    -     + (-)     -       -       -       -         -delayed_release


a, e, w, j  0     0       +       +       +       0         -consonantal
w, j, l, r  -     0       0       +       +       0         -syllabic, +approximant

"""


# extracts necessary place features
def assess_place(phonemes=[]):
  features_to_compare = []
  parent = None

  for feature_string in fm.get_shared_place_features(phonemes):
    # Instantiate as a Feature object, described in features_matrix.py
    feature = Feature(feature_string)

    # Assumption is that each shared feature set can only possibly have one 'parent'
    # place feature, and that given the order that we are assessing features, the parent
    # will be found before any of its children
    if feature.name in fm.place_tree["parents"] and feature.is_positive():
      parent = feature

    # Get all the shared features within the parent that they share
    if parent and feature.name in fm.place_tree.get(parent.name):
      features_to_compare.append(feature)

  return features_to_compare


def assess_vowels(phonemes):
  return [Feature(f) for f in fm.get_shared_vowel_features(phonemes)]


# extracts necessary voicing feature
def assess_voice(features):
	shared_features = fm.get_shared_voice_features(features)
	return shared_features


def assess_optimal(phonemes = []):
	optimal = []
	manner = assess_manner(phonemes)
	place = assess_place(phonemes)
	voice = assess_voice(phonemes)
	
	optimal.extend(manner)
	optimal.extend(place)
	if "-delayed_release" in manner or "-continuant" in manner or "-sonorant" in manner:
		optimal.extend(voice)
		
	return optimal


# Demonstrate usage of FeaturesMatrix
# May still need to implement something for unicode


print assess_optimal(["t", "k", "p"])
print assess_optimal(["w", "j"])

"""
print assess_manner(["i", "e"])	# vowels
print assess_manner(["w", "j"])	# glides
print assess_manner(["m", "n"])	# nasals
print assess_manner(["f", "s"])	# fricatives
print assess_manner(["t", "k"])	# stops
"""



"""
print fm.get_all_features("œ")
print fm.get_place_features("p")
print fm.get_place_features("b")
print fm.get_place_features("f")
print fm.get_place_features("v")
print fm.get_place_features("m")
x = fm.get_shared_place_features(["p", "b", "m", "f", "v"])
print x
place_features = assess_place(fm.sort_place_features(x))
print [f.full_string for f in place_features]	#ideally should say +labial"""


# Some vowels tests
print fm.get_place_features("œ")
print fm.get_place_features("ə")
print fm.get_place_features("ɛ")
place_features = assess_place(["œ", "ə", "ɛ"])
print fm.get_vowel_features("œ")
print fm.get_vowel_features("ə")
print fm.get_vowel_features("ɛ")
vowel_features = assess_vowels(["œ", "ə", "ɛ"])
print [f.full_string for f in place_features + vowel_features]

