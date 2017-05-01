# -*- coding: utf-8 -*-
from features_matrix import *
import random

fm = FeaturesMatrix()


# extracts necessary manner features
def assess_manner(phonemes=[]):
  # Use Feature class
  shared_features = [Feature(f) for f in fm.get_shared_manner_features(phonemes)]

  all_manner_features = fm.get_all_manner_features()

  efficient_features = []

  if len(shared_features) >= 5:  # all major manner features same, vowel/glide/liquid/nasal/fricative/affricate/stop
    shared_features[1].value = not shared_features[1].value  # have to flip consonantal feature momentarily :P

    if shared_features[0].is_positive():  # +syllabic
      efficient_features.append(shared_features[0])
      return efficient_features
    else:
      negative_counter = 0  # marks where overlap is
      for i, x in enumerate(shared_features):
        negative_counter = 5  # set default
        if x.is_positive():
          negative_counter = i
          break

      if negative_counter == 5:  # reached end of chart, nothing +, stop
        efficient_features.append(Feature("-delayed_release"))
        return efficient_features

      feature1 = all_manner_features[negative_counter - 1].make_negative()
      feature2 = all_manner_features[negative_counter].make_positive()

      efficient_features.append(feature1)
      efficient_features.append(feature2)

  for i, x in enumerate(efficient_features):
    if x.name == "consonantal":  # swapping back consonantal values bs
      if x.is_positive():
        efficient_features[i] = x.make_negative()
      else:
        efficient_features[i] = x.make_positive()

  return efficient_features


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
  pos_parent = None
  neg_parent = None

  # If parent is a coronal, use this function
  # To find the optimal set of child features
  def coronal(features):
    # only return 2 features for coronal
    MAX_FEATURES = 2
    for f in features:
      # If it is lateral, we only need that (we are assuming English)
      if f.full_string == "+lateral":
        return [f]
      # If -lateral, GET IT OUTTA HERE!
      # -lateral will never tell us anything useful in English
      elif f.full_string == "-lateral":
        features.remove(f)
    # return MAX_FEATURES random features, I believe which ones is inconsequential
    if len(features) > MAX_FEATURES:
      return list(random.sample(set(features), MAX_FEATURES))
    else:
      return features

  # If parent is a dorsal, use this function
  # To find the optimal set of child features
  def dorsal(features):
    neg_features = []
    for feature in features:
      # For English, we only care about high/low for consonants
      if feature.name in ["high", "low"]:
        # return the first high, low positive, as these identify
        # velars and pharyngeals, respectively, uniquely
        if feature.is_positive():
          return [feature]
        else:
          neg_features.append(feature)

    return neg_features

  # If parent is a dorsal, use this function
  # To find the optimal set of child features
  def labial(features):
    for feature in features:
      # Catch +labiodental, which is contrastive
      if feature.is_positive():
        return [feature]

    return features

  # Store parents, catch segments like ? that need all 3 neg to identify,
  # or w, which has multiple positive parent features
  pos_parents = []
  neg_parents = []

  for feature_string in fm.get_shared_place_features(phonemes):
    # Instantiate as a Feature object, described in features_matrix.py
    feature = Feature(feature_string)

    # Assumption is that each shared feature set can only possibly have one 'parent'
    # place feature, and that given the order that we are assessing features, the parent
    # will be found before any of its children
    if feature.name in fm.place_tree["parents"]:
      if feature.is_positive():
        pos_parents.append(feature)
      else:
        neg_parents.append(feature)

    # Get all the shared features within the positive parents that they share
    if pos_parents and feature.name in [f for pos_parent in pos_parents for f in fm.place_tree.get(pos_parent.name)]:
      features_to_compare.append(feature)

  # Return the children if there are any shared childern,
  # otherwise return the shared positive parent feature
  # lastly if there are no other shared features, return the shared negative feature
  if features_to_compare:
    for pos_parent in pos_parents:
      if pos_parent.name == "coronal":
        return coronal(features_to_compare)
      elif pos_parent.name == "dorsal":
        return dorsal(features_to_compare)
      elif pos_parent.name == "labial":
        return labial(features_to_compare)
  elif pos_parents:
    return pos_parents
  elif neg_parents:
    return neg_parents
  else:
    return []


def assess_vowels(features):
  # for each in matrix, if any +, only return +, else return all -
  return [Feature(f) for f in fm.get_shared_vowel_features(features)]


# extracts necessary voicing feature
def assess_voice(features):
  return [Feature(f) for f in fm.get_shared_voice_features(features)]


def assess_optimal(phonemes=[]):
  optimal = []
  manner = assess_manner(phonemes)
  place = assess_place(phonemes)
  vowel = assess_vowels(phonemes)
  voice = assess_voice(phonemes)

  optimal.extend(manner)

  # Assess vowels seperately from consonants regarding place
  if "+syllabic" in [f.full_string for f in optimal] and "+consonan" not in [f.full_string for f in optimal]:
    optimal.extend(vowel)
  else:
    optimal.extend(place)

  # Check if voicing is a necessary feature
  if not set(["-delayed_release", "-continuant", "-sonorant"]).isdisjoint([m.full_string for m in manner]):
    optimal.extend(voice)

  return [o.full_string for o in optimal]


# Demonstrate usage of FeaturesMatrix
# May still need to implement something for unicode

print assess_optimal(["p", "t"])
print assess_optimal(["p", "t", "k"])
print assess_optimal(["θ", "f"])
print assess_optimal(["f", "v"])
print assess_optimal(["f", "b"])
print assess_optimal(["e", "k"])
print assess_optimal(["ʔ"])
# Not sure if glides work
print assess_optimal(["w", "j", "ɥ"])
print assess_optimal(["h"])

"""
for p in fm.phonemes:
  if "+coronal" in fm.get_place_features(p):
    print unicode(p, "utf-8")


print assess_optimal(["t", "k", "p"])
print assess_optimal(["w", "j"])
print assess_optimal(["a", "e"])

print [f.full_string for f in assess_place(["p", "b", "m"])]
print [f.full_string for f in assess_place(["k", "b", "x", "ŋ"])]
print [f.full_string for f in assess_place(["n", "l", "r"])]
print [f.full_string for f in assess_place(["w"])]
print [f.full_string for f in assess_place(["o"])]
print [f.full_string for f in assess_place(["i", "y"])]
print [f.full_string for f in assess_place(["i", "y"])]
print assess_optimal(["ʃ"])
print assess_optimal(["o"])


print assess_manner(["m", "n"]) # nasals
print assess_manner(["f", "s"]) # fricatives
print assess_manner(["t", "k"]) # stops

"""

