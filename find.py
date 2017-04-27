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
  shared_features = fm.get_shared_manner_features(phonemes)

  return True

# extracts necessary place features
def assess_place(features):
  features_to_compare = []
  parent = None

  for feature_string in features:
    feature = Feature(feature_string)

    # Assumption is that each shared feature set can only possibly have one 'parent'
    # place feature, and that given the order that we are assessing features, the parent
    # will be found before any of its children
    if feature.name in fm.place_tree["parents"] and feature.is_positive():
      parent = feature

    if parent and feature.name in fm.place_tree.get(parent.name):
      features_to_compare.append(feature)

  return features_to_compare

def assess_vowels():
  return True

# extracts necessary voicing feature
def assess_voice():
  return True

# Demonstrate usage of FeaturesMatrix
# May still need to implement something for unicode
#print fm.get_place_features("d")
#print fm.get_voice_features("b")
#print fm.get_vowel_features("o")

print fm.get_place_features("r")
print fm.get_place_features("l")
x = fm.get_shared_place_features(["r", "l"])
print x
place_features = assess_place(fm.sort_place_features(x))
print [f.full_string for f in place_features]
#print fm._sort_features(["yo"])