# -*- coding: utf-8 -*-
from features_matrix import *
import itertools

fm = FeaturesMatrix()

phonemetofeatures = fm._get_phonemes_dict()

#featurestophonemes = dict((f,p) for p, f in phonemetofeatures.iteritems())
#print featurestophonemes

def findchange(a, b):
	afeatures = fm.get_all_features(a)
	bfeatures = fm.get_all_features(b)
	
	changedfeatures = []
	
	for i, afeature in enumerate(afeatures):
		# features are different between two phonemes
		if afeature != bfeatures[i]:
			# want positive value
			if afeature[0] == "+":
				changedfeatures.append((a, afeature))
			else:
				changedfeatures.append((b, bfeatures[i]))
				
	return changedfeatures


print findchange("p", "b")
print findchange("i", "y")
print findchange("p", "t")
