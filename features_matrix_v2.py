# PATH to the basefeatures file taken from Haye's Pheatures
# v2 changes: all_features list reordered to match basefeatures.txt, changing shared features functions to do intersection instead of union
basefeatures_path = "./basefeatures.txt"

# Class for interfacing with Hayes feature matrix
# Hard coded feature names per type
# phones_dict: the dict of {phone: {feature: value}}
class FeaturesMatrix(object):

  def __init__(self):
    # hard code features here in optimal order for comparison
    self.all_features = ["syllabic", "stress", "long", "consonantal", "sonorant", "continuant", "delayed_release", "approximant", "tap", "trill", "nasal",
                    "voice", "spread_gl", "constr_gl", "labial", "round", "labiodental", "coronal", "anterior", "distributed", "strident", "lateral", "dorsal",
                    "high", "low", "front", "back",  "tense"]

    self.manner_features = ["syllabic", "consonantal", "sonorant", "continuant", "delayed_release", "approximant", "tap", "trill", "nasal"]

    self.place_features = ["labial", "round", "labiodental", "coronal", "anterior", "distributed", "strident", "lateral",
                    "dorsal", "high", "low", "front", "back", "tense"]

    self.vowel_features = ["high", "low", "front", "back", "round", "tense"]
    self.voice_features = ["voice"]
    self.basefeatures_text = open(basefeatures_path).read()
    self.phonemes_dict = self._get_phonemes_dict()

  def _get_phonemes_dict(self):
    phonemes_dict = {}
    # Split into 2d list of the table
    matrix = [row.split(' ') for row in self.basefeatures_text.split('\n')]
    for row in matrix[1:]:
      # At each row, store phone as key, and list of key/value pairs of label and +/-/0
      phonemes_dict[row[0]] = dict(zip(self.all_features, row[1:]))
    #print phonemes_dict["a"]	#not being read in right

    #print phonemes_dict['t\xcd\xa1\xc9\xac']
    return phonemes_dict

  def get_manner_features(self, phoneme):
    phoneme_features_dict = self.phonemes_dict[phoneme]
    features = [phoneme_features_dict[feature] + feature for feature in self.manner_features if
                phoneme_features_dict[feature] != "0"]
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
    features = [phoneme_features_dict[feature] + feature for feature in self.all_features if
                phoneme_features_dict[feature] != "0"]
    return features

  def get_shared_features(self, phonemes=[]):
    shared = []
    for p in phonemes:
		shared.append(set(self.get_all_features(p)))
    return list(set.intersection(*shared))

  def get_shared_manner_features(self, phonemes=[]):
    shared = []
    for p in phonemes:
		shared.append(set(self.get_manner_features(p)))
    return list(set.intersection(*shared))

  def get_shared_place_features(self, phonemes=[]):
    shared = []
    for p in phonemes:
		shared.append(set(self.get_place_features(p)))
    return list(set.intersection(*shared))

  def get_shared_vowel_features(self, phonemes=[]):
    shared = []
    for p in phonemes:
		shared.append(set(self.get_vowel_features(p)))
    return list(set.intersection(*shared))

  def _sort_features(self, features):
    # Use order of self.all_features to make sure features are in the right order
    bare_features = [feature[1:] for feature in features]
    order = zip(self.all_features, range(1, len(self.all_features)))
    return bare_features
