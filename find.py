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
	shared_features = fm.get_shared_manner_features(phonemes)
	sorted_manner = fm.sort_manner_features(shared_features)

	all_manner_features = fm.manner_features
	
	efficient_features = []
	
	if len(sorted_manner) >= 5:		# all major manner features same, vowel/glide/liquid/nasal/fricative/affricate/stop
		for i, x in enumerate(sorted_manner):		# turning them into bools for my own sake
			if x[0] == "+":
				sorted_manner[i] = True
			else:
				sorted_manner[i] = False
		
		sorted_manner[1] = not sorted_manner[1] 	# have to flip consonantal feature momentarily :P
		
		if sorted_manner[0] == True:	# +syllabic
			efficient_features.append("+syllabic")
			return efficient_features
		else:
			negative_counter = 0	# marks where overlap is
			for i, x in enumerate(sorted_manner):
				negative_counter = 5	# set default
				if x == True:
					negative_counter = i
					break

			if negative_counter == 5:	# reached end of chart, nothing +, stop
				efficient_features.append("-delayed_release")
				return efficient_features
				
			feature1 = "-" + all_manner_features[negative_counter-1]
			feature2 = "+" + all_manner_features[negative_counter]
			
			efficient_features.append(feature1)
			efficient_features.append(feature2)
			


	for i, x in enumerate(efficient_features):
		if x[1:] == "consonantal":	# swapping back consonantal values bs
			if x[0] == "+":
				efficient_features[i] = "-" + x[1:]
			else:
				efficient_features[i] = "+" + x[1:]
				
	return efficient_features

"""

		syllabic	consonantal		approximant		sonorant		continuant		delayed release			Expected output
		
a, e, i		+			-				+				+				+				0					+syllabic
w, j		-			-	(+)			+				+				+				0					-syllabic, -consonantal
l, r		-			+	(-)			+				+				+				0					+consonantal, +approximant
m, n		-			+ 	(-)			-				+				-				0					-approximant, +sonorant
f, s		-			+	(-)			-				-				+				+					-sonorant, +continuant
affricate																									-continuant, +delayed release
t, k		-			+	(-)			-				-				-				-					-delayed_release


a, e, w, j	0			0				+				+				+				0					-consonantal
w, j, l, r	-			0				0				+				+				0					-syllabic, +approximant	

"""


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

    # Get all the shared features within the parent that they share
    if parent and feature.name in fm.place_tree.get(parent.name):
      features_to_compare.append(feature)

  return features_to_compare

def assess_vowels():
  return True

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


