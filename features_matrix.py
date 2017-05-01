# -*- coding: utf-8 -*-
# PATH to the basefeatures file taken from Haye's Pheatures
basefeatures_path = "./basefeatures.txt"

# Class for interfacing with Hayes feature matrix
# Hard coded feature names per type
# phones_dict: the dict of {phone: {feature: value}}
class FeaturesMatrix(object):

  def __init__(self):
    # hard code features here in optimal order for comparison
    self.all_features = ["syllabic", "stress", "long", "consonantal", "sonorant", "continuant", "delayed_release", "approximant", "tap",
                         "trill", "nasal", "voice", "spread_gl", "constr_gl", "labial", "round", "labiodental", "coronal", "anterior", "distributed",
                         "strident", "lateral", "dorsal", "high", "low", "front", "back", "tense"]

    self.manner_features = ["syllabic", "consonantal", "approximant", "sonorant", "continuant", "delayed_release"] #"tap", "trill", "nasal"]

    self.place_features = ["labial", "round", "labiodental", "coronal", "anterior", "distributed", "strident", "lateral",
                    "dorsal", "high", "low", "front", "back"]
    self.vowel_features = ["high", "low", "front", "back", "round", "tense"]
    self.voice_features = ["voice"]
    self.extra_features = ["tap", "trill", "nasal", "voice", "spread_gl", "constr_gl"]
    self.place_tree = {"parents": ["labial", "coronal", "dorsal"],
                       "labial": ["round", "labiodental"],
                       "coronal": ["anterior", "distributed", "strident", "lateral"],
                       "dorsal": ["high", "low", "front", "back"]}
    # left: all left features for vowel matrix
    # top: all top features for vowel matrix, round can be handled individually
    self.vowel_matrix_dict = {"left": ["high", "low", "tense"], "top": ["front", "back"]}
    self.basefeatures_text = open(basefeatures_path).read()
    self.phonemes_dict = self._get_phonemes_dict()
    self.phonemes = self.phonemes_dict.keys()

  def _get_phonemes_dict(self):
    phonemes_dict = {}
    # Split into 2d list of the table
    matrix = [row.split(' ') for row in self.basefeatures_text.split('\n')]
    for row in matrix[1:]:
      # At each row, store phone as key, and list of key/value pairs of label and +/-/0
      #print row[0]
      #print [row[0]]
      phonemes_dict[row[0]] = dict(zip(self.all_features, row[1:]))

    return phonemes_dict

  def get_all_manner_features(self):
    # Put negative palceholder for unvalued features
    return [Feature("-" + f) for f in self.manner_features]

  def get_manner_features(self, phoneme):
    phoneme_features_dict = self.phonemes_dict[phoneme]
    features = [phoneme_features_dict[feature] + feature for feature in self.manner_features]
    return features

  def get_place_features(self, phoneme):
    phoneme_features_dict = self.phonemes_dict[phoneme]
    features = [phoneme_features_dict[feature] + feature for feature in self.place_features if
                phoneme_features_dict[feature] != "0"]
    return features

  def get_voice_features(self, phoneme):
    phoneme_features_dict = self.phonemes_dict[phoneme]
    features = [phoneme_features_dict[feature] + feature for feature in self.voice_features if
                phoneme_features_dict[feature] != "0"]
    return features

  def get_vowel_features(self, phoneme):
    phoneme_features_dict = self.phonemes_dict[phoneme]
    features = [phoneme_features_dict[feature] + feature for feature in self.vowel_features if
                phoneme_features_dict[feature] != "0"]
    return features

  def get_all_features(self, phoneme):
    phoneme_features_dict = self.phonemes_dict[phoneme]
    features = [phoneme_features_dict[feature] + feature for feature in self.all_features]
    return features

  def get_shared_features(self, phonemes=[]):
    shared = []
    for p in phonemes:
		  shared.append(set(self.get_all_features(p)))
    return list(set.intersection(*shared))
  """
  def get_shared_features(self, phonemes=[]):
    shared = []
    out = []
    for p in phonemes:
		  shared.append(set(self.get_features(p)))

    shared_set = set(shared)

    feature_values = {}
    for s in shared_set:
      feature_values[s[1:]] = s

    for f in self.all_features:
      if f in feature_values.keys():
        out.append(feature_values[f])
      else:
        out.append("0" + f)"""

  def get_shared_manner_features(self, phonemes=[]):
    shared = []
    out = []
    for p in phonemes:
		  shared.append(set(self.get_manner_features(p)))

    shared_set = self.sort_manner_features(list(set.intersection(*shared)))

    feature_values = {}
    for s in shared_set:
      feature_values[s[1:]] = s

    for f in self.manner_features:
      if f in feature_values.keys():
        out.append(feature_values[f])
      else:
        out.append("0" + f)

    return out

  def get_shared_place_features(self, phonemes=[]):
    shared = []
    for p in phonemes:
		  shared.append(set(self.get_place_features(p)))
    return self.sort_place_features(list(set.intersection(*shared)))

  def get_shared_vowel_features(self, phonemes=[]):
    shared = []
    for p in phonemes:
		  shared.append(set(self.get_vowel_features(p)))
    return self.sort_vowel_features(list(set.intersection(*shared)))
    
  def get_shared_voice_features(self, phonemes=[]):
    shared = []
    for p in phonemes:
		  shared.append(set(self.get_voice_features(p)))
    return list(set.intersection(*shared))

  def sort_manner_features(self, features):
    input_features_dict = {}
    output_features = []

    for feature in features:
      input_features_dict[feature[1:]] = feature

    for ordered_feature in self.manner_features:
      if input_features_dict.get(ordered_feature):
        output_features.append(input_features_dict[ordered_feature])

    return output_features

  def sort_place_features(self, features):
    input_features_dict = {}
    output_features = []

    for feature in features:
      input_features_dict[feature[1:]] = feature

    for ordered_feature in self.place_features:
      if input_features_dict.get(ordered_feature):
        output_features.append(input_features_dict[ordered_feature])

    return output_features

  def sort_vowel_features(self, features):
    input_features_dict = {}
    output_features = []

    for feature in features:
      input_features_dict[feature[1:]] = feature

    for ordered_feature in self.vowel_features:
      if input_features_dict.get(ordered_feature):
        output_features.append(input_features_dict[ordered_feature])

    return output_features

class Feature(object):
  def __init__(self, feature_string):
    self.full_string = feature_string
    self.name = self.full_string[1:]
    self.value = self.full_string[0]

  def is_positive(self):
    return self.value == "+"

  def is_negative(self):
    return self.value == "-"
    
  def is_zero(self):
	  return self.value == "0"

  def make_positive(self):
    self.value = "+"
    self.full_string = self.value + self.name
    return self

  def make_negative(self):
    self.value = "-"
    self.full_string = self.value + self.name
    return self

  def make_opposite(self):
	#print "Entered make opposite"
	if self.value == "+":
		self.make_negative()
		return self
	if self.value == "-":
		self.make_positive()
	else:
		return
	return self
