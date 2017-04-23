# PATH to the basefeatures file taken from Haye's Pheatures
basefeatures_path = "./basefeatures.txt"

# Class for interfacing with Hayes feature matrix
# Hard coded feature names per type
# phones_dict: the dict of {phone: {feature: value}}
class FeaturesMatrix(object):

  def __init__(self):
    self.all_features = ["syllabic", "stress", "long", "consonantal", "sonorant", "continuant", "delayed_release",
                    "approximant",
                    "tap", "trill", "nasal", "voice", "spread_gl", "constr_gl", "labial", "round", "labiodental",
                    "coronal",
                    "anterior", "distributed", "strident", "lateral", "dorsal", "high", "low", "front", "back", "tense"]

    self.manner_features = ["consonantal", "sonorant", "continuant", "delayed_release", "approximant", "tap", "trill", "nasal"]

    self.place_features = ["labial", "round", "labiodental", "coronal", "anterior", "distributed", "strident", "lateral",
                    "dorsal", "high", "low", "front", "back", "tense"]

    self.vowel_features = ["round", "high", "low", "front", "back", "tense"]
    self.voice_features = ["voice"]
    self.basefeatures_lines = open(basefeatures_path).read()
    self.phones_dict = self._get_phones_dict()

  def _get_phones_dict(self):
    phones_dict = {}
    # Split into 2d list of the table
    matrix = [row.split(' ') for row in self.basefeatures_lines.split('\n')]
    for row in matrix[1:]:
      # At each row, store phone as key, and list of key/value pairs of label and +/-/0
      phones_dict[row[0]] = dict(zip(self.all_features, row[1:]))

    return phones_dict

  def get_manner_features(self, phone):
    phone_features_dict = self.phones_dict[phone]
    features = [phone_features_dict[feature] + feature for feature in self.manner_features if phone_features_dict[feature] != "0"]
    return features

  def get_place_features(self, phone):
    phone_features_dict = self.phones_dict[phone]
    features = [phone_features_dict[feature] + feature for feature in self.place_features if
                phone_features_dict[feature] != "0"]
    return features

  def get_voice_features(self, phone):
    phone_features_dict = self.phones_dict[phone]
    features = [phone_features_dict[feature] + feature for feature in self.voice_features if
                phone_features_dict[feature] != "0"]
    return features

  def get_vowel_features(self, phone):
    phone_features_dict = self.phones_dict[phone]
    features = [phone_features_dict[feature] + feature for feature in self.vowel_features if
                phone_features_dict[feature] != "0"]
    return features

  def get_all_features(self, phone):
    phone_features_dict = self.phones_dict[phone]
    features = [phone_features_dict[feature] + feature for feature in self.all_features if
                phone_features_dict[feature] != "0"]
    return features


