# -*- coding: utf-8 -*-
from features_matrix import *
import random

fm = FeaturesMatrix()


# extracts necessary manner features
def assess_manner(phonemes=[]):
  # Use Feature class
  shared_features = [Feature(f) for f in fm.get_shared_manner_features(phonemes)]
  shared_features[1].make_opposite()  # have to flip consonantal feature momentarily :P

  all_manner_features = fm.get_all_manner_features()

  efficient_features = []

  shared_num = 0
  for x in shared_features:
    if not x.is_zero():
      shared_num += 1

  if shared_num >= 5:  # all major manner features same, vowel/glide/liquid/nasal/fricative/affricate/stop
    if shared_features[0].is_positive():  # +syllabic
      efficient_features.append(shared_features[0])
      return efficient_features
    else:
      negative_counter = 0  # marks where overlap is
      for x in shared_features:
        if x.is_negative():
          negative_counter += 1
      #print "negative counter is: ", negative_counter
      if negative_counter == 6:  # reached end of chart, nothing +, stop
        efficient_features.append(Feature("-delayed_release"))
        return efficient_features
      elif negative_counter == 0:
        efficient_features.append(Feature("+syllabic"))

        # print [f.full_string for f in shared_features]
    feature1 = shared_features[negative_counter - 1]
    feature2 = shared_features[negative_counter]
    # print feature1.full_string, feature2.full_string

    efficient_features.append(feature1)
    efficient_features.append(feature2)

  if shared_num < 5:  # covers two classes or more
    zero_left = max([i for i, x in enumerate(shared_features[:5]) if x.is_zero() == True])
    zero_right = min([i for i, x in enumerate(shared_features[:5]) if x.is_zero() == True])

    # efficient_features.append(shared_features[zero_counter + 1])

    leftside = True
    rightside = True
    for i in range(0, zero_left):
      if not shared_features[i].is_zero():
        leftside = False

    for i in range(zero_left, 5):
      if not shared_features[i].is_positive():
        leftside = False

    for i in range(zero_right, 5):
      if not shared_features[i].is_zero():
        rightside = False
    for i in range(0, zero_right - 1):
      if not shared_features[i].is_negative():
        rightside = False

    if leftside:
      efficient_features.append(shared_features[zero_left + 1])
    elif rightside:
      efficient_features.append(shared_features[zero_right - 1])
    else:
      efficient_features.append(shared_features[zero_right - 1])
      efficient_features.append(shared_features[zero_left + 1])

    """
    for x in shared_features[:zero_counter]:
    if x.is_negative():
      efficient_features.append(x)
      # efficient_features.append(shared_features[zero_counter-1])
    """

  for x in efficient_features:
    if x.name == "consonantal":
      x.make_opposite()  # swapping back consonantal values

  return [f for f in efficient_features if not f.is_zero()]


"""

    syllabic  consonantal   approximant   sonorant    continuant    delayed release     Expected output

a, e, i   +     -       		+       	+       	+      		 0         			+syllabic
w, j    -     	- (+)     		+       	+       	+      		 0         			-syllabic, -consonantal
l, r    -     	+ (-)     		+       	+       	+      		 0         			+consonantal, +approximant
m, n    -     	+ (-)     		-       	+       	-       		0         		-approximant, +sonorant
f, s    -     	+ (-)     		-       	-       	+       		+         		-sonorant, +continuant
affricate                                                 								-continuant, +delayed release
t, k    -     	+ (-)     		-       	-       	-       		-         		-delayed_release


a, e, w, j  0     - (+)       	+       	+       	+       		0         		-consonantal
w, j, l, r  -     0       		+       	+       	+       		0         		-syllabic, +approximant
p, b, m		-	+ (-)			-			0			-				0				-continuant

"""


# extracts necessary place features
def assess_place(phonemes=[]):
  features_to_compare = []
  pos_parent = None
  neg_parent = None

  # If parent is a coronal, use this function
  # To find the optimal set of child features
  def coronal(features):
    for f in features:
      # If it is lateral, we only need that (we are assuming English)
      if f.full_string == "+lateral":
        return [f]
      # If -lateral, GET IT OUTTA HERE!
      # -lateral will never tell us anything useful in English
      elif f.full_string == "-lateral":
        features.remove(f)

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

  # If parent is a labial, use this function
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

  # Return the children if there are any shared childern, broken down by parent
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


def assess_vowels(phonemes=[]):
  matrix = fm.vowel_matrix_dict
  # for each in matrix, if any +, only return +, else return all -
  features = [Feature(f) for f in fm.get_shared_vowel_features(phonemes)]
  left = []
  top = []
  round = []
  ret_features = []
  for feature in features:
    # Start with features in left column of matrix
    if feature.name in matrix["left"]:
      left.append(feature)
    elif feature.name in matrix["top"]:
      top.append(feature)
    elif feature.name == "round":
      round.append(feature)

  # LEFT FEATURES:
  left_features = []
  for feature in left:
    remove_feature = False
    if feature.name == "low":
      # +low uniquely identifies low vowels, don't need -high.
      if feature.is_positive():
        left_features = [feature]
        break

      # Only need -low if high is positive or we do not have a tense feature
      remove_feature = "tense" in [f.name for f in left] or "+high" in [f.full_string for f in left]

    # All other left features seem necessary
    if not remove_feature:
      left_features.append(feature)

  ret_features += left_features

  # TOP FEATURES:
  # only care about positive, if no positive
  # return both negative
  top_pos = []
  for feature in top:
    if feature.is_positive():
      top_pos.append(feature)

  if top_pos:
    ret_features += top_pos
  else:
    ret_features += top

  # ROUND
  # lets try always returning round if it is a shared feature
  return ret_features + round if round else ret_features


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
  if "+syllabic" in [f.full_string for f in optimal] and "+consonantal" not in [f.full_string for f in optimal]:
    optimal.extend(vowel)
  else:
    optimal.extend(place)

  # Check if voicing is a necessary feature
  if not set(["-delayed_release", "-continuant", "-sonorant"]).isdisjoint([m.full_string for m in manner]):
    optimal.extend(voice)

  return [o.full_string for o in optimal]


# Demonstrate usage of FeaturesMatrix

print assess_optimal(["t", "d"])
print assess_optimal(["s", "z"])
print assess_optimal(["t", "d", "s", "z"])
print assess_optimal(["ɹ"])
#"ð", "θ", "d͡ʒ", "t͡ʃ", "t͡s", "ʃ", "s", "z", "n", "l", "ɹ", "ɾ"
print assess_optimal(["ð", "θ", "d͡ʒ", "t͡ʃ", "t͡s", "ʃ", "s", "z", "n", "l", "ɹ", "ɾ"])
print assess_optimal(["ð", "θ"])# "d͡ʒ", "t͡ʃ", "t͡s", "ʃ", "s", "z", "n", "l", "ɹ", "ɾ"])
print assess_optimal(["d͡ʒ", "t͡ʃ"])
print assess_optimal(["i", "y", "ɰ", "u"])
"""
##########Vowels##########

print assess_optimal(["i", "y", "ɰ", "u"])
print assess_optimal(["a"])
print assess_optimal(["e"])
print assess_optimal(["a", "e"])
print assess_optimal(["o", "e"])
print assess_optimal(["e", "ʌ"])
print assess_optimal(["i", "y", "ɪ", "ʏ"])
print assess_optimal(["ɪ", "ʏ"])
print assess_optimal(["ɪ"])

##########################

print assess_optimal(["l"])
print assess_optimal(["m", "n"])	# nasals
print assess_optimal(["f", "s"])	# fricatives
print assess_optimal(["t", "k"])	# stops
print assess_optimal(["m", "n"]) # nasals
print assess_optimal(["f", "s"]) # fricatives
print assess_optimal(["t", "k"]) # stops
print assess_optimal(['w', 'j', 'l'])
print assess_optimal(["p", "b", "m"])
print assess_optimal(["t͡ʃ", "d͡ʒ"])
"""