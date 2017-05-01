# -*- coding: utf-8 -*-
from features_matrix import *

fm = FeaturesMatrix()
phonemetofeatures_master = fm._get_phonemes_dict()


def find_phoneme(phoneme, changefeatures):
	
	phonemetofeatures = phonemetofeatures_master
	features = [Feature(f) for f in fm.get_all_features(phoneme)]
	for i, f in enumerate(features):
		for c in changefeatures:
			if f.name == c:
				features[i].make_opposite()
	
	#print [f.full_string for f in features]
	#print [phonemetofeatures["u"]]
	for guessphoneme, v in phonemetofeatures.items():
		for f in features:
			if f.full_string[0] != v[f.full_string[1:]]:
				if guessphoneme in phonemetofeatures:
					del phonemetofeatures[guessphoneme]
			
	return phonemetofeatures.keys()

# can only run one at a time	
"""
print find_phoneme("t", ["voice"])"""
print find_phoneme("j", ["syllabic"])
print find_phoneme("o", ["high"])

