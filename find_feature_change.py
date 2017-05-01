# -*- coding: utf-8 -*-
from features_matrix import *

fm = FeaturesMatrix()

phonemetofeatures = fm._get_phonemes_dict()


# featurestophonemes = dict((f,p) for p, f in phonemetofeatures.iteritems())
# print featurestophonemes

def findchange(a, b):
	afeatures = fm.get_all_features(a)
	bfeatures = fm.get_all_features(b)
	# print afeatures, bfeatures

	changedfeatures = []

	for i, afeature in enumerate(afeatures):
		# features are different between two phonemes
		if afeature != bfeatures[i]:
			# want positive value
			if afeature[0] == "+" and bfeatures[i][0] == "-":
				changedfeatures.append((a, afeature))
			if afeature[0] == "-" and bfeatures[i][0] == "+":
				changedfeatures.append((b, bfeatures[i]))

	changed_dict = {}
	for p, feature in changedfeatures:
		changed_dict.setdefault(p, []).append(feature)

	return changed_dict

"""
print "The contrastive features between ɯ and ɤ are: ", findchange("ɯ", "ɤ")
print "The contrastive features between ɑ and ɒ are: ", findchange("ɑ", "ɒ")
print "The contrastive features between j and ɥ are: ", findchange("j", "ɥ")
print "The contrastive features between u and y are: ", findchange("u", "y")
print "The contrastive features between i and y are: ", findchange("i", "y")
print "The contrastive features between i and ɪ are: ", findchange("i", "ɪ")
print "The contrastive features between ð and z are: ", findchange("ð", "z")
print "The contrastive features between l and ɹ are: ", findchange("l", "ɹ")
print "The contrastive features between h and ʔ are: ", findchange("h", "ʔ")
print "The contrastive features between p and t are: ", findchange("p", "t")
print "The contrastive features between t͡s and t͡ʃ are: ", findchange("t͡s", "t͡ʃ")
#print "The contrastive features between kj and k are: ", findchange("kj", "k")
print "The contrastive features between u and w are: ", findchange("u", "w")
print "The contrastive features between t̪͡θ and t͡s are: ", findchange("t̪͡θ", "t͡s")
print "The contrastive features between v and β are: ", findchange("v", "β")
print "The contrastive features between m and b are: ", findchange("m", "b")
print "The contrastive features between χ and x are: ", findchange("χ", "x")
print "The contrastive features between ʁ and ʕ are: ", findchange("ʁ", "ʕ")
#print "The contrastive features between k and kw are: ", findchange("k", "kw")
#print "The contrastive features between w and pw are: ", findchange("w", "pw")
#print "The contrastive features between u and y are: ", findchange("u", "y")
"""
