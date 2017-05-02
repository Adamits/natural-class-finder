# natural-class-finder
Python model to find natural classes of phonological features

## Usage

in validation/there are dev, guess, and correct files.

problem_xx_correct is the formatted correct answers for a problem set

problem_xx_dev is the inputs for a problem set

problem_xx_guesses is the output of guess.py, containing the guesses for the problem set, and the accuracy checker will check these guesses against problem_xx_correct

# features_matrix

FeatureMatrix is a wrapper over basefeatures.txt. Used for interfaceing with features and unicode representations of phonemes.
given a set of phonemes, its methods can find their shared features.

Feature is a class for working with individual features, instantiated by passing in the full_string e.g. "+sonorant".

# find
These functions assess the shared features by breaking them down into "categories" in which the most efficient set of features is optimized and returned.
