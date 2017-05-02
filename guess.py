# -*- coding: utf-8 -*-
from find import assess_optimal
from find_feature_change import findchange
from features_matrix import FeaturesMatrix

fm = FeaturesMatrix()

def guess_problem_1():
  lines = [line.strip() for line in open("./validation/problem_1_dev")]
  guesses_log_list = []

  def format_guess_1(guess_dict, chars=[]):
    ret = "%s %s" % (chars[0], chars[1])
    for char, guess_list in guess_dict.iteritems():
      ret += "~%s is %s" % (char, guess_list)

    return ret

  for line in lines:
    p1, p2 = [p for p in line.split(" ")]
    guesses_log_list.append(format_guess_1(findchange(p1, p2), [p1, p2]))

  with open("./validation/problem_1_guesses.txt", "w") as outfile:
    outfile.write('\n'.join(guesses_log_list))



def guess_problem_3():
  lines = [line.strip() for line in open("./validation/problem_1_dev")]
  guesses_log_list = []

  def format_guess_3(guess_list, chars=[]):
    ret = " ".join(chars)
    ret += "~%s" % guess_list

    return ret

  for line in lines:
    chars = line.split(" ")
    guesses_log_list.append(format_guess_3(assess_optimal(chars), chars))

  with open("./validation/problem_3_guesses.txt", "w") as outfile:
    outfile.write('\n'.join(guesses_log_list))

guess_problem_1()
guess_problem_3()

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

def score_problem_1():
  correct_lines = [line.strip() for line in open("./validation/problem_1_correct.txt")]
  guess_lines = [line.strip() for line in open("./validation/problem_1_guesses.txt")]

  preds = [line.split("~")[1] for line in guess_lines]
  true = [line.split("~")[1] for line in correct_lines]
  print preds
  print true

  print "accuracy for problem 1 is %s" % accuracy_score(true, preds)
  print "precision for problem 1 is %s" % precision_score(true, preds)
  print "recall for problem 1 is %s" % recall_score(true, preds)
  print "f1 for problem 1 is %s" % f1_score(true, preds)


def score_problem_3():
  correct_lines = [line.strip() for line in open("./validation/problem_3_correct.txt")]
  guess_lines = [line.strip() for line in open("./validation/problem_3_guesses.txt")]

  preds = [line.split("~")[1:] for line in guess_lines]
  true = [line.split("~")[1:] for line in correct_lines]
  accuracy_score(true, preds)

score_problem_1()