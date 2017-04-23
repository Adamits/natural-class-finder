from features_matrix import *

# main function
def find_natural_class(phonemes=[]):
  return True

# extracts necessary manner features
def assess_manner():
  return True

# extracts necessary place features
def assess_place():
  return True

# extracts necessary voicing feature
def assess_voice():
  return True

# Demonstrate usage of FeaturesMatrix
# May still need to implement something for unicode
fm = FeaturesMatrix()
print fm.get_manner_features("d")
print fm.get_place_features("d")
print fm.get_voice_features("d")
print fm.get_vowel_features("o")